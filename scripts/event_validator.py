#!/usr/bin/env python3
"""Validate local JSONL conversion events against an explicit event contract.

No network, writes, sends, or provider access. This checks recorded structure,
types and duplicate keys; it cannot establish that payment or consent occurred.
"""

import argparse
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import re
import sys
sys.dont_write_bytecode = True

from _sales_common import emit, loads, read_json

ROOT = Path(__file__).resolve().parents[1]
SENSITIVE_KEYS = {"password", "card_number", "cvv", "cvc", "access_token", "refresh_token", "secret_key"}
POSITIVE_EVENTS = {"purchase_completed", "subscription_renewed", "refund_issued"}
TIME_FIELDS = {"occurred_at", "received_at", "effective_at", "cohort_entered_at"}
TEXT_FIELDS = {"provider", "source", "billing_interval", "route"}


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("timestamp must be a string")
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None or result.utcoffset().total_seconds() != 0:
        raise ValueError("timestamp must include a UTC offset (Z or +00:00)")
    return result


def schema_from(contract):
    if not isinstance(contract, dict) or not isinstance(contract.get("events"), list):
        raise ValueError("Contract must contain an events array")
    result = {}
    for row in contract["events"]:
        if not isinstance(row, dict) or not isinstance(row.get("name"), str) or not row["name"].strip():
            raise ValueError("Every contract event requires a nonempty name")
        name = row["name"]
        if name in result:
            raise ValueError(f"Contract repeats event name {name}")
        for key in ("required", "dedupe_key", "allowed_sources"):
            values = row.get(key, [])
            if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
                raise ValueError(f"Contract {name}.{key} must be an array of nonempty strings")
            if len(values) != len(set(values)):
                raise ValueError(f"Contract {name}.{key} contains duplicate fields")
        result[name] = row
    if not result:
        raise ValueError("Contract has no events")
    return result


def sensitive_paths(value, prefix=""):
    found = []
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else key
            if key.casefold() in SENSITIVE_KEYS:
                found.append(path)
            found.extend(sensitive_paths(item, path))
    elif isinstance(value, list):
        for item in value:
            found.extend(sensitive_paths(item, prefix + "[]"))
    return found


def validate_events(events, contract):
    schema = schema_from(contract)
    issues = []
    counts = Counter()
    deliveries = {}
    outcomes = {}
    duplicate_deliveries = 0
    duplicate_outcomes = 0
    valid = 0
    errors = 0
    def add(line, level, code, message):
        nonlocal errors
        issues.append({"line": line, "level": level, "code": code, "message": message})
        errors += level == "error"
    for number, event in events:
        before = errors
        if not isinstance(event, dict):
            add(number, "error", "event_object", "Expected a JSON object")
            continue
        name = event.get("event")
        if not isinstance(name, str) or name not in schema:
            add(number, "error", "unknown_event", "event must match a declared contract event name")
            continue
        counts[name] += 1
        definition = schema[name]
        for key in sensitive_paths(event):
            add(number, "error", "sensitive_field", f"Remove unnecessary sensitive field: {key}")
        for key in definition.get("required", []):
            if key not in event or event[key] is None or (isinstance(event[key], str) and not event[key].strip()):
                add(number, "error", "required_field", f"Missing or empty required field: {key}")
        for key, value in event.items():
            if key in TEXT_FIELDS and (not isinstance(value, str) or not value.strip()):
                add(number, "error", "text_field_type", f"{key} must be nonempty text when supplied")
            if key.endswith("_id") and value is not None and (not isinstance(value, str) or not value.strip()):
                add(number, "error", "identifier_type", f"{key} must be nonempty text when supplied")
            if key.endswith("_minor_units"):
                if isinstance(value, bool) or not isinstance(value, int):
                    add(number, "error", "amount_type", f"{key} must be an integer in documented currency minor units")
                elif key == "amount_minor_units" and value < 0:
                    add(number, "error", "negative_amount", "Use an explicit refund event with a positive refund magnitude")
            if key in TIME_FIELDS:
                try:
                    timestamp(value)
                except (ValueError, TypeError, OverflowError):
                    add(number, "error", "timestamp", f"{key} must be an ISO-8601 UTC timestamp")
        if "currency" in event and (not isinstance(event["currency"], str) or not re.fullmatch(r"[A-Z]{3}", event["currency"])):
            add(number, "error", "currency_format", "currency must be a three-letter uppercase code; actual code validity is not checked")
        amount = event.get("amount_minor_units")
        if name in POSITIVE_EVENTS and type(amount) is int and amount <= 0:
            add(number, "error", "nonpositive_outcome", "This paid/refund outcome requires a positive recorded amount")
        allowed = definition.get("allowed_sources", [])
        if allowed and event.get("source") not in allowed:
            add(number, "error", "event_source", "source does not match this contract event's allowed_sources")
        elif name in POSITIVE_EVENTS and event.get("source") in ("client", "browser", "redirect", "thank_you_page"):
            add(number, "error", "unverified_payment_source", "A browser event or redirect is not a verified paid outcome")
        try:
            if "received_at" in event and timestamp(event["received_at"]) < timestamp(event["occurred_at"]):
                add(number, "warning", "negative_latency", "received_at precedes occurred_at; inspect clocks and ingestion")
        except (KeyError, ValueError, TypeError, OverflowError):
            pass
        delivery = event.get("event_id")
        canonical = json.dumps({k: v for k, v in event.items() if k != "received_at"}, sort_keys=True, allow_nan=False)
        if isinstance(delivery, str) and delivery:
            if delivery in deliveries:
                if deliveries[delivery] == canonical:
                    duplicate_deliveries += 1
                    add(number, "warning", "duplicate_delivery", "Repeated logical event_id; count this delivery once")
                else:
                    add(number, "error", "event_id_collision", "The same event_id has conflicting payloads")
                continue
            deliveries[delivery] = canonical
        else:
            add(number, "warning", "missing_event_id", "No event_id; delivery-level deduplication cannot be checked")
        dedupe_fields = definition.get("dedupe_key", [])
        key_valid = True
        for field in dedupe_fields:
            value = event.get(field)
            if not isinstance(value, (str, int)) or isinstance(value, bool) or (isinstance(value, str) and not value.strip()):
                add(number, "error", "business_key_type", f"Declared business-key field {field} must be nonempty text or an integer")
                key_valid = False
        if dedupe_fields and key_valid:
            family = "paid_transaction" if name in ("purchase_completed", "subscription_renewed") else name
            key = (family,) + tuple(sorted((field, event[field]) for field in dedupe_fields))
            if key in outcomes:
                duplicate_outcomes += 1
                add(number, "warning", "duplicate_business_key", "Repeated declared business key; reconcile before counting outcomes")
            else:
                outcomes[key] = number
        if errors == before:
            valid += 1
    decisions = contract.get("project_decisions", {})
    unresolved = [key for key, value in decisions.items() if value is None] if isinstance(decisions, dict) else []
    return {"recorded_events_by_name": dict(sorted(counts.items())), "structurally_valid_nonduplicate_deliveries": valid,
            "duplicate_deliveries": duplicate_deliveries, "duplicate_business_keys": duplicate_outcomes,
            "error_count": errors, "warning_count": len(issues) - errors,
            "unresolved_contract_decisions": unresolved, "issues": issues,
            "valid": errors == 0,
            "limits": ["Valid means these structural checks passed, not verified payment, consent, identity, cohort eligibility, completeness or causality.",
                       "Business-key duplicates may be intentional repeated exposures; apply the event's declared counting rule.",
                       "No values from sensitive fields are printed. Unknown sensitive field names are not detected.",
                       "Resolve project decisions and configure allowed_sources before relying on a production contract."]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", required=True, help="Local UTF-8 JSONL; one flat event object per line, with event naming the contract event")
    parser.add_argument("--contract", default=str(ROOT / "assets/event-contract.json"))
    args = parser.parse_args(argv)
    try:
        events = []
        for number, line in enumerate(Path(args.events).read_text(encoding="utf-8").splitlines(), 1):
            if line.strip():
                try:
                    events.append((number, loads(line)))
                except ValueError as exc:
                    raise ValueError(f"Events line {number}: {exc}") from exc
        if not events:
            raise ValueError("No events supplied")
        result = validate_events(events, read_json(args.contract))
        emit(result)
        return 0 if result["valid"] else 1
    except (ValueError, OSError, TypeError, KeyError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
