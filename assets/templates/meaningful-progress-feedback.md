# Meaningful progress and feedback specification

Template: `TMP-050` · Category: `activation`

## Use when

Help users understand what is complete, what remains, and whether useful work has succeeded.

## Required inputs

- Actual task states and completion signals
- Required milestones
- Processing and failure behavior
- User-editable decisions

## Milestone model

| Milestone | Real completion condition | User-facing label | Remaining work | Recovery |
| --- | --- | --- | --- | --- |
| [Useful step] | [Verified state/event] | [Plain wording] | [Next dependency] | [Supported action] |

**Progress display:** [Completed meaningful steps out of applicable steps; no invented percentage].
**Processing message:** [What is happening, known timing, useful available action].
**Success message:** “[Verified result] is ready. Review [important quality or limitation] and [next useful action].”
**Partial success:** [What completed and what needs attention].

Allow users to inspect or revise mistaken inputs. Do not count opening a screen as completing the underlying task. If the number of steps changes with the selected workflow, explain the relevant milestones rather than making progress jump unpredictably.

**Measurement:** [Verified completion and result use; abandonment at actual blockages].

## Completion check

Match every progress indicator to real state, test failure and resume paths, and ensure success copy does not imply quality or completion that was not verified.

Related tactics: `ACT-009`, `ACT-013`, `ACT-014`, `ACT-016`.
