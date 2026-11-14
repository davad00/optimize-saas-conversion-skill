"""Functional checks for resource retrieval, offer consistency, events and HTML."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import event_validator
import journey_lint
import offer_consistency
import resource_finder
from _sales_common import loads, safe_path

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent


def offer_fixture():
    return {"version": 1, "catalog": [
        {"plan_id": "basic", "interval": "month", "currency": "USD", "charge_minor": 1200, "unit": "flat", "provider_price_id": "pm"},
        {"plan_id": "basic", "interval": "year", "currency": "USD", "charge_minor": 11520, "unit": "flat", "provider_price_id": "py"}],
        "observations": [{"name": "annual card", "surface": "pricing", "plan_id": "basic", "interval": "year", "currency": "USD", "quantity": 1,
                          "headline_minor": 960, "headline_basis": "month", "headline_scope": "total", "disclosed_charge_minor": 11520,
                          "disclosed_interval": "year", "savings_percent": 20},
                         {"name": "annual checkout", "surface": "checkout", "plan_id": "basic", "interval": "year", "currency": "USD", "quantity": 1,
                          "displayed_due_now_minor": 11520, "quoted_due_now_minor": 11520, "disclosed_interval": "year", "submitted_price_id": "py"}],
        "default": {"selected_interval": "year", "reason": "New undecided buyer of an ongoing discounted service; explicit choices persist"}}


def event_fixture():
    contract = {"events": [{"name": "purchase_completed", "required": ["unit_id", "transaction_id", "provider", "amount_minor_units", "currency", "occurred_at"],
                            "dedupe_key": ["provider", "transaction_id"], "allowed_sources": ["billing_server"]}]}
    event = {"event": "purchase_completed", "event_id": "delivery-1", "unit_id": "u1", "transaction_id": "tx1", "provider": "example",
             "amount_minor_units": 11520, "currency": "USD", "occurred_at": "2026-01-01T00:00:00Z", "source": "billing_server"}
    return contract, event


class OfferTests(unittest.TestCase):
    def test_correct_annual_comparison_and_provider_quote(self):
        result = offer_consistency.validate(offer_fixture())
        self.assertTrue(result["valid"])
        self.assertEqual(result["checks"][0]["monthly_equivalent_total_minor"], "960")

    def test_original_annual_headline_problem_is_reported(self):
        data = offer_fixture()
        data["observations"][0].update(headline_minor=11520, headline_basis="year")
        result = offer_consistency.validate(data)
        self.assertFalse(result["valid"])
        self.assertIn("annual_headline_basis", {f["code"] for f in result["findings"]})

    def test_wrong_provider_interval_and_due_now(self):
        data = offer_fixture()
        data["observations"][1].update(submitted_price_id="pm", displayed_due_now_minor=960)
        result = offer_consistency.validate(data)
        self.assertEqual({f["code"] for f in result["findings"]}, {"wrong_submitted_price", "due_now_mismatch"})

    def test_no_due_now_quote_is_unverified(self):
        data = offer_fixture()
        del data["observations"][1]["quoted_due_now_minor"]
        self.assertIn("due_now_unverified", {f["code"] for f in offer_consistency.validate(data)["findings"]})

    def test_minimum_seats_and_payload_continuity(self):
        data = offer_fixture()
        for row in data["catalog"]:
            row.update(unit="per_unit", min_quantity=5)
        data["observations"][0]["submitted_quantity"] = 5
        codes = {f["code"] for f in offer_consistency.validate(data)["findings"]}
        self.assertIn("below_minimum_quantity", codes)
        self.assertIn("wrong_submitted_quantity", codes)

    def test_per_unit_checkout_requires_submitted_quantity(self):
        data = offer_fixture()
        for row in data["catalog"]:
            row.update(unit="per_unit", min_quantity=5)
        data["observations"] = [data["observations"][1]]
        data["observations"][0]["quantity"] = 5
        result = offer_consistency.validate(data)
        self.assertFalse(result["valid"])
        self.assertIn("checkout_quantity_unverified", {f["code"] for f in result["findings"]})

    def test_half_up_rounding_and_false_discount(self):
        data = offer_fixture()
        data["catalog"][1]["charge_minor"] = 10002
        data["observations"] = [data["observations"][0]]
        data["observations"][0].update(headline_minor=834, disclosed_charge_minor=10002, savings_percent=20)
        codes = {f["code"] for f in offer_consistency.validate(data)["findings"]}
        self.assertNotIn("headline_amount", codes)
        self.assertIn("savings_mismatch", codes)

    def test_zero_discount_is_valid_when_prices_are_equal(self):
        data = offer_fixture()
        data["catalog"][1]["charge_minor"] = 14400
        data["observations"] = [data["observations"][0]]
        data["observations"][0].update(headline_minor=1200, disclosed_charge_minor=14400, savings_percent=0)
        self.assertTrue(offer_consistency.validate(data)["valid"])

    def test_duplicate_catalog_and_boolean_money_rejected(self):
        data = offer_fixture()
        data["catalog"].append(deepcopy(data["catalog"][0]))
        with self.assertRaises(ValueError):
            offer_consistency.validate(data)
        data = offer_fixture()
        data["catalog"][0]["charge_minor"] = True
        with self.assertRaises(ValueError):
            offer_consistency.validate(data)


class EventTests(unittest.TestCase):
    def test_delivery_and_business_duplicates_are_separate(self):
        contract, event = event_fixture()
        other_delivery = dict(event, event_id="delivery-2")
        result = event_validator.validate_events([(1, event), (2, event), (3, other_delivery)], contract)
        self.assertEqual(result["duplicate_deliveries"], 1)
        self.assertEqual(result["duplicate_business_keys"], 1)
        self.assertTrue(result["valid"])

    def test_conflicting_delivery_id_is_error(self):
        contract, event = event_fixture()
        result = event_validator.validate_events([(1, event), (2, dict(event, amount_minor_units=1200))], contract)
        self.assertFalse(result["valid"])
        self.assertIn("event_id_collision", {f["code"] for f in result["issues"]})

    def test_paid_business_key_is_independent_of_contract_field_order(self):
        contract, event = event_fixture()
        renewal = deepcopy(contract["events"][0])
        renewal.update(name="subscription_renewed", dedupe_key=["transaction_id", "provider"])
        contract["events"].append(renewal)
        other = dict(event, event="subscription_renewed", event_id="renewal-delivery")
        result = event_validator.validate_events([(1, event), (2, other)], contract)
        self.assertEqual(result["duplicate_business_keys"], 1)

    def test_zero_purchase_and_client_source_are_rejected(self):
        contract, event = event_fixture()
        event.update(amount_minor_units=0, source="client")
        result = event_validator.validate_events([(1, event)], contract)
        codes = {f["code"] for f in result["issues"]}
        self.assertIn("nonpositive_outcome", codes)
        self.assertIn("event_source", codes)

    def test_non_utc_and_boolean_amount_are_rejected(self):
        contract, event = event_fixture()
        event.update(occurred_at="2026-01-01T00:00:00", amount_minor_units=True)
        codes = {f["code"] for f in event_validator.validate_events([(1, event)], contract)["issues"]}
        self.assertTrue({"timestamp", "amount_type"}.issubset(codes))

    def test_sensitive_values_never_echoed(self):
        contract, event = event_fixture()
        event["nested"] = {"password": "do-not-print-this-value"}
        result = event_validator.validate_events([(1, event)], contract)
        self.assertIn("sensitive_field", {f["code"] for f in result["issues"]})
        self.assertNotIn("do-not-print-this-value", json.dumps(result))

    def test_required_fields_and_unknown_events(self):
        contract, event = event_fixture()
        del event["transaction_id"]
        result = event_validator.validate_events([(1, event), (2, {"event": "not-declared"})], contract)
        self.assertTrue({"required_field", "unknown_event", "business_key_type"}.issubset({f["code"] for f in result["issues"]}))

    def test_malformed_provider_cannot_skip_business_deduplication(self):
        contract, event = event_fixture()
        event["provider"] = []
        result = event_validator.validate_events([(1, event), (2, dict(event, event_id="delivery-2"))], contract)
        self.assertFalse(result["valid"])
        codes = {f["code"] for f in result["issues"]}
        self.assertTrue({"text_field_type", "business_key_type"}.issubset(codes))


class HTMLTests(unittest.TestCase):
    def test_labeled_native_form_has_no_findings(self):
        html = '<meta name="viewport" content="width=device-width"><form method="post"><label for="e">Work email</label><input id="e" type="email" autocomplete="email" required><label>Password<input type="password" autocomplete="new-password"></label><button type="submit">Create workspace</button></form>'
        self.assertEqual(journey_lint.lint(html)["finding_count"], 0)

    def test_placeholder_and_auxiliary_submit_found(self):
        result = journey_lint.lint('<form><input placeholder="Work email"><button>Show details</button><a href="#"></a></form>')
        codes = set(result["counts_by_code"])
        self.assertTrue({"placeholder_only", "implicit_submit", "placeholder_destination", "action_name_unresolved"}.issubset(codes))

    def test_aria_reference_and_img_alt_resolved(self):
        html = '<meta name="viewport"><span id="name">Choose plan</span><button type="button" aria-labelledby="name"></button><a href="/pricing"><img alt="View pricing" src="p.png"></a>'
        self.assertEqual(journey_lint.lint(html)["finding_count"], 0)

    def test_hidden_templates_and_script_are_excluded(self):
        html = '<meta name="viewport"><template><input></template><div hidden><button></button></div><script>var x="&lt;input&gt;";</script>'
        result = journey_lint.lint(html)
        self.assertEqual(result["controls_checked"], 0)
        self.assertEqual(result["actions_checked"], 0)

    def test_hidden_content_does_not_name_action_but_explicit_reference_can(self):
        html = '<meta name="viewport"><button type="button"><span hidden>Buy</span></button><span hidden id="label">Continue</span><button type="button" aria-labelledby="label"></button>'
        result = journey_lint.lint(html)
        self.assertEqual(result["counts_by_code"].get("action_name_unresolved"), 1)

    def test_template_labels_and_viewport_do_not_affect_live_controls(self):
        html = '<template><meta name="viewport"><label for="e">Email</label><span id="b">Buy</span></template><input id="e"><button aria-labelledby="b" type="button"></button>'
        codes = set(journey_lint.lint(html)["counts_by_code"])
        self.assertTrue({"viewport_unobserved", "control_name_unresolved", "action_name_unresolved", "missing_label_reference"}.issubset(codes))

    def test_radio_group_not_counted_as_many_required_fields(self):
        html = '<meta name="viewport"><form>' + ''.join(f'<label>Choice {i}<input name="plan" type="radio" required></label>' for i in range(6)) + '</form>'
        self.assertNotIn("required_field_burden", journey_lint.lint(html)["counts_by_code"])


class ResourceTests(unittest.TestCase):
    def test_complete_catalog_counts_and_links(self):
        result = resource_finder.validate()
        self.assertEqual(result["errors"], [])
        self.assertEqual((result["patterns"], result["templates"], result["new_patterns"], result["new_templates"]), (66, 75, 44, 69))

    def test_search_filters_and_unknown_category(self):
        records = resource_finder.combine(*resource_finder.load_resources())
        templates = resource_finder.select(records, "template")
        matches = resource_finder.search(templates, "pricing", 5)
        self.assertTrue(matches)
        self.assertTrue(all(r["kind"] == "template" for r in matches))
        with self.assertRaises(ValueError):
            resource_finder.select(records, "template", "category-that-does-not-exist")

    def test_pattern_export_preserves_all_ids(self):
        rows = resource_finder.select(resource_finder.combine(*resource_finder.load_resources()), "pattern")
        output = resource_finder.export_markdown(rows, "pattern")
        self.assertEqual(sum(line.startswith("## PAT-") for line in output.splitlines()), 66)

    def test_paths_and_nonstandard_json_rejected(self):
        with self.assertRaises(ValueError):
            safe_path(ROOT, "../outside.md")
        for value in ('{"x":NaN}', '{"x":1,"x":2}'):
            with self.assertRaises(ValueError):
                loads(value)


class CLITests(unittest.TestCase):
    def run_tool(self, name, *args):
        return subprocess.run([sys.executable, "-B", str(SCRIPTS / name), *args], capture_output=True, text=True)

    def test_all_four_help_commands(self):
        for name in ("resource_finder.py", "event_validator.py", "offer_consistency.py", "journey_lint.py"):
            with self.subTest(tool=name):
                run = self.run_tool(name, "--help")
                self.assertEqual(run.returncode, 0, run.stderr)

    def test_real_input_clis(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            (folder / "offer.json").write_text(json.dumps(offer_fixture()))
            contract, event = event_fixture()
            (folder / "contract.json").write_text(json.dumps(contract))
            (folder / "events.jsonl").write_text(json.dumps(event) + '\n')
            (folder / "snapshot.html").write_text('<meta name="viewport"><button type="button">Continue</button>')
            cases = [("offer_consistency.py", "--input", str(folder / "offer.json")),
                     ("event_validator.py", "--events", str(folder / "events.jsonl"), "--contract", str(folder / "contract.json")),
                     ("journey_lint.py", "--html", str(folder / "snapshot.html")),
                     ("resource_finder.py", "show", "TMP-001", "PAT-001")]
            for name, *args in cases:
                with self.subTest(tool=name):
                    run = self.run_tool(name, *args)
                    self.assertEqual(run.returncode, 0, run.stderr)
                    self.assertIsNotNone(json.loads(run.stdout))

    def test_findings_and_bad_input_exit_codes(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "offer.json"
            data = offer_fixture()
            data["observations"][0]["headline_minor"] = 11520
            path.write_text(json.dumps(data))
            self.assertEqual(self.run_tool("offer_consistency.py", "--input", str(path)).returncode, 1)
            path.write_text('{"version":NaN}')
            run = self.run_tool("offer_consistency.py", "--input", str(path))
            self.assertEqual(run.returncode, 2)
            self.assertNotIn("Traceback", run.stderr)
        self.assertEqual(self.run_tool("resource_finder.py", "show", "TMP-999").returncode, 2)


if __name__ == "__main__":
    unittest.main()
