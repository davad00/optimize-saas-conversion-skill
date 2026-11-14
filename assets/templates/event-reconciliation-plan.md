# Event reconciliation plan

Template: `TMP-070` · Category: `measurement`

## Use when

Check that analytics events correspond to real product and billing outcomes.

## Required inputs

- Project event contract
- Sample client/server/provider records
- Identity and deduplication rules
- Known test journeys and consent behavior

## Trace matrix

| Journey action | Expected semantic event | Producer/source | Required properties | Dedupe key | Observed evidence |
| --- | --- | --- | --- | --- | --- |
| [Verified account created] | [Signup outcome] | [Server] | [Fields] | [Key] | [Record] |
| [Confirmed positive payment] | [Paid outcome] | [Verified billing] | [Fields] | [Transaction key] | [Record] |

## Reconciliation checks

- Event delivery versus economic outcome: [Retries and duplicate provider notifications].
- Identity: [Anonymous-to-account mapping and stable analysis unit].
- Time: [Occurred versus received timestamps and timezone].
- Amounts: [Currency, integer minor units, refunds, and zero-value invoices].
- Exposure: [Defined opportunity, assignment, and treatment consistency].
- Privacy: [No raw payment details, secrets, or unnecessary personal text].

**Mismatch register:** [Record, actual cause, correction, owner].
**Unavailable evidence:** [What cannot currently be verified].

A valid JSON event does not prove the underlying payment or product action occurred. Reconcile representative records with the authoritative system.

## Completion check

Exercise success, failure, retry, and delayed outcomes; verify deduplication and authoritative state before using events for sales or experiment conclusions.

Related tactics: `PAY-018`, `SIG-020`, `ACT-013`.
