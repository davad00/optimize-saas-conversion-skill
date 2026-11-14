# Task-starting empty state

Template: `TMP-049` · Category: `activation`

## Use when

Turn an empty screen into a clear first task with a useful example.

## Required inputs

- Screen purpose and supported actions
- Required inputs
- Example data or output
- Permissions and account limitations

## Empty-state block

**Heading:** “[Create or complete the useful task].”
**Explanation:** “[What will appear here] after you [specific action].”
**Primary action:** [Start the real task].
**Helpful example:** [Sample input, starter artifact, or short demonstration].
**Prerequisite:** [Necessary connection, permission, or input].
**Alternative:** [Relevant import, template, or assisted route if supported].

| Empty-state reason | Correct message | Action |
| --- | --- | --- |
| New workspace | [Start first task] | [Create/import] |
| Filter hides results | [No matches under current filters] | [Reset/edit filters] |
| Permission limits visibility | [Accurate access explanation] | [Supported request route] |
| Loading or service issue | [Actual status] | [Retry/status] |

Distinguish a genuine empty account from loading, errors, and hidden content. Avoid showing a blank-state acquisition pitch to an established user whose data failed to load.

## Completion check

Test each empty-state cause, verify the primary action works for the current role, and keep the explanation specific to the screen’s actual job.

Related tactics: `ACT-007`, `ACT-010`, `CTA-011`.
