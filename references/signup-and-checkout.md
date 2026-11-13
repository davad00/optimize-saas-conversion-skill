# Signup and checkout

Use this playbook when visitors choose an offer but struggle to create an account, complete payment, or receive access. Diagnose the failing step before changing the entire journey. Treat the implementation practices below as reliability and usability requirements; their conversion effect still needs measurement.

## 1. Collect what the next step needs

Inspect every required field and identify its immediate purpose: account access, fraud prevention, legal requirement, billing, or delivery of first value. Defer enrichment questions, team invitations, and optional profile details until they help the customer. Do not remove information necessary to provide the service merely to shorten a form. Evaluate progressive collection against completion and activation, since shifting effort can move abandonment downstream.

Use visible labels, appropriate input types and autocomplete tokens, and clear required/optional wording. Preserve valid entries after validation failures. Explain the correction next to the field, connect the message programmatically, and provide an accessible error summary for multiple failures. Announce asynchronous results without repeatedly interrupting typing. [W3C form notifications](https://www.w3.org/WAI/tutorials/forms/notifications/)

Keep password-manager autofill and paste available for passwords and verification codes. Offer recovery paths for forgotten passwords, expired links, existing accounts, and unavailable identity providers. Reuse the project's authentication integration; do not weaken account verification or abuse controls to remove a click. W3C identifies password managers and paste as mechanisms that reduce authentication's cognitive burden. [Accessible authentication](https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html)

## 2. Carry the purchase context through authentication

Document which values must survive signup, login, email verification, provider redirects, browser Back, and checkout cancellation: plan, billing interval, quantity, currency, eligible discount, and intended destination. Keep trusted offer configuration on the server. Treat browser parameters as selections to validate, never authority for price or entitlement.

Use the established session or signed state mechanism. Allowlist return destinations and bind checkout to the correct authenticated account or workspace. Restore a summary after a long interruption and resolve stale or unavailable offers explicitly. Check logged-in and logged-out paths; prevent an existing subscriber from unintentionally buying a second subscription.

Make the CTA describe the next action. “Start trial” must lead to the disclosed trial; “Subscribe” must not silently lead to a sales-contact form. If a prerequisite is necessary, explain it at that step.

## 3. Make the amount and commitment understandable

Keep the selected offer visible before commitment:

| Item | What the buyer needs to understand |
| --- | --- |
| Due now | Currency, quantity, billable total, applicable tax or when it is calculated |
| Recurrence | Billing interval, renewal amount or pricing basis, and renewal timing |
| Trial | Duration, payment-method requirement, charge trigger, and post-trial price |
| Annual plan | Full annual charge beside any monthly equivalent |
| Discount | Eligibility, duration, and price after expiry |
| Plan change | Effective date, immediate charge or credit, and next renewal |
| Usage pricing | Included allowance, metering unit, overage rate, and applicable limits |

Use existing verified billing data. Do not silently introduce prices, guarantees, refundable terms, or cancellation promises while editing copy. For usage-based totals that cannot be known in advance, expose the calculation and any estimate's assumptions. Use the payment provider's preview for prorations instead of reproducing billing arithmetic in presentation code; Stripe supports previewing prorations before applying changes. [Stripe prorations](https://docs.stripe.com/billing/subscriptions/prorations)

## 4. Connect payment to reliable access

Prefer the existing tested checkout integration. Verify server-side price mappings, account ownership, currency, quantity, discount eligibility, and test/live separation. Keep payment secrets and sensitive card data out of client bundles, logs, and analytics.

Payment completion and access provisioning need server verification. A thank-you page, client event, query parameter, or redirect alone must never grant paid access or record a purchase. Stripe requires webhook-backed fulfillment because customers may never reach the return page and some payments complete asynchronously. A return page may call the same idempotent server verification function for faster feedback. [Stripe fulfillment](https://docs.stripe.com/checkout/fulfillment.md?ui=full-page)

For Stripe webhook work, verify signatures against the unmodified request body using the official SDK. Persist receipt or enqueue durably before acknowledging success; keep slow work outside the request. Handle retries and duplicate events with stored event IDs and idempotent business operations. Do not assume delivery order or use a timestamp alone as a sequencing rule. Retrieve current provider objects when necessary and prevent stale processing from overwriting newer state. [Stripe webhooks](https://docs.stripe.com/webhooks)

Map provider subscription and entitlement states to the product's explicit access policy. A created subscription can be incomplete; a trial may legitimately have access without a payment. Handle renewal failure, cancellation timing, and entitlement changes instead of assuming checkout completion establishes permanent access. [Subscription webhooks](https://docs.stripe.com/billing/subscriptions/webhooks)

## 5. Design recovery and verify the full path

Provide distinct loading, authentication-required, payment-pending, failed, expired, cancelled, and confirmed states. “Processing” must not look like a decline or invite a duplicate charge. Show a safe retry or status-refresh action and a support route when reconciliation is delayed. Emit the defined purchase event once from verified transaction state; keep trial starts, renewals, refunds, and access activation separately identifiable.

Collect only data needed for the stated purpose, keep marketing choices explicit, and respect the project's consent settings. Avoid personal details in URLs and event properties. Do not record payment fields in session replay.

Test relevant paths in the provider's test environment: successful payment, decline, additional authentication, delayed payment, webhook replay, interrupted return, wrong-account access, cancellation, and plan changes. On mobile, inspect keyboard obstruction, autofill, long errors, price wrapping, focus order, and returning from an external provider. Verify the backend result and entitlement, not only the screenshot. Report unavailable checks, remaining defects, and a measurement plan; passing these checks establishes working behavior, not proven conversion uplift.
