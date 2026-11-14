# Payment state and recovery copy

Template: `TMP-041` · Category: `purchase`

## Use when

Guide buyers through failed, pending, authenticated, and interrupted payment attempts.

## Required inputs

- Provider state semantics
- Supported retry and payment methods
- Server fulfillment behavior
- Safe support identifiers

## State copy table

| Verified state | Buyer-facing message | Safe next action | Access consequence |
| --- | --- | --- | --- |
| Declined | [Useful supported reason] | [Correct method/details or contact bank] | [No false paid access] |
| Authentication required | [Bank confirmation needed] | [Resume supported challenge] | [Pending] |
| Processing | [Payment status still resolving] | [Wait/check status] | [Actual policy] |
| Buyer canceled | [No completed purchase confirmed] | [Return to offer] | [Existing access preserved] |
| Confirmed paid | [Receipt and package] | [Continue to product] | [Verified entitlement] |

**Repeated click protection:** [Idempotent server behavior].
**Lost return:** [Server/provider reconciliation route].
**Support reference:** [Nonsecret transaction context; never raw payment details].

Do not label a delayed payment as failed merely because the browser timed out. A redirect alone is not proof of settlement. Preserve the chosen package and valid nonpayment inputs where safe.

## Completion check

Test provider-supported states and retry behavior, including a lost redirect; confirm no duplicate charge and no unpaid access grant.

Related tactics: `PAY-008`, `PAY-009`, `PAY-010`, `PAY-011`, `PAY-019`, `PAY-020`.
