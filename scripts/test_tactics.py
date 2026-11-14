#!/usr/bin/env python3
"""Catalog integrity and read-only retrieval regression checks."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

import tactics


SCRIPT = Path(__file__).with_name("tactics.py")


class TacticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = tactics.load_catalog()

    def invoke(self, *args):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), *args], capture_output=True,
                              text=True, timeout=15)

    def result(self, *args):
        result = self.invoke(*args, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_complete_360_record_contract(self):
        self.assertEqual(len(self.records), 360)
        self.assertEqual(tactics.validate_records(self.records), [])
        self.assertEqual(len({r["id"] for r in self.records}), 360)

    def test_every_category_has_twenty_records(self):
        categories = self.result("categories")
        self.assertEqual(len(categories), 18)
        for category in categories:
            found = self.result("list", "--category", category["category"])
            self.assertEqual(len(found), 20)
            self.assertTrue(all(r["category"] == category["category"] for r in found))

    def test_lookup_preserves_requested_id_order_and_full_text(self):
        ids = [self.records[-1]["id"], self.records[0]["id"]]
        result = self.result("show", *ids)
        self.assertEqual([r["id"] for r in result], ids)
        self.assertEqual(result[0], self.records[-1])

    def test_unknown_id_is_an_error_instead_of_a_substitute(self):
        result = self.invoke("show", "PRI-999")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Unknown tactic IDs", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_scope_and_category_filters_do_not_leak_other_actions(self):
        found = self.result("list", "--category", "offers", "--scope", "commercial")
        self.assertTrue(found)
        self.assertTrue(all(r["category"] == "offers" and r["scope"] == "commercial" for r in found))

    def test_search_respects_scope_and_finds_exact_identifier(self):
        expected = self.records[0]
        result = self.result("search", expected["id"], "--limit", "1")
        self.assertEqual([r["id"] for r in result], [expected["id"]])
        found = self.result("search", "payment", "--category", "checkout", "--limit", "3")
        self.assertTrue(found)
        self.assertLessEqual(len(found), 3)
        self.assertTrue(all(r["category"] == "checkout" for r in found))

    def test_empty_search_invalid_filter_and_invalid_limit_fail(self):
        for args in (("search", "the and"), ("list", "--category", "missing"),
                     ("search", "pricing", "--limit", "0")):
            with self.subTest(args=args):
                result = self.invoke(*args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")

    def test_duplicate_interventions_are_rejected(self):
        first = copy.deepcopy(self.records[0])
        second = copy.deepcopy(first)
        second["id"] = first["id"][:-3] + "999"
        errors = tactics.validate_records([first, second], require_counts=False)
        self.assertTrue(any("duplicate title" in error for error in errors))
        self.assertTrue(any("duplicate action" in error for error in errors))

    def test_missing_action_wrong_scope_and_mismatched_id_are_rejected(self):
        bad = copy.deepcopy(self.records[0])
        bad["action"] = ""
        bad["scope"] = "automatically-change-billing"
        bad["id"] = "BAD-001"
        errors = tactics.validate_records([bad], require_counts=False)
        self.assertTrue(any("action" in error for error in errors))
        self.assertTrue(any("scope" in error for error in errors))
        self.assertTrue(any("prefix" in error for error in errors))

    def test_incomplete_catalog_is_rejected(self):
        errors = tactics.validate_records(self.records[:-1])
        self.assertTrue(any("Expected 360" in error for error in errors))
        self.assertTrue(any("missing IDs" in error for error in errors))

    def test_markdown_export_contains_every_record_once(self):
        rendered = tactics.markdown_export(self.records)
        self.assertEqual(rendered.count("### "), 360)
        for record in self.records:
            self.assertEqual(rendered.count(f"### {record['id']} — "), 1)
        self.assertIn("implementation hypotheses", rendered)

    def test_overlap_report_is_a_diagnostic_not_an_automatic_decision(self):
        first = copy.deepcopy(self.records[0])
        second = copy.deepcopy(first)
        second["id"] = "INT-999"
        result = tactics.similar_pairs([first, second])
        self.assertEqual(len(result), 1)
        self.assertAlmostEqual(result[0]["similarity"], 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
