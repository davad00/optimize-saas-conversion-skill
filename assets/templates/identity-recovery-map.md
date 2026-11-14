# Identity and invitation recovery map

Template: `TMP-039` · Category: `purchase`

## Use when

Help a buyer reach the correct account or workspace after identity conflicts.

## Required inputs

- Actual authentication methods
- Existing-account and invitation behavior
- Return destinations and plan state
- Security and recovery requirements

## Recovery paths

| Starting condition | Explain to the buyer | Available recovery | Context to preserve | Confirmed end state |
| --- | --- | --- | --- | --- |
| Existing account at signup | [Useful neutral wording] | [Sign in/reset] | [Task/offer] | [Correct account] |
| Invitation email differs | [Mismatch and options] | [Supported identity change] | [Invited workspace] | [Authorized membership] |
| Verification opens elsewhere | [Continue securely] | [Supported return route] | [Intended task] | [Verified session] |
| Partial account exists | [Accurate status] | [Resume or recover] | [Valid input] | [One usable account] |

**Privacy constraints:** [Avoid disclosing unnecessary account existence or membership].
**Fallback help:** [Safe reference and supported assistance].
**Expired link behavior:** [Explain expiry and allow a new valid route].

Never attach an invitation to a different identity without the product's actual authorization rules. Keep payment selection separate from authentication success.

## Completion check

Exercise each supported identity path in the real flow and confirm workspace ownership, task continuity, and absence of duplicate accounts or subscriptions.

Related tactics: `SIG-002`, `SIG-006`, `SIG-016`, `SIG-017`, `SIG-020`.
