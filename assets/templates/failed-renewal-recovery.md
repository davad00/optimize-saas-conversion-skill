# Failed renewal recovery plan

Template: `TMP-055` · Category: `lifecycle`

## Use when

Restore a subscription payment through the right account owner without confusing product access.

## Required inputs

- Confirmed failed-renewal state
- Provider retry schedule
- Account billing roles
- Grace period and access policy

## Recovery content

**Status:** “[Renewal payment state verified by the provider].”
**Affected subscription:** [Package and workspace].
**Amount:** [Actual due amount/currency].
**Required action:** [Secure billing portal or supported payment update].
**Timing:** [Actual retry or grace-period dates].
**Access consequence:** [Current and future state under the real policy].
**Help reference:** [Safe account/invoice reference].

| Recipient role | Relevant information | Available action | Suppression condition |
| --- | --- | --- | --- |
| Billing owner | [Invoice and secure route] | [Update payment] | [Paid/resolved] |
| Other member | [Only necessary access context] | [Contact billing owner if supported] | [No relevant impact] |

Avoid repeated prompts after settlement, duplicate collection, or exposing payment details to unauthorized members. Separate voluntary cancellation from an unpaid renewal. This plan prepares content and workflow; it does not authorize customer messages or payment collection changes.

## Completion check

Reconcile provider state before each action, verify secure role-appropriate links, and test resolution suppression plus accurate access restoration.

Related tactics: `RET-004`, `PAY-020`.
