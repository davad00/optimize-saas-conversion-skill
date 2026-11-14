#!/usr/bin/env python3
"""Summarize mature cohort retention with fixed denominators; read-only."""
import argparse
import sys
sys.dont_write_bytecode = True
from collections import defaultdict
import csv
from _analytics_common import boolean, count, emit, read_csv, ratio, text


def analyze(rows, mode):
    cohorts = defaultdict(dict)
    denominators = {}
    for row in rows:
        cohort = text(row["cohort"], "cohort")
        period = count(row["period"], "period")
        if period > 1200:
            raise ValueError("period must be at most 1200")
        eligible = count(row["eligible"], "eligible", positive=True)
        mature = boolean(row["mature"], "mature")
        if cohort in denominators and eligible != denominators[cohort]:
            raise ValueError(f"eligible denominator changes within cohort {cohort}")
        denominators[cohort] = eligible
        if period in cohorts[cohort]:
            raise ValueError(f"duplicate cohort/period: {cohort}/{period}")
        if not mature and row["retained"] != "":
            raise ValueError("immature rows must leave retained empty; do not treat incomplete observations as complete")
        retained = count(row["retained"], "retained") if mature else None
        if retained is not None and retained > eligible:
            raise ValueError("retained cannot exceed the original eligible cohort")
        cohorts[cohort][period] = {"period": period, "eligible": eligible, "retained": retained,
                                  "mature": mature, "rate": ratio(retained, eligible) if mature else None}
    periods = defaultdict(lambda: {"eligible": 0, "retained": 0, "mature_cohorts": 0, "immature_cohorts": 0})
    result_cohorts = []
    gaps = []
    for cohort in sorted(cohorts):
        observations = cohorts[cohort]
        last_retained = None
        immature_seen = False
        for period in sorted(observations):
            row = observations[period]
            if row["mature"]:
                if immature_seen:
                    raise ValueError(f"mature period follows an immature period in cohort {cohort}")
                if mode == "survival" and last_retained is not None and row["retained"] > last_retained:
                    raise ValueError(f"survival retention cannot increase in cohort {cohort}; use point mode for reactivation")
                last_retained = row["retained"]
                periods[period]["eligible"] += row["eligible"]
                periods[period]["retained"] += row["retained"]
                periods[period]["mature_cohorts"] += 1
            else:
                immature_seen = True
                periods[period]["immature_cohorts"] += 1
        missing = sorted(set(range(min(observations), max(observations) + 1)) - set(observations))
        if missing:
            gaps.append({"cohort": cohort, "missing_periods_between_first_and_last": missing})
        result_cohorts.append({"cohort": cohort, "periods": [observations[p] for p in sorted(observations)]})
    weighted = []
    for period, values in sorted(periods.items()):
        weighted.append({"period": period, **values,
                         "weighted_rate": ratio(values["retained"], values["eligible"]),
                         "cohorts_without_a_row": len(cohorts) - values["mature_cohorts"] - values["immature_cohorts"]})
    return {"tool": "cohort_retention", "mode": mode, "cohorts": result_cohorts,
            "weighted_by_period": weighted, "gaps": gaps,
            "warnings": [
                "Each cohort uses its original eligible denominator. Define the cohort-entry event, period length, retained event, timezone, and observation cutoff upstream.",
                "Only mature rows contribute to weighted rates. Missing or immature cells are not zero retention.",
                "Point retention can increase when users return; survival means continuously retained and must not increase.",
                "Averages at later periods can describe a different set of mature cohorts; this is descriptive, not a causal comparison.",
            ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="CSV: cohort,period,eligible,retained,mature; blank retained when immature")
    parser.add_argument("--mode", choices=("point", "survival"), required=True)
    args = parser.parse_args()
    try:
        emit(analyze(read_csv(args.input, ("cohort", "period", "eligible", "retained", "mature")), args.mode))
    except (ValueError, OSError, UnicodeError, csv.Error) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
