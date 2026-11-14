# Cohort retention and refund review

Template: `TMP-072` · Category: `measurement`

## Use when

Assess durable paid value while accounting for follow-up maturity and billing differences.

## Required inputs

- Customer entry cohort and plan interval
- Defined retained-use or paid status
- Refund and cancellation records
- Complete follow-up availability

## Cohort table

| Entry cohort | Starting eligible units | Mature for milestone? | Retained at defined milestone | Refund requests | Refunds issued | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| [Dates/segment] | [Count] | [Count or rule] | [Count/rate] | [Count/rate] | [Count/amount] | [Limits] |

**Retention definition:** [Meaningful use, active entitlement, or paid renewal; choose explicitly].
**Milestones:** [Comparable time since entry].
**Refund denominator:** [Eligible purchases with sufficient follow-up].
**Billing distinction:** [Monthly versus annual commitment and renewal opportunity].
**Confounders:** [Channel, customer mix, product changes, and offer differences].

Do not treat an annual account as retained solely because it has not reached renewal. Distinguish requests, approved refunds, issued refunds, cancellations, and chargebacks. A small immature cohort cannot support a precise interval-default verdict.

**Decision:** [Investigate, maintain, or adjust based on evidence and practical downside].

## Completion check

Compare mature like-for-like cohorts, report starting counts and missing follow-up, and keep operational payment events separate from customer intention.

Related tactics: `PRF-019`, `RET-017`, `RET-001`.
