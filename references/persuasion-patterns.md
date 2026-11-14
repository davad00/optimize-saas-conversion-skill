# Persuasion and buyer decision-making

Use this library of **66 persuasion patterns**: the **22 original foundation mechanisms plus 44 additional applied patterns**. The additional entries solve distinct decision problems; they are not renamed claims that 66 independent psychological laws guarantee purchases. Select a pattern because it addresses an observed buyer obstacle.

## Contents

- [Select and retrieve patterns](#select-and-retrieve-patterns)
- [Apply an evidence ladder](#apply-an-evidence-ladder)
- [Complete pattern index](#complete-pattern-index)
- [Handle popular "tricks" precisely](#handle-popular-tricks-precisely)
- [Truth and implementation checks](#truth-and-implementation-checks)

## Select and retrieve patterns

Use [persuasion-catalog.jsonl](persuasion-catalog.jsonl) for each pattern's trigger, exact application, illustrative example, proposed mechanism, implementation check, measure, evidence class, and related tactic IDs. Use [persuasion-evidence.md](persuasion-evidence.md) to resolve its source IDs. Examples are illustrative or contain placeholders; replace them with verified product facts before publishing.

Choose one primary obstacle: incomprehension, comparison effort, insufficient evidence, uncertain value, adoption risk, inability to act, group coordination, or unclear recurring value. Scan the matching family, inspect plausible records, and select the smallest coherent set. Combine with concrete interventions from [tactic-library.md](tactic-library.md); the 360 tactics and 66 persuasion patterns serve different purposes and are not additive counts of independent effects.

```bash
python3 <skill-dir>/scripts/resource_finder.py list --kind pattern --category comparison
python3 <skill-dir>/scripts/resource_finder.py search 'uncertain usage bill' --kind pattern
python3 <skill-dir>/scripts/resource_finder.py show PAT-024 PAT-043
```

Search uses literal terms; inspect the family index when a query misses the relevant wording. If the helper is unavailable, find an exact record with `rg '"id": "PAT-043"' <skill-dir>/references/persuasion-catalog.jsonl`. Do not load every record for a narrow task.

Use patterns to specify the implementation, not decorate a report with bias names. For example, choose PAT-043 when variable usage makes the bill hard to anticipate; it calls for defensible usage scenarios using the actual rate schedule. Choose PAT-024 when users cannot picture doing the task; it calls for a realistic rehearsal. Those are different interventions despite both potentially reducing uncertainty.

## Apply an evidence ladder

1. Observed product fact or defect: cite the actual source.
2. Research-linked mechanism or applicable requirement: identify the source's setting and limits.
3. Application hypothesis: explain why this buyer and this implementation may fit.
4. Site-validated effect: report population, outcome, observation window, uncertainty, and guardrails.

Research on a mechanism does not establish an untested SaaS uplift. Empty `source_ids` explicitly identifies a pattern with no particular study claimed. A source-backed record still needs product facts, working behavior, and outcome evidence before claiming conversion improved. Avoid stacking patterns until the page becomes noisy or the journey becomes longer.

## Complete pattern index


### Original foundations: PAT-001–PAT-022

| ID | Pattern | Inspect when |
| --- | --- | --- |
| PAT-001 | Processing fluency | Visitors misread the product, billing unit, or next action even though the facts are present. |
| PAT-002 | Specificity | Claims sound interchangeable because they omit the real task, output, audience, or operating condition. |
| PAT-003 | Salience and contrast | People can describe the offer but miss the purchase action or selected state in a visually crowded page. |
| PAT-004 | Social proof | Buyers doubt whether other relevant customers obtain useful results from the product. |
| PAT-005 | Authority | Evaluation depends on a specialist claim that the buyer cannot easily verify unaided. |
| PAT-006 | Anchoring | Buyers lack a meaningful reference for judging the subscription price or delivered value. |
| PAT-007 | Contrast and compromise | Multiple viable packages serve different needs, but buyers cannot see their meaningful trade-offs. |
| PAT-008 | Risk reversal | Appropriate buyers hesitate because they cannot resolve an important uncertainty before commitment. |
| PAT-009 | Reciprocity | The product’s expertise is hard to assess before purchase, and a small useful artifact can demonstrate it. |
| PAT-010 | Commitment and consistency | A visitor has a relevant goal but the next steps are disconnected from that goal. |
| PAT-011 | Ownership and investment | Buyers understand claims but have not experienced creating something useful with the product. |
| PAT-012 | Progress and goal proximity | A meaningful setup or evaluation task contains several steps and users cannot tell what remains. |
| PAT-013 | Defaults | A reversible starting choice can be reasonably inferred for a new undecided buyer. |
| PAT-014 | Loss framing | The current workflow has an evidenced recurring cost that is relevant to the buyer’s decision. |
| PAT-015 | Real scarcity | An actual capacity constraint affects access to a service, cohort, or assisted setup. |
| PAT-016 | Real urgency | A genuine deadline changes the available offer or the buyer’s ability to meet an important date. |
| PAT-017 | Mental accounting and price framing | The billable unit or payment interval obscures how the offer fits the buyer’s budget. |
| PAT-018 | Implementation intentions | A willing user knows what they want but does not translate that intention into a first concrete use. |
| PAT-019 | Autonomy | The journey pushes users into a configuration or commitment they cannot easily inspect or change. |
| PAT-020 | Anticipation and curiosity | The product can reveal a meaningful result, but the page describes it without making it tangible. |
| PAT-021 | Familiarity | Unusual labels or controls make an otherwise ordinary buying task feel difficult or unpredictable. |
| PAT-022 | Expectation management | Purchase success depends on setup, limits, human work, or conditions missing from the promise. |

### Comprehension: PAT-023–PAT-028

| ID | Pattern | Inspect when |
| --- | --- | --- |
| PAT-023 | Causal walkthrough | Visitors understand the claimed result but cannot explain how the product could produce it. |
| PAT-024 | Process rehearsal | Buyers want the outcome but hesitate because they cannot imagine performing the necessary steps. |
| PAT-025 | Ordinary-day narrative | Feature lists fail to show how the subscription would fit a recurring working situation. |
| PAT-026 | Bounded analogy mapping | The product introduces an unfamiliar concept that buyers repeatedly confuse with something else. |
| PAT-027 | Same-input joint evaluation | The product advantage is hard to see when the old and new workflows are described separately. |
| PAT-028 | Two-sided explanation | A sophisticated buyer distrusts an entirely positive claim or discovers important limitations only later. |

### Evidence: PAT-029–PAT-034

| ID | Pattern | Inspect when |
| --- | --- | --- |
| PAT-029 | Claim-to-evidence traceability | Buyers see strong claims but cannot find the underlying artifact, method, or source needed to evaluate them. |
| PAT-030 | Independent corroboration | All reassurance comes from repeated versions of the seller’s own claim. |
| PAT-031 | Typical-outcome calibration | The page highlights a spectacular result that may feel unattainable or create unrealistic expectations. |
| PAT-032 | Denominator-first proof | Large counts or percentages look impressive but leave buyers uncertain about the relevant population. |
| PAT-033 | Situation-matched identification | Available customer stories concern organizations or tasks that the current buyer finds hard to identify with. |
| PAT-034 | Freshness and version context | Buyers cannot tell whether a review, benchmark, or screenshot still describes the current product. |

### Comparison: PAT-035–PAT-040

| ID | Pattern | Inspect when |
| --- | --- | --- |
| PAT-035 | Preference construction before recommendation | A buyer cannot choose because they have not identified which differences matter most for their job. |
| PAT-036 | Must-have elimination | Buyers waste time evaluating packages that fail an essential requirement. |
| PAT-037 | Aligned attribute comparison | Competing plans or products describe the same capability in different units or unrelated language. |
| PAT-038 | Incremental value contrast | Existing customers see a full premium feature list but cannot tell what they would gain beyond current entitlements. |
| PAT-039 | Opportunity-cost salience | A buyer compares subscription price in isolation while their current process consumes relevant budget or staff effort. |
| PAT-040 | Recommendation with boundaries | A recommended plan looks arbitrary, overly confident, or selected for the seller’s margin. |

### Valuation: PAT-041–PAT-046

| ID | Pattern | Inspect when |
| --- | --- | --- |
| PAT-041 | Work-unit translation | Credits, tokens, requests, or seats do not tell buyers how much useful work they can complete. |
| PAT-042 | Integrated ownership cost | The advertised subscription omits required setup, extra tools, minimum seats, or recurring operational work. |
| PAT-043 | Budget range framing | Usage varies enough that a single optimistic estimate leaves buyers afraid of an unpredictable bill. |
| PAT-044 | Cash-flow timeline | A promotion, annual commitment, or installment schedule obscures what leaves the buyer’s account and when. |
| PAT-045 | Break-even threshold | Buyers cannot connect the subscription’s fixed cost to how often they would use its benefit. |
| PAT-046 | Flexibility option value | A lower annual equivalent competes with a real need for seasonal use, uncertain adoption, or limited commitment. |

### Adoption risk: PAT-047–PAT-052

| ID | Pattern | Inspect when |
| --- | --- | --- |
| PAT-047 | Reversible adoption map | Buyers fear lock-in but cannot tell which adoption decisions can be undone and what an exit would involve. |
| PAT-048 | Continuity bridge | The buyer sees future value but assumes switching requires an abrupt, risky replacement of the current workflow. |
| PAT-049 | Buyer-defined proof of value | A prospect keeps exploring features without resolving whether the product satisfies the actual buying requirement. |
| PAT-050 | Calibrated uncertainty with recovery | The product produces variable or probabilistic outputs, and buyers fear an unmanageable mistake. |
| PAT-051 | Responsibility attribution | A benefit sounds attractive, but the buyer cannot tell which work belongs to them, the software, or a service team. |
| PAT-052 | Specific fallback reassurance | Buyers worry about what happens when the normal workflow stalls, but the page offers only a vague support promise. |

### Action: PAT-053–PAT-058

| ID | Pattern | Inspect when |
| --- | --- | --- |
| PAT-053 | Goal shielding | An interested user is diverted from the chosen task by unrelated setup, promotional prompts, or competing workflows. |
| PAT-054 | Obstacle-linked if–then plan | Users intend to proceed but repeatedly stop at a predictable and recoverable obstacle. |
| PAT-055 | Just-in-time concept teaching | Users abandon a decision because a technical term or configuration choice requires knowledge they do not yet have. |
| PAT-056 | Choice-rationale reinstatement | A returning evaluator sees a saved selection but has forgotten why it seemed suitable. |
| PAT-057 | Action feedback and closure | After a meaningful action, users are unsure whether it succeeded or what useful step follows. |
| PAT-058 | Portable cognitive offloading | Evaluators must remember many trade-offs across sessions, tabs, or stakeholders. |

### Group buying: PAT-059–PAT-062

| ID | Pattern | Inspect when |
| --- | --- | --- |
| PAT-059 | Role-specific value translation | The person who benefits from the workflow is different from the person approving the purchase. |
| PAT-060 | Champion rehearsal | An enthusiastic evaluator struggles to explain the purchase internally without the vendor present. |
| PAT-061 | Shared evidence checkpoint | Different stakeholders repeat the same evaluation or assume someone else has resolved a blocking issue. |
| PAT-062 | Defined-group descriptive norms | A buyer wonders whether a workflow or adoption step is normal for peers in a relevant situation. |

### Continued value: PAT-063–PAT-066

| ID | Pattern | Inspect when |
| --- | --- | --- |
| PAT-063 | Episodic value recall | At a trial or upgrade decision, the user has experienced value but does not remember the concrete result. |
| PAT-064 | Attributable value accounting | The subscription performs useful recurring work, but the account owner cannot see what it delivered over a period. |
| PAT-065 | Mastery scaffolding | Users can complete a heavily guided first task but doubt their ability to use the product independently. |
| PAT-066 | Fresh-start reentry | A former evaluator returns at a real new project or planning period after an earlier incomplete attempt. |


## Handle popular "tricks" precisely

### Choice overload

Diagnose complexity, uncertainty, and decision difficulty. Neither "more choice is always better" nor "always show exactly three plans" is a reliable rule. The [2010 meta-analysis](https://doi.org/10.1086/651235) reported substantial variation; the [2015 meta-analysis](https://doi.org/10.1016/j.jcps.2014.08.002) examines moderators.

Start with recognizable customer needs, comparable units, a short list of decisive differences, and a way to inspect full details. Recommend a plan for a stated use case. Use "most popular" only with current supporting data and an appropriate population.

### Decoy pricing and the middle option

Know that context can shape comparison; do not assume it creates incremental demand. Offer real packages that make sense on their own. A higher service tier can be a truthful reference when it provides actual service. An intentionally useless tier is a poor default.

Measure overall revenue/contribution per eligible unit, choice satisfaction, and retention. More selection of the highlighted middle plan is not sufficient evidence of success.

### Scarcity and countdowns

The [scarcity review](https://ecommons.cornell.edu/entities/publication/167c0da3-fa55-44ad-be11-f258914ee9a3) concerns value and desirability; it does not validate evergreen SaaS countdown widgets.

Use an exact deadline and timezone only when real. Persist the actual deadline across refreshes and devices as appropriate. Stop the offer when it ends. Explain capacity constraints such as a fixed number of assisted onboarding appointments. Omit scarcity when supply is not constrained.

### Loss aversion and fear of missing out

Translate the status quo into a verifiable consequence. Let users edit calculator assumptions. Show both cost and benefit. Avoid alleging that a buyer is losing money, falling behind peers, or risking their business without evidence.

Do not use humiliating opt-out wording. Keep declining an offer understandable and respectful.

### Price endings

Treat whole numbers, .99 endings, precise numbers, currency display, and billing frames as positioning and comprehension experiments. Do not claim a universal premium or bargain effect. Keep total payable price visible and calculate savings correctly. Use segment-appropriate tests and contribution guardrails.

### Annual framing and starting selections

Inspect these explicitly on every pricing audit; do not assume accurate billing text means the presentation is effective. For comparable monthly/annual plans, keep the main comparison on a monthly basis: `$12/month` versus `$9.60/month`, with `$115.20 billed yearly` directly below the annual equivalent. Verify the 20% saving from actual prices and retain the full annual commitment. At checkout, foreground the actual amount due.

For a suitable discounted annual self-serve offer, use annual-first as the starting presentation hypothesis for an undecided new visitor, following the decision rules in `pricing-and-packaging.md`. Preserve an explicit monthly choice, account context, intended links, and experiment assignment. Do not infer that annual is appropriate from a discount alone when seasonal use, a monthly campaign promise, or observed buyer needs favor flexibility.

Implement authorized reversible presentation improvements with a clear mechanism and measurement plan. Lack of measured uplift is a reason to qualify the effect, not a reason to leave the observed problem untouched. Measure overall paid conversion and retained value as well as annual share; a higher annual share alone can conceal fewer total buyers.

### Personalization and self-selection

Use declared goals, role, company needs, language, region, or observed product usage where appropriate to the site's data policies. Make meaningful preferences editable. Show relevant proof and workflows; avoid fabricated personal messages or sensitive-trait inference.

Define segments before analysis. If a treatment changes who qualifies for a segment, do not read the resulting segment difference as a clean treatment effect.

## Truth and implementation checks

For each tactic, identify the required fact, its owner/source, the buyer question it answers, its rendered behavior, and its outcome. If a fact is missing, propose collecting it or remove the claim from publishable copy.

Replace fake urgency with an actual product reason to act; fake testimonials with a useful product demonstration; unsupported popularity with "For teams that need [verified capability]"; obstructive cancellation with optional relevant pause/downgrade choices.

Use the requested ambition to improve the offer and experience. Do not substitute a moral lecture for useful implementation.
