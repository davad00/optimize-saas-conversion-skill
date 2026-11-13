# Pricing and packaging

Use this playbook whenever pricing, plans, subscriptions, billing intervals, a paywall, or checkout are in scope. Run the concrete presentation checks even when no analytics are available: a generic discussion of packaging does not complete a pricing audit. Treat changes to positioning, packaging, price, and defaults as separate hypotheses. A higher conversion rate is insufficient if contribution, retention, or customer fit deteriorates.

## Contents

- Establish the economic offer
- Run the mandatory pricing pass
- Choose the initial billing interval deliberately
- Keep monthly and annual prices comparable
- Choose a value metric and buying motion
- Build understandable plans
- Present prices and savings accurately
- Design discounts and changes
- Implement one billing truth
- Evaluate the business result

## Establish the economic offer

Inspect the actual product catalog, prices, entitlements, billing configuration, and current customer contracts. Record currency, tax presentation, payment timing, minimum seats, included usage, overages, renewal, cancellation, refund terms, trial conditions, and existing discounts. Separate verified facts from proposals.

Identify who buys, who uses, who approves the budget, which outcome matters, and the alternative being replaced. Review objections and purchase behavior by segment. Do not infer willingness to pay from demographic stereotypes or a competitor's price alone. Customer interviews, comprehension sessions, observed purchasing, and appropriately designed offer experiments answer different questions; label their limitations.

Keep product economics visible: variable infrastructure or AI inference costs, payment fees, support, onboarding, refunds, and sales effort. A cheap acquisition offer can create expensive customers. Do not lower prices merely to improve the percentage of visitors who purchase.

## Run the mandatory pricing pass

Complete [the pricing audit](../assets/pricing-audit.md) before ranking optional improvements. Inspect the first load and every available billing interval, with at least one real plan selected through the next step. When code or a runnable site is available, inspect initialization as well as clicking the toggle. With screenshots, identify visible presentation issues and mark unobservable behavior as unverified; an explicitly reported default is user-provided evidence.

Six checks must appear in the result with an explicit disposition, even if the final narrative focuses on only three priorities:

1. **Initial interval:** what a new undecided visitor sees, why, and whether an annual offer should lead.
2. **Comparable headline:** whether monthly and annual modes use the same comparison unit, usually price per month for these recurring offers.
3. **Actual commitment:** whether the real annual charge and billing frequency remain adjacent and legible.
4. **Savings:** whether each plan's discount is correct and easy to notice at the decision point.
5. **Plan choice:** whether the useful difference, intended buyer, and upgrade value are clear.
6. **Purchase continuity:** whether the selected plan, interval, quantity, and charge reach checkout unchanged.

Use the baseline statuses `pass`, `fix`, `investigate`, or `not applicable`, with evidence and the exact action. Mark unavailable behavior as `investigate — unverified`. Separately label the action as an authorized presentation/functional change, a commercial proposal, or justified retention. Do not omit a baseline issue because another recommendation seems more strategic. Do not call a screenshot-only review a behavioral verification.

## Choose the initial billing interval deliberately

For a public self-serve offer with a genuine annual saving, **start with annual selected for new, undecided visitors** when the task authorizes conversion-oriented presentation changes and no contrary product evidence or explicit requirement applies. Make the saving visible and retain the monthly choice. This is an actionable starting hypothesis about emphasis, commitment, and cash collection; it is not a promise that paid conversion or retention will rise.

An existing monthly default is something to inspect, not a reason to preserve it automatically. If the user asks to promote the annual offer, implement that initial presentation within scope. Do not defer a reversible, authorized display change merely because it could eventually be A/B tested. If the task is audit-only, recommend the precise default change and explain the mechanism.

Apply these exceptions deliberately:

- Honor an explicit product requirement or credible experiment result favoring monthly. Explain the reason for retaining it.
- Preserve the buyer's explicit interval selection. A fresh valid plan/interval link should outrank a stale saved preference; subsequent manual changes should win for the current journey. Define and verify the application's precedence instead of letting random component initialization decide it.
- In an existing customer's billing or upgrade flow, use their contract and explicit selection as the context. Do not reset them to annual because the public acquisition page uses annual first.
- Do not default to annual merely because a toggle exists when there is no meaningful annual benefit, the offer is still unverified, cash constraints or a short-lived job make commitment a poor fit, or a campaign promises a particular monthly offer. Record the concrete reason and choose a suitable starting state.
- A display default must not itself start a subscription, change an existing contract, add a charge, or silently commit a buyer. The selected term and amount must be carried into an explicit purchase decision.

Inspect fresh load, reload, back navigation, authentication return, and a direct plan link. Ensure server rendering and hydration do not briefly show monthly and then flip to annual. The toggle label, price, disclosure, CTA payload, and analytics must agree from the first stable render.

## Keep monthly and annual prices comparable

For a flat recurring offer sold with monthly and yearly options, **make the annual monthly equivalent the primary price in annual mode**. Keep the comparison unit stable across the toggle: `$12 / month` becomes `$9.60 / month`, not a headline of `$115.20 / year`. Place the actual annual bill directly below it in readable text: `$115.20 billed yearly, before tax`. State tax treatment only when verified. The headline communicates the comparable rate; the adjacent line communicates the real payment schedule.

Do not bury the lower monthly equivalent in a footnote while promoting the larger annual total. Do not make the annual commitment a tooltip, fine print, or text that disappears on mobile. Conversion hierarchy and clear billing disclosure should work together.

This hierarchy is for offer comparison on pricing surfaces. **At checkout and payment confirmation, make the actual amount due now, payment interval, and renewal commitment prominent.** A monthly equivalent can remain a supporting comparison, but must not displace the real annual payment in the purchase summary.

### Worked presentation with verified prices

These generic example plans have a 20% annual saving:

| State | Plan A primary price | Plan A adjacent billing line | Plan B primary price | Plan B adjacent billing line |
| --- | --- | --- | --- | --- |
| Monthly | **$12 / month** | $12 billed monthly, before tax | **$24 / month** | $24 billed monthly, before tax |
| Annual | **$9.60 / month** | $115.20 billed yearly, before tax | **$19.20 / month** | $230.40 billed yearly, before tax |

For a new eligible visitor under the annual-first rule, start in the second row. Show `Yearly · Save 20%` at the interval control. Optional plan-specific support is `Save $28.80/year` for Plan A and `Save $57.60/year` for Plan B. Use a badge such as `Best annual value` only when the comparison supports it; do not turn a recommendation into an unsupported `Most popular` claim.

Calculate from authoritative values:

- `annual monthly equivalent = annual charge / 12`
- `annual savings amount = 12 × monthly charge − annual charge`
- `annual savings fraction = annual savings amount / (12 × monthly charge)`

Use decimal money arithmetic and the currency's display precision. If dividing the annual charge produces a rounded rate, label it as an average/equivalent when needed and keep the exact billed total authoritative. Never recompute the annual checkout charge by multiplying a rounded displayed monthly equivalent. If savings differ by plan, show plan-specific badges; a universal `Save 20%` is wrong when only one tier qualifies. If an annual price is not discounted, do not invent savings or use the discounted-annual default rule.

Use `scripts/cro_math.py pricing` from the skill directory to check the arithmetic. Its `suggested_presentation.monthly` and `.annual` fields separate the primary comparison amount from the actual billed amount and frequency. Apply verified currency precision, tax treatment, value-unit labels, and product context; the calculator does not decide which interval should be selected initially.

Retain the correct value metric: `/user/month` for per-seat pricing, minimum seats and total commitment when relevant, and clear included usage. Annual billing does not automatically make a monthly quota annual, multiply allowances by twelve, or change when usage resets. For one-time, usage-only, or contract pricing, use the genuinely meaningful comparison unit rather than forcing a monthly equivalent onto an unsuitable product.

## Choose a value metric and buying motion

Prefer a unit that buyers understand, can forecast, and associate with received value. Test the billing explanation with realistic workloads, including growth and occasional spikes.

| Model | Consider when | Inspect before recommending |
| --- | --- | --- |
| Flat rate | The service and costs are reasonably bounded | Heavy-user cost, limits, and small-customer fit |
| Per seat | Value and adoption scale with participating people | Whether paid seats discourage collaboration; guests and inactive users |
| Usage | Value or costs track a measurable activity | Predictability, metering accuracy, limits, alerts, and bill shock |
| Base fee plus usage | Access has value and consumption varies | Included allowance, overage calculation, unused credits |
| Outcome or custom contract | A measurable outcome or complex deployment justifies negotiation | Attribution, disputed outcomes, procurement, and delivery cost |

Stripe supports flat, per-seat, tiered, and usage models; volume and graduated tiers have different arithmetic. Inspect the chosen provider's implementation rather than using these labels interchangeably. [Stripe pricing models](https://docs.stripe.com/products-prices/pricing-models)

Match acquisition to evaluation needs. A trial suits an experience whose value can be demonstrated within an honest evaluation period. Freemium needs a useful ongoing free use case and sustainable service cost. Sales assistance can help when security review, integration, procurement, or contract scope dominates the decision. A hybrid may offer a product experience alongside assistance. These are design hypotheses, not universal rankings of conversion performance.

## Build understandable plans

Group offers by meaningful jobs, capacity, workflow, or service needs. A good/better/best ladder is one option; do not require exactly three plans. Choice research shows that complexity, decision difficulty, and uncertainty affect overload, so reducing card count alone does not establish an improvement. [Choice overload review](https://doi.org/10.1016/j.jcps.2014.08.002)

For each plan, state who it fits, the valuable capability unlocked, the important limit, the charge, and the next action. Order comparison rows by decisions buyers actually make. Keep shared essentials concise and disclose secondary details progressively without hiding exclusions. On mobile, retain plan context while comparing features.

Apply the basic presentation improvements before inventing new packaging:

- Replace vague tier descriptions with the supported buyer or job: for example, occasional individual use versus a higher-volume workflow. Do not create new entitlements to justify the copy.
- Make the decisive difference visible near the price and CTA. If a tier provides three times the included usage for twice the price, explain that exact relationship when verified; retain the actual quota and reset period.
- Give each plan a clear action. Where it helps comprehension, use interval-aware support such as `Billed yearly` near `Choose Pro`; avoid a CTA that appears to start a free trial when it actually opens a paid checkout.
- Use one justified recommended plan to help uncertain buyers when there is a known priority segment. Visual emphasis should follow the explanation of fit. Keep the lower tier and monthly option easy to find.
- Put the most relevant proof and objection answers near the purchase decision: evaluation conditions, cancellation, limits, security, support, migration, or compatibility only as the product can substantiate them.
- Check that primary actions remain easy to find on mobile, plan comparison does not require remembering off-screen prices, and small legal/usage text does not become the only explanation of the real offer.

Changing a label, hierarchy, initial display state, or existing verified savings presentation is different from changing a price, limit, discount, guarantee, trial, or contract. Implement authorized presentation work; separately identify proposed commercial changes with their economics and migration implications.

Use a real premium plan or credible alternative as a reference. Anchoring research supplies a mechanism to investigate, not a guaranteed SaaS uplift. [Tversky and Kahneman](https://doi.org/10.1126/science.185.4157.1124) Never invent a reference price or deliberately misleading comparison. A supposedly decoy plan must still be a genuine, usable offer with an explainable customer fit. Prefer helping buyers select a suitable plan to steering everyone toward the highest margin choice.

Use “Recommended for teams with…” when supported by fit. Use “Most popular” only with verified adoption data and a meaningful population/time period. Show prerequisites for enterprise features such as SSO, support commitments, or data residency; do not add badges for capabilities that do not exist.

Treat charm prices, rounded prices, and precise prices as contextual hypotheses. Compare comprehension and brand fit as well as purchases. Do not assert that .99, odd numbers, or a particular price ordering always performs best.

## Present prices and savings accurately

Keep the comparison price and actual commitment visible together: primary monthly-equivalent rate, adjacent billed total and frequency, currency, value unit, and any minimum commitment. For an annual offer, the prominent `/month` rate must have an equally understandable `billed yearly` explanation beside or directly below it; it must not imply monthly installments. Retain an understandable monthly option when it exists, and make the selected interval unmistakable. Show verified renewal terms near the purchase decision.

For a verified monthly price of $24 and annual charge of $228:

- Twelve monthly payments total $288.
- The annual equivalent is $19 per month, billed as $228 per year.
- The saving is $60 per year: `(288 - 228) / 288 × 100 = 20.8333…%`.
- Use an accurate presentation such as “Save $60/year” or “Save about 20.8%.” Do not label it “two months free”; that would be a different offer.

The primary annual-state price in this example is `$19 / month`, supported by `$228 billed yearly`. Do not replace it with `$228 / year` while demoting the monthly comparison to secondary copy.

State tax treatment and additional mandatory charges consistently. For seats, show seat count and total; for usage, provide a transparent example or calculator with editable assumptions. Never imply an unbounded “unlimited” entitlement when material limits apply.

For trials, show cost now, evaluation duration, payment-method requirement, post-trial amount, automatic conversion behavior, and cancellation route. Inspect SDK/API versions and current provider documentation before implementing changes. Trial APIs and supported interfaces evolve; do not substitute a generic integration. [Stripe trial documentation](https://docs.stripe.com/billing/subscriptions/trials)

## Design discounts and changes

Specify what each discount buys the business: commitment, a verifiable segment, a genuine launch promotion, or another defined objective. Record eligibility, actual deadline, amount, duration, renewal price, stacking, and refund treatment. A permanent promotion is part of the effective price; do not fabricate an expiring offer around it.

Bundle complementary value when customers need it together. Show what is included and how limits interact. Compare bundle economics against cannibalized standalone revenue and added service costs. Keep paid add-ons explicit and reversible before confirmation.

For a price or packaging change, define affected cohorts, grandfathering duration, migration dates, existing commitments, and communication. Do not silently migrate existing subscribers while changing the public pricing component. Follow authorization already provided and prepare concrete proposals for any unapproved commercial change.

Define upgrade and downgrade timing, entitlement timing, proration, credits, refunds, unpaid invoices, and taxes. Preview the actual provider calculation. Stripe documents that a negative proration does not automatically mean a cash refund and a positive proration need not be billed immediately. [Stripe prorations](https://docs.stripe.com/billing/subscriptions/prorations)

## Implement one billing truth

Use a shared authoritative offer mapping between pricing UI, checkout creation, server validation, confirmation, account billing, and analytics. Reject client-supplied amounts. Preserve selected plan, quantity, interval, and eligible promotion through authentication and return paths.

Verify both toggle directions and the initial state. The selected interval must be recognizable without color alone, accessible by keyboard, and exposed through the appropriate checked/selected semantics. Confirm that displayed price, saving, bill, period label, CTA payload, and analytics update together. Verify mobile comparison, currency formatting, coupon expiry, unavailable plans, errors, and test-mode invoice totals. Check annual renewal and midcycle changes. A convincing pricing page with a different checkout amount fails the acceptance criteria.

## Evaluate the business result

Define eligible visitors or accounts, assignment, purchase window, and cohort maturity before comparing offers. Use paid conversion alongside net revenue or contribution per eligible unit over a declared horizon. Define deductions and distinguish cash collected, recurring run rate, and recognized revenue; annual prepayment does not prove improved retention.

Inspect plan mix, activation, cancellations, refunds, downgrades, expansion, support, and usage cost. Model plausible outcomes when renewal evidence is unavailable, labeling assumptions. Deliver the exact proposed offer, UI disclosure, implementation changes, economic tradeoffs, validation performed, and measurement plan. Never declare a pricing winner solely because more people clicked a plan.
