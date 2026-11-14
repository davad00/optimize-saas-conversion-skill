# Metric definition card

Template: `TMP-069` · Category: `measurement`

## Use when

Define a business measure that different systems and reviewers can reproduce.

## Required inputs

- Business decision and outcome
- Eligible population and counting unit
- Available authoritative data
- Observation window and exclusions

## Metric contract

**Name:** [Plain measure name].
**Decision supported:** [What a change would justify].
**Numerator:** [Exact event or state, source, and deduplication rule].
**Denominator:** [Eligible units, entry rule, and exclusion policy].
**Counting unit:** [Person, account, opportunity, or transaction].
**Window:** [Enrollment period and outcome follow-up].
**Maturity:** [When a unit has complete opportunity to produce the outcome].
**Segmentation:** [Predefined dimensions and stable definitions].

| Edge case | Counting treatment | Reason/source |
| --- | --- | --- |
| [Retry/duplicate] | [Rule] | [Data semantics] |
| [Refund/zero invoice] | [Rule] | [Outcome definition] |
| [Identity merge] | [Rule] | [Approved policy] |

**Guardrail:** [Relevant downside with its own definition].
**Owner/version:** [Responsible role and change date].

Keep purchases, subscriptions, cash collected, recognized revenue, and retained value distinct. Do not divide unrelated event totals or switch the denominator after observing results.

## Completion check

Reproduce the measure on a small known cohort and reconcile edge cases; list missing data and maturity limitations before interpreting movement.

Related tactics: `PRF-015`, `PRF-019`.
