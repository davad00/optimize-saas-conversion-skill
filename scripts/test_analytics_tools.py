#!/usr/bin/env python3
"""Numerical and data-contract tests for the six read-only analytics tools."""
import csv
from decimal import Decimal
import importlib.util
import io
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).parent
TOOLS = ("funnel_analyzer", "cohort_retention", "revenue_bridge", "experiment_guardrails", "unit_economics", "offer_scenarios")


class AnalyticsToolsTests(unittest.TestCase):
    def run_tool(self, tool, *args, payload=None):
        with tempfile.TemporaryDirectory() as directory:
            command = [sys.executable, str(ROOT / (tool + ".py")), *map(str, args)]
            if payload is not None:
                path = Path(directory) / "input.txt"
                path.write_text(payload, encoding="utf-8")
                command += ["--input", str(path)]
            return subprocess.run(command, capture_output=True, text=True, timeout=20)

    def result(self, tool, *args, payload=None):
        result = self.run_tool(tool, *args, payload=payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout, parse_constant=lambda x: self.fail("nonfinite output: " + x))

    def invalid(self, tool, *args, payload=None):
        result = self.run_tool(tool, *args, payload=payload)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertIn("error:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def funnel(self, payload, *args):
        return self.result("funnel_analyzer", "--cohort", "eligible accounts", "--window", "entry Jan; 30-day follow-up",
                           "--unit", "account", "--same-cohort", *args, payload=payload)

    def test_all_six_help_and_missing_input_are_clean(self):
        for tool in TOOLS:
            with self.subTest(tool=tool):
                result = self.run_tool(tool, "--help")
                self.assertEqual(result.returncode, 0)
                self.assertIn("usage:", result.stdout)
                self.invalid(tool)

    def test_funnel_rates_and_largest_absolute_drop(self):
        result = self.funnel("stage,users\nlanding,1000\nsignup,250\nactivated,100\npaid,20\n")
        self.assertEqual(result["final_stage_rate"], .02)
        self.assertEqual(result["stages"][2]["step_completion_rate"], .4)
        self.assertEqual(result["largest_absolute_drop"], [{"from": "landing", "to": "signup", "units": 750}])

    def test_funnel_zero_denominator_is_null(self):
        result = self.funnel("stage,users\nlanding,0\npaid,0\n")
        self.assertIsNone(result["final_stage_rate"])
        self.assertIsNone(result["stages"][1]["step_completion_rate"])

    def test_funnel_requires_nested_counts_and_acknowledgment(self):
        args = ("--cohort", "x", "--window", "y", "--unit", "account")
        self.invalid("funnel_analyzer", *args, payload="stage,users\na,10\nb,5\n")
        for payload in ("stage,users\na,10\nb,11\n", "stage,users\na,10\na,5\n", "stage,users\na,NaN\nb,0\n"):
            self.invalid("funnel_analyzer", *args, "--same-cohort", payload=payload)

    def test_cohort_weights_and_excludes_immature_cells(self):
        payload = "cohort,period,eligible,retained,mature\nA,1,100,80,true\nA,2,100,70,true\nB,1,20,10,true\nB,2,20,,false\n"
        result = self.result("cohort_retention", "--mode", "point", payload=payload)
        self.assertEqual(result["weighted_by_period"][0]["weighted_rate"], .75)
        self.assertEqual(result["weighted_by_period"][1]["weighted_rate"], .7)
        self.assertEqual(result["weighted_by_period"][1]["eligible"], 100)
        self.assertEqual(result["weighted_by_period"][1]["immature_cohorts"], 1)

    def test_cohort_missing_period_is_not_zero(self):
        result = self.result("cohort_retention", "--mode", "point", payload="cohort,period,eligible,retained,mature\nA,1,10,8,1\nA,3,10,7,1\n")
        self.assertEqual(result["gaps"][0]["missing_periods_between_first_and_last"], [2])
        self.assertEqual([x["period"] for x in result["weighted_by_period"]], [1, 3])

    def test_cohort_survival_and_point_have_distinct_semantics(self):
        payload = "cohort,period,eligible,retained,mature\nA,1,10,5,1\nA,2,10,7,1\n"
        self.result("cohort_retention", "--mode", "point", payload=payload)
        self.invalid("cohort_retention", "--mode", "survival", payload=payload)

    def test_cohort_rejects_denominator_drift_and_fake_maturity(self):
        header = "cohort,period,eligible,retained,mature\n"
        for values in ("A,1,10,8,1\nA,2,8,7,1\n", "A,1,10,8,0\n", "A,1,10,,0\nA,2,10,8,1\n", "A,1,10,11,1\n", "A,1,10,8,1\nA,1,10,8,1\n"):
            self.invalid("cohort_retention", "--mode", "point", payload=header + values)

    def test_revenue_bridge_reconciles_and_separates_currencies(self):
        payload = "account_id,currency,start_mrr_minor,end_mrr_minor\na,USD,10000,15000\nb,USD,20000,12000\nc,USD,5000,0\nd,USD,0,7000\na,EUR,10000,10000\n"
        result = self.result("revenue_bridge", payload=payload)
        groups = {row["currency"]: row for row in result["currencies"]}
        usd = groups["USD"]
        self.assertEqual(usd["end_mrr_minor"], 34000)
        self.assertEqual(usd["expansion_mrr_minor"], 5000)
        self.assertEqual(usd["contraction_mrr_minor"], 8000)
        self.assertEqual(usd["churned_mrr_minor"], 5000)
        self.assertAlmostEqual(usd["gross_revenue_retention"], 22000 / 35000)
        self.assertAlmostEqual(usd["net_revenue_retention"], 27000 / 35000)
        self.assertTrue(usd["reconciles"])
        self.assertEqual(groups["EUR"]["end_mrr_minor"], 10000)
        self.assertNotIn("total_mrr", result)

    def test_revenue_zero_start_and_duplicates(self):
        header = "account_id,currency,start_mrr_minor,end_mrr_minor\n"
        result = self.result("revenue_bridge", payload=header + "a,USD,0,100\n")
        self.assertIsNone(result["currencies"][0]["net_revenue_retention"])
        for values in ("a,USD,1,1\na,USD,1,2\n", "a,usd,1,2\n", "a,USD,1.5,2\n", "a,USD,-1,2\n"):
            self.invalid("revenue_bridge", payload=header + values)

    def assignments(self, numbers):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["unit_id", "variant", "event", "occurred_at"])
        for variant, number in numbers.items():
            for index in range(number):
                writer.writerow([f"{variant}-{index}", variant, "assigned", "2026-01-01T00:00:00Z"])
        return output.getvalue()

    def test_experiment_two_arm_and_three_arm_srm(self):
        balanced = self.result("experiment_guardrails", "--allocation", '{"A":0.5,"B":0.5}', payload=self.assignments({"A": 50, "B": 50}))
        self.assertEqual(balanced["srm"]["p_value"], 1)
        self.assertFalse(balanced["srm"]["mismatch_detected"])
        unbalanced = self.result("experiment_guardrails", "--allocation", '{"A":0.5,"B":0.5}', payload=self.assignments({"A": 80, "B": 20}))
        self.assertAlmostEqual(unbalanced["srm"]["chi_square"], 36)
        self.assertAlmostEqual(unbalanced["srm"]["p_value"], math.erfc(math.sqrt(18)), places=15)
        self.assertTrue(unbalanced["srm"]["mismatch_detected"])
        multi = self.result("experiment_guardrails", "--allocation", '{"A":0.5,"B":0.25,"C":0.25}', payload=self.assignments({"A": 60, "B": 30, "C": 10}))
        self.assertAlmostEqual(multi["srm"]["chi_square"], 12)
        self.assertAlmostEqual(multi["srm"]["p_value"], math.exp(-6), places=14)

    def test_experiment_small_samples_omit_approximation(self):
        result = self.result("experiment_guardrails", "--allocation", '{"A":0.5,"B":0.5}', payload=self.assignments({"A": 2, "B": 2}))
        self.assertIsNone(result["srm"]["p_value"])

    def test_multiarm_tail_matches_standard_critical_values(self):
        spec = importlib.util.spec_from_file_location("experiment_guardrails", ROOT / "experiment_guardrails.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for degrees, statistic in ((1, 3.841458820694124), (2, 5.991464547107979),
                                   (3, 7.814727903251179), (5, 11.070497693516351),
                                   (10, 18.307038053275146), (99, 123.2252214533618)):
            with self.subTest(degrees=degrees):
                self.assertAlmostEqual(module.chi_square_tail(statistic, degrees), .05, places=12)

    def test_experiment_duplicates_are_deduped_and_reassignment_is_flagged(self):
        base = self.assignments({"A": 10, "B": 10})
        duplicate = "A-0,A,assigned,2026-01-01T00:00:00Z\n"
        result = self.result("experiment_guardrails", "--allocation", '{"A":0.5,"B":0.5}', payload=base + duplicate)
        self.assertEqual(result["exact_duplicate_rows_ignored"], 1)
        self.assertEqual(result["srm"]["p_value"], 1)
        result = self.result("experiment_guardrails", "--allocation", '{"A":0.5,"B":0.5}', payload=base + "A-0,B,assigned,2026-01-02T00:00:00Z\n")
        self.assertEqual(result["issues"]["variant_conflict"]["unit_count"], 1)
        self.assertFalse(result["assignment_integrity_checks_pass"])
        self.assertIsNone(result["srm"]["p_value"])

    def test_experiment_missing_assignment_and_order_defects(self):
        payload = self.assignments({"A": 10, "B": 10})
        payload += "missing,A,exposed,2026-01-01T00:00:00Z\nA-0,A,converted,2025-12-31T00:00:00Z\n"
        result = self.result("experiment_guardrails", "--allocation", '{"A":0.5,"B":0.5}', payload=payload)
        self.assertEqual(result["issues"]["missing_assignment"]["unit_count"], 1)
        self.assertEqual(result["issues"]["event_before_assignment"]["unit_count"], 1)
        self.assertIsNone(result["srm"]["p_value"])

    def test_experiment_invalid_allocations_and_timestamps(self):
        payload = self.assignments({"A": 10, "B": 10})
        for allocation in ('{"A":0.8,"B":0.8}', '{"A":1,"B":0}', '{"A":NaN,"B":0.5}', '{"A":0.5,"A":0.5}', '[]'):
            self.invalid("experiment_guardrails", "--allocation", allocation, payload=payload)
        self.invalid("experiment_guardrails", "--allocation", '{"A":0.5,"B":0.5}', payload=payload.replace("2026-01-01T00:00:00Z", "2026-01-01"))

    def economy(self, *extra):
        return self.result("unit_economics", "--cac", "100", "--monthly-revenue", "20", "--monthly-variable-cost", "5",
                           "--monthly-churn", "0.1", "--horizon-months", "12", "--currency", "USD", *extra)

    def test_unit_economics_finite_horizon_and_churn_payback(self):
        result = self.economy()
        self.assertEqual(result["monthly_contribution_per_active_customer"], "15")
        self.assertEqual(Decimal(result["horizon_expected_contribution"]), Decimal("107.63556952785"))
        self.assertEqual(result["modeled_payback_month_within_horizon"], 11)
        self.assertEqual(result["constant_churn_lifetime_contribution"], "150")

    def test_unit_economics_churn_boundaries_and_negative_margin(self):
        zero = self.economy("--monthly-churn", "0")
        self.assertEqual(zero["horizon_expected_contribution"], "180")
        self.assertIsNone(zero["constant_churn_lifetime_contribution"])
        self.assertEqual(zero["modeled_payback_month_within_horizon"], 7)
        full = self.economy("--monthly-churn", "1")
        self.assertEqual(full["horizon_expected_contribution"], "15")
        self.assertIsNone(full["modeled_payback_month_within_horizon"])
        negative = self.economy("--monthly-variable-cost", "30")
        self.assertEqual(negative["monthly_contribution_per_active_customer"], "-10")
        self.assertIsNone(negative["payback_months_ignoring_churn"])

    def test_unit_economics_rejects_nonfinite_and_invalid_rates(self):
        args = ["--cac", "100", "--monthly-revenue", "20", "--monthly-variable-cost", "5", "--monthly-churn", ".1", "--horizon-months", "12", "--currency", "USD"]
        for extra in (("--cac", "NaN"), ("--monthly-revenue", "Infinity"), ("--monthly-churn", "1.1"), ("--horizon-months", "0")):
            self.invalid("unit_economics", *args, *extra)

    def offer(self):
        plan = {"name": "Annual", "share": "1", "price": "120", "interval_months": 12, "full_refund_rate": "0.1",
                "monthly_service_cost": "2", "payment_fee_rate": "0.03", "payment_fee_fixed": "0.3"}
        return {"currency": "USD", "eligible_units": 1000, "scenarios": [{"name": "Annual offer", "paid_conversion_rate": "0.02", "plans": [plan]}]}

    def test_offer_separates_cash_mrr_refunds_and_costs(self):
        result = self.result("offer_scenarios", payload=json.dumps(self.offer()))
        total = result["scenarios"][0]["totals"]
        self.assertEqual(total["expected_buyers"], "20")
        self.assertEqual(total["expected_non_refunded_buyers"], "18")
        self.assertEqual(total["first_charge_gross_cash"], "2400")
        self.assertEqual(total["new_normalized_mrr_before_refunds"], "200")
        self.assertEqual(total["new_normalized_mrr_after_full_refunds"], "180")
        self.assertEqual(total["payment_fees"], "78")
        self.assertEqual(total["first_charge_net_cash_after_refunds_and_fees"], "2082")
        self.assertEqual(total["first_term_service_cost"], "480")
        self.assertEqual(total["normalized_monthly_contribution"], "133.5")

    def test_offer_validates_commercial_assumptions(self):
        for key, value in (("share", ".9"), ("price", "NaN"), ("price", "0"), ("full_refund_rate", "1.1"), ("interval_months", 0)):
            data = self.offer()
            data["scenarios"][0]["plans"][0][key] = value
            self.invalid("offer_scenarios", payload=json.dumps(data))
        data = self.offer()
        del data["scenarios"][0]["plans"][0]["payment_fee_fixed"]
        self.invalid("offer_scenarios", payload=json.dumps(data))

    def test_common_parser_rejects_duplicate_headers_and_malformed_json(self):
        self.invalid("revenue_bridge", payload="account_id,currency,start_mrr_minor,end_mrr_minor,currency\na,USD,1,2,USD\n")
        self.invalid("offer_scenarios", payload='{"currency":"USD","currency":"EUR"}')
        self.invalid("offer_scenarios", payload='{"currency":')

    def test_commands_do_not_create_bytecode_or_output_files(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            for name in ("unit_economics.py", "_analytics_common.py"):
                (folder / name).write_text((ROOT / name).read_text(), encoding="utf-8")
            before = set(folder.iterdir())
            completed = subprocess.run([sys.executable, str(folder / "unit_economics.py"),
                                        "--cac", "100", "--monthly-revenue", "20", "--monthly-variable-cost", "5",
                                        "--monthly-churn", ".1", "--horizon-months", "12", "--currency", "USD"],
                                       capture_output=True, text=True, timeout=20, cwd=folder)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(set(folder.iterdir()), before)


if __name__ == "__main__":
    unittest.main()
