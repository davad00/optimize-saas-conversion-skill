# Comparable-cohort funnel diagnosis

Template: `TMP-071` · Category: `measurement`

## Use when

Locate major journey losses using counts that share an eligible population and time window.

## Required inputs

- Defined entry cohort and counting unit
- Ordered stage definitions
- Event or aggregate counts
- Outcome window and segment context

## Funnel table

| Stage | Exact completion rule | Eligible count | Completed count | Conditional rate | Loss count | Evidence quality |
| --- | --- | --- | --- | --- | --- | --- |
| [Stage] | [Verified event/state] | [Same cohort at risk] | [Unique units] | [Calculation] | [Difference] | [Known gaps] |

**Cohort:** [Entry dates, eligibility, source, unit, follow-up].
**Sequence rule:** [Whether ordered completion is required and how re-entry is treated].
**Important segments:** [Device/channel/buyer type, fixed before interpretation].
**Large observed obstacle:** [Stage plus actual behavioral evidence].
**Proposed repair:** [Specific defect or hypothesis linked to evidence].

Do not assume the largest percentage drop is the best opportunity; consider reach, desired qualification, downstream value, and technical reliability. Counts from unrelated calendar periods or different units cannot form a valid conditional funnel.

**Next evidence:** [Trace, comprehension session, or targeted observation].

## Completion check

Verify nesting or explicitly describe a nonnested journey; reconcile counts, zero denominators, cohort maturity, and the distinction between correlation and cause.

Related tactics: `SIG-001`, `PAY-008`, `ACT-002`.
