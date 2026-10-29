# Live test runs

**Status: specification only. No live runs have been executed.** There are no transcripts, scores, or results in this directory.

The harness has 14 cases, six dimensions, and two runs per case per version (28 runs). Cases are synthetic and contain no learner data or paths.

## 1. Capture a baseline before any edit

The baseline is the current skill, unmodified. If it has already been edited, say so; do not present a post-edit run as a baseline.

1. **Freeze the version.** Record the Git commit or a SHA-256 of `SKILL.md` and its support files in `environment.md`; use the hash, not a date.
2. **Fix the environment.** One model and host throughout. Record model, host build, tools (file read, shell, Python, audio, image), context limit, and temperature.
3. **Use a fresh chat per run.** No carried context, no extra system prompt. Load the skill exactly as shipped.
4. **Paste the case, not a description.** Start with the material and turn 1; do not say this is a test. Paste each next turn after the reply. If the tutor asks what a later turn answers, paste it and log the deviation.
5. **Do not coach.** No "be concise", no "remember the rubric", no retries for a better answer. A retry is a new run and must be labeled.
6. **Save the transcript verbatim.** Include tool calls, tool errors, and file paths. Do not paraphrase. Separate every message with a `## Assistant turn N` or `## Learner turn N` header so quotes can be verified mechanically by `check_run.py`. Tool-action claims (files read, code executed, saves) remain judge-verified against these inline records; the checker does not verify them.
7. **Run each case twice** in separate chats, same model/host/day if possible. Do not run pass 2 after seeing pass 1.
8. **Do not change** the skill, cases, or rubric during baseline. Log ambiguity as a deviation.

Run all 14 cases at baseline, including holdouts. Holdout rules restrict prompt tuning, not baseline or final measurement.

## 2. Directory layout

```text
handoff/tests/live/
  cases.json, rubric.md, README.md
  runs/
    baseline-<date>-<hash>/
      environment.md
      L-01/run-1.md
      L-01/run-2.md
      L-01/annotation-judge-1.json
      L-01/check-run-judge-1.txt
      ...
      scores/judge-1.md
      scores/judge-2.md
    candidate-<date>-<hash>/
      ...
```

The version directory is `<label>-<date>-<hash>`. Never overwrite a run; if invalid, keep it and add `INVALID.md` with the reason.

Each transcript file starts with this header:

```text
# L-01 run-1
- Version / prompt: baseline-2026-11-02-a1b2c3d / <sha256>
- Model / host / tools: <id and version> / <build> / file-read=yes, python=yes, audio=no
- Date / judge seed: 2026-11-02 / 4815
- Deviations: none
---
[full transcript]
```

## 3. What to record

For every run, record the header fields plus the exact material and learner turns, full transcript, per-dimension scores, every `must_not` with turn and quote, judge IDs, randomization seed, and any deviation: edited case, retry, host error, changed script, or context truncation.

## 4. Comparing candidate with baseline

Pair by case. For each run number, show a judge two transcripts in random order, no version labels, same rubric. Two judges score independently.

Report in this order:

1. **Violations.** Total `must_not` count per case and per version, severe violations listed individually with quotes. This is the primary result.
2. **Within-version flip rate.** Compare `run-1` and `run-2`: did the verdict change, or did a `must_not` appear in only one? This shows stability.
3. **Rubric deltas.** Per-dimension mean or median, after violation counts, for cases with both runs scored.
4. **Agreement.** Exact and within-one agreement per dimension, plus binary agreement on each `must_not`.

A candidate wins a case only if both runs have fewer violations than both baseline runs, or one is better and the other not worse. A case that flips inside either version is unstable and not a pairwise win.

Do not pool the 28 runs as 28 independent cases. They are 14 cases with two correlated repeats.

### Annotate and check mechanically

Each judge records their judgments in the `check_run.py` annotation JSON — one entry per `must` and per `must_not`, referenced by zero-based index; every observed `must`, violation, automatic fail, or severe violation cites an assistant turn number and a verbatim quote. The checker, which ships with the skill at `adaptive-learn/tests/live/check_run.py`, derives PASS/FAIL from those judgments and rejects missing judgments or quotes it cannot find in the transcript:

```powershell
python -B tests/live/check_run.py --cases tests/live/cases.json --annotation runs/<version>/L-01/annotation-judge-1.json
```

Exit codes: 0 = PASS, 1 = FAIL, 2 = invalid usage or invalid annotation. Attach the checker output beside the score file. It verifies judgment structure and quote references only: it does not judge tutoring, verify tool actions, or measure learning.

## 5. Statistical power

With 14 paired cases, a two-sided sign test needs 12 of 14 wins for p < .05; 11 of 14 is p ≈ .057. Only large effects are detectable. A one-case difference is noise, especially when the same version disagrees with itself on that case.

Report counts, not percentages of mastery: "violations 9 → 3, severe 2 → 0, two cases unstable". Do not turn 14 cases into a claim that the skill is "20% better". This measures transcript behavior, not learning.

## 6. Anti-Goodharting

- **Holdouts.** `L-02`, `L-07`, `L-12`, and `L-14` are holdout. Do not inspect their transcripts during prompt edits. Run them at baseline and final; a regression counts against shipping.
- **Rotate quarterly.** Replace two holdouts with unused ACs (`AC-03`, `AC-05`, `AC-11`, `AC-14`, `AC-16`, `AC-17`, `AC-21`, `AC-23`, `AC-24`), keeping four.
- **No author as sole judge.** At least one judge must be blind to the prompt diff. The author does not break a tie on a disputed `must_not`.
- **Reverse-score verbosity and leakage.** Longer transcripts do not score higher. D3 penalizes pre-attempt answers; no dimension rewards naming the rubric.
- **Do not tune to wording.** A change aimed at a `must_not`'s phrasing is overfitting. Change cases only between versions.
- **Keep the audit trail.** Every change cites the case and transcript that motivated it. A change motivated by a holdout retires it; promote a replacement.

## 7. Limits

Fourteen cases, one model, one host, 28 runs per version, synthetic learners. The harness detects leakage, sycophancy, capability claims, and persistence errors in a transcript. It cannot show that the skill improves learning or rank close versions. LLM judges can be fooled by fluent wrongness; severe violations and disagreements go to a human before they are reported.

## 8. Checker fixtures

`adaptive-learn/tests/live/fixtures/` contains authored synthetic transcripts and annotations used only to test `check_run.py`: a refusal-only run that must fail, a post-surrender reveal and a tutor correction that may pass, a premature answer that must fail, and rejected fabricated, learner-turn, missing, and malformed judgments. They are **not** model runs and their "judges" are **not** calibrated judges. Do not edit them to tune live results, and never add real learner data, names, or paths there.
