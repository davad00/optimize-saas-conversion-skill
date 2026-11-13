# Sources and evidence boundaries

Research reviewed on 13 November 2026. Reopen current provider and standards documentation before implementation when versions or requirements matter. These references support the specific mechanisms and technical checks described here; they do not certify an uplift for an untested SaaS site.

## How to use the evidence

Label recommendations as observed defect, supported principle, application hypothesis, or site-validated effect. Cite project evidence beside observations. For external claims, cite the source and explain the transfer limit. Avoid borrowing percentages from unrelated products, vendor case studies, or behavioral experiments.

Most tactics in the playbooks are original operating hypotheses. A suggested layout, copy pattern, value metric, or test sequence is not an experimentally established universal law.

## Behavioral research

| Source | What it supports | Boundary |
| --- | --- | --- |
| [Elliot, Color and psychological functioning, 2015](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2015.00368/full) | Context and methodological issues in color research | No universal best CTA hue or SaaS uplift |
| [Scheibehenne, Greifeneder & Todd, choice overload meta-analysis, 2010](https://doi.org/10.1086/651235) | Variation in effects of assortment size | Does not prescribe exactly three plans |
| [Chernev, Böckenholt & Goodman, choice overload meta-analysis, 2015](https://doi.org/10.1016/j.jcps.2014.08.002) | Moderating roles of complexity, goals, difficulty, and uncertainty | Diagnose the decision rather than delete options blindly |
| [Tversky & Kahneman, Judgment under Uncertainty, 1974](https://doi.org/10.1126/science.185.4157.1124) | Anchoring as a judgment mechanism | Not a SaaS price optimization experiment |
| [Original-paper academic-host copy](https://www.columbia.edu/itc/hs/medinfo/g6080/misc/articles/TverksyKahneman1974.pdf) | Accessible copy of the preceding paper | Check document identity; do not infer modern billing guidance |
| [Muchnik, Aral & Taylor, Social influence bias, 2013](https://pubmed.ncbi.nlm.nih.gov/23929980/) | Social influence in an online-ratings experiment | Not evidence for a testimonial conversion percentage |
| [Lynn, Scarcity Effects on Value, 1991](https://ecommons.cornell.edu/entities/publication/167c0da3-fa55-44ad-be11-f258914ee9a3) | Scarcity and perceived value/desirability | Does not validate fake limits or evergreen countdowns |

Use other named effects in the persuasion catalog as hypotheses unless additional relevant evidence has been checked. Do not imply that all catalog entries were directly tested by the sources above.

## Standards and implementation references

| Primary source | Use |
| --- | --- |
| [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Applicable contrast, color, keyboard, focus, target size, reflow, and form criteria |
| [W3C accessible authentication](https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html) | Authentication that does not unnecessarily block assistive mechanisms |
| [W3C form notifications](https://www.w3.org/WAI/tutorials/forms/notifications/) | Discoverable errors, instructions, and feedback |
| [W3C keyboard](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html) | Keyboard task completion |
| [W3C reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html) | Layout under zoom/narrow width and criterion exceptions |
| [MDN reduced motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion) | CSS implementation of motion preference |
| [Google Web Vitals](https://web.dev/articles/vitals) | LCP, INP, CLS definitions, field assessment, and thresholds |
| [Stripe recurring pricing models](https://docs.stripe.com/products-prices/pricing-models) | Mechanics of flat, seat, tiered, and usage models |
| [Stripe trials](https://docs.stripe.com/billing/subscriptions/trials) | Current trial integration and version-specific constraints |
| [Stripe prorations](https://docs.stripe.com/billing/subscriptions/prorations) | Billing changes and provider-calculated proration |
| [Stripe fulfillment](https://docs.stripe.com/checkout/fulfillment.md?ui=full-page) | Verified payment and fulfillment behavior |
| [Stripe webhooks](https://docs.stripe.com/webhooks) | Verification, retries, duplicate events, and ordering considerations |
| [Stripe subscription webhooks](https://docs.stripe.com/billing/subscriptions/webhooks) | Subscription lifecycle and entitlement-related events |
| [Stripe Smart Retries](https://docs.stripe.com/billing/revenue-recovery/smart-retries) | Current failed-payment recovery capabilities |
| [Stripe customer management](https://docs.stripe.com/customer-management) | Supported self-service billing management |
| [Stripe subscription analytics](https://docs.stripe.com/billing/subscriptions/analytics) | Provider-specific metric definitions and configuration |

Stripe is an implementation example, not a required provider. Inspect the actual integration and its current official documentation. A UI copy change is not authorization or evidence for a backend billing migration. Accessibility checks are product requirements and usability evidence; they are not a numeric revenue forecast.

## Experimentation and numerical methods

| Primary source | Use |
| --- | --- |
| [Microsoft, Diagnosing Sample Ratio Mismatch](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/) | Investigate allocation anomalies before trusting effects |
| [Microsoft, Trustworthy Experimentation during the experiment](https://www.microsoft.com/en-us/research/articles/patterns-of-trustworthy-experimentation-during-experiment-stage/) | Distinguish outcome/diagnostic/guardrail metrics and monitor correctly |
| [NIST, comparing two proportions](https://www.itl.nist.gov/div898/handbook/prc/section3/prc33.htm) | Pooled two-proportion testing background |
| [NIST, proportion confidence limits](https://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/propconf.htm) | Wilson interval formula and interval alternatives |
| [Newcombe, independent-proportion interval comparison, 1998](https://pubmed.ncbi.nlm.nih.gov/9595617/) | Difference-of-proportions interval methodology |
| [statsmodels, two-proportion sample-size approximation](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.samplesize_proportions_2indep_onetail.html) | Normal-approximation planning assumptions |
| [statsmodels, independent-proportion confidence intervals](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.confint_proportions_2indep.html) | Method definitions and options |

The bundled utility uses Python's standard library, not a hidden third-party analytics service. Inspect its assumptions and warnings. It does not validate assignment, privacy, cohort maturity, causality, continuous revenue, cluster dependence, or sequential stopping.

## Skill design references supplied by the user

These projects informed the workflow structure. Their existence or visual quality is not evidence of increased purchases. This skill's prose, templates, and calculator are original; no third-party example/media packs, promotional blocks, or runtime dependencies are included.

| Project | Adapted idea | Deliberate boundary |
| --- | --- | --- |
| [Elephant–Goldfish Model](https://github.com/google/elephant-goldfish-model) | Review final artifacts with a fresh context | Its software-specification ceremony is not mandatory for routine CRO; self-review fallback is explicit |
| [Hallmark](https://github.com/nutlope/hallmark) | Inspect the existing design and verify rendered behavior | Brand-specific aesthetic bans are not conversion evidence |
| [MotionSites Web Builder](https://github.com/Motionsites-AI/claude-skill) | Specify copy and interaction precisely; inspect screenshots and fix concrete issues | Cinematic effects, sponsor messages, and media/example collections are not included |
| [Claude SEO](https://github.com/AgricIDaniel/claude-seo) | A concise router with focused references and evidence-linked outputs | SEO acquisition, design scores, and CRO outcomes remain distinct |

The two supplied labels "claude-seo" and "seo-cockpit" point to the same URL, so they are one unique reference here. The MotionSites repository names its skill "motionsites-web-builder."

For skill packaging, see [OpenAI's skill guidance](https://developers.openai.com/plugins/build/skills). Keep the entry point concise, use references only when needed, and reserve scripts for deterministic reusable work.
