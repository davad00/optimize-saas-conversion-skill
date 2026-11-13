# Activation and retention

Use this playbook when visitors register but do not experience value, trial users fail to buy, subscribers leave early, or expansion obscures underlying losses. Treat onboarding, paywall, trial, and retention changes as hypotheses with observable customer outcomes. Logging in, completing a tour, and receiving a reminder are not proof of value.

## Contents

- Define first meaningful value
- Reduce the path to that outcome
- Design trials and freemium transitions
- Place paywalls and upgrades in context
- Draft useful lifecycle communication
- Recover payments and manage renewal
- Make cancellation clear
- Measure mature cohorts and retained revenue

## Define first meaningful value

Identify the smallest outcome that demonstrates the product's promised utility for the target job. Examples: a report generated from real input that answers the buyer's question, an automated workflow completing successfully, or a teammate using a shared deliverable. Distinguish setup actions from outcomes and first value from repeated value.

Write an activation event contract with entity, eligible population, required state, timestamp, and exclusions. Use account-level activation when value depends on a team. Verify the event against actual product state; clicking “Generate” is insufficient if the job fails. Correlation between an activation event and retention does not establish that forcing the event causes retention.

Measure time from a consistent start to the verified outcome. Report the distribution among successful users and the fraction that never reaches it within the window; a fast median among a shrinking successful subset can conceal failure. Compare relevant acquisition sources, segments, and device contexts without changing the population after observing results.

## Reduce the path to that outcome

Walk through a new account on the actual product. Record required decisions, setup, waiting, data access, invitations, and recoverable errors. Remove or defer steps that do not serve the immediate outcome, service delivery, security, or necessary qualification.

Offer sample data when users need to understand the product before connecting their own. Mark sample results clearly and provide an obvious path to real data. For imports, explain required permissions and accepted formats; include validation, progress, failure recovery, and a usable empty state. Never present demonstration output as the user's achieved result.

Use progressive profiling to collect relevant information at the moment it helps. A default should be understandable and editable. Progress indicators must describe real work; allow skipping optional tasks and resuming later. Avoid artificial completion rewards, concealed paid defaults, and mandatory invitations that do not serve the immediate job.

For complex products, consider templates, guided setup, an interactive demo, migration assistance, or a contextual help route. Present these as alternatives to test against the observed obstacle. More onboarding screens do not necessarily create better understanding. Preserve expert paths for people who already know their task.

## Design trials and freemium transitions

Match evaluation length to realistic time-to-value and the buyer's working cycle. State start/end timing and timezone where relevant; distinguish account creation from the actual trial start. Explain cost now, payment-method requirement, post-trial price, renewal interval, included limits, end behavior, and cancellation.

A no-card trial may reduce entry friction but creates a later payment step. A card-required trial adds early commitment and can screen demand. Neither is universally superior. Compare purchases and retained revenue per eligible visitor, not merely trial-to-paid conversion among differently selected trial cohorts. Watch refund, support, and unwanted-renewal signals.

Inspect the existing provider, SDK/API version, billing mode, and supported checkout interface before implementation. Stripe's current documentation separates Trial Offers from legacy free-trial behavior; supported interfaces and version requirements differ. Recheck the live documentation rather than embedding one permanent trial API recipe. [Stripe trials](https://docs.stripe.com/billing/subscriptions/trials)

For freemium, define a useful free outcome and a comprehensible upgrade boundary tied to additional value or service cost. Monitor cost-to-serve and whether the free product attracts the intended users. Do not break completed work or quietly remove access to push payment. If a trial extension could help, specify a genuine evaluation reason and measure the eventual result rather than counting extension as conversion.

## Place paywalls and upgrades in context

Explain the unavailable capability, the relevant plan, total charge, timing, and what happens to existing work. Let users return to their task or choose an available alternative. Show an upgrade when its benefit relates to the attempted job; avoid blocking unrelated basic operations with repeated promotions.

Preserve user input across checkout and authentication. After verified purchase, grant the correct entitlement and resume the intended task. Test payment failure, delayed confirmation, duplicate callbacks, canceled checkout, plan changes, and browser refresh. A paid event and a successful product experience are separate outcomes.

Offer seats, capacity, or advanced workflow features when demonstrated need makes the value legible. An expansion event is not automatically a customer success event. Track whether the expanded capability is used and whether contribution and satisfaction persist.

## Draft useful lifecycle communication

Draft messages around customer state: setup stalled, first result achieved, trial ending, relevant limit approached, payment failed, or renewal approaching. Give each message a clear purpose, accurate trigger, useful next action, and suppression rule after the action is complete.

Record recipient eligibility, channel, frequency, timezone, preferences, and excluded states. Distinguish requested service notices from promotional messages. Do not add customers to a campaign or send messages without explicit authorization; previously granted send authorization remains valid within its scope. Continue drafting and implementing authorized reversible work without asking again.

State verified value, charges, and dates. Avoid implying that an account is endangered when it is not. Test links and message variables with fixtures; do not expose real customer information in previews. Measure the intended action and downstream purchase or retained use, with complaints and opt-outs as guardrails.

## Recover payments and manage renewal

Separate voluntary churn from failed collection, expired credentials, authentication requirements, and product-access defects. Reuse the provider's supported retry and payment-update flows instead of adding competing retry jobs. Some failures require a new payment method or customer action; more retries are not always a remedy. [Stripe payment retries](https://docs.stripe.com/billing/revenue-recovery/smart-retries)

Inspect which payment method the subscription actually uses, retry state, webhook handling, grace period, and entitlement policy. Test recovery and terminal failure. Make the next action and payment status understandable; reconcile access with authoritative billing events.

For renewals, show the forthcoming charge, date, interval, applicable change, and account-management route. Keep communication consistent with the actual contract and authorized policy. Measure recovered collections and continued useful service separately from temporarily postponed churn.

## Make cancellation clear

Provide an accessible cancellation route and explicit effective date, remaining access, future charge behavior, and data consequences. Confirm the final state. Cancellation at period end differs from immediate cancellation and from pausing; label each accurately.

A relevant pause, downgrade, or save offer can be optional and easy to dismiss. Do not require a call, repeated screens, or a survey merely to suppress cancellation metrics. Collect reasons voluntarily and use them to improve product fit. Verify provider support for the actual subscription configuration; customer-portal features have integration-specific limits. [Stripe customer portal](https://docs.stripe.com/customer-management)

## Measure mature cohorts and retained revenue

Define cohort entry, observation window, unit, plan, and treatment. Compare trials only after the full evaluation and payment window; compare retention at equal cohort ages. Keep first payment, renewal, reactivation, expansion, contraction, refund, and cancellation distinct. Do not treat a billing status alone as verified cash collection.

For a declared period and original paying cohort, let `B` be starting normalized recurring revenue, `C` churn loss, `D` contraction, and `E` expansion. Under this explicitly chosen convention:

- `GRR = (B - C - D) / B` excludes expansion and new customers.
- `NRR = (B - C - D + E) / B` includes expansion, excludes new customers, and may exceed 100%.
- With `B = 10,000`, `C = 500`, `D = 500`, and `E = 2,000`, GRR is 90% and NRR is 110%.

Require `B > 0`. Define reactivation, discounts, currency effects, delinquency, metered usage, and account mergers; prevent double-counting movements. Provider definitions vary, including discount and active-subscriber settings. [Stripe billing analytics](https://docs.stripe.com/billing/subscriptions/analytics)

Pair NRR with GRR and customer retention so expansion cannot conceal widespread loss. Neither recurring run rate nor a short-term cancellation save proves lifetime value. Report realized retained revenue or contribution over the measured horizon, uncertainty, and any modeled assumptions separately.
