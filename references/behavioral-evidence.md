# Behavioral mechanisms and evidence

Research expanded on 14 November 2026. Use this guide to explain a proposed mechanism and its limits. The 360 tactic records are original implementation hypotheses. The papers below do not directly test all of those implementations or establish a conversion uplift for an untested SaaS product.

## Use the research precisely

Name the mechanism, describe the actual study context, and distinguish the proposed application. For example: a study of progress toward a reward can motivate an onboarding hypothesis; it cannot establish that a particular checklist will raise paid subscriptions. Avoid universal percentages, neuroscience claims, and claims that a mechanism overrides product fit or price.

Apply the ordinary evidence ladder: project observation → supported general mechanism or usability requirement → application hypothesis → measured site result. These are different kinds of evidence. Use the primary paper or official documentation for an external factual claim, and inspect current technical documentation before implementing an unfamiliar integration.

## Research map

| Mechanism | Primary source and research context | Useful application boundary |
| --- | --- | --- |
| Anchoring and reference points | [Tversky & Kahneman, 1974, Judgment under Uncertainty](https://doi.org/10.1126/science.185.4157.1124). Examines judgment heuristics, including anchoring. | Use a real, relevant comparison and verified numbers. An arbitrary inflated reference price is not justified by the existence of anchoring. |
| Gain/loss framing and uncertainty | [Kahneman & Tversky, 1979, Prospect Theory](https://doi.org/10.2307/1914185), with an [academic-host copy](https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Behavioral_Decision_Theory/Kahneman_Tversky_1979_Prospect_theory.pdf). Models decisions under risk and reference-dependent valuation. | Explain an actual cost of the current workflow or an achievable gain. Do not invent losses, imply a universal two-to-one effect, or assume a framing result predicts SaaS purchases. |
| Context-dependent comparisons | [Huber, Payne & Puto, 1982, Adding Asymmetrically Dominated Alternatives](https://doi.org/10.1086/208899). Studies how adding an alternative changes choice probabilities. | Explain useful real options and their trade-offs. Do not create a deceptive or unusable plan simply to make another look attractive. Overall purchases, value, and retention matter beyond plan mix. |
| Defaults | [Johnson & Goldstein, 2003, Do Defaults Save Lives?](https://pubmed.ncbi.nlm.nih.gov/14631022/). Examines defaults in organ-donation decisions. | A visible, reversible starting choice can be a hypothesis for a different setting. This paper is not evidence that annual-first universally improves SaaS revenue. Preserve explicit preferences and actual account context. |
| Mental accounting | [Thaler, 1985, Mental Accounting and Consumer Choice](https://pubsonline.informs.org/doi/10.1287/mksc.4.3.199). Develops a model connecting framing of gains/losses to consumer decisions. | Explain costs using a unit the buyer budgets for, while retaining the actual bill. Do not hide commitment behind tiny daily equivalents or assume all buyers share a budget frame. |
| Goal proximity and progress | [Nunes & Drèze, 2006, The Endowed Progress Effect](https://doi.org/10.1086/500480). Examines persistence toward a goal when progress is endowed. | Credit real work already completed or automatically performed, and make the remaining useful steps clear. A fake progress meter or unnecessary setup task can misrepresent value and add friction. |
| Implementation intentions | [Gollwitzer, 1999, Implementation Intentions](https://doi.org/10.1037/0003-066X.54.7.493). Reviews research on linking situational cues with planned action. | Help a willing buyer choose a concrete first task or appropriate setup moment. Do not force scheduling work before the product demonstrates value. |
| Participation and ownership | [Norton, Mochon & Ariely, 2012, The IKEA Effect](https://www.hbs.edu/ris/Publication%20Files/norton%20mochon%20ariely_6f7b1134-06ef-4940-a2a5-ba1b3be7e47e.pdf). Studies valuation of self-created objects and boundaries including successful completion. | Let a prospect create a useful result they can understand and retain. Extra labor, failed setup, or trapping their work is not established as a beneficial SaaS intervention. |
| Small voluntary commitments | [Freedman & Fraser, 1966, Compliance without Pressure](https://pubmed.ncbi.nlm.nih.gov/5969145/), with an [academic-host original paper](https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Influence_Compliance/Freedman_Fraser_Foot-in-the-door.pdf). Studies sequential requests. | A small relevant action can be a testable adoption step. It is not permission to conceal a larger commitment or force a sequence of unrelated micro-actions. |
| Social influence | [Muchnik, Aral & Taylor, 2013, Social Influence Bias](https://pubmed.ncbi.nlm.nih.gov/23929980/). Reports an experiment involving online ratings. | Use authentic, relevant evidence from similar buyers. A ratings effect does not supply a testimonial, logo-strip, or SaaS conversion percentage. |
| Choice complexity | [Scheibehenne, Greifeneder & Todd, 2010](https://doi.org/10.1086/651235), and [Chernev, Böckenholt & Goodman, 2015](https://doi.org/10.1016/j.jcps.2014.08.002). Meta-analyses examine variation and moderators of choice overload. | Reduce irrelevant comparisons and clarify decision criteria. Neither paper establishes an always-correct number of plans. |
| Scarcity and perceived value | [Lynn, 1991, Scarcity Effects on Value](https://ecommons.cornell.edu/entities/publication/167c0da3-fa55-44ad-be11-f258914ee9a3). Reviews scarcity and value/desirability. | Explain an actual capacity limit or deadline when it affects the buyer. A resettable timer, fabricated stock count, or invented waiting list is not a supported application. |
| Color and context | [Elliot, 2015, Color and Psychological Functioning](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2015.00368/full). Reviews findings and methodological/contextual limits. | Choose readable contrast, coherent semantic color, and brand-appropriate emphasis. No universal purchasing color or palette can be inferred. |

Other catalog explanations, such as reducing uncertainty, making a comparison easier, maintaining continuity, and showing relevant proof, are plain-language application hypotheses unless a specific source or project result supports a stronger claim. Do not attach a famous bias name merely to make an ordinary usability change sound scientific.

## Translate mechanisms into useful work

| Buyer obstacle | Candidate mechanism | Concrete design direction | What could undermine it |
| --- | --- | --- | --- |
| Cannot judge whether the price is worthwhile | Relevant anchor, budget framing, explicit trade-off | Compare a verified current workflow cost or show a realistic editable cost model | Inflated assumptions or an irrelevant alternative |
| Cannot tell which plan fits | Decision criteria, reduced complexity, visible recommendation | Ask a relevant need question and explain the recommendation | Unnecessary quiz steps or a recommendation chosen only for margin |
| Doubts the product can do the job | Specificity, evidence, uncertainty reduction | Show a real input/output, fit-matched case, or inspectable sample | A staged outcome that omits limitations or current availability |
| Starts but does not reach value | Meaningful progress, concrete next action, participation | Resume completed work and guide the next useful task | Cosmetic chores, false completion, or blocked output |
| Hesitates because of commitment | Control, clarity, real risk reversal | Explain payment timing, an actual policy, and a usable exit or evaluation path | Unsupported guarantees, hidden restrictions, or a confusing cancellation flow |

Choose the intervention from the observed obstacle. A mechanism alone is insufficient reason to add a widget, badge, quiz, countdown, extra form, or discount.

## Technical and outcome evidence

Use the official sources already listed in `sources.md` for accessibility, payment, performance, and experiment mechanics. [WCAG 2.2](https://www.w3.org/TR/WCAG22/) supplies applicable accessibility criteria; it does not forecast purchases. A payment provider's current documentation explains integration behavior; it does not verify this site's configuration. An experiment method supplies assumptions and an analysis, not proof that its inputs are valid.

Report functional verification separately from business outcomes. Track meaningful paid conversion, delivered value, refunds, support, and retained economics. Keep the distinction between annual cash collected and revenue over a comparable horizon. With low traffic, combine task observations with transparent cohort reporting instead of manufacturing a precise uplift.
