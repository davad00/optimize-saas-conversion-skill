# SaaS Conversion Optimizer

A Codex skill for improving SaaS purchases, paid subscriptions, and retained customer value.

Use it to audit an existing website, improve a pricing page, implement a clearer signup or checkout journey, reduce trial friction, and design a useful measurement plan. The workflow connects observed buyer obstacles to concrete changes in copy, design, offers, and code.

**10 focused playbooks · 22 persuasion patterns · 5 reusable templates · Mandatory pricing-state audit · Tested Python calculator**

## What it covers

| Area | Capabilities |
| --- | --- |
| Strategy and research | Buyer needs, acquisition intent, funnel diagnosis, objections, prioritization, and low-traffic research |
| Positioning and copy | Value propositions, headlines, product demonstrations, proof, CTAs, offers, and objection handling |
| Visual design | Color theory, palette relationships, contrast, typography, hierarchy, mobile layouts, motion, and accessibility |
| Persuasion | Anchoring, social proof, authority, reciprocity, risk reversal, progress, ownership, defaults, price framing, and genuine urgency |
| Pricing and packaging | Initial billing defaults, monthly-equivalent annual headlines, real savings, value metrics, tiers, seat/usage/hybrid models, discounts, upgrades, and economic tradeoffs |
| Signup and checkout | Form friction, authentication, plan selection, billing clarity, payment recovery, and verified fulfillment |
| Activation and retention | Trials, freemium, first value, contextual paywalls, renewals, failed-payment recovery, cancellation, and expansion |
| Measurement | Event contracts, cohort maturity, sample sizes, uncertainty, allocation checks, and revenue/retention guardrails |
| Implementation | Existing-stack integration, responsive behavior, targeted verification, and independent review |

The main [SKILL.md](SKILL.md) routes Codex to the relevant playbooks. Detailed material loads only when needed.

## Pricing basics it must check

Every pricing review must inspect the initial billing state and every supported interval, then report a concrete default decision and a price-state matrix. A short priority list cannot omit these checks.

- **Starting selection:** use annual-first as a practical starting hypothesis for a suitable, genuinely discounted self-serve offer and a new undecided visitor. Respect explicit instructions, buyer choices, valid offer links, existing accounts, experiment assignment, and evidence favoring monthly.
- **Comparable headline prices:** show the monthly equivalent prominently in annual mode, with the exact annual charge and `billed yearly` directly underneath. Keep the comparison unit consistent across the toggle.
- **Real savings and tier value:** calculate each plan's actual discount, explain meaningful upgrade benefits, and use supported plan-fit recommendations.
- **Purchase continuity:** preserve the selected plan and interval through signup and checkout. At payment, give the actual amount due now clear prominence.
- **Visual and behavioral verification:** check both switch directions, readable mobile terms, selected-state semantics, and relevant return paths. Mark unavailable checks explicitly.

For example, a verified **$12/month** plan with a **$115.20/year** option should show **$9.60/month** as its primary annual-mode comparison, with **$115.20 billed yearly** immediately below. Its annual saving is **$28.80, or 20%**. The skill treats this as a concrete presentation improvement; conversion uplift still needs outcome evidence.

The same coverage approach applies across landing pages, proof and objections, signup, checkout, activation, visual hierarchy, and measurement. See the [pricing audit template](assets/pricing-audit.md) and [independent review checklist](assets/review-checklist.md).

## Install in Codex

### Ask Codex to install it

Use the built-in skill installer:

```text
Use $skill-installer to install the skill at the root of
https://github.com/davad00/optimize-saas-conversion-skill
with the name optimize-saas-conversion.
```

### Manual installation for local Codex

Clone this repository into your user skill directory:

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/davad00/optimize-saas-conversion-skill.git \
  ~/.agents/skills/optimize-saas-conversion
```

Keep the complete folder, including references, assets, and scripts. If you already have a skill with this name, update that installation instead of creating a duplicate.

Codex's documented user skill location is `~/.agents/skills`; project skills can be placed in `.agents/skills` within a repository. See [OpenAI's skill documentation](https://learn.chatgpt.com/docs/build-skills) for current discovery and configuration details.

Invoke the skill with `$optimize-saas-conversion`, or choose it from the skill picker.

## How to use it

For a complete improvement pass in an existing project:
```
Use $optimize-saas-conversion on this SaaS website.

Inspect the landing page, pricing, signup, checkout, and onboarding.
Identify the biggest obstacles to paid subscriptions, implement the
most promising improvements, verify the affected journeys, and give
me a measurement plan.

Preserve our existing brand and use verified product and pricing facts.
```

For pricing specifically:
```
Use $optimize-saas-conversion to improve our pricing page.

Review the value metric, plan structure, feature comparison, annual
offer, price framing, and upgrade paths. Implement the presentation
improvements and clearly identify any proposed commercial changes.
```

For an early SaaS with limited traffic:
```
Use $optimize-saas-conversion to improve paid conversion with low traffic.

Prioritize clear defects, offer comprehension, customer objections,
and time to first value. Implement the useful changes and recommend
a realistic way to learn whether they help.
```

## Workflow

1. Establish the buyer, offer, conversion outcome, and verified product facts.
2. Inspect the relevant journey and complete the applicable baseline checks, including every pricing state.
3. Record each check's result, then prioritize a small, coherent set of improvements.
4. Write exact copy and behavior, then implement within the requested scope.
5. Verify the affected experience and report any unavailable checks.
6. Define how to measure business outcomes and distinguish hypotheses from demonstrated effects.

The skill preserves the existing stack and design system. It treats purchases, revenue, activation, and retention as distinct measures. It does not promise a conversion uplift before suitable outcome data exists.

## Package contents

| Path | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Main instructions and playbook routing |
| [agents/openai.yaml](agents/openai.yaml) | Skill display and invocation metadata |
| [references/](references/) | Ten focused playbooks and source register |
| [assets/conversion-brief.md](assets/conversion-brief.md) | Business, buyer, offer, and intervention brief |
| [assets/experiment-brief.md](assets/experiment-brief.md) | Experiment design and decision record |
| [assets/event-contract.json](assets/event-contract.json) | Adaptable analytics event definitions |
| [assets/review-checklist.md](assets/review-checklist.md) | Independent or self-review checklist |
| [assets/pricing-audit.md](assets/pricing-audit.md) | Required billing-state matrix, default decision, savings, tier value, and checkout verification |
| [scripts/cro_math.py](scripts/cro_math.py) | Sample-size, conversion, pricing, and contrast calculations |
| [scripts/test_cro_math.py](scripts/test_cro_math.py) | Calculator tests |

## Calculator

The utility uses Python's standard library and makes no network requests.

```bash
python3 scripts/cro_math.py --help

python3 scripts/cro_math.py plan-ab \
  --baseline 0.05 --relative-mde 0.20 --eligible-users-per-day 1000

python3 scripts/cro_math.py compare-ab \
  --control-users 10000 --control-conversions 500 \
  --variant-users 10000 --variant-conversions 600

python3 scripts/cro_math.py pricing \
  --monthly-price 24 --annual-price 228 --currency USD

python3 scripts/cro_math.py contrast '#ffffff' '#2563eb'
```

Read the assumptions and warnings in each JSON result. The statistical commands assume independent binary outcomes and do not validate experiment assignment, stopping rules, cohort maturity, revenue distributions, or causality. A contrast result is not a complete accessibility audit.

The pricing command includes `suggested_presentation.monthly` and `.annual` with separate primary comparison prices and actual billed amounts. It marks rounded equivalents, retains exact charges, and avoids savings labels for equal-price or more-expensive annual offers. It does not choose a billing default or change the commercial offer.

Run the calculator tests:

```bash
python3 -B -m unittest discover -s scripts -p test_cro_math.py -v
```

## Evidence and inspirations

The playbooks distinguish observed defects, research-supported principles, application hypotheses, and effects validated on the actual site. Persuasion uses accurate product claims, genuine proof, understandable billing, and real offer conditions.

Workflow inspiration includes [Elephant–Goldfish Model](https://github.com/google/elephant-goldfish-model), [Hallmark](https://github.com/nutlope/hallmark), [MotionSites Web Builder](https://github.com/Motionsites-AI/claude-skill), and [Claude SEO](https://github.com/AgricIDaniel/claude-seo).

See [references/sources.md](references/sources.md) for research, official technical documentation, and the boundaries of those adaptations. The skill's instructions, templates, and calculator are original; third-party media packs and promotional content are not included.
