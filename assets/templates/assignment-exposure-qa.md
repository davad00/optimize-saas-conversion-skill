# Experiment assignment and exposure QA

Template: `TMP-073` · Category: `measurement`

## Use when

Check whether a planned comparison can support the intended experiment analysis.

## Required inputs

- Experiment allocation and randomization unit
- Assignment and exposure logs
- Eligibility and identity policy
- Variant implementation and exclusion rules

## Validity checks

| Check | Expected behavior | Observed evidence | Status | Action |
| --- | --- | --- | --- | --- |
| Eligibility | [Defined before treatment] | [Record] | [Pass/investigate] | [Fix] |
| Assignment stability | [One variant per unit] | [Record] | [Status] | [Action] |
| Allocation | [Intended proportions] | [Counts and diagnostic] | [Status] | [Action] |
| Exposure opportunity | [Comparable chance to see treatment] | [Record] | [Status] | [Action] |
| Crossovers/interference | [Known boundaries] | [Record] | [Status] | [Action] |

**Cohort maturation:** [Enrollment cutoff and complete outcome window].
**Exclusions:** [Predeclared rule; never remove inconvenient outcomes post hoc].
**Multiple tests:** [Concurrent experiment and comparison handling].
**Stopping method:** [Fixed horizon or specified sequential approach].

An allocation diagnostic can identify a problem but does not explain its cause. Avoid conditioning exposure on a downstream action the treatment can change.

## Completion check

Resolve material validity issues before interpreting uplift, preserve raw evidence, and label results inconclusive when assignment or exposure cannot be trusted.

Related tactics: `DEC-007`, `CTA-006`.
