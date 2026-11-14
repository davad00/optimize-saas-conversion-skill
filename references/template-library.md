# Reusable template selector

Use these **75 templates: the six original assets plus 69 additional task-specific templates**. Choose the output needed for the observed obstacle. Fill it from verified project facts, leave unresolved fields visibly unknown, and adapt its wording to the product. A template is a working aid; it does not require a new document, add an approval gate, or authorize commercial changes or customer messages.

## Contents

- [Select by task](#select-by-task)
- [Retrieve a template](#retrieve-a-template)
- [Complete the selected output](#complete-the-selected-output)
- [All 75 templates](#all-75-templates)

## Select by task

| Task | Template family | Count | Typical output |
| --- | --- | ---: | --- |
| Establish scope and mandatory checks | Core | 6 | Conversion brief, pricing gate, review checklist |
| Understand buying obstacles | Research | 8 | Interviews, win/loss review, customer language, journey evidence |
| Convert qualified incoming demand | Acquisition | 7 | Campaign match, intent routing, comparison and integration pages |
| Explain value and support a decision | Landing | 7 | Hero, page structure, proof, demo, FAQ, CTA specification |
| Clarify or propose the offer | Pricing | 9 | Plan fit, comparisons, bill examples, cost models, quotes |
| Complete signup and purchase reliably | Purchase | 7 | Identity recovery, order summary, payment states, continuity |
| Reach meaningful first value | Activation | 7 | First-value path, starter work, import recovery, upgrade resume |
| Support durable customer value | Lifecycle | 7 | Trial decisions, limits, renewals, recovery, exit, handoff |
| Help a real opportunity reach a decision | Sales | 10 | Discovery, demo, champion memo, business case, pilot, proposal |
| Learn whether changes help | Measurement | 7 | Metric definitions, event checks, cohorts, experiments, rollout |

The mandatory baseline and pricing audit in `SKILL.md` still apply. Templates supplement those checks; selecting a convenient template does not make omitted journey states pass.

## Retrieve a template

Resolve scripts from the installed skill directory:

```bash
python3 <skill-dir>/scripts/resource_finder.py list --kind template --category pricing
python3 <skill-dir>/scripts/resource_finder.py search 'champion approval' --kind template
python3 <skill-dir>/scripts/resource_finder.py show TMP-061
python3 <skill-dir>/scripts/resource_finder.py render TMP-061
```

`show` returns catalog metadata; `render` emits the existing template text to stdout. These operations do not fill, save, send, publish, or execute the template. If Python is unavailable, use the links below or read `template-catalog.json`. Keyword retrieval is a candidate finder; inspect the purpose and required inputs before choosing.

## Complete the selected output

1. Select the smallest useful artifact for the actual task and related tactic IDs.
2. Replace placeholders with sourced facts. Label illustrative figures, proposals, and unresolved inputs.
3. Keep account-specific payments, actual entitlements, and commercial commitments consistent with their authoritative sources.
4. Implement authorized changes when requested; a filled planning template is not implementation.
5. Perform its completion checks and record unavailable verification accurately.

Communication templates are drafts until sending is explicitly authorized. Use authorization already present; do not ask again solely because a template mentions commercial or outreach scope. Prepare concrete proposed terms before requesting a genuinely missing decision. Keep private customer evidence in the user's intended project context, not in this reusable skill.

## All 75 templates

### Core — 6

| ID and template | Use when |
| --- | --- |
| [TMP-001 — Conversion brief](../assets/conversion-brief.md) | Establish the buyer, outcome, verified offer, and authorized work. |
| [TMP-002 — Conversion experiment brief](../assets/experiment-brief.md) | Plan a causal test or explicitly observational rollout with decision criteria. |
| [TMP-003 — Adaptable event contract](../assets/event-contract.json) | Define semantic analytics and billing events before adapting them to the project. |
| [TMP-004 — Independent review checklist](../assets/review-checklist.md) | Review the final conversion change against functional, factual, and measurement requirements. |
| [TMP-005 — Mandatory pricing audit](../assets/pricing-audit.md) | Inspect all pricing states, defaults, savings, and payment continuity. |
| [TMP-006 — Tactic decision record](../assets/tactic-decisions.md) | Record relevant family coverage, selected tactics, exact actions, and verification. |

### Research — 8

| ID and template | Use when |
| --- | --- |
| [TMP-007 — Buyer interview guide](../assets/templates/buyer-interview-guide.md) | Investigate the circumstances behind a real buying or abandoning decision. |
| [TMP-008 — Win, loss, and no-decision review](../assets/templates/win-loss-review.md) | Compare documented buying outcomes to locate preventable obstacles and unsuitable demand. |
| [TMP-009 — Objection and evidence map](../assets/templates/objection-evidence-map.md) | Place the right answer and supporting proof where a specific buying doubt appears. |
| [TMP-010 — Customer language lexicon](../assets/templates/customer-language-lexicon.md) | Replace internal jargon with accurate language buyers use to describe their work. |
| [TMP-011 — Buyer segment priority decision](../assets/templates/segment-priority-decision.md) | Choose which qualified buying situation a page or campaign should primarily serve. |
| [TMP-012 — Journey evidence map](../assets/templates/journey-evidence-map.md) | Connect buyer expectations and observed behavior across the entire purchase path. |
| [TMP-013 — Offer comprehension session](../assets/templates/comprehension-session.md) | Discover whether buyers understand the product, price, commitment, and next step. |
| [TMP-014 — Support-ticket obstacle coding](../assets/templates/support-ticket-coding.md) | Turn recurring support questions into specific conversion and onboarding repairs. |

### Acquisition — 7

| ID and template | Use when |
| --- | --- |
| [TMP-015 — Campaign-to-page message map](../assets/templates/campaign-message-match.md) | Keep the acquisition promise, offer, and landing-page next step consistent. |
| [TMP-016 — Search-intent destination map](../assets/templates/search-intent-route.md) | Route research, comparison, and purchase intent to useful destinations. |
| [TMP-017 — Factual competitor evaluation page](../assets/templates/competitor-evaluation-page.md) | Help buyers compare real alternatives on criteria relevant to their work. |
| [TMP-018 — Integration entry-page brief](../assets/templates/integration-entry-page.md) | Convert integration interest by showing the supported workflow and required setup. |
| [TMP-019 — Useful resource-to-product bridge](../assets/templates/useful-resource-bridge.md) | Turn a genuinely useful educational asset into a relevant product evaluation route. |
| [TMP-020 — Partner referral destination](../assets/templates/partner-referral-page.md) | Explain a referring relationship and continue a partner-specific buying context. |
| [TMP-021 — Expired campaign recovery page](../assets/templates/expired-offer-recovery.md) | Give visitors a useful and truthful route when an old promotion or campaign ends. |

### Landing — 7

| ID and template | Use when |
| --- | --- |
| [TMP-022 — Hero copy and action block](../assets/templates/hero-copy-block.md) | Make the first screen explain the customer, outcome, mechanism, and next step. |
| [TMP-023 — Landing-page decision outline](../assets/templates/landing-page-outline.md) | Arrange page sections around the questions a buyer must answer before proceeding. |
| [TMP-024 — Evidence-backed proof card](../assets/templates/proof-card.md) | Turn an approved customer or product result into a credible proof block. |
| [TMP-025 — Customer outcome case study](../assets/templates/customer-case-study.md) | Explain how a real customer achieved a result and what another buyer can reasonably learn. |
| [TMP-026 — Product demo storyboard](../assets/templates/product-demo-storyboard.md) | Show one useful task and its result without making the evaluator sit through an unrelated tour. |
| [TMP-027 — Decision-focused FAQ block](../assets/templates/objection-faq-block.md) | Answer remaining purchase questions directly at the relevant page location. |
| [TMP-028 — CTA action and state specification](../assets/templates/cta-action-spec.md) | Make an action's wording, destination, commitment, and feedback agree. |

### Pricing — 9

| ID and template | Use when |
| --- | --- |
| [TMP-029 — Plan-fit card](../assets/templates/plan-fit-card.md) | Help buyers recognize the right plan through use case, capacity, and meaningful limits. |
| [TMP-030 — Differences-only plan comparison](../assets/templates/plan-difference-table.md) | Make the upgrade decision depend on real incremental value. |
| [TMP-031 — Value-metric decision worksheet](../assets/templates/value-metric-decision.md) | Evaluate which billable unit buyers can understand, predict, and connect to value. |
| [TMP-032 — Usage bill explainer](../assets/templates/usage-bill-explainer.md) | Explain variable, tiered, or minimum pricing with reproducible worked examples. |
| [TMP-033 — Editable break-even widget specification](../assets/templates/break-even-widget.md) | Help a buyer estimate the workload needed to justify a subscription under their own assumptions. |
| [TMP-034 — Promotion and renewal timeline](../assets/templates/promotion-timeline.md) | Make introductory discounts and later recurring charges understandable before purchase. |
| [TMP-035 — Commercial offer proposal](../assets/templates/commercial-offer-proposal.md) | Prepare a concrete pilot, guarantee, bonus, credit, or installment offer for an authorized decision. |
| [TMP-036 — Switching-cost comparison](../assets/templates/switching-cost-case.md) | Help buyers compare adoption effort and ongoing cost against their actual current workflow. |
| [TMP-037 — Buyer-specific quote summary](../assets/templates/buyer-quote-summary.md) | Summarize the complete configured purchase so buyers can compare and share it accurately. |

### Purchase — 7

| ID and template | Use when |
| --- | --- |
| [TMP-038 — Signup field necessity review](../assets/templates/signup-field-review.md) | Remove registration effort that is not required for the immediate account or task. |
| [TMP-039 — Identity and invitation recovery map](../assets/templates/identity-recovery-map.md) | Help a buyer reach the correct account or workspace after identity conflicts. |
| [TMP-040 — Checkout order summary](../assets/templates/checkout-order-summary.md) | Make the actual purchase commitment clear immediately before payment. |
| [TMP-041 — Payment state and recovery copy](../assets/templates/payment-state-recovery.md) | Guide buyers through failed, pending, authenticated, and interrupted payment attempts. |
| [TMP-042 — Checkout continuity matrix](../assets/templates/checkout-continuity-matrix.md) | Preserve a buyer’s deliberate plan, interval, quantity, and task across interruptions. |
| [TMP-043 — Existing-account plan-change preview](../assets/templates/plan-change-preview.md) | Explain the actual financial and entitlement effect of an upgrade or downgrade. |
| [TMP-044 — Purchase confirmation and first-use handoff](../assets/templates/purchase-confirmation.md) | Confirm a verified payment and give the buyer a direct route to useful access. |

### Activation — 7

| ID and template | Use when |
| --- | --- |
| [TMP-045 — First-value path map](../assets/templates/first-value-path.md) | Reduce the work between account creation and the first meaningful customer result. |
| [TMP-046 — Goal-based onboarding route](../assets/templates/goal-based-onboarding.md) | Adapt initial guidance to a user’s declared task without adding unnecessary questioning. |
| [TMP-047 — Editable starter-work specification](../assets/templates/editable-starter-example.md) | Give a new account useful sample work that demonstrates the product without creating unwanted commitments. |
| [TMP-048 — Import preview and recovery plan](../assets/templates/import-preview-recovery.md) | Help users trust and complete data import without losing progress. |
| [TMP-049 — Task-starting empty state](../assets/templates/task-starting-empty-state.md) | Turn an empty screen into a clear first task with a useful example. |
| [TMP-050 — Meaningful progress and feedback specification](../assets/templates/meaningful-progress-feedback.md) | Help users understand what is complete, what remains, and whether useful work has succeeded. |
| [TMP-051 — Upgrade-and-resume journey specification](../assets/templates/upgrade-and-resume.md) | Let a user continue valuable blocked work after an authorized paid upgrade. |

### Lifecycle — 7

| ID and template | Use when |
| --- | --- |
| [TMP-052 — Trial decision summary](../assets/templates/trial-decision-summary.md) | Help an evaluator judge paid fit using actual results and remaining requirements. |
| [TMP-053 — Usage-limit notice and next-step block](../assets/templates/usage-limit-notice.md) | Explain an approaching allowance limit before it unexpectedly interrupts useful work. |
| [TMP-054 — Renewal value and commitment review](../assets/templates/renewal-value-review.md) | Prepare a renewal decision using realized value, current needs, and exact upcoming terms. |
| [TMP-055 — Failed renewal recovery plan](../assets/templates/failed-renewal-recovery.md) | Restore a subscription payment through the right account owner without confusing product access. |
| [TMP-056 — Cancellation, pause, and downgrade options](../assets/templates/cancellation-options.md) | Offer relevant alternatives while keeping the requested exit clear and operable. |
| [TMP-057 — Reason-based reactivation brief](../assets/templates/reactivation-reason-brief.md) | Prepare a relevant return path when the specific reason for leaving has changed. |
| [TMP-058 — Account champion handoff](../assets/templates/account-champion-handoff.md) | Preserve useful adoption and billing continuity when the customer’s internal owner changes. |

### Sales — 10

| ID and template | Use when |
| --- | --- |
| [TMP-059 — Sales discovery call plan](../assets/templates/discovery-call-plan.md) | Qualify a current buying opportunity and identify the next useful evaluation step. |
| [TMP-060 — Buyer-specific sales demo runbook](../assets/templates/buyer-specific-demo.md) | Demonstrate the prospect’s decisive workflow and capture evaluation evidence. |
| [TMP-061 — Champion approval memo](../assets/templates/champion-approval-memo.md) | Give an internal supporter a concise document they can use in their own approval process. |
| [TMP-062 — Buyer-owned business case](../assets/templates/buyer-business-case.md) | Build a reviewable purchase case using the buyer’s economics, objectives, and uncertainty. |
| [TMP-063 — Mutual evaluation plan](../assets/templates/mutual-evaluation-plan.md) | Coordinate the buyer and seller around concrete evidence and an actual decision process. |
| [TMP-064 — Pilot success agreement](../assets/templates/pilot-success-agreement.md) | Define a bounded evaluation that can produce an interpretable adoption decision. |
| [TMP-065 — Current sales proposal](../assets/templates/sales-proposal.md) | Present one authoritative offer with scope, cost, dependencies, and acceptance steps. |
| [TMP-066 — Procurement review tracker](../assets/templates/procurement-review-tracker.md) | Remove avoidable buying delays by assigning requirements, evidence, and dependencies. |
| [TMP-067 — Sales objection response card](../assets/templates/sales-objection-response.md) | Help a seller respond to a specific live concern without guessing the buyer’s reason. |
| [TMP-068 — Sales-to-implementation handoff](../assets/templates/sales-implementation-handoff.md) | Preserve the exact customer promise and success criteria after a purchase. |

### Measurement — 7

| ID and template | Use when |
| --- | --- |
| [TMP-069 — Metric definition card](../assets/templates/metric-definition-card.md) | Define a business measure that different systems and reviewers can reproduce. |
| [TMP-070 — Event reconciliation plan](../assets/templates/event-reconciliation-plan.md) | Check that analytics events correspond to real product and billing outcomes. |
| [TMP-071 — Comparable-cohort funnel diagnosis](../assets/templates/funnel-diagnosis-sheet.md) | Locate major journey losses using counts that share an eligible population and time window. |
| [TMP-072 — Cohort retention and refund review](../assets/templates/cohort-retention-review.md) | Assess durable paid value while accounting for follow-up maturity and billing differences. |
| [TMP-073 — Experiment assignment and exposure QA](../assets/templates/assignment-exposure-qa.md) | Check whether a planned comparison can support the intended experiment analysis. |
| [TMP-074 — Low-traffic learning plan](../assets/templates/low-traffic-learning-plan.md) | Learn from a small customer base without pretending it supports a precise uplift estimate. |
| [TMP-075 — Conversion rollout and rollback plan](../assets/templates/rollout-rollback-plan.md) | Release an authorized change with observable checks and a concrete recovery path. |
