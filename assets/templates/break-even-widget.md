# Editable break-even widget specification

Template: `TMP-033` · Category: `pricing`

## Use when

Help a buyer estimate the workload needed to justify a subscription under their own assumptions.

## Required inputs

- Comparison horizon and verified fixed subscription cost over it
- Buyer-provided task time and value
- Supported product mechanism
- One-time implementation/setup cost and fixed ongoing effort
- Incremental per-task cost, including usage charges and fees

## Inputs and formula

| Input | Default source | Editable? | Unit and range |
| --- | --- | --- | --- |
| Current effort per task | [Buyer input or labeled example] | Yes | [Minutes] |
| Remaining effort with product | [Measured or assumed] | Yes | [Minutes] |
| Value of time | [Buyer assumption] | Yes | [Currency/hour] |
| Comparison horizon | [Buyer decision period] | Yes | [Months or another explicit period] |
| Fixed subscription cost over horizon | [Verified offer and term] | [Appropriate control] | [Currency] |
| Setup and fixed ongoing effort | [Actual cost or labeled time valuation] | Yes | [Currency over horizon] |
| Incremental cost per task | [Usage/transaction charges minus avoided per-task cash costs] | Yes | [Currency/task] |

**Time-value benefit per task:** [Time difference ÷ 60 × chosen hourly value].
**Net benefit per task:** [Time-value benefit minus incremental per-task cost].
**Fixed horizon cost:** [Subscription over horizon + one-time setup + fixed ongoing effort over horizon].
**Simple break-even workload:** [Round up fixed horizon cost ÷ positive net benefit per task to a feasible whole workload].
**Nonpositive or missing net benefit:** [Explain that this model yields no calculated break-even].

The simple formula assumes constant incremental per-task cost. For tiered pricing or changing rates, calculate the smallest feasible workload where modeled total benefit covers modeled total cost using the actual schedule; do not apply the constant-cost formula across tiers.

## Output copy

“Under your assumptions, approximately [quantity] tasks would offset [defined cost]. This is an estimate, not a guaranteed saving. [Excluded costs or constraints].”

Show a range when inputs vary. Keep cash savings distinct from time capacity and avoid treating saved hours as automatically realizable revenue.

## Completion check

Validate the horizon, units, fixed and incremental costs, zeros, negative net benefit, tier boundaries and rounding. Check double counting and editable assumptions; do not publish ROI claims that the actual product cannot support.

Related tactics: `PRI-006`, `CPY-010`.
