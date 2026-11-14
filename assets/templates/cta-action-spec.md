# CTA action and state specification

Template: `TMP-028` · Category: `landing`

## Use when

Make an action's wording, destination, commitment, and feedback agree.

## Required inputs

- Buyer state and intended next step
- Routes and authentication behavior
- Plan or task context
- Loading, error, and disabled conditions

## Action contract

- Label: [Verb describing the immediate action].
- Accessible name: [Same intent, with context where needed].
- Destination or handler: [Actual route/action].
- Context preserved: [Plan, interval, task, workspace].
- Adjacent commitment: [Relevant accurate payment or signup fact].

| State | Label and feedback | Interaction | Next valid state |
| --- | --- | --- | --- |
| Ready | [Action] | [Click/Enter] | [Expected route] |
| Pending | [Specific progress] | [Prevent duplicate work] | [Success/retry] |
| Unavailable | [Reason] | [Explanation or correction] | [Ready] |
| Error | [Actionable recovery] | [Preserve valid input] | [Retry/help] |

**Secondary action:** [Different legitimate need, visually subordinate].
**Repeated placements:** [Consistent label and context].

Do not label a paid commitment as a harmless preview. Native controls should match the action; auxiliary form buttons must not accidentally submit the main form.

## Completion check

Exercise pointer, keyboard, loading, failure, and return states; verify the CTA promise matches its actual destination and financial consequence.

Related tactics: `CTA-001`, `CTA-002`, `CTA-019`, `CTA-020`.
