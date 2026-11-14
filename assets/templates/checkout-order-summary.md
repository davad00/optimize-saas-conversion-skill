# Checkout order summary

Template: `TMP-040` · Category: `purchase`

## Use when

Make the actual purchase commitment clear immediately before payment.

## Required inputs

- Authoritative checkout amounts
- Plan, quantity, interval, and currency
- Renewal and cancellation terms
- Tax, discounts, and receiving workspace

## Summary block

**Buying for:** [Account/workspace].
**Package:** [Plan, quantity, included allowance, and relevant limits].
**Billing:** [Actual interval and commitment].

| Item | Amount |
| --- | --- |
| [Subscription or service] | [Provider subtotal] |
| [Applied discount and duration] | [Actual reduction] |
| [Tax/fees and status] | [Calculated amount or clearly unresolved] |
| **Due now** | **[Actual payable total and currency]** |

**Next charge:** [Date/rule, amount/rule, and interval].
**Commitment and cancellation:** [Relevant exact consequence].
**Final action:** [Accurate payment or subscription action].
**Edit:** [Quantity/plan route preserving valid checkout context].

A monthly equivalent can assist comparison but must not replace the amount charged today. Recalculate the summary whenever quantity, tax details, discount, or plan changes. Do not trust client-entered prices as the billing source of truth.

## Completion check

Verify the displayed and submitted totals agree with provider state for new purchases, account changes, discounts, taxes, and each supported currency.

Related tactics: `PAY-001`, `PAY-003`, `PAY-005`, `PAY-012`, `PAY-014`.
