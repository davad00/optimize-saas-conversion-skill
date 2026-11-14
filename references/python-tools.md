# Python tools for sales and conversion work

## Contents

- [Choose a tool](#choose-a-tool)
- [Read-only contract and interpretation](#read-only-contract-and-interpretation)
- [Patterns and templates](#patterns-and-templates)
- [Offer consistency](#offer-consistency)
- [Event validation](#event-validation)
- [HTML journey review](#html-journey-review)
- [Analytics inputs and calculations](#analytics-inputs-and-calculations)
- [Validation and sources](#validation-and-sources)

## Choose a tool

Resolve scripts relative to the installed skill directory. Use Python 3.10 or later and the standard library; no package installation is required. Select a tool only when the available inputs answer a relevant task question.

| Tool | Use it for | Input | Interpret with |
| --- | --- | --- | --- |
| [cro_math.py](../scripts/cro_math.py) | Existing binary experiment planning/comparison, monthly/annual arithmetic, color contrast | CLI arguments | Its independent-unit and fixed-test assumptions; contrast is one accessibility check |
| [tactics.py](../scripts/tactics.py) | Existing 360-tactic category scan, search, lookup, export | Bundled JSONL catalogs | Match observed triggers; keyword overlap is not semantic recommendation |
| [resource_finder.py](../scripts/resource_finder.py) | Find 66 persuasion patterns and 75 fillable templates | Bundled catalogs; query or ID | Read the complete selected record, then use verified project facts |
| [offer_consistency.py](../scripts/offer_consistency.py) | Compare displayed prices and checkout selections with catalog truth | Catalog plus observed values in JSON | Fixed flat/per-unit monthly/yearly offers; provider quotes for actual due now |
| [event_validator.py](../scripts/event_validator.py) | Catch malformed events, duplicate deliveries/outcomes and wrong source declarations | Event JSONL plus adaptable contract | Structure does not prove payment, consent, identity or complete tracking |
| [journey_lint.py](../scripts/journey_lint.py) | Find static form, label and action obstacles | Local rendered HTML snapshot | Review cues; verify CSS, keyboard behavior and journey in a browser |
| [funnel_analyzer.py](../scripts/funnel_analyzer.py) | Locate absolute and proportional stage drop-offs | Nested same-cohort stage CSV | Cohort, denominator, window and unit must be defined upstream |
| [cohort_retention.py](../scripts/cohort_retention.py) | Summarize mature cohort retention | Cohort/period CSV | Point retention differs from continuous survival; missing is not zero |
| [revenue_bridge.py](../scripts/revenue_bridge.py) | Reconcile new, expansion, contraction and churned MRR; GRR/NRR | Account-level starting/ending MRR CSV | Normalize intervals first; keep currencies separate |
| [experiment_guardrails.py](../scripts/experiment_guardrails.py) | Detect reassignment, missing joins, event timing and sample-ratio problems | Assignment/exposure/outcome CSV and allocation | A passed diagnostic does not establish randomization or select a winner |
| [unit_economics.py](../scripts/unit_economics.py) | Explore contribution, CAC payback and finite-horizon churn assumptions | Explicit money, cost, churn and horizon arguments | Scenario arithmetic; not measured LTV, recognized revenue or a forecast |
| [offer_scenarios.py](../scripts/offer_scenarios.py) | Compare assumed conversion, plan mix, first-charge cash, refunds and cost | Scenario JSON | Annual cash and normalized recurring value are separate; assumptions remain visible |

There are **12 user-facing tools**: the original two and ten additions. Shared `_*.py` modules and `test_*.py` files support them and do not count as extra tools.

## Read-only contract and interpretation

All tools read local files or CLI arguments and write results to stdout. They make no network requests, write no report files, change no site or billing configuration, install nothing, send no messages and select no shipping decision. The added CLIs suppress local bytecode-cache writes. A shell redirection such as `> report.json` is an explicit caller-chosen file write, outside the tool itself.

Keep customer inputs local. Use pseudonymous identifiers where IDs are needed. None of these tools needs raw card data, passwords or sensitive free text. A supplied provider quote is still supplied evidence; the tool does not authenticate it.

`--help` documents invocation. Calculation tools emit JSON; retrieval also supports exact template text and Markdown export. Monetary JSON types differ intentionally: analytics tools serialize exact Decimal values as strings, MRR/offer checks use integer minor units, and existing `cro_math.py` documents its own output. Never silently combine currencies or assume that every currency has two decimal places.

Successful analysis exits `0`. Invalid input exits `2` with an error on stderr. `resource_finder.py validate`, `offer_consistency.py` and `event_validator.py` exit `1` when their output contains failing checks. HTML review cues and analytics diagnostics remain successful analyses even when they reveal a problem; inspect the returned findings and warnings.

## Patterns and templates

```bash
python3 <skill-dir>/scripts/resource_finder.py categories
python3 <skill-dir>/scripts/resource_finder.py list --kind pattern
python3 <skill-dir>/scripts/resource_finder.py search 'buyer uncertainty' --kind pattern --limit 5
python3 <skill-dir>/scripts/resource_finder.py search 'pricing' --kind template --limit 5
python3 <skill-dir>/scripts/resource_finder.py show PAT-023 TMP-007
python3 <skill-dir>/scripts/resource_finder.py render TMP-005
python3 <skill-dir>/scripts/resource_finder.py validate
```

`list` accepts `--category` using a value returned by `categories`. `show` prints complete records. `render` prints the exact bundled template to stdout; it does not fill placeholders, execute content or send drafts. Search uses literal word overlap and boosts title matches; category lists are the fallback when terminology differs.

The [pattern catalog](persuasion-catalog.jsonl) and [template manifest](template-catalog.json) are the source of truth. Validation checks exact counts, IDs, fields, referenced tactics, local template paths, original-template retention and the 69 new files. It cannot establish semantic uniqueness or conversion effectiveness. Human review still matters.

To regenerate the public repository's readable indexes, intentionally redirect exports from that repository's working directory:

```bash
python3 scripts/resource_finder.py export --kind pattern > PERSUASION.md
python3 scripts/resource_finder.py export --kind template > TEMPLATES.md
```

## Offer consistency

Use this after inspecting catalog truth and actual pricing/checkout states. The checker does not extract values from screenshots, source code or a live provider. Its inputs must be observed or verified, not inferred from expected behavior.

```bash
python3 <skill-dir>/scripts/offer_consistency.py --input offer-observations.json
```

Illustrative complete input (USD minor units; actual product facts must replace it):

```json
{
  "version": 1,
  "catalog": [
    {"plan_id": "basic", "interval": "month", "currency": "USD", "charge_minor": 1200, "unit": "flat", "provider_price_id": "price_month"},
    {"plan_id": "basic", "interval": "year", "currency": "USD", "charge_minor": 11520, "unit": "flat", "provider_price_id": "price_year"}
  ],
  "observations": [
    {
      "name": "Annual pricing card", "surface": "pricing",
      "plan_id": "basic", "interval": "year", "currency": "USD", "quantity": 1,
      "headline_minor": 960, "headline_basis": "month", "headline_scope": "total",
      "disclosed_charge_minor": 11520, "disclosed_charge_scope": "total",
      "disclosed_interval": "year", "savings_percent": 20
    },
    {
      "name": "Annual checkout", "surface": "checkout",
      "plan_id": "basic", "interval": "year", "currency": "USD", "quantity": 1,
      "displayed_due_now_minor": 11520, "quoted_due_now_minor": 11520,
      "disclosed_interval": "year", "submitted_price_id": "price_year", "submitted_quantity": 1
    }
  ],
  "default": {
    "selected_interval": "year",
    "reason": "Suitable discounted ongoing offer for a new undecided visitor; explicit choices persist"
  }
}
```

### Contract and limits

- Catalog identity is `(plan_id, interval, currency)`; duplicates are rejected. Supported intervals are `month` and `year`. `charge_minor` is the verified base charge per billing interval, using the currency's documented minor unit.
- Set `unit` to `flat` or `per_unit`; `min_quantity` defaults to one. Flat offers require quantity one. For per-unit offers, supply the real minimum and selected quantity. The recurring total is unit charge × quantity.
- `headline_scope` is `per_unit` or `total`. A yearly offer is compared at `charge / 12`, rounded half-up to one minor unit. This checks one declared rounding policy; visibly label rounded equivalents where useful.
- `disclosed_charge_scope` defaults to `total`. A per-unit disclosure with multiple units produces a review cue to show the whole bill as well. `disclosed_interval` must match the selection.
- A yearly headline expressed per year produces a review cue to use a comparable monthly headline or document the justified exception. A passing math check does not establish readable adjacent terms.
- Optional `savings_percent` is checked against 12 comparable monthly payments at the selected quantity; permitted rounding error is 0.05 percentage points. For whole-percent marketing rounding, inspect the exact result and explain the rounding rather than silently accepting it.
- For checkout, `displayed_due_now_minor` is compared with `quoted_due_now_minor`, supplied from the actual provider quote including applicable tax, discounts, credits or proration. A missing quote is unverified. Never derive an upgrade charge solely from the recurring catalog.
- Optional `submitted_price_id` is compared with the catalog's `provider_price_id`; `submitted_quantity` must match selection. A checkout without a submitted price ID remains unverified; a per-unit checkout also needs its submitted quantity.
- The default is a recorded decision, not a generated recommendation. Apply the skill's buyer-context rules and verify selection persistence independently.

The output separates errors from review items and is only clear when both are empty. It does not handle tiered/usage prices, tax calculation, real currency conversion, browser behavior, payments or fulfillment. Use the actual provider/test journey for those.

## Event validation

```bash
python3 <skill-dir>/scripts/event_validator.py \
  --events events.jsonl --contract project-event-contract.json
```

Start from [the existing event contract](../assets/event-contract.json), fill its project decisions, map names to the actual event system and set `allowed_sources` when source checking is needed. Without `--contract`, the bundled adaptable contract is used and unresolved decisions are reported. It is not a deployable analytics schema.

Each nonblank JSONL line is a flat event object whose `event` value matches a contract event's `name`. Example:

```json
{"event":"purchase_completed","event_id":"evt-example","unit_id":"u-example","account_id":"a-example","transaction_id":"tx-example","provider":"example","plan_id":"basic","billing_interval":"year","currency":"USD","amount_minor_units":11520,"occurred_at":"2026-01-01T00:00:00Z","source":"billing_server"}
```

A minimal customized contract entry could be:

```json
{
  "events": [{
    "name": "purchase_completed",
    "required": ["unit_id", "transaction_id", "provider", "amount_minor_units", "currency", "occurred_at"],
    "dedupe_key": ["provider", "transaction_id"],
    "allowed_sources": ["billing_server"]
  }]
}
```

The validator checks required nonempty fields; string identifiers and core text fields; integer minor-unit amounts; UTC timestamp syntax; positive paid/refund outcomes; declared allowed sources; duplicate logical event IDs; repeated declared business keys; and a small set of sensitive field names. Declared business-key components must be nonempty text or integers, so malformed values cannot silently skip deduplication. It rejects duplicate JSON keys and nonstandard NaN/Infinity literals.

Repeated `event_id` with identical payload apart from `received_at` is reported as a duplicate delivery. Conflicting payloads sharing that ID are errors. Different event IDs sharing the declared business key are a separate warning. Purchase and renewal transaction keys share a namespace so the same charge is not casually counted twice. Repeated exposures can be legitimate events; apply the defined per-unit counting rule to the relevant metric.

`structurally_valid_nonduplicate_deliveries` is an event-structure count, **not** paid customers. Missing tracking, verified payment truth, consent, currency-code validity, identity merges, cohort windows and revenue reconciliation need separate evidence. The sensitive-field checker is not a complete privacy scanner.

## HTML journey review

```bash
python3 <skill-dir>/scripts/journey_lint.py --html pricing-rendered.html
python3 <skill-dir>/scripts/journey_lint.py --html signup-rendered.html --required-field-review 5
```

Save or supply a complete rendered HTML snapshot through the project's authorized inspection workflow. This tool reads the file only. Do not pass a URL, JSX component or a screenshot as if it were rendered HTML.

Findings include unresolved control/action names, placeholder-only labels, missing label references, duplicate IDs, implicit form-submit buttons, placeholder link destinations, absent email/password autocomplete hints, native password forms using GET, high required-field burden and an unobserved viewport declaration. Required radio choices sharing a name count as one field group. The field threshold is a configurable review cue, not a universal optimal form length.

The checker recognizes common native labels, ARIA labels/references, button text and image alt text. It excludes explicitly hidden/inert/template content but does not compute CSS visibility or the complete accessible-name algorithm. Every finding is labeled for review; there is no numeric conversion score or claim of WCAG conformance. Confirm rendered behavior, keyboard operation, labels, mobile layout and the complete purchase journey.

## Analytics inputs and calculations

Read [analytics-tools.md](analytics-tools.md) for the six analytical tools' exact CSV/JSON schemas, runnable examples, formulas, boundaries and primary technical references. Select the smallest useful analysis:

- Use funnel counts for a defined nested cohort; do not divide unrelated dashboard totals.
- Use mature retention rows and explicit point/survival semantics.
- Reconcile monthly recurring-value snapshots by currency before using GRR or NRR.
- Investigate assignment and tracking defects before reading experiment effects.
- Use observed cost/rate ranges to explore sensitivity; keep assumptions distinct from forecasts.
- Compare purchase count, contribution and retained value alongside annual mix and first-charge cash.

## Validation and sources

Run tests from the skill root:

```bash
python3 -B -m unittest discover -s scripts -p 'test_*.py' -v
python3 -B scripts/tactics.py validate
python3 -B scripts/resource_finder.py validate
```

Primary technical references for these implementation choices:

- [Python Decimal](https://docs.python.org/3/library/decimal.html): exact decimal calculations and explicit rounding; this toolkit's half-up policy is stated rather than assumed universal.
- [Python JSON](https://docs.python.org/3/library/json.html): local JSON decoding/encoding and strict handling of invalid numeric constants.
- [W3C labeling controls](https://www.w3.org/WAI/tutorials/forms/labels/): persistent labels and native form associations.
- [W3C accessible names and descriptions](https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/): input/action naming; the static tool only approximates a subset.
- [W3C Labels or Instructions](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions): an accessible name alone does not establish that a visible label is sufficient.

These sources support technical checks, not sales uplift claims. Use actual outcomes to assess whether implemented changes helped.
