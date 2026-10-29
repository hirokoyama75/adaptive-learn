# Novel-rule benchmark results

Completed 2026-10-29. **Tutoring and worked-example self-study tied at 32/32 valid unseen items each; no instruction scored 0/32. No incremental tutoring benefit was demonstrated.** This is synthetic open-context rule application, not human learning or retained knowledge.

## What ran

- Twelve distinct actual learner sessions, four replies each: **48 preserved replies**, all protocol-valid. No failed learner run, replacement, retry, or additional learner session was needed.
- Every learner used `opencode-go/deepseek-v4.1-flash#low`. No medium-effort or pretend-human learner was used.
- Development: worlds 43 and 107. Confirmation: worlds 211 and 509. The [protocol](PROTOCOL.md), generator/grader, all questions, arm order, and primary measure were frozen before learners ran.
- After development, the [recorded decision](DEVELOPMENT_DECISION.md) was **no teaching amendment**. Confirmation used the unchanged teaching implementation and skill. The decision hash, frozen hashes, and unchanged skill hash are in [verification/audit.json](verification/audit.json).
- Each instructed learner received the same complete rulebook and initial worked example as its matched counterpart, attempted two practice items, and received checked solutions. Tutoring could target submitted intermediate values; self-study received a generic self-check solution. Controls received no rules or solutions.

## Primary result

Correct final value **and** route on the eight preregistered valid unseen inputs per session:

| Phase | World | Tutoring | Self-study | No instruction |
| --- | --- | --- | --- | --- |
| Development | 43 | 8/8 | 8/8 | 0/8 |
| Development | 107 | 8/8 | 8/8 | 0/8 |
| Confirmation | 211 | 8/8 | 8/8 | 0/8 |
| Confirmation | 509 | 8/8 | 8/8 | 0/8 |
| **Total** | | **32/32** | **32/32** | **0/32** |

Tutoring minus self-study was zero in every matched world, including confirmation. This is a ceiling-limited null contrast, **not proof that the methods are generally equivalent**. The no-instruction contrast mainly establishes the importance of having the invented rules available; it does not establish the value of adaptive teaching.

## Secondary observations and exposure

| Measure, across four sessions per arm | Tutoring | Self-study | No instruction |
| --- | --- | --- | --- |
| Pretest, before receiving rules | 0/16 | 0/16 | 0/16 |
| Practice items, correct final value and route | 8/8 | 8/8 | 0/8 |
| Surface-transfer items, subset of primary | 8/8 | 8/8 | 0/8 |
| Invalid-input abstentions, separate from primary | 8/8 | 8/8 | 8/8 |
| Trace matches on primary items | 32/32 | 32/32 | 6/32 |
| Invalid replies | 0/16 replies | 0/16 replies | 0/16 replies |
| Clarification questions | 4 | 3 | 4 |
| Prompt whitespace words per session | 586 | 566 | 413 |
| Prompt characters, total | 18,634 | 18,066 | 14,320 |
| Reply whitespace words, total | 109 | 64 | 72 |
| Reply characters, total | 4,431 | 4,164 | 4,307 |

All clarification questions occurred at pretest. No additional unscheduled help was given. Tutor prompts contained 20 more whitespace words per session than self-study prompts. Whitespace words are not provider tokens, cost, latency, or reasoning effort; minified JSON often counts as one word. Neither effort nor token usage was equated or measured.

Controls abstained on every item. That earns invalid-input credit without demonstrating the rules. Their six trace matches are empty traces on stop items **with incorrect routes**, not six correct solutions. These metrics must not be combined into a learning or mastery percentage.

## Strengths actually observed

1. **Correct composed execution with supplied rules.** Both instructed arms handled arithmetic transformations, order of operations, priority stops, and the tested boundaries without an observed final-answer or trace error.
2. **Limited surface transfer.** Both handled the two prose-paraphrased inputs in every world. This tests a formatting change, not structural transfer to a new domain or selecting an unprompted method.
3. **Appropriate abstention.** Instructed learners declined to fill missing/unlisted fields; uninstructed learners did not invent a rulebook. Correctness depended on information actually supplied.
4. **Reproducible measurement.** An independent composition implementation checked the oracle over all 528 valid world/input combinations. Every actual reply is retained with its declared prompt, continuation identifier, hash, and deterministic grade. Confirmation reproduced development without policy tuning.

These observations support this checked, bounded implementation on these tasks. They do not validate every execution of `adaptive-learn/SKILL.md`.

## Weaknesses and limits

- **Ceiling and no correction opportunities.** Every instructed practice attempt was already correct. No corrective adaptive branch was used in any of the eight tutor feedback turns. The intervention mostly differed by a short acknowledgment; the experiment cannot establish whether diagnosing and repairing mistakes helps.
- **Strong common treatment.** Both instruction arms had the complete rulebook, worked example, practice, and solutions available in context. Their success cannot be attributed specifically to tutoring, practice feedback, or the skill. There was no rulebook-only ablation.
- **Simplified teacher.** Feedback came from program-checked orchestrator templates aligned with selected skill principles, not an unconstrained model executing the entire skill. Broad teaching quality, novice support, misconception repair, and self-correction remain unmeasured.
- **Four parameterizations, not four domains.** Every world has the same underlying algorithm. There is only one learner run per world/arm; item counts are not independent participant replications. No significance, equivalence, or population-effect claim is supported.
- **Unequal item-category coverage.** A post-run coverage audit found that world 509's intended ordinary count=10 boundary was already in its pretest and was dropped by the uniqueness filter. Its eight valid posttest inputs contain three stop items and five ordinary transformations; the other worlds contain one stop and seven transformations each. No question or score was changed after discovery. This weakens coverage and makes world 509 easier; future generation needs category invariants before freezing, not a silent correction of this dataset.
- **Open context only.** Rules and prior feedback stayed visible. This does not measure unaided recall, delayed retention, model-weight learning, or human education. A fresh model chat would not itself establish retained learner knowledge.
- **Instruction-based isolation.** Learners were told not to use tools or sources, but child tools were not technically disabled and internal traces were unavailable. No sandbox-verified or contamination-free claim is made. Provider-side model identity, sampling details, and compute usage cannot be independently authenticated by the recorder.
- **Manual capture.** The orchestrator preserved actual tool-returned text, adding a terminal newline. Stored prompts are declared inputs, not exported provider traces. Local consistency checks cannot prove provider execution or resist a writer who can replace all evidence and hashes.

## Improvement made, and what was deliberately left alone

**Kept the skill and frozen teaching/scoring unchanged.** No observed skill instruction failed, and a perfect self-study baseline is not grounds for adding teaching rules. The benchmark's stopping rule was reached; no positive-result fishing or further learner runs were performed.

**Hardened the measurement recorder.** Audit showed that the original reporter checked raw-reply hashes but trusted saved grades/exposure/identity metadata and did not verify saved prompts. Two new regression methods reproduced eleven inconsistent-fixture failures before the fix; the actual red output and before-source hash are retained in [verification/report-integrity-red.txt](verification/report-integrity-red.txt). The reporter now:

- regenerates every declared prompt from frozen inputs and the prior actual reply, then checks content and hash;
- recomputes the existing grades from raw replies;
- checks model, run, stage, phase, arm, session continuity, and exposure lengths.

This is an evidence-supported infrastructure improvement, **not an improved-learning claim**. No actual reply, metadata record, frozen question, generator, protocol, or original phase report was overwritten. The hardened reporter reproduced both original phase reports exactly. It checks consistency, not cryptographic authenticity; run without Python's `-O` because integrity guards use assertions.

## Verification and reproduction

| Check | Result |
| --- | --- |
| Existing package tests, Python 3.13.14 | 74 passed, zero skips |
| Existing package tests, Python 3.10 | 74 passed, zero skips |
| Benchmark/recorder tests, Python 3.13.14 | 9 passed |
| Benchmark/recorder tests, Python 3.10 | 9 passed |
| Actual captures and session continuity | 48 replies; 12 distinct sessions; raw/recorded copies match |
| Original development and confirmation reports | Match freshly recomputed reports exactly |
| Frozen protocol, generator/data, and skill hashes | Unchanged |
| Existing 14-case instrument and four-case holdout | Validated; frozen holdout hash unchanged |
| Final syntax, links, whitespace, and artifact checks | Python 3.10 syntax and 8 local Markdown destinations valid; no diff whitespace errors or package learner/cache artifacts |

Windows's `py -3.13` launch failed because the Store-installed interpreter was not registered with that launcher; the complete suite then passed using the verified `python` 3.13.14 executable. This was an interpreter-launch error, not a skipped or failed test. It is recorded in the planning log.

From the workspace root:

```text
python -B -m unittest discover -s handoff/benchmarks/novel-rules -p "test_*.py" -v
py -3.10 -B -m unittest discover -s handoff/benchmarks/novel-rules -p "test_*.py" -v
python -B handoff/benchmarks/novel-rules/record.py report --phase all
```

From `adaptive-learn/`, run `python -B -m unittest discover -s tests -v` and the same command with `py -3.10 -B`.

Artifacts: [development results](development-results.json), [confirmation results](confirmation-results.json), [all per-run results](all-results.json), [aggregate/coverage/integrity audit](verification/audit.json), `raw/`, and `sessions/`. Existing package holdouts were not used to design or tune these tasks. No real learner records, dependencies, telemetry, global installation, commits, or publication were added.

## Next experiment, not executed

1. Pilot genuinely harder invented rules on separate, non-evaluation seeds, with a fixed pilot budget. Require natural, non-ceiling attempts; never force errors or role-play a weaker human. Stop if this model remains unsuitable for measuring correction.
2. Reserve disjoint coverage categories **before** assigning pretest inputs. Check exactly which transformations, priority exceptions, boundaries, invalid inputs, and meaningful transfer cases are represented before freezing.
3. Compare an actual skill-driven tutor against the same checked self-study material under a matched exposure budget, with repeated fresh sessions and new frozen confirmation tasks. Keep item keys hidden from teaching until instruction is fixed. Measure whether a real identified error is repaired on a new case.
4. Treat closed-context reconstruction or retention as a separate outcome with an explicitly specified information boundary. Human learning would require a separate voluntary study, not another synthetic score.

The next useful improvement is a more discriminating experiment. This run supplies no basis for a teaching-policy edit or a human-efficacy claim.
