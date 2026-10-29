# Baseline protocol

**Status: protocol only. No baseline has been executed.**

This file defines how to capture the current skill's live behavior before any edit. There are no results here and none may be added by anyone who did not run the sessions. If you are the implementing model and have not run these sessions, write "baseline not run" in every report.

The baseline exists so that a later change can be compared against something. Without it, every improvement claim is a guess. Do not edit the skill between baseline runs; a baseline taken mid-edit measures nothing.

## Preconditions

- Record the exact commit hash and a SHA-256 of `SKILL.md`, `references/`, `playbooks/`, `scripts/`, and `tests/`. If the working tree has uncommitted changes, list them in the manifest and name the before-state `<commit>-dirty` (for example `1485e0b-dirty`); never label it with the bare commit hash. Recording the snapshot does not require committing or tagging the user's work.
- The mechanical suite passes on the target Python version. Run `python -B -m unittest discover -s tests -v` from the skill folder and record the count.
- The case set is fixed and hashed before the first run. Use the 14 cases in `tests/live/cases.json`; `check_cases.py --verify-holdout` must pass.
- One model, one host, one configuration for the whole baseline. Record all three.
- Fresh chat per run. No memory carryover, no prior transcript in context.

## Roles

Three separate sessions. One model may not fill more than the learner role.

- **Tutor** — a fresh chat with only the shipped skill loaded. This is the object under test. It sees the case material, its own replies, and nothing else.
- **Learner** — a fixed script. Paste `turns[0]`, then `turns[1]`, and so on, verbatim and in order. Do not improvise, coach, add helpful detail, or answer a question the case does not answer; paste the next turn and log the deviation. A learner who invents turns makes the version comparison meaningless.
- **Judge** — a different model, or a human. Blind to version labels and to the manifest. Never the tutor session. If one model must both tutor and judge, the run is a demo, not a measurement.

A model that plays learner and judge is grading its own homework. A model that plays tutor and judge is doing the same. Label any single-model run `demo` and keep it out of `runs/`.

## Directory layout

```
tests/live/runs/baseline/
  manifest.md
  <case-id>/
    case.md
    run-1.md
    run-2.md
    score-1.md
    score-2.md
```

- `<case-id>` matches the case identifier exactly (`L-01`, `AC-06`, or whichever set is used). Do not rename.
- `case.md` is a frozen copy of the case as run, so a later case edit cannot silently change what was measured.
- `run-1.md` and `run-2.md` are complete transcripts, verbatim, including tutor messages, learner messages, tool calls, and errors.
- `score-1.md` and `score-2.md` are the judge outputs for the corresponding run, unedited.

Do not store these under the skill's learner-data paths and do not store learner names, school, or a home directory path. Redact the root to `<root>` before committing a transcript.

## What to record

**`manifest.md`** — one table, one row per session:

| Field | Value |
|---|---|
| Case ID | |
| Run | 1 or 2 |
| Date and time (UTC) | |
| Model name and version | |
| Host and version | |
| Tools available | file read, write, shell, Python version, none |
| Skill commit | |
| Case hash | |
| Prompt version | tag or hash of `SKILL.md` and the files read |
| Files the model actually read | exact paths |
| Persistence root | `session-only` or `<root>` |
| Deviations | anything that differed from this protocol |
| Judge | model name, or `human` |

**Per transcript** — before the learner turns, record the verbatim prompt used to start the session, then every turn in order. Mark tool calls inline. Mark truncation explicitly as `[... truncated ...]`; never paraphrase a missing section. Record the wall-clock length only if the case involves a budget.

**Per score** — the judge's full output, including per-dimension scores, `must_not` results, quotes, PASS/FAIL verdict, agreement, and confidence. Save each judge's annotation JSON and the `check_run.py` output beside the score file; the checker derives the verdict mechanically and does not judge tutoring. If two judges are used, keep both and record agreement.

## Scoring sheet

Copy this table into `score-<n>.md` for every case. Leave cells blank until scored.

```
Case: <case-id>    Run: <1|2>    Judge: <id>    Date: <UTC>

| Dimension            | Score (0-2 / N/A) | Evidence quote |
|----------------------|-------------------|----------------|
| Diagnosis            |                   |                |
| Hint calibration     |                   |                |
| Answer restraint     |                   |                |
| Evidence honesty     |                   |                |
| Language / register  |                   |                |
| Persistence          |                   |                |

| must item (index) | Observed (Y/N) | Assistant turn(s) | Evidence quote |
|-------------------|----------------|-------------------|----------------|
|                   |                |                   |                |

| must_not item (index) | Violation (Y/N) | Severe? | Assistant turn(s) | Quote |
|-----------------------|-----------------|---------|-------------------|-------|
|                       |                 |         |                   |       |

Verdict: PASS / FAIL (PASS needs every applicable must observed, zero violations,
zero automatic fails). The authoritative record is the judge's annotation JSON;
run tests/live/check_run.py to derive the verdict mechanically.

Notes:
```

A dimension the case does not exercise is recorded as N/A with one line saying why; N/A is never summed into a total. There is no composite score row and no winner line: a leaked answer still fails a case whose other dimensions scored 2.

When both runs of a case are scored, add a one-line comparison: `run-1 vs run-2: same verdict | flipped | both fail`. A version that disagrees with itself is evidence about the case, not about the version.

## Rules

1. **Two runs per case.** No exceptions. One run cannot distinguish a version from its own variance.
2. **No cherry-picking.** Every run that was started is recorded, including abandoned and failed ones. If a run was void because the harness broke, keep it and mark `void` with the reason.
3. **No edits between runs.** Do not fix a prompt, tighten a case, or reword a learner turn after seeing run 1. If a case is broken, retire it for the whole baseline and say so.
4. **No fabricated results.** Do not fill in a score you did not receive, a transcript you did not capture, or a model you did not use. An empty cell is honest; an invented number poisons every later comparison.
5. **No learner data.** Use synthetic personas. If a real session informs a case, rewrite it so no identifying detail survives.
6. **Judges are blind.** Randomize A/B order per case and record the mapping separately from the judge output. Do not let the judge see the manifest.
7. **Freeze before editing.** Retain the source snapshot and its per-file hashes before runs. A tag or branch is optional; never commit or tag user work merely to satisfy this protocol. Later comparisons name the same exact frozen source.

## After the baseline

Report only: case count, runs completed, total severe `must_not` violations, per-dimension totals over applicable (non-N/A) dimensions, and run-to-run flip count. Do not report a mean score as an improvement metric; violation counts are the primary signal.

Then, and only then, begin Phase 1 of the work order.
