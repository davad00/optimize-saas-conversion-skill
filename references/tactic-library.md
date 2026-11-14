# Select and implement conversion tactics

Use this library after identifying the buyer, verified offer, relevant journey, and observed obstacles. It contains **360 additional concrete tactics: 18 families with 20 entries each**. The two existing annual-pricing baseline rules are not included in that count. Complete those rules and the other baseline checks even when no catalog entry is selected.

## Contents

- Retrieve relevant entries
- Route by the buyer's task
- Select a coherent intervention
- Respect the action scope
- Verify the result and learn
- Read the record format
- Maintain the catalog

## Retrieve relevant entries

Resolve the scripts from this skill's installed directory. The tool uses Python's standard library and reads only the bundled catalog. It does not browse, write files, contact customers, alter billing, or launch experiments.

```bash
python3 <skill-dir>/scripts/tactics.py categories
python3 <skill-dir>/scripts/tactics.py list --category pricing
python3 <skill-dir>/scripts/tactics.py search 'minimum seats total cost' --category pricing --limit 5
python3 <skill-dir>/scripts/tactics.py search 'uncertainty' --category decisions --limit 5
python3 <skill-dir>/scripts/tactics.py show PRI-001 DEC-001
```

For an in-scope family, scan all 20 titles and triggers, then read the complete entries whose conditions match the page. Search is a retrieval aid, not a ranking of expected revenue or a substitute for the family scan. Search uses literal words; try ordinary synonyms or list the family if results are poor. A search hit is not evidence that the tactic applies.

Load only relevant families and matching details. If Python is unavailable, read the corresponding `references/tactics-<family>.jsonl` file; each line is one complete entry. Do not skip the tactic pass because the helper cannot run. The main skill links every family directly.

## Route by the buyer's task

| Task or obstacle | Start with these families | Add when the evidence calls for it |
| --- | --- | --- |
| Landing page fails to explain fit or motivate action | intent, positioning, copy, proof, demo, objections, cta, visual, decisions | pricing, packaging, offers when plans appear on the page |
| Pricing, annual offers, or plan choice | pricing, packaging, offers, decisions, cta, visual | proof and objections for trust gaps; checkout for the purchase handoff |
| Signup, verification, or payment abandonment | signup, checkout, cta, objections | decisions for unresolved choices; visual for layout/attention defects |
| Trial, freemium, first value, or contextual upgrades | activation, upgrades, retention | offers for trial economics; demo for evaluation; decisions for setup choices |
| Paid retention, failed payments, or cancellation | retention, activation, upgrades | checkout for payment recovery; sales for account-level renewal processes |
| Enterprise evaluation and internal approval | sales, objections, proof, demo, packaging | pricing for procurement economics; signup for evaluation access |
| Complete SaaS improvement pass | Consider all 18 families at the scope level | Scan every family relevant to an accessible journey; record unavailable evidence |

Match the actual surface rather than the URL name. A landing page with pricing cards needs the pricing gate. An account screen that asks for an upgrade needs applicable pricing, checkout, and upgrade checks. An email suggestion remains outreach work even if it is discovered while reviewing an onboarding screen.

Keep a compact coverage record using `assets/tactic-decisions.md`: which families were considered, what evidence was available, which IDs matched, and what was implemented, proposed, deferred, or ruled out. A one-line reason can cover an irrelevant family. Do not create a separate long document for each family or postpone an obvious authorized repair while expanding paperwork.

## Select a coherent intervention

1. **Identify the obstacle.** Describe the exact text, state, step, or missing explanation and its source. A tactic title is not a diagnosis.
2. **Check the trigger.** Match the entry's condition to this product and buyer. If the condition is absent, skip it with a short reason when material.
3. **Verify the facts.** Establish prices, capabilities, proof, limits, available support, and relevant customer context. Reconcile advertised capacity with actual service limits before emphasizing an offer.
4. **Choose the mechanism.** State why this change may help this buyer: easier comparison, reduced uncertainty, salient value, meaningful progress, or another concrete explanation. Use `behavioral-evidence.md` when making an external psychological claim.
5. **Combine compatible tactics.** Select a small implementation batch, usually 3–7 coherent changes. Multiple IDs may describe complementary parts of one change; do not inflate the number of findings by counting each separately.
6. **Specify and act.** Write the final copy and behavior, implement authorized reversible work, and verify the affected journey. Use a proposal for an unapproved commercial change. Preserve existing authorization; do not ask again merely because the record has a scope label.

A tactic library expands the candidate set. It does not require changing every component or adding every persuasion device. Keep useful existing content when the trigger is absent. Start with a broken purchase path or a false price before optional framing experiments.

Consider conflicts explicitly. A sticky CTA can obstruct a focused input; a longer proof section can bury a simple offer; an annual emphasis can be unsuitable for a short-lived job; a trial can impose unsustainable service costs. Choose the combination that resolves the observed problem with the fewest new obstacles.

## Respect the action scope

| Scope | Meaning | How to act |
| --- | --- | --- |
| `presentation` | Copy, hierarchy, explanation, display framing, or a visible starting selection | Implement when the task authorizes presentation changes, using verified facts |
| `journey` | Forms, states, navigation, product behavior, payment handoff, or setup flow | Implement within the requested project scope; verify consequential transitions |
| `commercial` | A new price, discount, entitlement, trial, guarantee, billing model, or commitment | Use existing authorization if present; otherwise prepare the exact offer and economics as a proposal |
| `outreach` | Email, messaging, reminders, invitations, or sales contact | Prepare copy/logic as useful; send or launch only with explicit authorization and applicable preferences |

These are routing labels, not permission grants or mandatory new approval gates. A record can have dependencies in another scope. For example, explaining an existing guarantee is presentation; introducing that guarantee changes the offer. Review the actual action rather than blindly trusting the label.

## Verify the result and learn

Use the record's check and measure alongside the primary conversion contract. Convert its metric names into an explicit eligible population, denominator, and observation window. A click or selected tier is diagnostic unless the task is limited to that step. Keep paid outcomes, value delivered, refunds, support, and retained economics visible as relevant.

Exercise affected states, including returning visitors and existing customers. A pricing default can change which provider offer is most often purchased even when billing backend code is unchanged. Check the actual selected offer and fulfillment in test mode when available; state exactly what remains unverified when provider access is absent. Passing unrelated tests does not verify that purchase path.

For refunds, distinguish requests from issued refunds and use comparable first-purchase cohorts with adequate follow-up. For usage estimates, state the assumption rather than promising a fixed number of successful tasks. For capacity limits, distinguish a daily reset, a per-account allowance, and a cumulative spending stop. A visually persuasive card cannot resolve an offer that the service cannot deliver.

Use behavioral studies to explain plausible mechanisms, not borrowed uplift percentages. A tactic may be sensible to implement without a powered experiment; report it as a hypothesis until outcome evidence supports a stronger claim. With limited traffic, use comprehension/task observations and mature cohort summaries, and label what the data can establish.

## Read the record format

| Field | Purpose |
| --- | --- |
| `id` | Stable reference for retrieval and the decision record, such as `PRI-001` |
| `category` | One of the 18 families |
| `title` | The distinct intervention, not a promise of success |
| `trigger` | Observable condition that makes the tactic relevant |
| `action` | Concrete copy, UI, offer, or behavior to implement or propose |
| `mechanism` | Proposed explanation for the buyer response |
| `guardrail` | Specific fact, condition, limitation, or behavior to check |
| `measure` | Outcome and relevant downside to operationalize for this project |
| `scope` | Presentation, journey, commercial, or outreach classification |

All 360 records are application hypotheses. A record can address an observed defect when the project supplies evidence of that defect. It becomes a site-validated effect only after suitable outcome evidence. The catalog does not claim 360 distinct psychological laws or 360 independently proven revenue effects.

## Maintain the catalog

Each `references/tactics-*.jsonl` file is the source of truth for one family. Preserve stable IDs when refining an entry. Keep interventions distinct: changing audience names, devices, or synonyms alone does not create a new tactic. Do not count the two original annual-pricing baseline fixes as additional entries.

```bash
python3 <skill-dir>/scripts/tactics.py validate --similar
python3 -B -m unittest discover -s <skill-dir>/scripts -p 'test_*.py' -v
python3 <skill-dir>/scripts/tactics.py export
```

Validation checks the current 360-entry contract, schema, IDs, and exact duplicates. The optional overlap report finds lexical candidates for human review; it neither proves semantic uniqueness nor decides whether two interventions serve different purposes. The export command produces the readable public `TACTICS.md` from the records. Update its generated copy when publishing catalog changes.
