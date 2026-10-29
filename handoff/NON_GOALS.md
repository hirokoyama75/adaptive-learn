# Adaptive Learn — Non-Goals and Preservation Rules

Binding constraints for any patch to `adaptive-learn/`. Each rule is checkable. On conflict with a task instruction, stop and report.

**Scope.** These rules govern implementation, not the proposal. If your review concludes that one of them should change, recommend it in `PROPOSAL.md` and mark it for approval; this file is not a reason you cannot raise it.

## Files and areas not to touch

- `LICENSE` and `NOTICE`: never edit. `PROVENANCE.md` only for the single approved claims line.
- `.gitignore` scope: never remove ignore rules; only add or narrow.
- `scripts/learn_state.py` outside the named defect fixes (P-01, P-02, P-03, P-04, P-06, P-07, P-08, P-10, P-12) and the D6 schema/migration work. No refactors, renames, or reordering while fixing.
- `tests/acceptance-cases.md` — worked examples stay as historical record. New live cases go in `tests/live/`.
- Any file under `.planning/` or `sessions/`; any learner data, `LEARNER.md`, or `.learning/` tree.
- The 11 playbooks: no rewrites at P1 or P2. Adding final-bullet transfer or self-explanation prompt lines is allowed only where D-clauses name it, and counts against the budget.
- Host configuration, global skill directories, and any other skill in the repository.

## Preserve these properties

Reject a patch that weakens any of the following. Each is a behavior, not a slogan.

1. **Independence vs assistance.** Independence is binary; assistance stays prose. Assisted success is never recorded as independent, and a named method in `cues` limits what the evidence establishes.
2. **Prepared criteria before the question.** An objective answer key or open-ended criteria exist before the learner's response. "I'll judge it when I see it" is a violation.
3. **Session-only default.** No files are created unless continuity is requested and a root is confirmed.
4. **Bounded resume.** Resume returns a selected slice with omission counts, never full-history replay. The active task is never silently cut.
5. **Corrections without rewritten history.** Invalidations are annotated, withdrawn claims keep their IDs, corrections cite the reason. No silent edits, no apology-only responses.
6. **No mastery percentage.** No mastery score, retention probability, ability label, or confidence-as-competence inference anywhere in prose, schema, or output.
7. **Uncertainty stays visible.** "Provisional," "not yet rechecked," and "cannot verify" survive edits.

## Voice and style

- Keep the existing register: short declarative sentences, imperative guidance, no motivational filler, no second-person sales copy.
- Preserve existing `##` headings in `SKILL.md` unless a decision removes one. New subsections allowed; reordering is not.
- No emoji, bold-label bullets, "pro tip," or rhetorical questions to the model.
- Every rule carries a trigger. Ban "when useful," "as appropriate," "if helpful," "when needed" without a stated condition.
- No new tables in `SKILL.md`; prefer prose.
- One behavior per sentence. Do not bundle five prohibitions into one line.

## Dependencies and installs

- Standard library only. Python 3.10+ remains the floor. No `pip install`, no virtualenv, no Node, no network calls at runtime.
- No global installation, no editing of user shell profiles, no auto-copy into `~/.config`. Installation stays a documented manual copy.
- No new binary assets, fonts, or vendored libraries.
- Helper invocations must keep working with `python`, `python3`, and `py -3`; document the fallback rather than assuming one.

## Privacy

- No telemetry, analytics, usage counters, crash reporting, or remote logging — not even opt-in.
- No secrets or out-of-root paths in any written file.
- No learner quotes, names, or root paths in `tests/live/` runs, `LESSONS.md`, or issue text.
- Persistence stays off by default for under-13 use; no names, DOB, school, or location in `LEARNER.md`.
- Any privacy wording must distinguish "the helper makes no network requests" from "the conversation is private." Never claim erasure from provider history, backups, Git objects, or cloud version history.

## Forbidden pedagogical claims

Reject text asserting or implying:

- that the tutor doubles learning, closes achievement gaps, or guarantees exam performance;
- that practice success predicts exam readiness;
- that hint-assisted success is independent performance;
- that a new chat is evidence of retention;
- that confidence, fluency, or speed measures understanding;
- that learning styles, left/right brain, the learning pyramid, or 10,000 hours are valid;
- that interleaving, retrieval, or Socratic withholding always helps (interleaving harms vocabulary learning; novices need explicit instruction);
- that micro-breaks, Pomodoro, body doubling, or growth-mindset slogans are evidence-based performance levers;
- that a model can verify its own answer by re-reading it, or can hear audio, see images, or time performance without host support.

## Forbidden product moves

No dashboard, status UI, query service, database, web app, chat UI, or CLI beyond the three existing commands. No gamification: streaks, points, badges, leaderboards, nudges. No per-turn self-critique. No FSRS or fitted scheduler. No new subject playbooks. No automatic transcript capture. No multi-user or classroom mode. No auto-deletion of history. No schema field for numeric confidence.

## Diff budget

| Phase | Max files | Max changed lines | `SKILL.md` lines |
| --- | --- | --- | --- |
| P1 | 4 | 150 | 60 |
| P2 | 8 | 350 | 80 |
| P3 | 2 | 80 | 0 |

- Count added plus removed lines, including blank-line churn.
- Per patch: ≤60 changed lines, one named behavior, one test, one stated revert.
- **Reject any patch that rewrites a whole file**, replaces more than half a file's lines, or reformats untouched text. Deletions must be line-targeted and must show the preserved headings in the diff.
- A patch touching two phases is split; one without a rollback sentence is rejected.
- Exceeding the budget requires explicit approval naming the decision ID and the reason; it never happens silently.

## Gate before claiming done

1. Word count of `SKILL.md` ≤1,400; both new references ≤45 lines.
2. `python -B -m unittest discover -s tests -v` passes; new tests fail before the fix.
3. Every changed rule has a trigger and a decision ID.
4. No banned claim appears: search for "mastery", "guarantee", "proves", "always helps", "doubles".
5. Diff budget satisfied; privacy wording names the provider and cloud sync; rollback stated.
