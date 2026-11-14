"""Small internal helpers for local, read-only analytics commands.

Not a standalone tool. No network calls or filesystem mutations.
"""
import csv
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import json
import re


MAX_COUNT = 2**53 - 1


def count(value, name="count", positive=False):
    if isinstance(value, bool) or not re.fullmatch(r"[0-9]+", str(value)):
        raise ValueError(f"{name} must be a nonnegative integer")
    result = int(value)
    if result > MAX_COUNT or (positive and result == 0):
        raise ValueError(f"{name} must be {'positive and ' if positive else ''}at most {MAX_COUNT}")
    return result


def decimal(value, name="amount", minimum=None, maximum=None):
    if isinstance(value, bool) or value is None:
        raise ValueError(f"{name} must be a finite decimal")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{name} must be a finite decimal") from exc
    if not result.is_finite():
        raise ValueError(f"{name} must be a finite decimal")
    if len(result.as_tuple().digits) > 28 or (result != 0 and not -12 <= result.adjusted() <= 18):
        raise ValueError(f"{name} supports at most 28 significant digits and nonzero magnitudes from 1e-12 to below 1e19")
    if minimum is not None and result < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    if maximum is not None and result > maximum:
        raise ValueError(f"{name} must be at most {maximum}")
    return result


def probability(value, name="rate"):
    return decimal(value, name, Decimal(0), Decimal(1))


def currency(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Z]{3}", value):
        raise ValueError("currency must be a declared three-letter uppercase currency code")
    return value


def text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be nonempty text")
    return value.strip()


def boolean(value, name):
    if value in ("1", "true", "True"):
        return True
    if value in ("0", "false", "False"):
        return False
    raise ValueError(f"{name} must be true/false or 1/0")


def timestamp(value, name="occurred_at"):
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, AttributeError) as exc:
        raise ValueError(f"{name} must be an ISO-8601 timestamp with a timezone") from exc
    if result.tzinfo is None:
        raise ValueError(f"{name} must include a timezone")
    return result.astimezone(timezone.utc)


def read_csv(path, required):
    with open(path, encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames
        if not fields or len(fields) != len(set(fields)):
            raise ValueError("CSV must have a unique header row")
        missing = set(required) - set(fields)
        if missing:
            raise ValueError("CSV missing required columns: " + ", ".join(sorted(missing)))
        rows = []
        for line_number, row in enumerate(reader, 2):
            if None in row:
                raise ValueError(f"CSV row {line_number} has more values than its header")
            if not any(value for value in row.values()):
                continue
            if any(value is None for value in row.values()):
                raise ValueError(f"CSV row {line_number} has missing cells")
            rows.append({key: value.strip() for key, value in row.items()})
    if not rows:
        raise ValueError("CSV has no data rows")
    return rows


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json(value):
    def reject(value):
        raise ValueError(f"non-finite JSON value: {value}")
    return json.loads(value, parse_float=Decimal, parse_constant=reject, object_pairs_hook=_pairs)


def read_json(path):
    with open(path, encoding="utf-8-sig") as stream:
        return parse_json(stream.read())


def require_keys(value, keys, name):
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    missing = set(keys) - set(value)
    if missing:
        raise ValueError(f"{name} is missing: " + ", ".join(sorted(missing)))


def decimal_text(value):
    rendered = format(value, "f")
    return rendered.rstrip("0").rstrip(".") if "." in rendered else rendered


def emit(result):
    def encoder(value):
        if isinstance(value, Decimal):
            return decimal_text(value)
        raise TypeError(f"cannot serialize {type(value).__name__}")
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False, default=encoder))


def ratio(numerator, denominator):
    return None if denominator == 0 else float(numerator / denominator)
