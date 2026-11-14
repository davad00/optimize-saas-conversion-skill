#!/usr/bin/env python3
"""Model monthly per-customer contribution, CAC payback, and churn sensitivity."""
import argparse
import sys
sys.dont_write_bytecode = True
from decimal import Decimal, localcontext
from _analytics_common import count, currency, decimal, emit, probability, ratio


def analyze(cac, monthly_revenue, monthly_variable_cost, monthly_churn, horizon_months, code):
    cac = decimal(cac, "cac", Decimal(0))
    revenue = decimal(monthly_revenue, "monthly revenue", Decimal(0))
    cost = decimal(monthly_variable_cost, "monthly variable cost", Decimal(0))
    churn = probability(monthly_churn, "monthly churn")
    horizon = count(horizon_months, "horizon months", positive=True)
    if horizon > 1200:
        raise ValueError("horizon months must be at most 1200")
    code = currency(code)
    with localcontext() as context:
        context.prec = 50
        contribution = revenue - cost
        survival = Decimal(1)
        accumulated = Decimal(0)
        payback = 0 if cac == 0 else None
        schedule = []
        for month in range(1, horizon + 1):
            expected = contribution * survival
            accumulated += expected
            if payback is None and accumulated >= cac:
                payback = month
            schedule.append({"month": month, "active_fraction_at_start": survival,
                             "expected_contribution": expected, "cumulative_contribution": accumulated,
                             "cumulative_after_cac": accumulated - cac})
            survival *= 1 - churn
        ltv = contribution / churn if churn > 0 else None
        return {"tool": "unit_economics", "currency": code,
                "assumptions": {"cac": cac, "monthly_revenue_per_active_customer": revenue,
                                "monthly_variable_cost_per_active_customer": cost,
                                "constant_monthly_logo_churn": churn, "horizon_months": horizon},
                "monthly_contribution_per_active_customer": contribution,
                "contribution_margin": ratio(contribution, revenue),
                "payback_months_ignoring_churn": cac / contribution if contribution > 0 else (Decimal(0) if cac == 0 else None),
                "modeled_payback_month_within_horizon": payback,
                "horizon_expected_contribution": accumulated,
                "horizon_expected_contribution_after_cac": accumulated - cac,
                "constant_churn_lifetime_contribution": ltv,
                "constant_churn_contribution_to_cac": ltv / cac if ltv is not None and cac > 0 else None,
                "schedule": schedule,
                "warnings": [
                    "A new customer contributes for the first month; churn occurs at month end and independently repeats at the same assumed rate.",
                    "Revenue and variable cost remain constant per active customer; no expansion, discounting, taxes, refunds, fixed overhead, cash timing, or capacity constraints are modeled.",
                    "The constant-churn lifetime expression is a geometric-series scenario, not measured LTV or a forecast; zero churn leaves it undefined.",
                    "Payback is contribution recovery, not gross revenue. Null modeled payback means it was not reached within the selected horizon.",
                    "Use matched customer segments and observed cost/churn ranges; rerun assumptions to assess sensitivity before committing spend.",
                ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cac", required=True, help="Acquisition cost per new customer, currency units")
    parser.add_argument("--monthly-revenue", required=True, help="Recurring revenue per active customer/month, currency units")
    parser.add_argument("--monthly-variable-cost", required=True, help="All variable service costs per active customer/month")
    parser.add_argument("--monthly-churn", required=True, help="Assumed monthly logo churn fraction, 0..1")
    parser.add_argument("--horizon-months", required=True, help="Finite modeling horizon, 1..1200")
    parser.add_argument("--currency", required=True, help="Declared three-letter uppercase currency code")
    args = parser.parse_args()
    try:
        emit(analyze(args.cac, args.monthly_revenue, args.monthly_variable_cost, args.monthly_churn, args.horizon_months, args.currency))
    except (ValueError, ArithmeticError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
