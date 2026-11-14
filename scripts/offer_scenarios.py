#!/usr/bin/env python3
"""Compare assumed new-customer offers: buyers, first-charge cash, and run rates."""
import argparse
import sys
sys.dont_write_bytecode = True
from decimal import Decimal, localcontext
from _analytics_common import count, currency, decimal, emit, probability, read_json, require_keys, text


PLAN_KEYS = ("name", "share", "price", "interval_months", "full_refund_rate", "monthly_service_cost", "payment_fee_rate", "payment_fee_fixed")


def analyze(data):
    require_keys(data, ("currency", "eligible_units", "scenarios"), "input")
    code = currency(data["currency"])
    eligible = count(data["eligible_units"], "eligible_units", positive=True)
    scenarios = data["scenarios"]
    if not isinstance(scenarios, list) or not 1 <= len(scenarios) <= 100:
        raise ValueError("scenarios must contain 1 to 100 objects")
    output = []
    names = set()
    with localcontext() as context:
        context.prec = 50
        for scenario in scenarios:
            require_keys(scenario, ("name", "paid_conversion_rate", "plans"), "scenario")
            name = text(scenario["name"], "scenario name")
            if name in names:
                raise ValueError(f"duplicate scenario name: {name}")
            names.add(name)
            conversion = probability(scenario["paid_conversion_rate"], "paid conversion rate")
            plans = scenario["plans"]
            if not isinstance(plans, list) or not 1 <= len(plans) <= 100:
                raise ValueError("each scenario needs 1 to 100 plans")
            parsed = []
            plan_names = set()
            for plan in plans:
                require_keys(plan, PLAN_KEYS, "plan")
                plan_name = text(plan["name"], "plan name")
                if plan_name in plan_names:
                    raise ValueError(f"duplicate plan name within scenario: {plan_name}")
                plan_names.add(plan_name)
                interval = count(plan["interval_months"], "interval months", positive=True)
                if interval > 120:
                    raise ValueError("interval_months must be at most 120")
                parsed.append({"name": plan_name, "share": probability(plan["share"], "plan share"),
                               "price": decimal(plan["price"], "price", Decimal(0)), "interval_months": interval,
                               "full_refund_rate": probability(plan["full_refund_rate"], "full refund rate"),
                               "monthly_service_cost": decimal(plan["monthly_service_cost"], "monthly service cost", Decimal(0)),
                               "payment_fee_rate": probability(plan["payment_fee_rate"], "payment fee rate"),
                               "payment_fee_fixed": decimal(plan["payment_fee_fixed"], "payment fee fixed", Decimal(0))})
            if sum(plan["share"] for plan in parsed) != Decimal(1):
                raise ValueError(f"plan shares must sum exactly to 1 in scenario {name}")
            if any(plan["price"] <= 0 and plan["share"] > 0 for plan in parsed):
                raise ValueError("positive-share paid plans require a positive price; exclude free signups from paid_conversion_rate")
            buyers = eligible * conversion
            totals = {key: Decimal(0) for key in (
                "expected_buyers", "expected_non_refunded_buyers", "first_charge_gross_cash", "full_refund_cash",
                "payment_fees", "first_charge_net_cash_after_refunds_and_fees", "new_normalized_mrr_before_refunds",
                "new_normalized_mrr_after_full_refunds", "first_term_service_cost", "first_term_contribution",
                "normalized_monthly_service_cost", "normalized_monthly_payment_fees", "normalized_monthly_contribution")}
            details = []
            for plan in parsed:
                n = buyers * plan["share"]
                gross = n * plan["price"]
                refunds = gross * plan["full_refund_rate"]
                fees = n * (plan["price"] * plan["payment_fee_rate"] + plan["payment_fee_fixed"])
                retained = n * (1 - plan["full_refund_rate"])
                service = n * plan["monthly_service_cost"] * plan["interval_months"]
                net = gross - refunds - fees
                recurring = retained * plan["price"] / plan["interval_months"]
                monthly_service = n * plan["monthly_service_cost"]
                monthly_fees = fees / plan["interval_months"]
                result = {"expected_buyers": n, "expected_non_refunded_buyers": retained,
                          "first_charge_gross_cash": gross, "full_refund_cash": refunds,
                          "payment_fees": fees, "first_charge_net_cash_after_refunds_and_fees": net,
                          "new_normalized_mrr_before_refunds": gross / plan["interval_months"],
                          "new_normalized_mrr_after_full_refunds": recurring,
                          "first_term_service_cost": service, "first_term_contribution": net - service,
                          "normalized_monthly_service_cost": monthly_service,
                          "normalized_monthly_payment_fees": monthly_fees,
                          "normalized_monthly_contribution": recurring - monthly_service - monthly_fees}
                details.append({"plan": plan["name"], "assumptions": plan, **result})
                for key in totals:
                    totals[key] += result[key]
            output.append({"name": name, "assumed_paid_conversion_rate": conversion, "plans": details, "totals": totals})
    return {"tool": "offer_scenarios", "currency": code, "eligible_units": eligible, "scenarios": output,
            "warnings": [
                "All conversion rates, mix, prices, refunds, fees, and costs are supplied assumptions. Fractional expected customers are arithmetic expectations, not observed customers or forecasts.",
                "Cash covers the first charge only. Annual cash is separate from monthly-normalized recurring value; neither is accounting revenue recognition.",
                "Full refunds remove the entire first charge and recurring value. Payment fees are assumed nonrefundable; service cost is conservatively incurred for every buyer's full first term, including refunded buyers.",
                "First-term totals span different durations when intervals differ. Use normalized comparisons with their assumptions; do not call a larger annual cash receipt more profit.",
                "No renewals, churn after the refund window, acquisition costs, taxes, overhead, partial refunds, or payment failures are modeled. Use unit_economics for explicit monthly churn scenarios.",
                "No offer or billing configuration is changed. Commercial terms remain proposals until authorized.",
            ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Local JSON with currency, eligible_units, scenarios; see references/analytics-tools.md")
    args = parser.parse_args()
    try:
        emit(analyze(read_json(args.input)))
    except (ValueError, OSError, UnicodeError, ArithmeticError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
