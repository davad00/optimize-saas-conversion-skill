# Journey evidence map

Template: `TMP-012` · Category: `research`

## Use when

Connect buyer expectations and observed behavior across the entire purchase path.

## Required inputs

- Routes and account states
- Available analytics or session evidence
- Verified offer facts
- Primary conversion outcome and window

## Journey map

| Step | Buyer expectation | Actual surface/state | Evidence | Friction or mismatch | Next valid state |
| --- | --- | --- | --- | --- | --- |
| Entry | [Promised outcome] | [Campaign/page] | [Source/date] | [Observed gap] | [Relevant offer] |
| Evaluation | [Proof and cost] | [Demo/pricing] | [Source] | [Gap] | [Chosen plan] |
| Commitment | [Actual charge] | [Signup/checkout] | [Source] | [Gap] | [Verified purchase] |
| First value | [Usable result] | [Product workflow] | [Source] | [Gap] | [Meaningful success] |

## Priority handoff

**Broken transition:** [Exact source and destination].
**User context to preserve:** [Plan, interval, input, workspace, or task].
**Responsible system:** [UI/auth/payment/product].
**Repair:** [Concrete behavior].
**Verification:** [Actual journey exercised and unavailable portions].

Inspect successful, interrupted, and returning-user paths. Keep screenshot evidence separate from tested behavior. Do not infer private data, hidden failures, or conversion counts from visual inspection alone.

## Completion check

Every claimed defect needs an observable source; distinguish a journey map from a validated funnel with comparable denominators.

Related tactics: `INT-001`, `CTA-006`, `PAY-018`, `ACT-013`.
