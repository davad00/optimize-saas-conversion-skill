# Diagnose the conversion opportunity

Treat this playbook as operating guidance, not evidence of a universal uplift. Use the source register for research claims.

## Establish the denominator

Choose the population whose business outcome matters. For a marketing page, it may be new eligible visitors; for a B2B trial, newly eligible accounts; for an upgrade, existing accounts that can actually buy the feature. Record bots, employees, current customers, unsupported regions, and test accounts as predeclared exclusions. Do not remove inconvenient users after seeing outcomes.

Align unit, dates, eligibility, and maturity before computing a rate. A November payment may belong to an October trial. A count of pageviews is not a count of people; a count of teammates is not a count of buying accounts.

Use a connected cohort funnel when available:

| Step | Definition to confirm | Common false diagnosis |
| --- | --- | --- |
| Eligible visit | Unique eligible unit enters relevant surface | Treating repeat pageviews as new prospects |
| Offer viewed | Pricing/offer is meaningfully exposed | Assuming page load means the below-fold price was seen |
| Signup completed | Durable account is created | Counting click or attempted request |
| Activated | Product-specific value action completes | Defining "activated" as login or a tutorial click without evidence |
| First payment | Confirmed paid transaction, with trial/zero invoices distinguished | Counting checkout redirect or subscription object creation |
| Retained paid | Same cohort remains paid under a defined horizon | Comparing young and mature cohorts |
| Expansion | Incremental recurring value from an existing account | Counting migration or retries as new revenue |

If sequential conditional rates are based on the same nested cohort, their product equals end-to-end conversion. If not, do not multiply them. Separate descriptive arithmetic from causal attribution.

## Collect the smallest useful evidence set

Inspect the actual journey, then seek evidence that could change the recommendation:

- Analytics: stage counts, segmentation, error rate, time to first value, refunds, repeat usage, and current event definitions.
- Customer language: sales questions, support conversations, cancellation reasons, win/loss notes, reviews, and voluntarily provided feedback.
- Product reality: real screenshots, task completion, integration limitations, required setup, migration effort, security facts, and billing settings.
- Context: campaign promise, search intent, competitor or manual alternative, buyer role, procurement needs, region, and device.

Access only connected or supplied data within scope. Avoid collecting sensitive form contents or raw payment details. Session recordings and surveys should fit the site's consent and data policies; verify current requirements where implementation depends on law.

Use interviews to understand mechanisms, not to estimate a conversion percentage. Start with a small varied set of real target users, continue where answers conflict, and keep frequency claims proportional to the sample.

## Ask useful research questions

Prefer concrete past behavior to hypothetical willingness:

- What happened immediately before you looked for a solution?
- How did you handle this task last time, and what did it cost in time or effort?
- What did you compare us with? What made an option unacceptable?
- What would you need to verify before paying or recommending this to your team?
- Show how you would choose a plan and complete the first valuable task.
- Where did you hesitate? What did you think would happen next?
- For a lost buyer: what ultimately happened, including doing nothing?

Do not lead with "Would this clearer page make you buy?" Preserve exact quotes only with provenance and permission appropriate to their use. Use internal notes as research evidence; do not turn private comments into public testimonials automatically.

## Match the diagnosis to the intervention

| Signal | Inspect first | Candidate intervention | Validate beyond |
| --- | --- | --- | --- |
| Many visits, little relevant engagement | Traffic intent, mobile render, promise clarity | Message-matched page, specific offer, usable hero | Time on page |
| Pricing views, little purchase intent | Segment fit, hidden limits, comparison burden | Plan guidance, total price, real proof | Pricing clicks |
| Signup starts, few completions | Errors, auth redirects, field necessity | Fix failures; remove genuinely unnecessary input | Button CTR |
| Many trials, low activation | Setup, data import, first useful output | Templates, sample data, guided first task | Trial volume |
| Activation, little payment | Upgrade value, budget, pricing unit, decision-maker | Contextual value gate, trial support, offer test | Paywall views |
| New purchases, fast refunds/churn | Promise mismatch, poor fit, reliability | Honest qualification, onboarding, product repair | Day-one revenue |
| Strong segment, weak aggregate | Segment mix and acquisition changes | Segment-specific experience or acquisition focus | Blended average |
| Abandoned checkout | Total cost, payment errors, authentication, eligibility | Clear total and recurring terms, recovery | Checkout starts |

Do not redesign a page to solve an upstream acquisition problem without examining intent. Do not discount to solve a product defect.

## Prioritize without fake precision

Use four practical buckets:

1. Repair: broken CTA, unusable form, wrong price, missing entitlement, inaccessible critical control.
2. Clarify: who the product is for, what outcome it delivers, what happens after clicking, what it costs.
3. Demonstrate: relevant product evidence, integration proof, objection handling, first value.
4. Experiment: alternative offer, packaging, trial structure, proof placement, and presentation.

Estimate reach from observed traffic when possible; otherwise use high/medium/low and say unknown. State impact as a mechanism and a plausible range only when assumptions are available. Treat confidence as source quality, not enthusiasm. Consider cost, rollout risk, and reversibility.

A prioritization score can organize a backlog; it cannot predict conversion. Label any worksheet weights as a local heuristic. Prefer one clear high-value intervention to an unrelated bundle that will be impossible to interpret.

## Low-traffic operating mode

If an experiment cannot reach its planned sample within a useful window:

- Repair demonstrable defects immediately within scope.
- Observe real customers completing the valuable task; investigate contradictory cases.
- Compare stronger propositions or workflows, rather than tiny color changes.
- Use pilots, concierge onboarding, or a limited rollout to learn feasibility and failure modes.
- Track outcomes over mature cohorts with dated notes on channel mix, releases, and seasonality.
- Report directional observation and uncertainty. Do not declare a causal winner from a handful of purchases.

Use a sales-assisted trial for complex onboarding when the service and economics support it. Do not create a waitlist or fake-door purchase that misrepresents availability; clearly describe pilots and prototypes.

## Bound the output

Record what was actually inspected, the data period, missing facts, and the selected intervention. An "unknown" item is not a scored failure. A screenshot-only audit cannot verify payment, loading, keyboard behavior, speed, or retention. Keep those checks explicitly unverified.
