# Conversion rollout and rollback plan

Template: `TMP-075` · Category: `measurement`

## Use when

Release an authorized change with observable checks and a concrete recovery path.

## Required inputs

- Exact implemented change and dependencies
- Existing release authorization
- Functional verification and event checks
- Baseline and material downside thresholds

## Release decision

**Change:** [Routes, components, offer presentation, and affected users].
**Authorization:** [Already authorized scope; any genuinely missing final decision].
**Verified behavior:** [Actual checks, including payment/entitlement if affected].
**Unavailable checks:** [Named gaps and practical consequence].
**Release mechanism:** [Existing deployment/flag process].

| Monitor | Definition and source | Review timing | Investigation/rollback condition | Owner |
| --- | --- | --- | --- | --- |
| [Payment or journey failure] | [Concrete event] | [Appropriate interval] | [Material threshold] | [Role] |
| [Paid outcome/guardrail] | [Eligible denominator/window] | [Mature follow-up] | [Predefined condition] | [Role] |

**Rollback:** [Exact version, flag, or reversible configuration].
**Data and billing consequences:** [What rollback does and does not reverse].
**Post-release record:** [What was observed, action taken, and remaining uncertainty].

Prepare the implementation and recovery path before asking for any missing release authorization. Do not roll back valid purchases or customer data as an incidental consequence of reverting presentation code.

## Completion check

Confirm the recovery mechanism works for this change, monitor concrete risks, and distinguish release verification from proof of business uplift.

Related tactics: `PAY-011`, `PAY-018`, `RET-016`.
