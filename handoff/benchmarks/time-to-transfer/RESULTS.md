# Harder pilot: time to demonstrated understanding

**Completed: four fresh DeepSeek-low learners, twelve actual replies, no retries.** All 16 final task certificates were correct, but only **three of four learners** met the explanation-plus-transfer criterion. The failed final is preserved. This run does **not** establish efficient human learning within ten minutes or a tutoring advantage.

The useful improvement is to spend time on the demonstrated obstacle: a local repair, one focused check, then changed-case transfer. Do not optimize for fewer messages or repeatedly test everything because one sentence was wrong.

## Results, not just final answers

| World / condition | First qualifying checkpoint | Final certificates | Final explanation checks | Confirmed criterion |
| --- | --- | --- | --- | --- |
| 617 / tutoring | 2, after two local corrections | 4/4 | 2/3 | **No** |
| 617 / self-study | Entry, before feedback | 4/4 | 3/3 | Yes |
| 1291 / self-study | 1, after worked solutions | 4/4 | 3/3 | Yes |
| 1291 / tutoring | 1, after one local correction | 4/4 | 3/3 | Yes |

The [frozen protocol](PROTOCOL.md) required reverse execution, ambiguity witnesses, a universal-equivalence judgment/counterexample, construction, and a short accurate explanation. Both arms started with identical definitions and one worked example. There was no uninformative unknown-rule pretest. The orchestrator used the actual skill and mathematics playbook for targeted feedback; self-study received checked solutions. Feedback was not equated in length or content.

Every executable certificate was correct: **48/48 across all attempts**, including 16/16 on final transfer. That part of the benchmark is still at ceiling. Explanation checks caught problems that final answers hid:

- A tutor-arm learner stated a false W-inverse formula. A checked, focused explanation repaired that formula, but the next reply had an inconsistent written operation order. A second local correction resolved it.
- One self-study reply gave the wrong numerical output for an otherwise valid counterexample. Its subsequent explanation was correct after worked solutions.
- Another tutor-arm reply said there were infinitely many starts in a finite seven-value domain. A local clarification repaired that claim.
- The first tutor-arm learner's final answer still said copying erased the **original second** coordinate after a preceding swap. It actually erased the original first coordinate. Its numerical witnesses were correct, but the explanation contradicted them. It failed full transfer; no extra retry was allowed.

[REVIEW_NOTES.md](REVIEW_NOTES.md) explains the conservative judgments and their limits. A written-order typo or cardinality slip is not a global ability diagnosis. Explanations were reviewed by the orchestrator, not a calibrated independent human judge; literal quote checks establish attribution, not semantic accuracy. These four runs are exploratory case evidence, not a reliable method ranking.

## Human time: what is and is not known

**Actual human learning time was not measured.** A model's execution speed cannot supply it. There is no demonstrated human “time to grasp,” ten-minute success rate, delayed retention, or causal learning-speed improvement.

The following is only the preregistered **workload sensitivity calculation**, using the human-facing material actually sent. JSON/tool instructions are excluded. Thinking/answering and short explanation allowances are included. Live tutor waiting is **not** included.

`assumed active seconds = 60 × material words / reading speed + task allowances + explanation allowances`

| Actual path | Human-facing words | Fast assumptions | Reference assumptions | Slower assumptions |
| --- | --- | --- | --- | --- |
| 617 / tutor, **criterion failed** | 703 | 12.26 min | 17.90 min | 25.86 min |
| 617 / self-study, criterion met | 353 | 6.14 min | 8.96 min | 12.94 min |
| 1291 / self-study, criterion met | 573 | 9.39 min | 13.68 min | 19.77 min |
| 1291 / tutor, criterion met | 543 | 9.26 min | 13.52 min | 19.52 min |

- Fast: 240 reading words/minute, 30 seconds per task, 20 seconds per packet's explanation.
- Reference: 180 words/minute, 45 seconds per task, 30 seconds per explanation.
- Slower: 120 words/minute, 60 seconds per task, 60 seconds per explanation.

These rates are unvalidated assumptions, not predictions for a human. The model's short answers do not calibrate them. Dense notation, prior knowledge, access needs, fatigue, and actual difficulty may change the required time substantially. The allowances are for activities, not intrinsic penalties for messages; splitting a useful exchange into more messages is not itself a learning cost, although its real waiting time must count.

**Only one path fits the ten-minute reference scenario before waiting**, leaving 62.3 seconds for all live tutor/service waiting. None fits the slower scenario. Both world-1291 paths fit only the fast scenario, with roughly 37–44 seconds left for waiting. The full-packet workflow is therefore **not robustly ten-minute-ready**.

Do not interpret the roughly ten-second reference difference between the world-1291 conditions as faster learning: it follows mechanically from 30 fewer feedback words in an assumed reading-rate formula. Both needed the same conceptual checkpoint, and neither had measured human time. World 617 also had unequal entry explanation performance before either condition's feedback, so comparing its later path lengths is not a causal treatment estimate.

## Observed timing boundaries

Launch/capture UTC timestamps and monotonic elapsed envelopes are recorded for every actual exchange. They range from **86.6 to 183.3 seconds per exchange** and include parallel-batch waiting, dispatch, orchestration, manual review/capture, and—in the final batch—a quote/console-encoding correction. They are **not pure provider latency**, a reliable estimate of live user-visible waiting, or human thinking time. Offline setup and gaps between exchanges are outside those envelopes. Summing or ranking them as human study time would be misleading.

One quote annotation was rejected before any final record was written. A diagnostic print then hit Windows cp1252's arrow-encoding limit. Authentic ASCII substrings were used for annotations; original UTF-8 raw replies, including arrows/em dashes, remained intact. No learner answer, failed grade, or actual record was repaired or overwritten. Details are in the planning log.

## What improved

### A usable, clock-aware human lesson draft

- [HUMAN_LESSON.md](HUMAN_LESSON.md): learner-facing material, shown one section at a time, without agent JSON overhead.
- [FACILITATOR.md](FACILITATOR.md): independently checked keys, local-repair branches, changed-case checks, deadline checkpoints, and explicit stop/unfinished wording.

The draft targets recoverability, inverse order, and tracking original information. Universal-equivalence proof and arbitrary construction are **explicit extensions**. This narrower core is not the pilot's original four-part outcome. It must not be presented as achieving the same full benchmark criterion faster.

The pilot's repair rule forced another four-task packet after any failed explanation dimension. The revised lesson instead repairs/checks that dimension alone, then checks transfer. Three unrelated reassessment tasks are no longer scheduled automatically after a local slip. At a hypothetical 45-second task allowance that avoids scheduling 135 seconds of unrelated work per such event; that is an accounting example, **not an observed human time saving**. Useful extra questions or responses are welcome.

The new lesson also avoids a coverage weakness: world 617's entry reverse task happened to contain no W, allowing a wrong W-inverse explanation alongside a correct reverse certificate. The human lesson includes W in its first inverse attempt and explicitly tracks the original coordinates through a swap/copy. Every lesson key and valid ambiguity family was checked over all 25 possible inputs.

**No skill rewrite.** The existing skill already prescribes local-slip repair, independent checks, coherent work, and respecting the agreed budget. The waste came from this experiment's full-battery rechecking design, not a demonstrated missing skill instruction. The lesson revision is post-pilot and has **not** been validated on agents or humans. No later run was added to chase a positive result.

## Strengths and remaining weaknesses

- Strong: executable alternative witnesses/programs are accepted; explanation checks catch contradictions hidden by correct numbers; local formula correction visibly worked on a new task; the failed final was not relabeled success.
- Still limited: all executable tasks remained at ceiling; the final construction was simpler than the entry construction; category coverage did not guarantee every operation in every reverse chain. These are not calibrated human difficulty levels.
- Two worlds share one underlying algorithm, with one learner per condition/world. No population, significance, equivalence, or human efficacy claim is supported.
- Open conversation context remained available. This is not unaided or delayed retention. Learners were instructed not to use tools, but tools were not technically disabled and internal traces were unavailable.
- Manual declared-input/reply capture and local hashes cannot authenticate provider execution or resist a writer who can replace all evidence. Integrity assertions require running Python without `-O`.

## Verification

Both Python 3.10 and 3.13 passed:

- **74** existing package tests, zero skips;
- **9** original novel-rule benchmark/recorder tests;
- **5** harder-pilot/lesson tests, including independent matrix-composition checks, task coverage, immutable capture, quoted review consistency, timing-scenario arithmetic, and all human-lesson keys.

The existing 14-case instrument and four-case holdout validate unchanged. The skill, original benchmark reports, frozen pilot source/protocol/data, and actual reply copies are intact. [verification.json](verification.json) records the checks, counts, timing range, and hashes; [results.json](results.json) contains the complete per-run results and timing scenarios. `raw/`, `sessions/`, and `feedback/` preserve the actual evidence. [TEACHING_COMPLETE.md](TEACHING_COMPLETE.md) was recorded before any final packet was opened.

Reproduce from the workspace root:

```text
python -B -m unittest discover -s handoff/benchmarks/time-to-transfer -p "test_*.py" -v
py -3.10 -B -m unittest discover -s handoff/benchmarks/time-to-transfer -p "test_*.py" -v
python -B handoff/benchmarks/time-to-transfer/pilot.py
```

No dependencies, global installation, commits, publication, telemetry, or real learner data were added.

## What would establish actual human efficiency

Use an actual learner's agreed target and deadline, not an assumed ten-minute universal target. In a voluntary trial, time from the first visible instruction through independent changed-case success, counting reading, thinking, responses, feedback, and real waiting. Record failure to meet the deadline rather than extrapolating a success time. A broader claim that this method beats self-study needs a controlled, comparable human study; durable grasp needs a later check as well.

The pilot supports a practical lesson-design correction. It does not yet support “humans learn this within ten minutes.”
