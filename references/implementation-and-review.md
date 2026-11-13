# Implementation and review

Use this playbook when changing a site, preparing an implementation specification, or reviewing a completed conversion journey. Produce a usable change at the requested scope, with verification proportional to the actual risk.

## 1. Establish the project and scope

Read applicable `AGENTS.md` files, project instructions, package scripts, routes, components, design tokens, analytics adapters, and relevant tests. Inspect the current worktree before editing so unrelated changes remain intact. Follow the installed framework and dependency versions; consult current official documentation when an unfamiliar API matters.

Distinguish an audit from implementation. An audit produces grounded findings and concrete proposed changes. An implementation request authorizes completing reversible local work and its verification. Continue using authorization already given; do not introduce a new approval checkpoint for each file, copy choice, or screenshot. Live billing changes, publication, experiment launch, and customer communication must remain within the user's actual scope.

With only screenshots, state what can be assessed visually. With a live URL, inspect the accessible journey without pretending to have source access. With code, trace the flow through the relevant backend where available. Work usefully with partial access and name the specific missing evidence.

## 2. Define the change before editing

Write a short implementation contract: buyer task, observed obstacle, proposed mechanism, components/routes affected, verified offer facts, event changes, acceptance checks, and rollback approach. Keep this proportional; a CTA clarification needs a few lines, not a design ceremony.

Preserve established brand tokens, typography, component behavior, and content facts. Introduce new styles only to solve the identified problem. Reuse the canonical plan catalog and shared price formatter. Do not make a static pricing card disagree with checkout or replace a functioning integration with a decorative mockup.

Map every important CTA to its real destination and expected next state. Specify what happens for new visitors, authenticated customers, existing subscribers, and people returning from an interrupted flow. Document the meaning of “selected,” “current,” “recommended,” “unavailable,” and “pending.” A highlighted plan must not silently change the purchase selection.

For any pricing work, complete `assets/pricing-audit.md` from the skill root. Specify the initial billing default, selection precedence, each plan's monthly and annual display, actual bill, savings, and checkout payload before editing. Use the monthly equivalent as the annual-mode primary price for comparable plans, with the annual charge directly below. Treat an annual-first new-visitor default as a presentation hypothesis under the pricing playbook, not a change to billing terms.

## 3. Implement coherent states

Keep plan, interval, currency, quantity, and experiment assignment consistent across server rendering, hydration, navigation, authentication, and checkout. Prevent a flash of the wrong price or variant. Prefer the project's stable assignment mechanism; do not randomize a visitor independently on every render. Count exposure when the eligible variant is actually presented according to the experiment contract.

Keep display unit separate from charge interval: an annual plan may display a per-month equivalent while still sending the verified annual price identifier to checkout. Derive both views from the same catalog. Never construct an annual checkout amount by multiplying a rounded monthly-equivalent label. Apply the default only when no higher-priority explicit selection, valid intended link, account context, or experiment assignment applies; do not reset a monthly choice during hydration or navigation.

Keep essential offer content and navigation readable while enhancement loads. Use real links for navigation and real buttons for actions. If the checkout provider requires JavaScript, display a useful explanation or recovery path when it cannot initialize; never show a false success state. Reserve space for asynchronous content so a purchase target does not jump while someone clicks.

Reuse state and error components, preserve user input, and make retries safe. Ensure the displayed success agrees with the server outcome. For billing-sensitive behavior, follow `signup-and-checkout.md` and the provider's current integration documentation.

## 4. Verify accessibility and rendering

Operate the changed journey using the keyboard: navigation, plan selectors, interval switches, form submission, errors, dialogs, and recovery. Verify visible focus, sensible order, focus restoration, and freedom from keyboard traps. WCAG requires keyboard operability except for functions that inherently depend on a movement path. [Keyboard guidance](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html)

Inspect reflow at narrow widths and zoom, including long translated text, large prices, comparison tables, and sticky controls. Essential information must remain available without two-dimensional scrolling except where the content genuinely requires it. W3C's horizontal-language reflow criterion uses a width equivalent to 320 CSS pixels. [Reflow guidance](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)

Check labels, accessible names, error announcements, semantic headings, and contrast in default, focus, hover, disabled, and selected states. Do not communicate plan status or errors through color alone. Respect `prefers-reduced-motion`; remove nonessential movement while preserving understandable state feedback. [Reduced-motion media feature](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion)

When browser tools are available, capture the baseline and result at comparable desktop and mobile viewports, then actually inspect them. Exercise the interaction as well as its appearance. Screenshots do not establish payment correctness or complete accessibility. If browser access is unavailable, perform available code checks and say rendering remains unverified; never manufacture screenshots or claim visual inspection.

## 5. Check performance and behavior proportionately

Use existing lint, type, build, and targeted integration checks that cover the changed paths. Add tests for meaningful behavioral risks: wrong plan submitted, duplicate purchase handling, inaccessible selection, or lost return state. Do not create brittle tests that merely repeat the implementation or broaden testing without a concrete unresolved risk.

For pricing changes, verify fresh state, monthly → annual → monthly, explicit selection through navigation/authentication, and the CTA payload for every affected plan. Check the initial server render and hydrated state when relevant. Inspect both the prominence of the price and readability of the billed total at mobile and desktop sizes. A string-presence assertion alone cannot validate either hierarchy or legibility. When browser execution is unavailable, verify code/arithmetic and label rendered hierarchy, persistence, and payment behavior unverified as appropriate.

Compare relevant loading, responsiveness, and layout stability evidence. Separate controlled lab diagnostics from real-user field data; a Lighthouse result alone is not a field measurement or conversion result. Current Core Web Vitals guidance uses LCP, INP, and CLS, evaluated at the 75th percentile with mobile and desktop segmentation. Check current guidance when applying thresholds. [Web Vitals](https://web.dev/articles/vitals)

Inspect introduced media, scripts, fonts, and third-party widgets. Keep an animation or analytics addition only when it serves the buyer task or measurement plan at an acceptable cost. Verify event payloads and deduplication without exposing personal data.

## 6. Review and deliver

For broad or consequential changes, use an independent reviewer with fresh context when available. Supply the artifact or running page, buyer task, verified offer facts, and acceptance criteria. Withhold the author's preferred diagnosis and claimed winning variant. Ask for observable failures, unsupported claims, journey breaks, and measurement weaknesses, each with a location and reproducible evidence.

Adjudicate findings against the actual task. Fix relevant defects; do not chase arbitrary aesthetic scores or force repeated review rounds after the change is adequately verified. If independent review is unavailable, perform and label a self-review. Keep useful work moving.

Require the baseline coverage record and pricing state matrix, where applicable, during review. The highest-priority shortlist does not excuse an unchecked billing default, inconsistent comparison unit, unsupported savings label, or lost selection. Resolve each required check as pass, fix, investigate, or not applicable with evidence.

Deliver the changes, rationale, checks performed, material limitations, and the next measurement decision. Include before/after evidence when captured and distinguish local readiness from deployment status. State the expected conversion mechanism as a hypothesis. Functional correctness, accessible controls, better screenshots, and reviewer agreement do not establish a causal sales increase; that conclusion requires suitable outcome data.
