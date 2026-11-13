# Pricing audit and acceptance record

Use for every in-scope pricing surface, including pricing cards on a landing page, a full pricing page, an upgrade dialog, and relevant checkout steps. Read [pricing-and-packaging.md](../references/pricing-and-packaging.md) for the decision rules. Inspect the default and all billing states before choosing the final priority list.

This is a coverage record, not a requirement to make every possible change. Complete every applicable row. A small number of headline recommendations must not hide an unchecked default, price unit, savings label, or checkout mismatch.

## Verified offer and context

- Surface, route, device, and evidence inspected:
- Requested scope: audit / implementation / new page.
- Buyer and buying motion:
- Authoritative prices, currency, tax treatment, seats, allowances, reset period, trial, and renewal terms:
- Initial default observed or reported, and source:
- Existing customer / prior selection / deep-link behavior:
- Explicit business or user requirement for billing emphasis, if any:
- Missing facts that affect a display decision or commercial change:

Use `observed`, `user-reported`, `code-inspected`, or `unverified` for behavioral evidence. A screenshot shows a selected interval, but cannot by itself establish a fresh-visitor default or prove that checkout preserves it.

## Billing state matrix

Fill one row per plan and available interval. Add currency, seat-count, or offer variants only when applicable. Check desktop and mobile presentation.

| Plan and state | Primary displayed price and unit | Adjacent real bill and frequency | Savings claim and arithmetic | CTA destination / plan / interval | Evidence or remaining check |
| --- | --- | --- | --- | --- | --- |
| Plan A · monthly | | | | | |
| Plan A · annual | | | | | |
| Plan B · monthly | | | | | |
| Plan B · annual | | | | | |

Expected presentation for comparable recurring plans: annual mode prominently shows `annual charge ÷ 12 / month` with `actual total billed yearly` directly below, while monthly mode shows its actual monthly price. Keep the value unit, limits, and usage reset period correct. The annual bill must remain legible without a tooltip or an extra click.

At checkout and payment confirmation, reverse the emphasis to the actual amount due now and the renewal commitment. The monthly equivalent may support comparison, but must not become the apparent charge in the payment summary.

## Mandatory six-check disposition

Use exactly one baseline status per row: `pass`, `fix`, `investigate`, or `not applicable`. Mark unavailable behavior `investigate — unverified`. Add the reason and exact repair, and distinguish an authorized presentation/functional fix from a proposed commercial change. A `fix` status does not grant permission to change prices or contracts.

| Check | Status | Evidence and consequence | Exact change or reason to retain | Verification |
| --- | --- | --- | --- | --- |
| Fresh-visitor default and annual-offer emphasis | | | | |
| Same comparison unit and annual monthly-equivalent headline | | | | |
| Adjacent, readable actual charge and billing commitment | | | | |
| Correct, noticeable per-plan savings | | | | |
| Clear tier fit, decisive difference, and upgrade value | | | | |
| Selected offer preserved into checkout | | | | |

Default decision: use annual first for a new undecided visitor to a genuinely discounted public self-serve annual offer when presentation work is authorized and no contrary requirement or concrete product evidence applies. Preserve explicit buyer choices and existing-account context. State the reason for any monthly-first exception. Do not treat the existing default as an intentional business policy without evidence.

## Other applicable pricing fundamentals

Record the same statuses for these checks; combine related findings in the final recommendation when useful.

| Check | Status and evidence | Change or justified retention |
| --- | --- | --- |
| Plan title and description identify buyer/job rather than a vague tier label | | |
| Value metric, included amount, reset period, minimum seats, and overage are understandable | | |
| Important tier differences appear near the decision; shared features do not drown them out | | |
| Recommended-plan emphasis has a supported fit; popularity and reference-price claims are verified | | |
| Each plan has a clear CTA with truthful next-step expectations | | |
| Trial/payment requirements, renewal, cancellation, and relevant exclusions answer real objections | | |
| Useful proof is placed near the purchase decision without invented testimonials or guarantees | | |
| Monthly alternative and selected interval remain obvious without relying on color alone | | |
| Mobile cards, comparison, disclosure text, and actions are readable and usable | | |
| Currency, decimal rounding, discount differences, and tax wording agree across the journey | | |
| Pricing, feature descriptions, billing catalog, account UI, and checkout share the same offer facts | | |
| Checkout loading, unavailable offers, authentication returns, and payment errors preserve useful state | | |

Do not add a third plan, discount, fake anchor, urgency message, or `Most popular` badge simply to fill a checklist. An unverified commercial opportunity belongs in proposals with the fact needed to decide it.

## State and purchase verification

Run only applicable checks supported by the available environment. Mark unavailable checks explicitly.

- Fresh undecided visitor receives the intended initial interval without a misleading first-render flip.
- Switching monthly → annual and annual → monthly updates the headline, real bill, saving, selected-state semantics, and CTA together.
- Explicit selection survives appropriate navigation, authentication, and return paths; a validated current link outranks a stale stored preference as designed.
- Existing subscribers retain their contract context unless they explicitly choose a change.
- The annual CTA opens the intended annual offer; the monthly CTA opens the intended monthly offer. Quantities and currencies are consistent.
- Checkout shows the exact billed total; it does not derive the annual amount from a rounded monthly display rate.
- Monthly quotas and their reset period remain correct when annual billing is selected.
- Keyboard interaction and selected-state announcements work; mobile keeps the billed total near the primary price.
- Purchase confirmation and entitlements match the selected offer when test-mode purchase verification is available.

## Final decision and measurement

List the immediate changes, commercial proposals, retained choices with reasons, and unverified behavior. Show exact before/after pricing copy. Do not write only “test annual billing” or “make pricing clearer.”

For default or display changes, measure paid subscriptions per eligible visitor/account and net revenue over a declared window. Inspect annual plan mix, checkout completion, refunds, activation, and cancellation as relevant. Keep cash collected distinct from recurring run rate and future renewal. With limited traffic, validate comprehension and journey reliability first and label before/after outcome evidence appropriately. Neither passing this record nor an attractive annual presentation proves conversion uplift.
