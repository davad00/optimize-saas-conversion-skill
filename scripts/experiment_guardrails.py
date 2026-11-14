#!/usr/bin/env python3
"""Check assignment, exposure, outcome joins, and sample allocation; read-only."""
import argparse
import sys
sys.dont_write_bytecode = True
from collections import defaultdict
import csv
from decimal import Decimal
import math
from _analytics_common import emit, parse_json, probability, read_csv, text, timestamp


def chi_square_tail(statistic, degrees):
    """Chi-square survival probability for integer df, via gamma recurrence.

    Q(a+1,x)=Q(a,x)+exp(a*log(x)-x-lgamma(a+1)). Bases are
    Q(1,x)=exp(-x) and Q(1/2,x)=erfc(sqrt(x)). Supports 1..99 df.
    """
    if statistic == 0:
        return 1.0
    x = statistic / 2
    a = .5 if degrees % 2 else 1.0
    value = math.erfc(math.sqrt(x)) if degrees % 2 else math.exp(-x)
    target = degrees / 2
    while a < target:
        value += math.exp(a * math.log(x) - x - math.lgamma(a + 1))
        a += 1
    return min(1.0, max(0.0, value))


def analyze(rows, allocation, threshold):
    if not isinstance(allocation, dict) or not 2 <= len(allocation) <= 100:
        raise ValueError("allocation must be an object with 2 to 100 variants")
    shares = {text(key, "variant"): probability(value, f"share for {key}") for key, value in allocation.items()}
    if any(value <= 0 for value in shares.values()) or sum(shares.values()) != Decimal(1):
        raise ValueError("allocation shares must be positive and sum exactly to 1")
    threshold = probability(threshold, "srm threshold")
    if not 0 < threshold < 1:
        raise ValueError("srm threshold must be strictly between 0 and 1")
    units = defaultdict(list)
    exact_seen = set()
    duplicate_rows = 0
    for row in rows:
        unit = text(row["unit_id"], "unit_id")
        variant = text(row["variant"], "variant")
        if variant not in shares:
            raise ValueError(f"variant absent from allocation: {variant}")
        event = row["event"]
        if event not in {"assigned", "exposed", "converted"}:
            raise ValueError("event must be assigned, exposed, or converted")
        occurred = timestamp(row["occurred_at"])
        key = (unit, variant, event, occurred)
        if key in exact_seen:
            duplicate_rows += 1
            continue
        exact_seen.add(key)
        units[unit].append((variant, event, occurred))
    issues = {"variant_conflict": [], "missing_assignment": [], "event_before_assignment": [],
              "conversion_without_exposure": [], "conversion_before_exposure": []}
    counts = {variant: {"assigned_units": 0, "exposed_units": 0, "converted_units": 0} for variant in shares}
    repeated_assignment_rows = 0
    for unit, records in units.items():
        variants = {record[0] for record in records}
        assigned = [record for record in records if record[1] == "assigned"]
        if len(variants) > 1:
            issues["variant_conflict"].append(unit)
        if not assigned:
            issues["missing_assignment"].append(unit)
            continue
        repeated_assignment_rows += max(0, len(assigned) - 1)
        if len(variants) > 1:
            continue
        variant = assigned[0][0]
        assigned_at = min(record[2] for record in assigned)
        exposed = [record[2] for record in records if record[1] == "exposed"]
        converted = [record[2] for record in records if record[1] == "converted"]
        counts[variant]["assigned_units"] += 1
        counts[variant]["exposed_units"] += bool(exposed)
        counts[variant]["converted_units"] += bool(converted)
        if any(record[2] < assigned_at for record in records if record[1] != "assigned"):
            issues["event_before_assignment"].append(unit)
        if converted and not exposed:
            issues["conversion_without_exposure"].append(unit)
        if converted and exposed and min(converted) < min(exposed):
            issues["conversion_before_exposure"].append(unit)
    total = sum(values["assigned_units"] for values in counts.values())
    expected = {variant: float(share * total) for variant, share in shares.items()}
    integrity_fail = any(issues[key] for key in ("variant_conflict", "missing_assignment", "event_before_assignment"))
    statistic = sum((counts[variant]["assigned_units"] - expected[variant]) ** 2 / expected[variant]
                    for variant in shares) if total else None
    p_value = None
    if not integrity_fail and total and min(expected.values()) >= 5:
        p_value = chi_square_tail(statistic, len(shares) - 1)
    reasons = []
    if integrity_fail:
        reasons.append("Assignment/identity/timing defects require investigation; SRM p-value withheld.")
    if not total:
        reasons.append("No unambiguous assigned units are available.")
    elif min(expected.values()) < 5:
        reasons.append("An expected assignment count is below 5; chi-square approximation withheld.")
    mismatch = p_value < float(threshold) if p_value is not None else None
    return {"tool": "experiment_guardrails", "expected_allocation": shares,
            "variants": [{"variant": variant, **counts[variant], "expected_assigned_units": expected[variant]}
                         for variant in shares],
            "exact_duplicate_rows_ignored": duplicate_rows,
            "repeated_same_variant_assignment_rows": repeated_assignment_rows,
            "issues": {key: {"unit_count": len(values), "example_unit_ids": sorted(values)[:10]}
                       for key, values in issues.items()},
            "assignment_integrity_checks_pass": not integrity_fail and total > 0,
            "srm": {"chi_square": statistic, "degrees_of_freedom": len(shares) - 1,
                    "p_value": p_value, "investigation_threshold": threshold, "mismatch_detected": mismatch,
                    "omission_reasons": reasons},
            "warnings": [
                "Input must cover one experiment and fixed intended allocation, with stable pseudonymous units; do not pool different ramps or post-treatment segments.",
                "SRM uses unique assigned units, never conversions. Repeated events are counted once per unit; conflicting variant units are flagged and excluded from descriptive counts.",
                "Missing exposure before conversion is a diagnostic: whether it invalidates an outcome depends on the predefined exposure and intent-to-treat design.",
                "A passed check does not verify randomization, complete logging, outcome maturity, clustering, repeated looks, or business benefit; no winner is selected.",
            ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="CSV: unit_id,variant,event,occurred_at; assigned/exposed/converted events")
    parser.add_argument("--allocation", required=True, help='Predeclared JSON shares, e.g. {"control":0.5,"variant":0.5}')
    parser.add_argument("--srm-threshold", default="0.001", help="Diagnostic threshold; default 0.001, not a shipping rule")
    args = parser.parse_args()
    try:
        emit(analyze(read_csv(args.input, ("unit_id", "variant", "event", "occurred_at")), parse_json(args.allocation), args.srm_threshold))
    except (ValueError, OSError, UnicodeError, csv.Error, ArithmeticError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
