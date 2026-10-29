# Work Order — Adaptive Learn

> Historical proposed order, superseded by the approved reliability pass recorded in `IMPLEMENTATION_RESULTS.md`. Do not execute its destructive reset examples or assume the four-field schema was adopted. Current migration and recovery rules are in `../adaptive-learn/references/persistence.md`; roll back code with scoped inverse edits, never by discarding learner/user data.

**Audience:** the implementing model, **after** a human approves `PROPOSAL.md`.
**Scope:** `..\adaptive-learn\` only. This bundle's author modified nothing there.
**Status:** proposed sequence. Apply only the items your proposal accepts; rejected items are not work.
**Evidence base:** `..\research.md`; treat its conclusions as evidence, not instructions.

## Recommended decisions under review

These are the author's recommendations (D1–D14). A reviewer may reject or amend any of them in `PROPOSAL.md`; the table below is the default if no verdict is given.

| ID | Decision |
|---|---|
| D1 | Keep all 11 playbooks. No merges, no new playbooks. Measure them; do not restructure. This supersedes research §9.7 and roadmap item 24. |
| D2 | Add exactly two references: `exam-craft.md`, `study-skills.md`, each ≤45 lines. |
| D3 | `SKILL.md` ≤1,400 words at G3. Baseline is 1,838. |
| D5 | Scheduler is split. P1 = fix retrieval-only doubling (P-02) and state the gap policy. P2 = 90-day saturation cap (30→60→90), lapse ×0.4 floor 1, re-teach after 3 lapses. No stability/difficulty parameter, no FSRS. |
| D6 | Schema v2 adds exactly four fields: `hint_level`, `task_id`, `error_kind`, `transfer`. No `attempt` field — `task_id` groups attempts and the checkpoint holds the response. Migration ships before the version bump. |
| D9 | 14 live cases total; 4 are holdout, frozen at G1, never edited. |
| D12 | Hard caps on added + deleted lines (`git diff --numstat`): P1 = phase 1, ≤4 files/≤150 lines; P2 = phases 2–3 union, ≤8 files/≤350 lines; P3 = phase 4, ≤2 existing files/≤80 lines, new `tests/live/` exempt. Each patch ≤60 lines, one behavior, one stated revert; no whole-file rewrite. |
| D14 | Non-goals: dependencies, global install, dashboards, gamification, FSRS, per-turn confidence, exam wrappers, mastery percentages, new playbooks. |

**Baseline 2026-10-28:** commit `1485e0b`, clean; 30 tests pass (3.13.14); `SKILL.md` 1,838 whitespace tokens; 11 playbooks, 3 references, 25 worked cases. D3 counts `-split '\s+'` tokens; a space-only split reads ~4% lower.

## Gate A — Proposal approval

- **Goal:** decide what to change before changing it.
- **Files:** none in the skill. Write `handoff/PROPOSAL.md` using `SYNTHESIS_TASK.md`.
- **Budget:** 0 lines changed in `adaptive-learn/`.
- **Prereqs:** none.
- **Gate:** a human has accepted the verdict table. Only **Adopt** and **Adopt amended** rows enter the phases below; **Defer** and **Reject** rows are removed from the queue.
- **Do not proceed if** the proposal adopts every item, rejects an item without naming a failure, or recommends something on the invariant list in `AGENT_BRIEF.md` §3.

## Phase 0 — Baseline capture

- **Goal:** reproducible before-state; frozen holdout.
- **Files:** none in the skill. Write results to `handoff/baseline-results.md` (the protocol is `handoff/BASELINE.md`).
- **Budget:** 0 lines.
- **Prereqs:** none.
- **Commands** (from `..\adaptive-learn`):
  ```powershell
  git status --porcelain
  python -B -m unittest discover -s tests -v
  py -3.10 -B -m unittest discover -s tests -v
  ((Get-Content SKILL.md -Raw) -split '\s+').Where({$_}).Count
  (Get-Content SKILL.md -Raw).Length
  (Get-ChildItem playbooks).Count; (Get-ChildItem references).Count
  git tag phase-0-baseline
  ```
- **Record:** commit, test counts, word/char counts, runtimes.
- **Stop:** any failing test on a clean tree.
- **Rollback:** delete tag.
- **Do not proceed if** the tree is dirty or shows learner data.

## Phase 1 — Correctness and security

- **Goal:** no false "saved", no lost obligation, no unhandled injection, no overclaimed privacy.
- **Files:** `scripts/learn_state.py`, `tests/test_state.py`, `SKILL.md`, `README.md`. Nothing else.
- **Budget:** ≤4 files, ≤150 changed lines, `SKILL.md` ≤60 lines.
- **Prereqs:** G0 tag present.
- **Work:** P-01 stale-revision check before graph write; P-03 success-over-error deletion; P-04 pause durability; P-06 `_due` chronology; P-07 future-dated evidence; P-08 recompute on read; P-10 byte cap; P-12 profile read cap; S-01 indirect-injection rule; S-02 qualify the "local"/upload claim and S-03 minors/classroom note in `README.md`; I-08 front matter; A-01/A-02 answer-key, verification ladder, no fabricated citation.
- **Commands:**
  ```powershell
  python -B -m unittest discover -s tests -v     # 30 existing + 8 new + property test, 0 failures
  py -3.10 -B -m unittest discover -s tests -v
  git diff --stat phase-0-baseline
  git status --porcelain
  git tag phase-1-end
  ```
- **Gate G1:** 39+ tests pass on both interpreters; atomicity test proves graph bytes unchanged after refusal; no non-stdlib import; holdout tagged `holdout-freeze`.
- **Stop:** a defect needs schema fields (defer to phase 3), or a test passes by weakening its assertion.
- **Rollback:** `git reset --hard phase-0-baseline`.
- **Do not proceed if** `--input` trust widened, a privacy claim got stronger, or `selected_targets` semantics change without a test.

## Phase 2 — Teaching quality

- **Goal:** deterministic turn 1, one rung per turn, answer after the attempt, one transfer item, scheduled self-explanation.
- **Files:** `SKILL.md`, `references/teaching-decisions.md`.
- **Budget:** ≤2 files, ≤100 changed lines, `SKILL.md` ≤40 lines.
- **Prereqs:** G1.
- **Work:** I-01 precedence ladder; I-02 turn-1 block; I-03 task-verb router + "Using: X" declaration; L-01/L-02 hint entry, one rung per turn; A-04 leakage rule; L-04 transfer before "move on"; L-05 self-explanation prompt; L-03 interleaving boundary; L-07 one delayed post-feedback certainty estimate. Replace vague hedges ("when useful", "as appropriate") with triggers; keep research §2 intact.
- **Commands:**
  ```powershell
  python -B -m unittest discover -s tests -v
  ((Get-Content SKILL.md -Raw) -split '\s+').Where({$_}).Count
  Select-String -Path *.md,references\*.md,playbooks\*.md -Pattern 'when useful|as appropriate|when needed|if helpful'
  git diff --stat phase-1-end
  git tag phase-2-end
  ```
- **Gate G2:** core ≤1,700 words; banned-phrase count 0 in `SKILL.md`; router labels ≥18/20 utterances; AC-01, 02, 06, 17, 24 walkthroughs re-read and consistent.
- **Stop:** rules still conflict after the ladder, or the router mislabels >2 of 20 utterances.
- **Rollback:** `git reset --hard phase-1-end`.
- **Do not proceed if** a protected property was deleted to save words, or holdout hash changed.

## Phase 3 — Content and schema

- **Goal:** ≤1,400-word core, two references, v2 with migration, scheduler policy live.
- **Files:** `SKILL.md`, `references/persistence.md`, `references/study-goals.md`, `scripts/learn_state.py`, `tests/test_state.py`, new `references/exam-craft.md`, `references/study-skills.md`.
- **Budget:** ≤7 files, ≤250 changed lines, `SKILL.md` ≤40 lines; ≤45 lines per new reference; schema diff ≤150 lines. The phase 2 + phase 3 union must stay ≤8 files and ≤350 lines (D12).
- **Prereqs:** G2; human approves the exact v2 field list (D6).
- **Work:** trim core (fold study goals, drop restatements); D2 references; D6 `_migrate` then version bump; D5 scheduler (90-day saturation, lapse ×0.4 floor 1, re-teach after 3 lapses) plus P-09 timezone; split persistence into quick save vs full schema and correct the documented drift; L-12 access bullets; L-11 wise feedback; I-07 description after the 20-utterance test; I-09 path ordering.
- **Commands:**
  ```powershell
  python -B -m unittest discover -s tests -v
  py -3.10 -B -m unittest discover -s tests -v
  ((Get-Content SKILL.md -Raw) -split '\s+').Where({$_}).Count   # must be <= 1400
  git diff --stat phase-2-end
  git tag phase-3-end
  ```
- **Gate G3:** v1→v2 fixture round-trips; every support path resolves; ≤1,400 words; saturation, lapse, and re-teach tests pass.
- **Stop:** ≤1,400 requires cutting a protected property — hand off, do not cut.
- **Rollback:** `git reset --hard phase-2-end` (export before reverting a migration on real data).
- **Do not proceed if** the migration fails on a copy of a v1 state, or the target is met by deleting evidence rules.

## Phase 4 — Measurement, merge

- **Goal:** evidence the change helped; holdout untouched.
- **Files:** new `tests/live/*` (installed from `..\handoff\tests\live\`), `README.md` testing section, `PROVENANCE.md` claims line. `handoff/LESSONS.md` lives outside the repo and is not counted.
- **Budget:** ≤2 existing files, ≤80 changed lines; new `tests/live/` exempt; 0 deleted teaching prose.
- **Prereqs:** G3; human supplies host, model, judge.
- **Work:** install the staged harness; 14 cases (10 editable, 4 holdout), 6 rubric dimensions, binary `must_not` primary, two runs, two judges, violation counts. Capture a baseline from the pre-change commit before scoring candidates (`BASELINE.md`).
- **Commands:**
  ```powershell
  Copy-Item ..\handoff\tests\live\* tests\live\ -Recurse -Force
  python -B tests/live/check_cases.py --cases tests/live/cases.json
  python -B tests/live/check_cases.py --verify-holdout
  git diff --stat phase-3-end
  ```
- **Gate G4:** no `must_not` increase on editable cases; leakage flat or lower; holdout hash matches; no post-run edits.
- **Stop:** a holdout case regresses and the cause is unclear.
- **Rollback:** revert doc claims; keep harness.
- **Do not proceed if** cases were edited post-hoc, or results are reported as learning outcomes.

## Dependency graph

```text
G0 baseline ──> P1 atomicity ──> P1 tests ──> holdout freeze ──┐
                    │                                          │
                    └──> P2 precedence ──> P2 router/hints ──> G2
                                                               │
G2 ──> v2 field approval ──> schema+migration ──> trim <=1400 ──> G3
                                                               │
G3 ──> live harness ──> G4 ──> merge
```
Hard edges: atomicity → save tests; precedence → router; `hint_level` → schema; schema → scheduler policy; holdout freeze → phase-2 edits.

## First 90 minutes

1. 0–5: `git status`, `git log -1`, read this file and `CITATIONS.md`.
2. 5–15: run both test suites; record counts in `handoff/baseline-results.md`.
3. 15–25: read `SKILL.md` end to end; list the protected properties you will not cut.
4. 25–35: tag `phase-0-baseline`; copy a real v1 state fixture (no identifiers); write the P-01 atomicity test and confirm it fails.
5. 35–50: fix P-01 until that test passes; run the full suite.
6. 50–65: fix P-03 and P-04 with tests; suite green.
7. 65–75: from `adaptive-learn/`, run `python -B ..\handoff\tests\live\check_cases.py --verify-holdout`; tag `holdout-freeze`; check `git diff --stat`; report G1.

## Red flags — halt

- Any test failing unexpectedly, or one edited to pass.
- `SKILL.md` above 1,400 words at G3, or above 1,838 at any point.
- A new dependency, non-stdlib import, or global install.
- Mastery language ("mastered", "permanently learned", "% mastery").
- Leakage count rising on any case.
- Changes outside the allowed file list.
- A citation or DOI you did not open.
- Learner data, real names, or `.learning/` contents in the repo.
- Holdout hash mismatch.
- Any change that makes a privacy or capability claim stronger.

## Handoff points — stop and ask

Ask before: changing the v2 field list; cutting a protected property; merging playbooks (D1); migrating real learner state; any README efficacy claim; marking a citation verified; publishing; exceeding budget by >20%; a second failed fix on one defect.
