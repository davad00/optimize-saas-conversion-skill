#!/usr/bin/env python3
"""Decompose two account MRR snapshots by currency; read-only integer arithmetic."""
import argparse
import sys
sys.dont_write_bytecode = True
from collections import defaultdict
import csv
from _analytics_common import count, currency, emit, read_csv, ratio, text


def analyze(rows):
    groups = defaultdict(lambda: {"start_mrr_minor": 0, "end_mrr_minor": 0, "new_mrr_minor": 0,
                                 "expansion_mrr_minor": 0, "contraction_mrr_minor": 0,
                                 "churned_mrr_minor": 0, "accounts": 0,
                                 "new_accounts": 0, "churned_accounts": 0, "starting_accounts": 0})
    seen = set()
    for row in rows:
        account = text(row["account_id"], "account_id")
        code = currency(row["currency"])
        key = (account, code)
        if key in seen:
            raise ValueError(f"duplicate account/currency snapshot: {account}/{code}")
        seen.add(key)
        start = count(row["start_mrr_minor"], "start_mrr_minor")
        end = count(row["end_mrr_minor"], "end_mrr_minor")
        group = groups[code]
        group["start_mrr_minor"] += start
        group["end_mrr_minor"] += end
        group["accounts"] += 1
        group["starting_accounts"] += int(start > 0)
        if start == 0 and end > 0:
            group["new_mrr_minor"] += end
            group["new_accounts"] += 1
        elif start > 0 and end == 0:
            group["churned_mrr_minor"] += start
            group["churned_accounts"] += 1
        elif end > start:
            group["expansion_mrr_minor"] += end - start
        elif end < start:
            group["contraction_mrr_minor"] += start - end
    currencies = []
    for code, group in sorted(groups.items()):
        start = group["start_mrr_minor"]
        lost = group["churned_mrr_minor"] + group["contraction_mrr_minor"]
        existing_end = start - lost + group["expansion_mrr_minor"]
        group.update({"currency": code,
                      "net_change_mrr_minor": group["end_mrr_minor"] - start,
                      "gross_revenue_retention": ratio(start - lost, start),
                      "net_revenue_retention": ratio(existing_end, start),
                      "logo_retention": ratio(group["starting_accounts"] - group["churned_accounts"], group["starting_accounts"]),
                      "reconciles": existing_end + group["new_mrr_minor"] == group["end_mrr_minor"]})
        currencies.append(group)
    return {"tool": "revenue_bridge", "currencies": currencies,
            "warnings": [
                "Inputs must be monthly-normalized recurring values in each currency's declared minor unit, with consistent tax, discount, delinquency, and rounding policies.",
                "Currency groups are never added together. MRR is not cash collected or accounting revenue.",
                "Two snapshots show net movement, not all intervening transactions; zero-to-positive includes reactivation unless segmented upstream.",
                "GRR and NRR exclude new accounts from their numerators; zero starting MRR produces null retention rates.",
            ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="CSV: account_id,currency,start_mrr_minor,end_mrr_minor")
    args = parser.parse_args()
    try:
        emit(analyze(read_csv(args.input, ("account_id", "currency", "start_mrr_minor", "end_mrr_minor"))))
    except (ValueError, OSError, UnicodeError, csv.Error) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
