# Upgrade-and-resume journey specification

Template: `TMP-051` · Category: `activation`

## Use when

Let a user continue valuable blocked work after an authorized paid upgrade.

## Required inputs

- Actual current and target entitlements
- Draft persistence rules
- Provider checkout and fulfillment states
- Existing-plan alternatives

## Contextual upgrade block

**Attempted task:** [What the user was trying to finish].
**Blocked capability:** [Exact limit or paid feature].
**Upgrade benefit:** [Specific capability unlocked].
**Financial summary:** [Real due-now amount, interval, renewal, and account-change terms].
**Current-plan route:** [Useful supported alternative].
**Saved work:** [What is retained and for how long].

| State | Stored context | User action | Resume condition |
| --- | --- | --- | --- |
| Before payment | [Draft and intended task] | [Review upgrade] | [None yet] |
| Canceled/failed | [Preserved draft] | [Retry or continue alternative] | [Current access] |
| Payment confirmed | [Same draft] | [Return to task] | [Verified target entitlement] |

Resume only after the server confirms entitlement. Do not make the buyer recreate useful work or infer payment from a browser return. Explain any genuine data retention constraints before leaving the task.

## Completion check

Exercise upgrade success, failure, cancellation, delayed fulfillment, and return; verify the exact artifact resumes under the correct account and entitlement.

Related tactics: `UPG-002`, `UPG-003`, `UPG-014`, `UPG-015`.
