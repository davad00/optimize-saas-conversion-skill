#!/usr/bin/env python3
"""Behavioral and numerical regression checks; run with Python's stdlib only."""

import json
from pathlib import Path
import subprocess
import sys
import unittest


SCRIPT = Path(__file__).with_name("cro_math.py")


class CroMathTests(unittest.TestCase):
    def invoke(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True, timeout=15)

    def result(self, *args):
        completed = self.invoke(*args)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stderr, "")
        def reject_constant(value):
            raise ValueError(f"Nonstandard JSON number: {value}")
        return json.loads(completed.stdout, parse_constant=reject_constant)

    def invalid(self, *args):
        completed = self.invoke(*args)
        self.assertEqual(completed.returncode, 2, completed.stderr)
        self.assertEqual(completed.stdout, "")
        self.assertIn("error:", completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)

    def comparison(self, nc=10000, xc=500, nv=10000, xv=600, *extra):
        return self.result("compare-ab", "--control-users", nc, "--control-conversions", xc,
                           "--variant-users", nv, "--variant-conversions", xv, *extra)

    def test_help_documents_real_commands(self):
        completed = self.invoke("--help")
        self.assertEqual(completed.returncode, 0)
        for command in ("plan-ab", "compare-ab", "pricing", "contrast"):
            self.assertIn(command, completed.stdout)
            self.assertEqual(self.invoke(command, "--help").returncode, 0)

    def test_sample_size_benchmark_and_accrual(self):
        # Standard two-normal approximation; independently checked with SciPy
        # normal-tail power at n=8158: 0.800014 (not a runtime dependency).
        result = self.result("plan-ab", "--baseline", .05, "--relative-mde", .20,
                             "--eligible-users-per-day", 1000)
        self.assertEqual(result["users_per_arm"], 8158)
        self.assertEqual(result["users_total"], 16316)
        self.assertEqual(result["minimum_accrual_days"], 17)
        self.assertAlmostEqual(result["mde_percentage_points"], 1)
        self.assertAlmostEqual(result["target_rate"], .06)
        absolute = self.result("plan-ab", "--baseline", .05, "--absolute-mde", .01)
        self.assertEqual(absolute["users_per_arm"], result["users_per_arm"])

    def test_planning_power_and_precision_require_more_users(self):
        base = self.result("plan-ab", "--baseline", .05, "--absolute-mde", .01)
        narrow = self.result("plan-ab", "--baseline", .05, "--absolute-mde", .005)
        powerful = self.result("plan-ab", "--baseline", .05, "--absolute-mde", .01, "--power", .9)
        self.assertGreater(narrow["users_per_arm"], base["users_per_arm"])
        self.assertGreater(powerful["users_per_arm"], base["users_per_arm"])

    def test_planning_invalid_inputs(self):
        for baseline in ("0", "1", "NaN", "inf", "-0.1"):
            with self.subTest(baseline=baseline):
                self.invalid("plan-ab", "--baseline", baseline, "--relative-mde", .2)
        for extra in (("--absolute-mde", "0"), ("--absolute-mde", "1"),
                      ("--absolute-mde", "1e-300"), ("--relative-mde", "NaN"),
                      ("--relative-mde", ".2", "--power", ".5"),
                      ("--relative-mde", ".2", "--alpha", "1e-300"),
                      ("--relative-mde", ".2", "--absolute-mde", ".01")):
            with self.subTest(extra=extra):
                self.invalid("plan-ab", "--baseline", .05, *extra)

    def test_conversion_benchmark_matches_independent_reference(self):
        result = self.comparison()
        diff = result["variant_minus_control"]
        # Wilson and Pearson values independently checked using SciPy.
        self.assertAlmostEqual(result["control"]["wilson_ci"][0], .045898482690584774, places=13)
        self.assertAlmostEqual(result["control"]["wilson_ci"][1], .054447115843024155, places=13)
        self.assertAlmostEqual(diff["pooled_two_sided_normal_p_value"], .0019246872509622623, places=14)
        self.assertAlmostEqual(diff["percentage_point_difference"], 1)
        self.assertAlmostEqual(diff["relative_lift"], .2)
        self.assertLess(diff["newcombe_wilson_ci"][0], diff["rate_difference"])
        self.assertGreater(diff["newcombe_wilson_ci"][1], diff["rate_difference"])
        self.assertFalse(result["sample_ratio_mismatch"]["investigate"])
        self.assertNotIn("winner", result)

    def test_difference_symmetry_when_groups_are_swapped(self):
        original = self.comparison(1200, 61, 900, 59)["variant_minus_control"]
        swapped = self.comparison(900, 59, 1200, 61)["variant_minus_control"]
        self.assertAlmostEqual(original["rate_difference"], -swapped["rate_difference"])
        self.assertAlmostEqual(original["newcombe_wilson_ci"][0], -swapped["newcombe_wilson_ci"][1])
        self.assertAlmostEqual(original["newcombe_wilson_ci"][1], -swapped["newcombe_wilson_ci"][0])
        self.assertAlmostEqual(original["pooled_two_sided_normal_p_value"], swapped["pooled_two_sided_normal_p_value"])

    def test_zero_conversions_have_defined_absolute_uncertainty(self):
        result = self.comparison(100, 0, 100, 0)
        diff = result["variant_minus_control"]
        self.assertIsNone(diff["relative_lift"])
        self.assertIsNone(diff["pooled_two_sided_normal_p_value"])
        self.assertLess(diff["newcombe_wilson_ci"][0], 0)
        self.assertGreater(diff["newcombe_wilson_ci"][1], 0)
        self.assertGreater(result["control"]["wilson_ci"][1], 0)

    def test_all_conversions_and_small_samples_stay_bounded(self):
        for counts in ((100, 100, 100, 100), (1, 0, 1, 1), (4, 1, 5, 2)):
            with self.subTest(counts=counts):
                result = self.comparison(*counts)
                self.assertIsNone(result["variant_minus_control"]["pooled_two_sided_normal_p_value"])
                lower, upper = result["variant_minus_control"]["newcombe_wilson_ci"]
                self.assertGreaterEqual(lower, -1)
                self.assertLessEqual(upper, 1)
                self.assertLessEqual(lower, upper)

    def test_sample_ratio_mismatch_is_diagnostic_and_supports_planned_split(self):
        mismatched = self.comparison(8000, 400, 12000, 600)
        self.assertTrue(mismatched["sample_ratio_mismatch"]["investigate"])
        self.assertLess(mismatched["sample_ratio_mismatch"]["p_value"], .001)
        planned = self.comparison(8000, 400, 12000, 600, "--expected-variant-share", .6)
        self.assertFalse(planned["sample_ratio_mismatch"]["investigate"])
        self.assertEqual(planned["sample_ratio_mismatch"]["p_value"], 1)
        tiny = self.comparison(1, 0, 1, 1)
        self.assertIsNone(tiny["sample_ratio_mismatch"]["investigate"])

    def test_counts_reject_fractional_negative_impossible_or_oversized_values(self):
        base = ["compare-ab", "--control-users", "100", "--control-conversions", "5",
                "--variant-users", "100", "--variant-conversions", "6"]
        for index, value in ((2, "0"), (2, "2.5"), (4, "-1"), (4, "101"),
                             (6, str(2**53)), (8, "NaN")):
            with self.subTest(index=index, value=value):
                args = base.copy()
                args[index] = value
                self.invalid(*args)

    def test_annual_savings_exact_fraction_and_billing_label(self):
        result = self.result("pricing", "--monthly-price", "24", "--annual-price", "228")
        self.assertEqual(result["comparison"], "discount")
        self.assertEqual(result["annual_amount_saved_vs_monthly"], "60")
        self.assertEqual(result["percent_saved_exact_fraction"], "125/6")
        self.assertEqual(result["monthly_equivalent_exact_fraction"], "19")
        self.assertIn("USD 228 per year, billed annually", result["billing_label"])

    def test_decimal_money_surcharge_and_display_precision(self):
        # 0.10 * 12 is exactly 1.20; no binary-float money arithmetic.
        result = self.result("pricing", "--monthly-price", ".10", "--annual-price", "1.08")
        self.assertEqual(result["annual_amount_saved_vs_monthly"], "0.12")
        self.assertEqual(result["percent_saved_exact_fraction"], "10")
        surcharge = self.result("pricing", "--monthly-price", "10", "--annual-price", "132")
        self.assertEqual(surcharge["comparison"], "surcharge")
        self.assertEqual(surcharge["percent_saved_exact_fraction"], "-10")
        repeating = self.result("pricing", "--monthly-price", "24", "--annual-price", "230", "--display-decimals", "2")
        self.assertEqual(repeating["monthly_equivalent_exact_fraction"], "115/6")
        self.assertIn("approximately USD 19.17", repeating["billing_label"])

    def test_money_invalid_inputs(self):
        for value in ("0", "-1", "NaN", "sNaN", "Infinity", "1e1000000"):
            with self.subTest(value=value):
                self.invalid("pricing", "--monthly-price", value, "--annual-price", "120")
        self.invalid("pricing", "--monthly-price", "10", "--annual-price", "120", "--currency", "US dollars")
        self.invalid("pricing", "--monthly-price", "10", "--annual-price", "120", "--display-decimals", "20")

    def test_black_white_and_identical_color_contrast(self):
        result = self.result("contrast", "#000", "#FFF")
        self.assertEqual(result["contrast_ratio"], 21)
        self.assertTrue(result["wcag_2_aa_normal_text_4_5"])
        same = self.result("contrast", "#fff", "#ffffff")
        self.assertEqual(same["contrast_ratio"], 1)
        self.assertFalse(same["wcag_2_aa_large_text_3"])

    def test_contrast_must_not_round_a_failure_into_a_pass(self):
        borderline = self.result("contrast", "#777", "#fff")
        self.assertAlmostEqual(borderline["contrast_ratio"], 4.478089453577214, places=12)
        self.assertFalse(borderline["wcag_2_aa_normal_text_4_5"])
        self.assertTrue(borderline["wcag_2_aa_large_text_3"])
        better = self.result("contrast", "#767676", "#ffffff")
        self.assertTrue(better["wcag_2_aa_normal_text_4_5"])
        reversed_colors = self.result("contrast", "#fff", "#777")
        self.assertEqual(borderline["contrast_ratio"], reversed_colors["contrast_ratio"])

    def test_contrast_rejects_alpha_and_non_hex_inputs(self):
        for color in ("#ffff", "#ffffffff", "white", "#ggg", "#12345"):
            with self.subTest(color=color):
                self.invalid("contrast", color, "#000")


if __name__ == "__main__":
    unittest.main(verbosity=2)
