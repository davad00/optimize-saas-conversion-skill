# Goal-based onboarding route

Template: `TMP-046` · Category: `activation`

## Use when

Adapt initial guidance to a user’s declared task without adding unnecessary questioning.

## Required inputs

- Supported first tasks
- Actual setup dependencies per task
- Available starter data
- Editable user preferences

## Goal selection

**Prompt:** “What would you like to complete first?”
**Options:** [A small set of real supported tasks], plus [continue without choosing if viable].

| Declared goal | Required input | First useful action | Relevant guidance | Deferred setup |
| --- | --- | --- | --- | --- |
| [Task] | [Input] | [Action] | [Specific hint/example] | [Unrelated work] |

## Route copy

“You chose [task]. To produce [result], provide [minimum input]. You can change this goal at [location].”

**Optional first-use plan:** [Task, input, intended session time].
**Expert route:** [Direct access to the workflow].
**Unknown goal:** [Useful default with visible choices and no invented personalization].

Do not infer sensitive traits or impose a role the user did not choose. A goal choice should materially change the next helpful step; remove it if every option leads to identical setup.

## Completion check

Verify every option leads to a working relevant task, preserves editable preferences, and avoids collecting information with no immediate purpose.

Related tactics: `ACT-001`, `ACT-008`, `ACT-020`.
