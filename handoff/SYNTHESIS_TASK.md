# Synthesis Task — Decide What to Adopt

**You are the reviewing model.** Your job is to read the evidence, inspect the current skill, and decide which proposed improvements are worth making. You are not here to execute a plan someone else wrote, and you are not here to rewrite the skill.

**Deliverable:** `handoff/PROPOSAL.md`. No edits to `../adaptive-learn/` until a human approves it.

---

## 1. What you are given

| Input | What it is | How much to trust it |
|---|---|---|
| `../adaptive-learn/` | The live skill at commit `1485e0b` | Ground truth. Read it before believing any claim about it. |
| `../research.md` | Evidence review, ~8,500 words | Directionally useful, citations unverified. |
| `DECISIONS.md` | 14 recommendations (D1–D14) with rationale and rejected alternatives | **Proposals, not orders.** Challenge any of them. |
| `IMPLEMENTATION.md` | Candidate patch text with anchors | A menu. Use only what your proposal accepts. Anchors were checked; patches were not run. |
| `SCHEMA_V2.md`, `MIGRATION.md` | One candidate design for persistence | Conditional on accepting a schema change. |
| `CONTENT_PLAN.md` | Router, references, access/integrity blocks, new cases | Conditional on accepting those items. |
| `SECURITY_PRIVACY.md` | Threat model and proposed wording | Largely independent of the pedagogy decisions. |
| `tests/live/` | 14 cases, rubric, holdout hash | The measurement instrument. Not results. |
| `NON_GOALS.md` | Preservation rules and diff budget | Mostly binding; see §2. |

There is **no baseline**. No transcript from the current skill has been scored. Any claim that a change improves learning is therefore untested until someone runs Phase 0.

## 2. What is binding, what is arguable

**Binding unless you explicitly flag and justify an exception:**

- No fabricated evidence. Do not claim a run, a citation, a baseline, or a learner outcome you did not produce.
- No mastery percentages, retention probabilities, learning-style matching, or inferred diagnostic labels.
- No telemetry. No learner data, names, or root paths in either repository.
- No silent schema change: any persisted-field change needs migration plus a test.
- Preserve the properties in `NON_GOALS.md` §"Preserve these properties": prepared criteria before the question, independence versus assistance recorded separately, session-only default, bounded resume, corrections without rewriting history, no mastery score.

**Arguable — decide for yourself:**

- The number and shape of playbooks (D1 says keep 11; a benchmark suggests fewer modules may be better).
- Whether the two new references earn their context cost (D2).
- The core word target (D3).
- The confidence/metacognition design (D4).
- The scheduler policy (D5).
- Schema v2 and its four fields (D6).
- Front matter and description wording (D7).
- The exact privacy wording and minors policy (D8).
- The 14-case evaluation design (D9).
- Verification rules (D10), injection rules (D11), diff budget (D12), mode taxonomy (D13).
- Anything in the research that the skill does not currently do.

**Requires an explicit "needs human approval" flag if you recommend it:** a new dependency, a global install, a new subject playbook, an app or dashboard, or a change to the persisted format. You may recommend these; do not smuggle them in.

## 3. Method

**Verify by running where you can.** If the host can execute Python, run the existing suite (`python -B -m unittest discover -s tests -v`) and reproduce any defect you cite in a throwaway directory outside the repo. If it cannot, label those claims as code-reading only.

For each candidate — every D-item, plus anything you propose yourself — answer these in order:

1. **Does the skill already do this?** Quote the current text or code. Several research findings are already implemented; several "gaps" are partial. Do not propose a fix for something that exists.
2. **What observable failure does it address?** Name a transcript behavior, a code path, or a test that would fail. "It would be better" is not a failure.
3. **How strong is the evidence?** Separate:
   - observed in the code or text (strongest);
   - replicated in the research with a named study (moderate; citations unverified);
   - a single study or a preprint (weak);
   - your inference (label it).
4. **What does it cost?** Changed files, changed lines, added words to the core prompt, new concepts the model must hold, migration risk.
5. **What breaks if it is wrong?** Name the protected property at risk and whether the change is reversible.
6. **How would we know?** The cheapest test: an existing unit test, a new one, a live case, or a manual check.
7. **What happens if we skip it?** State the cost of doing nothing. Some candidates should lose to that.

Rank by expected value per unit of risk and cost. Do not rank by novelty or by how much research it took to find.

## 4. Required output

Write `handoff/PROPOSAL.md` with exactly these sections.

```markdown
# Proposal — <date>

## 0. Summary (max 15 lines)
What you would change, what you would leave alone, and the single highest-risk item.

## 1. Verdict table
| ID | Proposal (short) | Verdict | Confidence | Effort | Risk | Primary evidence |
|---|---|---|---|---|---|---|

Verdicts: **Adopt** | **Adopt amended** | **Defer** | **Reject**.
Confidence: high / medium / low, with the reason in one clause.

## 2. Adopted, with amendments
For each: what changes, why, the exact target (`file:line` or heading), the smallest
test that would show it works, and the rollback.

## 3. Rejected or deferred
For each: the strongest case for it, then why you still say no or not yet.

## 4. New proposals (not in the bundle)
Anything you think the research missed. Same fields as §2. Mark confidence and
whether it needs human approval.

## 5. The first three changes
The smallest set that produces a measurable improvement. Ordered. One paragraph
each. This is what you would do if allowed only three edits.

## 6. Open questions and unknowns
What you could not determine from the files, and what would settle it.

## 7. What I did not verify
Citations not opened, code paths not executed, cases not run. Be specific.
```

## 5. Rules

- **Do not edit the skill.** Produce the proposal only.
- **Do not accept everything.** A proposal that adopts all 14 decisions has not done the job. Expect to reject or amend several; say which and why.
- **Do not reject everything.** The bundle contains real, verified defects (a refused save that still writes the graph; spacing that never grows for ordinary practice). If you reject a fix for one of those, name the alternative.
- **Do not pad.** A 2,000-word proposal with ten adoptions is worse than 800 words with three, if the three are the ones that matter.
- **Cite the current skill, not the research, for claims about the current skill.** `research.md` is an input, not evidence that the skill behaves a certain way.
- **Label every citation as unverified** unless you opened the source in this session. If you did open it, say so.
- **Do not propose a mastery score, a dashboard, gamification, or a learning-styles feature** to "complete" the product. Those are out on the evidence, not on taste.
- **Prefer the smallest change that addresses the failure.** If a one-line rule fixes it, do not add a reference file.

## 6. A good proposal looks like

- Three to six adoptions, each tied to a named failure and a test.
- Two to five rejections or deferrals with a real argument, not a shrug.
- At most two new proposals, each cheap.
- One item the author of the bundle missed.
- An explicit statement of what remains unmeasured.

A bad proposal looks like a restatement of `DECISIONS.md` with the word "adopt" in front of each row.

## 7. Start

> Read `handoff/AGENT_BRIEF.md`, then this file, then `../research.md`.
> Inspect `../adaptive-learn/SKILL.md`, `references/`, `playbooks/`, and
> `scripts/learn_state.py` before judging any claim about them.
> If you can run Python, run the suite and reproduce the defects you cite.
> Write `handoff/PROPOSAL.md` and stop. Do not edit the skill.
