#!/usr/bin/env python3
"""Check supplied monthly/yearly offer observations against a verified catalog.

Local JSON only. Supports fixed flat or per-unit prices, not tiered/usage prices.
Reads observed values; does not browse, call a provider, or verify a live charge.
"""

import argparse
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re
import sys
sys.dont_write_bytecode = True

from _sales_common import emit, integer, read_json, text


def catalog_key(row):
    return (row["plan_id"], row["interval"], row["currency"])


def fixed_charge(row, quantity):
    return row["charge_minor"] * (quantity if row["unit"] == "per_unit" else 1)


def validate(payload):
    if not isinstance(payload, dict) or type(payload.get("version")) is not int or payload["version"] != 1:
        raise ValueError("Input must be an object with version: 1")
    if not isinstance(payload.get("catalog"), list) or not payload["catalog"]:
        raise ValueError("catalog must be a nonempty array")
    if not isinstance(payload.get("observations"), list) or not payload["observations"]:
        raise ValueError("observations must be a nonempty array")
    catalog = {}
    for i, row in enumerate(payload["catalog"], 1):
        if not isinstance(row, dict):
            raise ValueError(f"Catalog row {i} must be an object")
        text(row.get("plan_id"), f"Catalog row {i} plan_id")
        if row.get("interval") not in ("month", "year"):
            raise ValueError("Catalog interval must be month or year")
        if not isinstance(row.get("currency"), str) or not re.fullmatch(r"[A-Z]{3}", row["currency"]):
            raise ValueError("Catalog currency must be three uppercase letters")
        integer(row.get("charge_minor"), "charge_minor")
        if row.get("unit") not in ("flat", "per_unit"):
            raise ValueError("Catalog unit must be flat or per_unit")
        integer(row.get("min_quantity", 1), "min_quantity", 1)
        if row["unit"] == "flat" and row.get("min_quantity", 1) != 1:
            raise ValueError("Flat offers require min_quantity 1")
        if "provider_price_id" in row:
            text(row["provider_price_id"], "provider_price_id")
        key = catalog_key(row)
        if key in catalog:
            raise ValueError("Duplicate plan/interval/currency catalog entry")
        catalog[key] = row
    findings = []
    checked = []
    names = set()
    def add(name, level, code, message):
        findings.append({"observation": name, "level": level, "code": code, "message": message})
    for row in payload["observations"]:
        if not isinstance(row, dict):
            raise ValueError("Every observation must be an object")
        name = text(row.get("name"), "Observation name")
        if name in names:
            raise ValueError("Observation names must be unique")
        names.add(name)
        for field in ("plan_id", "interval", "currency"):
            text(row.get(field), f"{name}.{field}")
        if row.get("surface") not in ("pricing", "checkout"):
            raise ValueError("Observation surface must be pricing or checkout")
        quantity = integer(row.get("quantity"), f"{name}.quantity", 1)
        offer = catalog.get(catalog_key(row))
        if offer is None:
            add(name, "error", "unknown_offer", "No catalog entry matches this plan, interval and currency")
            continue
        if quantity < offer.get("min_quantity", 1):
            add(name, "error", "below_minimum_quantity", "Selected quantity is below the actual catalog minimum")
        if offer["unit"] == "flat" and quantity != 1:
            add(name, "error", "flat_quantity", "A flat offer must use quantity 1 in this schema")
        total = fixed_charge(offer, quantity)
        months = 12 if row["interval"] == "year" else 1
        checked.append({"name": name, "currency": row["currency"], "catalog_charge_minor": total,
                        "monthly_equivalent_total_minor": str(Decimal(total) / months)})
        if "submitted_price_id" in row:
            text(row["submitted_price_id"], "submitted_price_id")
            if "provider_price_id" not in offer:
                add(name, "review", "missing_provider_mapping", "Cannot compare submitted price ID without a verified catalog mapping")
            elif row["submitted_price_id"] != offer["provider_price_id"]:
                add(name, "error", "wrong_submitted_price", "Submitted provider price ID does not match the selected offer")
        if "submitted_quantity" in row:
            integer(row["submitted_quantity"], "submitted_quantity", 1)
            if row["submitted_quantity"] != quantity:
                add(name, "error", "wrong_submitted_quantity", "Checkout payload quantity differs from the selected quantity")
        if row["surface"] == "pricing":
            headline = integer(row.get("headline_minor"), f"{name}.headline_minor")
            if row.get("headline_basis") not in ("month", "year"):
                raise ValueError("headline_basis must be month or year")
            if row.get("headline_scope") not in ("per_unit", "total"):
                raise ValueError("headline_scope must be per_unit or total")
            if row["interval"] == "year" and row["headline_basis"] != "month":
                add(name, "review", "annual_headline_basis", "Use a monthly-equivalent primary comparison with the annual charge adjacent, or document the buying-context exception")
            if row["interval"] == "month" and row["headline_basis"] != "month":
                add(name, "error", "monthly_headline_basis", "Monthly pricing must state its actual month unit in this schema")
            base = offer["charge_minor"] if row["headline_scope"] == "per_unit" else total
            if row["headline_basis"] == "month":
                expected = (Decimal(base) / months).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
            else:
                expected = Decimal(base)
            if Decimal(headline) != expected:
                add(name, "error", "headline_amount", f"Primary comparison should be {expected} minor units using half-up display rounding")
            disclosure = row.get("disclosed_charge_minor")
            if disclosure is None:
                add(name, "error", "missing_billed_total", "Actual recurring charge must be supplied and displayed beside the comparison")
            else:
                integer(disclosure, "disclosed_charge_minor")
                scope = row.get("disclosed_charge_scope", "total")
                if scope not in ("per_unit", "total"):
                    raise ValueError("disclosed_charge_scope must be per_unit or total")
                expected_disclosure = offer["charge_minor"] if scope == "per_unit" else total
                if disclosure != expected_disclosure:
                    add(name, "error", "billed_total_mismatch", "Displayed recurring charge differs from the catalog at its declared scope")
                if scope == "per_unit" and quantity > 1:
                    add(name, "review", "whole_bill_missing", "Also show the total payable for the minimum or selected quantity")
            if row.get("disclosed_interval") != row["interval"]:
                add(name, "error", "billing_disclosure_interval", "Billing disclosure interval differs from the selected interval or is missing")
            if "savings_percent" in row:
                if isinstance(row["savings_percent"], bool):
                    raise ValueError("savings_percent must be numeric")
                value = Decimal(str(row["savings_percent"]))
                if not value.is_finite() or not 0 <= value <= 100:
                    raise ValueError("savings_percent must be finite and between 0 and 100")
                monthly = catalog.get((row["plan_id"], "month", row["currency"]))
                if row["interval"] != "year" or monthly is None or monthly["unit"] != offer["unit"] or quantity < monthly.get("min_quantity", 1):
                    add(name, "review", "savings_comparison_unavailable", "A comparable monthly offer at this quantity is needed to check savings")
                else:
                    reference = fixed_charge(monthly, quantity) * 12
                    if reference <= 0:
                        add(name, "review", "zero_savings_reference", "Cannot calculate percentage savings against a zero monthly reference")
                    else:
                        expected_saving = Decimal(reference - total) * 100 / reference
                        # Permit only display rounding to at most one tenth of a percentage point.
                        if expected_saving < 0 or abs(value - expected_saving) > Decimal("0.05"):
                            add(name, "error", "savings_mismatch", f"Actual saving is {expected_saving.quantize(Decimal('0.01'))}% against 12 monthly payments")
        else:
            if offer["unit"] == "per_unit" and "submitted_quantity" not in row:
                add(name, "review", "checkout_quantity_unverified", "Supply the submitted checkout quantity to verify per-unit selection continuity")
            due = integer(row.get("displayed_due_now_minor"), f"{name}.displayed_due_now_minor")
            quote = row.get("quoted_due_now_minor")
            if quote is None:
                add(name, "review", "due_now_unverified", "Supply the actual provider quote, including tax, discount or proration, to verify due-now wording")
            else:
                integer(quote, "quoted_due_now_minor")
                if due != quote:
                    add(name, "error", "due_now_mismatch", "Displayed amount due now differs from the supplied provider quote")
            if row.get("disclosed_interval") != row["interval"]:
                add(name, "error", "checkout_interval", "Checkout recurring interval differs from the selected offer or is missing")
            if "submitted_price_id" not in row:
                add(name, "review", "checkout_selection_unverified", "Supply the submitted provider price ID to check selection continuity")
    default = payload.get("default")
    if default is not None:
        if not isinstance(default, dict) or default.get("selected_interval") not in ("month", "year"):
            raise ValueError("default must contain selected_interval month or year")
        reason = default.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            add("default", "review", "default_reason_missing", "Record the fresh-visitor default decision and buyer-context reason; retain explicit user selections")
    else:
        add("default", "review", "default_unobserved", "Inspect and record the fresh-visitor default separately from existing preferences")
    errors = sum(f["level"] == "error" for f in findings)
    reviews = sum(f["level"] == "review" for f in findings)
    return {"catalog_entries": len(catalog), "observations_checked": len(checked), "checks": checked,
            "error_count": errors, "review_count": reviews, "findings": findings,
            "valid": errors == 0 and reviews == 0,
            "limits": ["These are supplied observations; no live DOM, provider, payment, selected-state behavior or fulfillment was tested.",
                       "Use documented currency minor units consistently. No currency conversion or currency-exponent lookup is performed.",
                       "Fixed flat/per-unit monthly/yearly offers only; use provider quotes for taxes, credits, trials, usage, tiers and proration.",
                       "Rounding assumes half-up to a currency minor unit. Readability, proximity and disclosure meaning still need rendered review.",
                       "A recorded default reason does not validate its suitability; apply the skill's mandatory pricing gate."]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Local JSON catalog and observed pricing/checkout values; schema in references/python-tools.md")
    args = parser.parse_args(argv)
    try:
        result = validate(read_json(args.input))
        emit(result)
        return 0 if result["valid"] else 1
    except (ValueError, OSError, TypeError, KeyError, InvalidOperation) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
