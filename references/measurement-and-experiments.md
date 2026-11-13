# Measurement and trustworthy experiments

Use measurement to distinguish a shipped improvement, a useful observation, and a supported causal effect. Read the source register for methodology references. The operating recommendations below are an original synthesis, not a claim that every experiment needs enterprise infrastructure.

## Define success before reading a result

Specify the eligible population, randomization/counting unit, entry time, outcome, observation window, and exclusions. Choose the unit that can receive an independent experience: often a visitor for a marketing page or an account for B2B pricing and onboarding. Keep the same buying account in one variant when teammates influence each other.

| Metric | Definition | Interpretation limit |
| --- | --- | --- |
| Paid conversion | Eligible units with a verified first paid outcome within the defined window / eligible units | Not checkout starts or zero-value trial invoices |
| Trial-to-paid | Trial cohort units that pay within the declared maturity window / eligible trial cohort units | A newer cohort has had less chance to convert |
| Qualified opportunity | Units meeting a predefined qualification rule / eligible units | Proxy for revenue; track later wins |
| Revenue per eligible unit | Declared net revenue in a fixed horizon / eligible units, including zeros | Define refunds, discounts, taxes, currency, and attribution |
| Contribution per eligible unit | Revenue less declared variable costs in the horizon / eligible units | Not full accounting profit or a lifetime forecast |
| Activation | Eligible units completing a product-specific valuable task / eligible units | Validate its relationship to retention instead of assuming login is value |
| Retention/refund/support | Cohort-based measures with explicit denominators and horizon | Lag may exceed the first conversion window |

Price changes can raise revenue while lowering conversion, or raise conversions while reducing margin. Define the economic goal accordingly. Annual cash collected, normalized recurring revenue, and recognized revenue are different quantities; do not combine them in one comparison without a declared accounting basis.

For a simple one-purchase example, expected revenue per visitor equals paid-conversion probability times average revenue conditional on purchasing. This is arithmetic under that setup, not a complete model of SaaS retention or lifetime value.

## Establish the event contract

Adapt [assets/event-contract.json](../assets/event-contract.json) to the existing system rather than installing an unnecessary analytics stack.

Record assignment separately from exposure. Define exposure at the opportunity to receive the treatment, consistently across arms; do not condition it on a later click that the treatment can change. Preserve assignment across navigation, refreshes, and login according to the chosen unit. If identity merges are unavoidable, specify how conflicts are handled before analysis.

Use events to diagnose the journey, with a verified server/payment outcome as the purchase source of truth. Distinguish first purchase, renewal, expansion, reactivation, trial, refund, and payment failure. Deduplicate event IDs and transaction/order/invoice outcomes; a webhook retry is not a new customer.

Minimize payloads: pseudonymous identifiers where appropriate, experiment/variant, route, stable plan identifier, interval, amount in documented minor units, currency, event time, ingestion time, and relevant cohort metadata. Do not log full payment details, passwords, free-text form contents, or unnecessary personal information. Respect the site's consent and data handling configuration. If measurement is incomplete, disclose the affected population.

Before testing, verify: assignment balance, event uniqueness, source/amount reconciliation, timestamps, cross-domain redirects, identity merges, consent behavior, and time-to-conversion lag. An A/A or controlled instrumentation check is useful when the experiment system itself is uncertain.

## Plan the experiment

Use [assets/experiment-brief.md](../assets/experiment-brief.md). Write:

- Hypothesis, exact variants, target segment, and one primary decision outcome.
- Eligibility and exclusions fixed before exposure.
- Stable allocation, unit, exposure definition, and interference risks.
- Baseline and its dated data source; minimum worthwhile effect and planning MDE.
- Statistical method, alpha or decision threshold, power where applicable, sample size, and duration.
- Outcome maturity window, business cycles, enrollment cutoff, and analysis time.
- Diagnostic metrics and guardrails with material harm/rollback criteria.
- Handling of multiple variants, multiple outcomes, overlapping experiments, and predeclared segments.
- Rollout, rollback, and decision owner consistent with already-granted authorization.

MDE is a planning sensitivity, not an expected uplift. A minimum commercially useful change and a detectable change need not be equal.

For a two-arm equal-allocation independent Bernoulli outcome:

    python3 <skill-dir>/scripts/cro_math.py plan-ab --baseline 0.05 --relative-mde 0.20 --eligible-users-per-day 1000

A baseline of 5% and a relative MDE of 20% means a target of 6%, an absolute change of 1 percentage point. The bundled normal approximation plans 8,158 units per arm at its default 5% two-sided alpha and 80% power. Reproduce with the script and preserve assumptions. The accrual estimate excludes ramp-up, business-cycle coverage, and outcome maturation.

Do not count the same returning person as a fresh independent unit every day. Do not use the calculator for account-clustered users, continuous revenue, sequential tests, or unequal-allocation power planning. Use an appropriate established method when those features matter.

## Monitor safely and analyze at the planned time

Monitor severe payment, security, accessibility, or performance failures continuously and act on material harm. This is separate from repeatedly searching for a conversion winner.

For a conventional fixed-horizon test, complete the planned enrollment and relevant time window, then allow outcomes to mature. Do not stop when a p-value first dips below .05 or extend only when the result is disappointing. If continuous efficacy monitoring is required, choose a valid sequential method in advance. Bayesian analysis also requires a specified model, priors, and decision policy; it is not permission to ignore experiment design.

A [Microsoft experimentation reference](https://www.microsoft.com/en-us/research/articles/patterns-of-trustworthy-experimentation-during-experiment-stage/) distinguishes outcome, diagnostic, data-quality, and guardrail metrics. Use the distinction to keep a click increase from overriding harm to paid customers.

## Check validity before interpreting effects

1. Verify intended versus observed allocation for the chosen population. Investigate sample-ratio mismatch (SRM); do not "fix" it by dropping users until groups match.
2. Check assignment stability, missing logs, consent differences, bot filters, duplicate payments, and unequal failures.
3. Preserve the eligible assigned population where feasible. Triggered analyses need symmetric, treatment-independent definitions or a justified causal method.
4. Check conversion lag and equal follow-up; do not compare complete control cohorts with immature treatment cohorts.
5. Check concurrent launches, campaigns, seasonality, and spillovers. Randomization helps; it does not repair a broken assignment or analysis pipeline.
6. Apply the declared multiple-testing approach. Treat unplanned subgroup discoveries as exploratory.
7. Inspect customer harms and business economics, not only the primary p-value.

Microsoft's [SRM guidance](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/) explains why allocation mismatches can indicate bias. The utility's default investigation threshold is a configurable heuristic, not a universal standard. Supply the actual planned allocation. Passing SRM does not prove randomization or data quality.

## Report estimates with honest uncertainty

    python3 <skill-dir>/scripts/cro_math.py compare-ab --control-users 10000 --control-conversions 500 --variant-users 10000 --variant-conversions 600

The descriptive rates are 5% and 6%: +1 percentage point and +20% relative. The utility reports Wilson per-arm intervals, a Newcombe-Wilson difference interval, a pooled normal p-value when its cell-size checks pass, and an SRM diagnostic. These methods are approximations with different constructions; do not force their threshold decisions to agree.

A p-value is not the probability that the variant is better. A conventional confidence interval is not a posterior probability statement. Report direction, magnitude, precision, business relevance, and validity separately. Zero observed conversions do not prove a zero underlying rate. "Inconclusive" does not mean "no effect."

Use user/account-level methods appropriate for skewed revenue and clustering. Aggregate conversion counts cannot estimate revenue uncertainty. Do not convert a binary-conversion interval into a lifetime-value interval.

Choose a disposition: ship within scope, continue to the prespecified endpoint, iterate a new hypothesis, roll back for harm, or investigate invalid data. Give the reason and unresolved assumptions. A statistically detectable tiny effect may not justify cost; a promising imprecise estimate may justify further study.

## If no causal test is feasible

Use a dated observational baseline, a clear change log, comparable mature cohorts, and segmented outcomes. Document traffic, pricing, product, and campaign changes. Label differences as associations, especially with small samples or changing acquisition mix.

Use customer observation and interviews to explain friction; use pilots to test feasibility. Repair known defects without waiting for significance. Never fabricate a percentage uplift because a project needs a persuasive case study.
