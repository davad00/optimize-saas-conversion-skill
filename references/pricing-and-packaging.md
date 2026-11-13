# Pricing and packaging

Use this playbook when buyers cannot identify the right plan, understand the commitment, predict their bill, or justify the value. Treat changes to positioning, packaging, price, and defaults as separate hypotheses. A higher conversion rate is insufficient if contribution, retention, or customer fit deteriorates.

## Contents

- Establish the economic offer
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

Use a real premium plan or credible alternative as a reference. Anchoring research supplies a mechanism to investigate, not a guaranteed SaaS uplift. [Tversky and Kahneman](https://doi.org/10.1126/science.185.4157.1124) Never invent a reference price or deliberately misleading comparison. A supposedly decoy plan must still be a genuine, usable offer with an explainable customer fit. Prefer helping buyers select a suitable plan to steering everyone toward the highest margin choice.

Use “Recommended for teams with…” when supported by fit. Use “Most popular” only with verified adoption data and a meaningful population/time period. Show prerequisites for enterprise features such as SSO, support commitments, or data residency; do not add badges for capabilities that do not exist.

Treat charm prices, rounded prices, and precise prices as contextual hypotheses. Compare comprehension and brand fit as well as purchases. Do not assert that .99, odd numbers, or a particular price ordering always performs best.

## Present prices and savings accurately

Keep the charged amount, billing period, currency, unit, minimum commitment, and renewal visible together. An annual monthly equivalent is explanatory; it must not appear to be a monthly charge. Retain an understandable monthly option when it exists, and make the selected interval unmistakable.

For a verified monthly price of $24 and annual charge of $228:

- Twelve monthly payments total $288.
- The annual equivalent is $19 per month, billed as $228 per year.
- The saving is $60 per year: `(288 - 228) / 288 × 100 = 20.8333…%`.
- Use an accurate presentation such as “Save $60/year” or “Save about 20.8%.” Do not label it “two months free”; that would be a different offer.

State tax treatment and additional mandatory charges consistently. For seats, show seat count and total; for usage, provide a transparent example or calculator with editable assumptions. Never imply an unbounded “unlimited” entitlement when material limits apply.

For trials, show cost now, evaluation duration, payment-method requirement, post-trial amount, automatic conversion behavior, and cancellation route. Inspect SDK/API versions and current provider documentation before implementing changes. Trial APIs and supported interfaces evolve; do not substitute a generic integration. [Stripe trial documentation](https://docs.stripe.com/billing/subscriptions/trials)

## Design discounts and changes

Specify what each discount buys the business: commitment, a verifiable segment, a genuine launch promotion, or another defined objective. Record eligibility, actual deadline, amount, duration, renewal price, stacking, and refund treatment. A permanent promotion is part of the effective price; do not fabricate an expiring offer around it.

Bundle complementary value when customers need it together. Show what is included and how limits interact. Compare bundle economics against cannibalized standalone revenue and added service costs. Keep paid add-ons explicit and reversible before confirmation.

For a price or packaging change, define affected cohorts, grandfathering duration, migration dates, existing commitments, and communication. Do not silently migrate existing subscribers while changing the public pricing component. Follow authorization already provided and prepare concrete proposals for any unapproved commercial change.

Define upgrade and downgrade timing, entitlement timing, proration, credits, refunds, unpaid invoices, and taxes. Preview the actual provider calculation. Stripe documents that a negative proration does not automatically mean a cash refund and a positive proration need not be billed immediately. [Stripe prorations](https://docs.stripe.com/billing/subscriptions/prorations)

## Implement one billing truth

Use a shared authoritative offer mapping between pricing UI, checkout creation, server validation, confirmation, account billing, and analytics. Reject client-supplied amounts. Preserve selected plan, quantity, interval, and eligible promotion through authentication and return paths.

Verify monthly/annual toggles, mobile comparison, keyboard operation, currency formatting, coupon expiry, unavailable plans, errors, and test-mode invoice totals. Check annual renewal and midcycle changes. A convincing pricing page with a different checkout amount fails the acceptance criteria.

## Evaluate the business result

Define eligible visitors or accounts, assignment, purchase window, and cohort maturity before comparing offers. Use paid conversion alongside net revenue or contribution per eligible unit over a declared horizon. Define deductions and distinguish cash collected, recurring run rate, and recognized revenue; annual prepayment does not prove improved retention.

Inspect plan mix, activation, cancellations, refunds, downgrades, expansion, support, and usage cost. Model plausible outcomes when renewal evidence is unavailable, labeling assumptions. Deliver the exact proposed offer, UI disclosure, implementation changes, economic tradeoffs, validation performed, and measurement plan. Never declare a pricing winner solely because more people clicked a plan.
