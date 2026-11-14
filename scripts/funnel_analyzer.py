#!/usr/bin/env python3
"""Analyze ordered, nested stage counts from one eligible cohort; read-only."""
import argparse
import sys
sys.dont_write_bytecode = True
import csv
from _analytics_common import count, emit, read_csv, ratio, text


def analyze(rows, cohort, window, unit):
    stages = []
    seen = set()
    for row in rows:
        name = text(row["stage"], "stage")
        if name in seen:
            raise ValueError(f"duplicate stage: {name}")
        seen.add(name)
        users = count(row["users"], f"users for {name}")
        if stages and users > stages[-1]["users"]:
            raise ValueError("stage counts must be nested and non-increasing; do not mix independent event totals")
        stages.append({"stage": name, "users": users})
    if len(stages) < 2:
        raise ValueError("at least two ordered stages are required")
    eligible = stages[0]["users"]
    for index, stage in enumerate(stages):
        stage["share_of_eligible"] = ratio(stage["users"], eligible)
        if index:
            previous = stages[index - 1]
            stage["from_stage"] = previous["stage"]
            stage["step_completion_rate"] = ratio(stage["users"], previous["users"])
            stage["drop_count"] = previous["users"] - stage["users"]
            stage["step_drop_rate"] = ratio(stage["drop_count"], previous["users"])
    maximum = max(stage["drop_count"] for stage in stages[1:])
    return {
        "tool": "funnel_analyzer", "cohort": text(cohort, "cohort"),
        "observation_window": text(window, "window"), "counting_unit": text(unit, "unit"),
        "same_cohort_acknowledged": True, "stages": stages,
        "final_stage_rate": ratio(stages[-1]["users"], eligible),
        "largest_absolute_drop": [{"from": row["from_stage"], "to": row["stage"], "units": maximum}
                                  for row in stages[1:] if row["drop_count"] == maximum],
        "warnings": [
            "Counts must represent the same deduplicated eligible units, ordered prerequisite stages, and a mature outcome window; the acknowledgment cannot verify this.",
            "A large drop identifies where to investigate, not its cause, economic value, or recoverable sales.",
            "Undefined zero-denominator rates are null. Branching or optional stages need separate compatible funnels.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="UTF-8 CSV: stage,users; rows in journey order")
    parser.add_argument("--cohort", required=True, help="Eligible cohort definition")
    parser.add_argument("--window", required=True, help="Cohort entry and outcome observation window")
    parser.add_argument("--unit", required=True, help="Unique counting unit, e.g. account")
    parser.add_argument("--same-cohort", action="store_true", required=True, help="Acknowledge nested unique units and common mature window")
    args = parser.parse_args()
    try:
        emit(analyze(read_csv(args.input, ("stage", "users")), args.cohort, args.window, args.unit))
    except (ValueError, OSError, UnicodeError, csv.Error) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
