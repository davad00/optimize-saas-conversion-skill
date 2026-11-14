# Analytics and commercial scenario tools

Choose a tool for a concrete question after defining the eligible population, counting unit, period, and source of truth. These six commands complement `cro_math.py`; they do not replace the mandatory pricing and purchase checks.

## Contents

- [Shared behavior](#shared-behavior)
- [Funnel drop-off](#funnel-drop-off)
- [Cohort retention](#cohort-retention)
- [Recurring revenue bridge](#recurring-revenue-bridge)
- [Experiment data guardrails](#experiment-data-guardrails)
- [Per-customer unit economics](#per-customer-unit-economics)
- [Offer scenarios](#offer-scenarios)
- [Sources and calculation boundaries](#sources-and-calculation-boundaries)

## Shared behavior

Resolve each script from this skill's directory, regardless of the project's working directory. All six use Python 3's standard library. They read specified local input files or arguments and print JSON; they make no network requests, change no files, send no messages, and change no billing. The internal `_analytics_common.py` helper must remain beside them. They suppress Python bytecode-cache creation when run as commands.

`--help` describes arguments. A successful analysis exits `0`; invalid inputs exit `2` with an explanation on stderr and no partial JSON. Successful output can still contain a data-quality failure or an undefined result: inspect warnings and fields, not only exit status. Rates are fractions (`0.05` means 5%). Decimal monetary values are JSON strings; count and minor-unit snapshot fields are integers. `null` means undefined or withheld, never zero. Currency codes are declared three-letter uppercase labels; the tools do not validate provider support or exchange rates.

CSV files must be UTF-8, have unique named headers, and contain the required columns. Blank optional `retained` cells are accepted only where specified. JSON rejects duplicate keys and non-finite constants. Use pseudonymous unit/account IDs and the minimum necessary data; inputs are processed locally. Never infer absent eligibility, successful payment, cohort maturity, or an intended allocation from downstream conversion behavior.

## Funnel drop-off

**Use:** locate the largest observed stage losses in a nested journey with one eligible cohort.

```bash
python3 <skill-dir>/scripts/funnel_analyzer.py --input funnel.csv \
  --cohort 'New qualified accounts entering in January' \
  --window 'January entry; 30 days of follow-up per account' \
  --unit account --same-cohort
```

```csv
stage,users
landing,1000
signup,250
activated,100
paid,20
```

Rows define journey order. Stage names must be unique; counts must be nonnegative integers and cannot increase. Supply deduplicated units that reached all preceding prerequisite stages. For optional or branching actions, create separate compatible funnels. The required `--same-cohort` flag records acknowledgment; it cannot establish that the export is correct.

**Read:** eligible-to-stage rates, previous-stage completion/drop rates, final-stage rate, and all ties for the largest absolute drop. In the example, the largest loss is 750 between landing and signup; the final-stage rate is 2%. A zero denominator produces `null`. A large loss is an investigation target, not the number of purchases a redesign would recover. Check buyer fit, event validity, reach, and downstream value before prioritizing.

## Cohort retention

**Use:** compare mature retention periods without treating missing observations as lost customers.

```bash
python3 <skill-dir>/scripts/cohort_retention.py --input retention.csv --mode point
```

```csv
cohort,period,eligible,retained,mature
January,1,100,80,true
January,2,100,70,true
February,1,20,10,true
February,2,20,,false
```

Define cohort entry, period duration, retained event, and observation cutoff upstream. `period` is a nonnegative integer, at most 1200. `eligible` is the positive **original** cohort size and must remain constant within a cohort. `retained` cannot exceed it. An immature period must leave `retained` empty. Duplicate cohort/period cells, changing denominators, and a mature period following an immature period are rejected.

Choose `point` when the user is active in the specified period; return activity may make it increase. Choose `survival` only when retained means continuously retained through that period; increases are rejected. This is not a censored survival estimator and does not implement Kaplan–Meier.

**Read:** each cohort's observations, missing periods between its first and last supplied rows, and denominator-weighted rates by period. Only mature cohorts contribute. In the example, period 1 is `90/120 = 75%`; period 2 is `70/100 = 70%`, with February excluded. Changes across periods can reflect a changing set of mature cohorts, so inspect cohort rows before claiming deterioration or improvement.

## Recurring revenue bridge

**Use:** explain net movement between two comparable monthly recurring revenue snapshots.

```bash
python3 <skill-dir>/scripts/revenue_bridge.py --input mrr.csv
```

```csv
account_id,currency,start_mrr_minor,end_mrr_minor
account-a,USD,10000,15000
account-b,USD,20000,12000
account-c,USD,5000,0
account-d,USD,0,7000
account-e,EUR,10000,10000
```

Provide one row per account/currency and nonnegative integer monthly-normalized values in that currency's documented minor unit. Normalize billing intervals and apply a consistent discount, tax, delinquency, and rounding policy before export. A recurring annual amount must not be entered as a monthly value. Zero-to-positive values include reactivation; segment history upstream when new and returning accounts must be separated.

**Read:** new, expansion, contraction, churn, net change, and exact reconciliation for each currency. Currencies remain separate. The tool calculates:

- `GRR = (starting MRR − contraction − churn) / starting MRR`.
- `NRR = (starting MRR − contraction − churn + expansion) / starting MRR`.
- `logo retention = (starting positive-MRR accounts − churned accounts) / starting positive-MRR accounts`.

New accounts are excluded from GRR and NRR numerators. Zero starting denominators produce `null`. These snapshots show net movement; they cannot reveal all expansions and cancellations between snapshots. MRR is neither collected cash nor accounting revenue.

## Experiment data guardrails

**Use:** check whether assignment, exposure, and outcome logs can be joined coherently before analyzing treatment effects.

```bash
python3 <skill-dir>/scripts/experiment_guardrails.py --input experiment.csv \
  --allocation '{"control":0.5,"variant":0.5}' --srm-threshold 0.001
```

```csv
unit_id,variant,event,occurred_at
unit-a,control,assigned,2026-01-01T10:00:00Z
unit-a,control,exposed,2026-01-01T10:01:00Z
unit-a,control,converted,2026-01-02T09:00:00Z
unit-b,variant,assigned,2026-01-01T11:00:00Z
```

Supply one experiment and a fixed intended allocation, with 2–100 variants whose positive shares sum exactly to 1. Do not combine ramp periods or derive allocation from observed sales. Events are `assigned`, `exposed`, or `converted`; timestamps need explicit timezones. Map conversions to the predefined verified outcome upstream.

**Read:** exact duplicates ignored; repeated assignment records; units with conflicting variants; missing assignments; events before assignment; and conversions with absent or later exposure. Conflicting units are excluded from descriptive variant counts and make assignment integrity fail. Event counts never substitute for unique assigned units.

The sample-ratio-mismatch check compares unique assigned-unit counts with intended shares using Pearson's chi-square statistic and `variants − 1` degrees of freedom. Its p-value is withheld when assignment/identity/timing defects exist or any expected count is below 5. The default `0.001` threshold is a diagnostic configuration, not a universal shipping rule. Exposure diagnostics need the experiment's predefined intent-to-treat and exposure semantics. A passed check does not establish causal validity, full logging, outcome maturity, or customer benefit. Use `cro_math.py compare-ab` only after the relevant design checks pass and its assumptions fit.

## Per-customer unit economics

**Use:** examine whether a paid acquisition or offer assumption can recover its customer-acquisition cost through contribution.

```bash
python3 <skill-dir>/scripts/unit_economics.py --cac 100 \
  --monthly-revenue 20 --monthly-variable-cost 5 --monthly-churn 0.1 \
  --horizon-months 12 --currency USD
```

Amounts are currency units per customer; rates are fractions. CAC and monthly revenue/cost must be nonnegative. Churn can range from 0 to 1; the horizon is 1–1200 months. All inputs are explicit assumptions. Contribution is revenue less variable service cost. The model starts with one active customer in month 1, then applies constant logo churn at each month end:

`expected contribution in month t = (monthly revenue − monthly cost) × (1 − churn)^(t−1)`.

**Read:** contribution margin, payback ignoring churn, the first modeled month cumulative contribution covers CAC, the finite monthly schedule, and finite-horizon contribution after CAC. In the example, monthly contribution is $15; 12-month expected contribution is $107.63556952785, and CAC recovery occurs in month 11 under the stated assumptions.

For positive churn, the infinite geometric-series expression is `monthly contribution / churn`; it is explicitly labeled a constant-churn lifetime contribution scenario. At zero churn it is `null`, while finite-horizon totals remain available. Negative contribution is retained and cannot recover positive CAC. No expansion, discounting, tax, refunds, fixed overhead, or payment timing is included. Rerun observed low/base/high assumptions; do not present this arithmetic as measured LTV or a forecast.

## Offer scenarios

**Use:** compare how explicit paid-conversion and plan-mix assumptions affect purchases, first-charge cash, and normalized contribution.

```bash
python3 <skill-dir>/scripts/offer_scenarios.py --input offers.json
```

```json
{
  "currency": "USD",
  "eligible_units": 1000,
  "scenarios": [
    {
      "name": "Annual offer",
      "paid_conversion_rate": "0.02",
      "plans": [
        {
          "name": "Annual",
          "share": "1",
          "price": "120",
          "interval_months": 12,
          "full_refund_rate": "0.1",
          "monthly_service_cost": "2",
          "payment_fee_rate": "0.03",
          "payment_fee_fixed": "0.3"
        }
      ]
    }
  ]
}
```

Each scenario needs a unique name, a paid-conversion fraction, and 1–100 uniquely named plans. All displayed plan fields are required. Shares must sum exactly to 1. Positive-share paid plans need positive prices. `interval_months` is 1–120. Add a second scenario with alternative assumptions to compare the result; changing the input does not alter the product's actual offer.

**Read:** expected paid and non-refunded buyers; first-charge gross cash; full refunds; payment fees; cash after refunds and fees; normalized new MRR; first-term service costs; and contribution. The example yields 20 expected buyers, $2,400 first-charge cash, $200 normalized MRR before refunds, $180 after full refunds, $78 fees, and $2,082 cash after refunds and fees.

Explicit modeling assumptions: full refunds remove the entire first charge and recurring value; payment fees are nonrefundable; every buyer incurs the full first-term service cost, including refunded buyers. Monthly-normalized fees amortize that first charge's fees over its interval. First-term contribution spans different durations when billing intervals differ, so compare normalized values alongside cash and commitments. There are no renewal, later-churn, partial-refund, acquisition-cost, tax, overhead, or payment-failure estimates. Fractional expected buyers are scenario arithmetic. Separate annual cash from recurring value and never interpret a larger upfront receipt as proven incremental profit.

## Sources and calculation boundaries

The tools implement the explicit arithmetic described above, with no external services or dependencies at runtime. The following primary references inform definitions and limits, checked 2026-11-14:

- [NIST chi-square goodness-of-fit reference](https://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/chsqgood.htm): statistic, approximate chi-square distribution, and expected-frequency condition. Here variant probabilities are specified in advance, so degrees of freedom are `k−1`; no fitted probability parameters are subtracted.
- [Fabijan et al., 2019, Microsoft Research](https://www.microsoft.com/en-us/research/publication/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments-a-taxonomy-and-rules-of-thumb-for-practitioners/): SRM is a symptom of experimental data-quality problems that needs diagnosis, not a business effect estimate.
- [Stripe's MRR/ARR definitions](https://support.stripe.com/questions/understanding-monthly-recurring-revenue-%28mrr%29-and-annual-recurring-revenue-%28arr%29): monthly normalization and the distinction between recurring metrics, invoices, and accounting revenue. Provider-specific inclusion policies are not automatically reproduced by these scripts.

Use project and provider records to determine actual values. A mathematically valid result cannot repair a biased cohort, incomplete outcome data, an incorrect offer, or a broken payment journey.
