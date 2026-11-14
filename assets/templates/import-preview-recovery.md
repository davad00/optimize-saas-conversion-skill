# Import preview and recovery plan

Template: `TMP-048` · Category: `activation`

## Use when

Help users trust and complete data import without losing progress.

## Required inputs

- Supported formats and limits
- Actual parser behavior
- Field mapping and validation rules
- Storage, retry, and cancellation semantics

## Import stages

| Stage | Show the user | Action available | State preserved |
| --- | --- | --- | --- |
| Before upload | [Formats, size, required fields] | [Sample/check fit] | [Chosen task] |
| Preview | [Rows and field mapping] | [Correct mapping] | [Valid input] |
| Validation | [Specific affected records] | [Fix/skip if supported] | [Successful checks] |
| Processing | [Actual progress and status] | [Supported cancel/resume] | [Completed work] |
| Complete | [Imported and rejected counts] | [Inspect/use result] | [Source reference] |

**Unsupported input copy:** [Exact issue, supported example, next action].
**Partial failure:** [What succeeded, what did not, how retry avoids duplicates].
**Data handling:** [Accurate retention and deletion behavior].

Do not display cosmetic progress unrelated to processing. Confirm destructive replacement or irreversible merge behavior through the product's existing controls, not a vague import button.

## Completion check

Test a valid file, malformed file, partial error, interruption, and retry; reconcile result counts and ensure recovery does not duplicate or silently discard data.

Related tactics: `ACT-004`, `ACT-005`, `ACT-017`, `OBJ-005`.
