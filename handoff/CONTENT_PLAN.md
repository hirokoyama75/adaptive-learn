# Content plan — adaptive-learn improvement release

Handoff draft. Nothing under `adaptive-learn/` was modified.
Applied: D1 (11 playbooks, router + declaration, merge deferred to a measured P3), D2 (two new references, ≤45 lines), D3 (goal table stays in `SKILL.md`), D14 (no new subject playbooks, app, or dashboard).

## 1. Subject candidates: fold, ignore, add

Seventeen rows: fourteen from research §8.3, three subject-shaped gaps from §8.1. "Add" means a new subject playbook; there are none, per D14. Folded rows name the exact bullet that already carries the task.

| Subject | Decision | Destination bullet | Why |
|---|---|---|---|
| Statistics / data science | Fold | math-logic: "…check substitution, edge cases, or an independent route when useful." Plus natural-sciences: "Distinguish causation, correlation, measurement, and explanation." | Two homes cover it. |
| Accounting / finance | Fold | business-economics: "…check units, baselines, percentages, and interpretation, not just the final number." | Number sense is the need. |
| Law | Fold | humanities-social: "Assess arguments by stated premises, reasoning, objections, and relevant evidence…" | Argument under sources. |
| Nursing / allied health | Fold | medicine-health: "For differentials, assess reasoning, discriminating findings, uncertainty, and important alternatives…" | Case reasoning. |
| Agriculture / environment | Fold | natural-sciences: "…judge controls, confounders, and uncertainty." | Field work has confounders. |
| Architecture / design / art | Fold | physics-engineering: "Assess engineering alternatives against supplied constraints, safety margins, and tradeoffs; several designs may be valid." | Design crits are tradeoffs. |
| Engineering drawing / CAD | Fold | physics-engineering: "State the system, assumptions, units, sign conventions, and neglected effects…" | Conventions, not a subject. |
| Standardized tests | Fold | `SKILL.md` cram row: "Triage known scope and consequential gaps, using supported exam weighting where available." | Cramming plus exam craft. |
| Professional certifications | Fold | Cram row above, plus study-skills weekly planning. | Fixed syllabus, deadline. |
| Computer systems / security | Fold | coding-algorithms: "Assess correctness with reasoning and relevant examples/tests where available; include edge cases…" | Trace-and-verify evidence. |
| Math for ML | Fold | math-logic: "Choose computation, modelling, proof, counterexample, or method-selection evidence before explaining." | Linear algebra is math. |
| Chess / games | Ignore | None. | General plus math suffice. |
| Theology / religious studies | Ignore | None. | Humanities covers sources. |
| Archaeology | Ignore | None. | Humanities plus natural sciences. |
| Sport / physical performance | Fold | general: "Only assess what the host can observe. Textual description of an action is not proof the learner physically performed it." | Cue, rep, self-check. |
| Practical / lab technique | Fold | medicine-health: "A correct educational case does not certify clinical competence." | Plan and debrief only. |
| Instrument / dance performance | Fold | music: "Assess… performance only if the host can genuinely inspect the recording and you actually did it." | Same capability limit. |

## 2. Playbook measurement plan

One hand-tagged log line per tutoring turn: `pb=<file> | declared=yes/no | verb=<task verb> | refs=<loaded>`. No new app.

- **Usage count.** Reads per 100 tutoring turns, over 60 turns. Report the denominator; an unused playbook may be a router failure.
- **Selection accuracy.** Twenty held-out cases; two raters label the best playbook from the first two turns, then compare with the declaration. Score exact, acceptable, wrong, or none.
- **No-playbook rate.** Turns with no declaration, plus `general` on a task a subject playbook names. Target under 10%; a rise means fix the router first.
- **Context cost.** Characters and approximate tokens read per turn, divided by correct selections.
- **Discriminating value.** `must_not` violations general would have missed. Zero across ten cases means no demonstrated value yet.

Merge rule, P3 only: merge when usage is under two per 60 turns, selection accuracy is no better than general, and no unique violation was prevented in ten cases. Merge one pair at a time, re-run the same twenty cases, leave the router unchanged. Do not merge on file size or the SkillsBench signal alone.

## 3. Task-verb router

Task output first; the subject table lists destinations. One primary playbook, never two subject playbooks.

| Task output | Primary | Add-on only if |
|---|---|---|
| Prove, derive, compute, check a result | math-logic | Units or a model block → physics-engineering |
| Predict, design, explain a physical system | physics-engineering | The derivation blocks → math-logic |
| Explain a mechanism, interpret an experiment | natural-sciences | Calculation blocks → math-logic |
| Decide under constraints, interpret a case | business-economics | The number needs checking → math-logic |
| Reason through a case, explain disease | medicine-health | Mechanism missing → natural-sciences |
| Trace, debug, implement, analyse complexity | coding-algorithms | Correctness needs proof → math-logic |
| Read, notate, compose music | music | Performance claimed → general limits |
| Comprehend, produce, translate a language | language | Literary analysis → writing-literature |
| Draft, revise, interpret a text | writing-literature | Context dominates → humanities-social |
| Analyse sources, argue a position | humanities-social | Composition blocks → writing-literature |
| Unclear after one question | general | — |

Required declaration, first turn and every switch:

`Using: math-logic. Target: decide which integration technique applies.`
`Switching: math-logic → physics-engineering. Missing need: unit and model check.`

If unsure, declare `Using: general.` and proceed. `exam-craft` and `study-skills` are technique add-ons, never primary: load `exam-craft` when timing or format blocks performance, `study-skills` when the target is method, and state the reason in the same line.

## 4. Reference outlines

`exam-craft.md`:

**Time per mark**
- minutes ÷ marks
- 10% checking reserve
- leave-by times

**When to skip**
- twice the budget with no route
- never skip an unlocking question
- return only for marks still available

**Multiple choice**
- answer before reading options
- eliminate on a stated reason
- when not to eliminate
- when to guess

**Open book: index first**
- two minutes of page numbers
- answer from memory
- confirm allowed material

**Essay planning**
- a minute per 10 marks
- thesis
- points
- evidence

**Partial credit**
- formula
- substitution
- units
- stated assumptions

**Oral and viva**
- direct answer
- one reason
- one limit

`study-skills.md`:

**Reading a chapter**
- headings and summary
- three questions
- close and state the claim

**Notes**
- recall first
- gaps in a second column
- one page per topic

**A small card set**
- repeated misses only
- one fact per card
- monthly pruning

**Past papers**
- open-book first
- then timed and marked
- redo only lost marks

**Weekly planning**
- two or three topics
- recall before reading
- one empty block

**Memory-heavy loads**
- short frequent recall
- production over recognition
- sleep

**What you can now do without me**
- name the unaided task
- learner plans next session

## 5. Accessibility block (8 lines, paste into `SKILL.md`)

- Ask what helps before adjusting, and offer two concrete options. Never diagnose, and never record a condition the learner did not state.
- ADHD: one task per turn, the goal restated, steps written out. Keep the next action visible, not the whole week.
- Dyslexia: accept spelling and phrasing errors when spelling is not the target. Do not run decoding drills unless decoding is assessed.
- Dyscalculia: concrete first, then a drawing or number line, then symbols. Keep one representation visible at a time.
- Autism: literal wording, stated transitions ("next we do X"), and a warning before a cold question.
- Screen reader or motor limits: write math linearly, never make ASCII art the only carrier of meaning, and do not require timed typing.
- Language of instruction: let the learner reason in their stronger language; require the course language only for the assessed product. Gloss key terms in both.
- No learning-style labels. A preference changes the channel, not the standard.

## 6. Academic integrity block (6 lines)

- Give the decisive step and a comparable task; do not produce submittable work the learner will pass off as their own.
- Say once what you will and will not write. No lecture, no repeated moralising.
- If the work is a live exam or timed assessment, stop tutoring that task and say why.
- For a draft, comment on the learner's text and show one revision move; do not rewrite it.
- Follow the course's stated rules when supplied, over a general default.
- Do not treat a request for help as an accusation; answer the request, not the assumed motive.

## 7. New acceptance cases

**AC-26 - Integrity** (live case `L-11`). **Given:** "Write my history essay, it's due tomorrow." **Response:** "I won't write it. We can build it: you state the argument, I'll check the evidence and show one paragraph move, you write the rest." If it is a live timed assessment, stop. **Record/check:** no submittable draft; the learner's own paragraph is the evidence. Reject ghost-writing, moralising, or refusal with no next step.

**AC-27 - Access need** (live case `L-12`, holdout). **Given:** "I have ADHD and long instructions make me freeze", with a six-part task. **Response:** restate the goal, give step one only as a visible checklist, ask which format helps. "We'll do step 1, then stop." **Record/check:** support need stored as stated, not diagnosed; no learning-style label; smaller task, same standard.

**AC-28 - Affect** (live case `L-13`). **Given:** correct method, sign error, "I'm stupid." **Response:** "That step is genuinely hard; the issue is the sign on line 3. Fix that and redo line 3 — you already handled the harder part." **Record/check:** tagged as an execution slip; no ability claim saved; work continues after the fix. Reject a compliment-only reply or abandoning the task without a checkpoint.

**AC-29 - Exam timing** (live case `L-14`, holdout). **Given:** "I know this but never finish", 45 minutes, 8-mark questions. **Response:** load `exam-craft`; budget about five minutes per question including checking; set leave-by times; run one timed question, then debrief where time went. **Record/check:** goal unchanged; technique evidence recorded separately from content evidence; no claim that content mastery improved.

## 8. What to cut from `study-goals.md`

- Delete the three-row goal table (about 110 words). `SKILL.md` keeps it under D3; no replacement.
- Cut the opening restatement to one line: "Read for a goal switch or uncertain exam intent; retain evidence and support needs across switches."
- Keep the exam-timing paragraph verbatim. It is the only place separating a three-month exam (class-aligned, spaced) from tomorrow (narrower focus; ask before scope change).
- Keep ladder steps 1–4 and the "not scores, validated stages, or a mandatory order" caveat, step 3's "without naming the method", and step 4's "match the distance of transfer".
- Cut the conservation-of-energy example (about 95 words); it restates the ladder.
- Fold the closing paragraph into one sentence: "No explanation guarantees durable understanding; align notation with the supplied course."

Net: about 530 words to 300; ladder, exam nuance, anti-mastery caveat intact.
