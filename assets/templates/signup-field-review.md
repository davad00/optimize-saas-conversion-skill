# Signup field necessity review

Template: `TMP-038` · Category: `purchase`

## Use when

Remove registration effort that is not required for the immediate account or task.

## Required inputs

- Current form and server requirements
- Authentication and fraud constraints
- Downstream uses of collected fields
- Target device and buyer task

## Field decision table

| Field | Immediate purpose | Required by what? | Remove, defer, or retain | Input behavior | Error and recovery |
| --- | --- | --- | --- | --- | --- |
| [Field] | [Specific current use] | [Actual dependency] | [Decision and reason] | [Type/autocomplete] | [Accurate correction] |

## Revised form contract

**Minimum inputs:** [Only what the immediate flow needs].
**Deferred collection:** [When another field becomes useful and why].
**Validation timing:** [After meaningful input, with server enforcement].
**Error summary:** [Focus and links to affected fields].
**Preserved values:** [Valid nonsensitive entries retained after failure].
**Submission:** [Keyboard and pointer behavior; duplicate prevention].

Do not remove a field solely because shorter forms sound preferable; verify whether it supports identity, tax, required eligibility, or the promised workflow. Conversely, future marketing convenience alone should not silently become a required registration step.

**Measure:** [Completed usable accounts and qualified paid outcomes, plus identity/recovery failures].

## Completion check

Test retained fields with mobile keyboards, password managers, server errors, and accessibility; verify deferred data is requested only when needed.

Related tactics: `SIG-001`, `SIG-009`, `SIG-010`, `SIG-011`.
