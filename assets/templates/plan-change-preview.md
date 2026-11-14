# Existing-account plan-change preview

Template: `TMP-043` · Category: `purchase`

## Use when

Explain the actual financial and entitlement effect of an upgrade or downgrade.

## Required inputs

- Current actual entitlement and subscription
- Provider proration or scheduled-change rules
- Target plan and quantity
- Credits, taxes, and renewal schedule

## Change summary

**Current:** [Actual package, including legacy/add-on/complimentary entitlements].
**Proposed:** [Target package and quantities].
**Effective time:** [Immediate or scheduled, using actual provider rules].

| Consequence | Before | After | Source |
| --- | --- | --- | --- |
| Capabilities and allowance | [Actual] | [Target] | [Entitlement system] |
| Due now or credit | [Current balance context] | [Provider preview] | [Billing preview] |
| Renewal amount/date | [Current] | [Updated] | [Provider] |
| Existing work/data | [Current] | [Preserved/limited behavior] | [Product rules] |

**Confirmation action:** [Accurate change label].
**Decline or return:** [Keep current subscription unchanged].
**Uncertainty:** [What cannot be quoted until required details are supplied].

Do not reuse a public new-purchase amount for an existing subscriber. Treat a preview as informational until the change succeeds and reconcile the resulting entitlement with confirmed billing state.

## Completion check

Verify proration, effective date, remaining access, and failure recovery against the provider; confirm actual account exceptions are respected.

Related tactics: `PAY-017`, `UPG-004`, `UPG-011`, `UPG-019`.
