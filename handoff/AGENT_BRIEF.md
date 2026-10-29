# Agent Brief — Adaptive Learn Improvement Handoff

**Audience:** the model that will review this bundle and decide what to change.
**Skill under review:** `../adaptive-learn/`, a published OpenCode skill at commit `1485e0b`, Apache-2.0.
**Your deliverable:** `handoff/PROPOSAL.md`. One file. No edits to the skill.

---

## 1. The task

Read the evidence and the current skill, then decide which proposed improvements are worth making.

You are not executing a plan. `DECISIONS.md` records one reviewer's judgments, with reasoning. Some are right, some are probably wrong, and a few were written before the code was read closely. Your value is in telling them apart — not in applying all fourteen.

The full assignment, output template, and verdict rules are in `SYNTHESIS_TASK.md`. Read that second.

## 2. Read order

| # | File | Why |
|---|---|---|
| 1 | `AGENT_BRIEF.md` (this file) | Scope and constraints |
| 2 | `SYNTHESIS_TASK.md` | The assignment and required output |
| 3 | `../research.md` | Evidence base. Citations unverified. |
| 4 | `NON_GOALS.md` | What must be preserved |
| 5 | `DECISIONS.md` | The 14 recommendations you are judging |
| 6 | `WORK_ORDER.md` | Proposed sequence, gates, budgets |
| 7 | `IMPLEMENTATION.md` | Candidate patches; use only what you accept |
| 8 | `tests/live/cases.json` and `tests/live/rubric.md` | How behavior would be judged |

Then the actual skill: `SKILL.md`, `references/`, `playbooks/`, `scripts/learn_state.py`, `tests/`. Do not rely on the bundle's description of what the skill does. Read the source.

Conditional references: `SCHEMA_V2.md` and `MIGRATION.md` only if you consider a schema change; `CONTENT_PLAN.md` for router/reference/access items; `SECURITY_PRIVACY.md` for injection and privacy; `CITATIONS.md` before repeating any citation; `BASELINE.md` for how a before-state would be captured.

## 3. What binds you

These are the user's values, not research conclusions. A proposal that violates one is rejected regardless of its expected benefit:

- **No fabricated evidence.** No claimed run, citation, baseline, transcript, or learner outcome that did not happen.
- **No pseudo-measurement.** No mastery percentages, retention probabilities, confidence scores presented as mastery, or diagnostic labels inferred from behavior.
- **No learning-style matching.** Accommodations are fine; VAK labels are not.
- **No telemetry, and no learner data in either repository.** No names, birth dates, school, or root paths.
- **Preserve the honesty properties** listed in `NON_GOALS.md`: prepared criteria before the question, assistance versus independence recorded separately, session-only default, bounded resume, corrections without rewriting history, "move on provisionally" rather than mastery.
- **No silent schema change.** Any persisted-field change needs migration and a test.

These require an explicit "needs approval" flag if you recommend them: a new dependency, a global install, a new subject playbook, an app or dashboard, a format change.

Everything else is yours to judge. Playbook count, the two proposed references, the 1,400-word target, confidence design, scheduler policy, schema v2, front matter, privacy wording, and the evaluation design are all open. `DECISIONS.md` argues for one option; you may reject it.

## 4. Evidence rules

- Distinguish **observed** (you read the code or text), **reported** (a study in `research.md`), and **inferred** (your judgment). Label which.
- Cite current behavior as `file:line`, not as a summary.
- `research.md` is a secondary source. `CITATIONS.md` marks every entry unverified. Do not promote a DOI or effect size into a proposal as fact.
- If a proposed fix addresses something the skill already does, say so and reject it.
- If you cannot tell whether a failure is real, say what would settle it. Do not guess in the confident voice.

## 5. Budget expectations

The point of the bundle is restraint. A good proposal usually:

- adopts 3–6 items;
- amends 1–3;
- defers or rejects 3–6;
- adds at most two ideas of its own;
- names one thing the bundle got wrong.

If your proposal rewrites the core, adds three references, and adopts everything, you have misunderstood the task. If it rejects everything, you have not read the code.

## 6. Stop conditions

Stop and report instead of proceeding if:

- you cannot inspect the skill source (then the analysis is guesswork — say so);
- a claim in the bundle contradicts the code and you cannot tell which is current;
- you are about to recommend something that requires a dependency, a global install, or a format change (flag it, do not plan it silently);
- you are about to write a claim you cannot support with either `file:line` or an opened source.

## 7. What is known to be missing

- **No baseline.** No transcript from the current skill has been executed or scored. "Improves learning" is untested for every item in this bundle.
- **No patch has been applied.** `IMPLEMENTATION.md` anchors were checked against the files, but the proposed code was never run.
- **Citations are unverified.** Treat effect sizes as claims to check, not facts.
- **The 14 live cases have never been run.** They are a measurement instrument, not evidence.
- **The holdout set is frozen** (`tests/live/holdout.json`). Do not tune against `L-02`, `L-07`, `L-12`, `L-14`.

## 8. After the proposal

Do not start implementing. `WORK_ORDER.md` Phase 0 begins only after a human approves `PROPOSAL.md`. If approval is given, the accepted items — not the full D-list — become the work order.
