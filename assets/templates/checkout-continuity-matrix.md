# Checkout continuity matrix

Template: `TMP-042` · Category: `purchase`

## Use when

Preserve a buyer’s deliberate plan, interval, quantity, and task across interruptions.

## Required inputs

- Offer-selection state model
- Authentication and payment routes
- Persistence requirements
- Deep-link and account-state rules

## Transition matrix

| Transition | State before | State after | Source of truth | Verification result |
| --- | --- | --- | --- | --- |
| Pricing to signup | [Plan/interval/quantity] | [Same valid selection] | [Catalog + explicit selection] | [Observed] |
| Email verification return | [Offer and task] | [Restored context] | [Secure persisted state] | [Observed] |
| Supporting details and back | [Selection] | [Selection retained] | [Expected navigation] | [Observed] |
| Interrupted checkout | [Valid order] | [Revalidated order] | [Server/provider] | [Observed] |

**Precedence rules:** [Explicit choice, valid intended link, account context, experiment assignment, then default].
**Invalid or stale selection:** [Explain change and require an appropriate current choice].
**Sensitive data:** [Never persist raw payment details in URLs or ordinary local storage].
**Reset action:** [Buyer-controlled way to change the selection].

Preserving context does not mean preserving obsolete prices without revalidation. Treat account upgrades separately from new subscriptions.

## Completion check

Exercise back, reload, sign-in, verification, and interruption paths; verify restored state remains valid and never silently creates a different commitment.

Related tactics: `CTA-006`, `CTA-018`, `PAY-002`, `PAY-016`.
