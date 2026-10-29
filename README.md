# Adaptive Learn

A tutoring skill for OpenCode that adjusts explanations, hints, and practice to the work you show. Study for class, cram, or learn in depth, with optional progress across chats.

**Experimental:** file handling has automated tests, and limited synthetic tutoring checks are recorded below. Better or faster human learning has not been demonstrated. Correct feedback and lasting mastery are not guaranteed.

## Quick start

Open the folder containing `SKILL.md` in OpenCode and ask:

> Read SKILL.md and help me learn linear equations for class. Start with a useful problem. Use session-only learning for now.

You can request practice, review, or a direct explanation. Supply relevant notes, assignments, or exam materials. There is no compulsory placement test or long intake interview.

You need OpenCode with a configured model. Saving and resuming require Python 3.10 or newer, with no extra packages. Session-only tutoring can work without Python. Git is optional for privacy checks.

Local use does not require global installation. If you later want automatic skill discovery, see [installation](#installation).

## Choose how you want to study

| Goal | What the tutor prioritizes | Example request |
| --- | --- | --- |
| Cramming | Useful coverage within your available effort, important gaps, concise examples, and exam-like practice. It should say what remains uncovered. | "I have 45 minutes to cram these objectives." |
| Learning for class | Your course material and assessment criteria, with enough understanding to apply ideas independently and recall them later. | "Help me understand this week's lecture and practise for the assignment." |
| Learning in depth | Explanations, mechanisms, connections, unfamiliar applications, and the limits of an idea. | "Help me understand why this works, including when it stops working." |

Switching goals preserves recorded progress. Help still depends on your work: a beginner can study in depth, and an experienced learner can cram. An exam paper alone establishes neither urgency nor complete coverage.

### In-depth learning and the Feynman-inspired activities

The tutor can work through these activities where useful:

1. Explain the idea in everyday language with a concrete example.
2. Find a missing step or unclear term, teach it, and improve the explanation.
3. Apply the idea independently to a new case.
4. Test assumptions, counterexamples, or a different application.

Skip activities you have already demonstrated. These are not mastery scores; explaining fluently does not prove you can apply an idea. See [study goals](references/study-goals.md).

## The learning workflow

```mermaid
flowchart TD
    A["Your goal and supplied material"] --> B["Reuse context and choose a starting point"]
    B --> C["Explain or practise one connected task"]
    C --> D["Check the work and adjust the help"]
    D --> E["Continue, move on, or stop"]
    E -->|Continue learning| C
    E -.->|After other work or time| F["Recall an important idea in a new situation"]
    F --> D
    C -.->|Saving enabled| G["Save the task, hints, and next step"]
    E -.->|Saving enabled| G
    G -.->|Next chat| B
```

The tutor reuses known information and skips redundant steps. You should have room to work through a meaningful task without constant interruption.

1. **Choose a useful target:** something you should be able to do. Ask only clarifications that change the next action.
2. **Start near that task:** a representative attempt can reveal where to begin. If you cannot start, explain or demonstrate enough to help.
3. **Teach the blocking part:** use examples, direct instruction, or useful questions. Define unfamiliar terms and symbols before relying on them.
4. **Reduce help when ready:** move from examples or partial tasks toward independent work, skipping support you no longer need.
5. **Move on for now, then revisit:** independent success supports progress. Important correct answers, errors, and assisted successes can all need later review.

Practice works under any goal. Named-method drills teach execution; later tasks can test choosing the method. An immediate copy after a hint does not establish later recall.

## How the tutor chooses the next move

```mermaid
flowchart TD
    A["Your answer or attempt"] --> B{"Question or feedback challenged?"}
    B -->|Yes| C["Recheck assumptions and feedback"]
    C --> D{"What does the attempt show?"}
    B -->|No| D
    D -->|Sound and independent| E["Move on for now"]
    D -->|Correct with help| F["Reduce help on a comparable task"]
    D -->|Small slip| G["Correct that step"]
    D -->|Blocked or missing an idea| H["Explain or model the missing move"]
```

The tutor should make these decisions without a repeated questionnaire. Ambiguous work may need one useful follow-up.

- Typing speed and confidence alone do not establish understanding. Hint-assisted success remains assisted evidence.
- Objective problems need checked solutions. Writing, interpretation, and design need relevant criteria that allow defensible alternatives.
- Wrong tutor feedback should be acknowledged and corrected in affected records and reviews.
- Unfinished thinking stays on the current problem. You can request hints, the solution, a different pace, a skip, or a break.

Stop at your agreed task or budget without clearing every due review. See [teaching decisions](references/teaching-decisions.md) and [worked acceptance cases](tests/acceptance-cases.md) for examples.

## How it handles different subjects

The tutor chooses the kind of work, then reads one short subject guide. It adds another only for a specific need. A proof and a composition need different ways of judging a good answer.

The [guide index](SKILL.md#route-by-task-then-subject) covers mathematics, sciences, engineering, business, medicine, music, languages, writing, humanities, and coding, plus a general fallback. Mixed topics keep one progress record rather than duplicating attempts across folders.

Supplied sources come first; uncertain, disputed, or current claims may need checking. Research is not compulsory before every explanation. Tool limits must be stated: text cannot establish pronunciation or musical performance. Medical cases are educational, not patient-specific care.

## Optional memory across chats

Session-only learning creates no learner files. To keep progress, choose a separate learning folder and confirm it with the tutor before the first save.

```text
my-learning/
  LEARNER.md                 shared context and preferences
  algebra/
    .learning/
      state.json             current task, learner evidence, and reviews
      state.v1.json          original v1 state, only when upgrading an old workspace
      graph.json             reusable ideas and optional relationships
      plan.md                current path, not a competence score
      sessions/              short dated summaries, not full transcripts
```

`state.json` holds the active task, prepared answer or assessment criteria, your attempt, hints, remaining difficulty, and next action. Plans and summaries provide context; detailed graphs are optional.

State format 2 adds durable pause decisions only; graph and profile formats remain version 1. Old state is read without rewriting it. Its first successful save preserves `state.v1.json` before upgrading; older helpers refuse the new state. See the [migration and recovery contract](references/persistence.md#safe-writes-and-recovery) before upgrading an existing folder. A state backup is not a rollback of subsequent graph changes.

For manual setup, run these from the folder containing `SKILL.md`. Learner files go in a separate sibling folder:

```text
python scripts/learn_state.py init --root "../my-learning" --subject algebra
python scripts/learn_state.py resume --root "../my-learning" --subject algebra
```

For the next chat, give the confirmed folder's path:

> Read SKILL.md and resume algebra from my learning folder at `<path>`. Continue the saved task and keep its earlier hints in mind.

Resumption loads the current task and selected relevant progress, with omitted material counted. The active task is never silently cut to fit. Saving does not clear chat context. At a break, consider a fresh chat or compaction (summarizing older messages), if your host supports it.

Reviews use a simple scheduling rule, not a memory prediction. The default view suggests at most three; you can defer or pause them. There are no background notifications.

The [persistence reference](references/persistence.md) covers saving, file formats, corrections, and recovery. Tutoring does not require you to edit JSON yourself.

## What each file does

| File | Responsibility |
| --- | --- |
| [SKILL.md](SKILL.md) | Instructions for starting, teaching, feedback, practice, routing, and continuity. |
| [Study goals](references/study-goals.md) | Explains the three goals and in-depth activities. |
| [Teaching decisions](references/teaching-decisions.md) | Gives examples of choosing support and correcting tutor mistakes. |
| [Python helper](scripts/learn_state.py) | File validation, checkpoints, review records, and selected context for resumption. |
| [Worked acceptance cases](tests/acceptance-cases.md) | Expected behavior in 26 situations, including time budgets, alternative answers, and new-chat recovery. |

Subject guides advise the same assistant; they are not separate teachers. The diagrams describe model instructions. Python handles records and cannot establish understanding or execute the teaching decision tree.

## Privacy and limits

- Keep learner records out of the repository. Setup adds narrow Git ignore rules and checks tracking when Git is available. Existing tracking and conflicting rules produce warnings, not automatic removal or overwrites. Inspect before sharing.
- OneDrive or other cloud folders may sync local files. Your model provider can process active context. The helper does not upload records; private details must stay out of research queries. Sharing and export are opt-in.
- Use one writer. There is no multi-writer lock or cloud-conflict handling. Invalid formats and failed saves should be reported, with session-only tutoring available instead of deleting or resetting data.
- Unsaved work can be lost. There is no automatic transcript capture, secure exam proctoring, or automatic history deletion. Forgetting requests need a clear scope and cannot guarantee erasure from host history or backups.
- The model can still misgrade work or misjudge your level. Instructions cannot guarantee compliance.

## Testing and release status

From the folder containing `SKILL.md`, run:

```text
python -B -m unittest discover -s tests -v
```

All 74 tests passed on Windows with Python 3.10 and 3.13, with no skips: 51 state/CLI regressions and 23 evaluation-checker tests. They cover file handling, version migration/recovery, pause durability, review scheduling and selection, corrections, bounded reads/resumption, privacy warnings, commands, and judgment validation. Git checks use temporary repositories. Checker tests use explicitly authored synthetic fixtures, not learner outcomes.

The 26 acceptance cases are worked examples, not results from live tutoring sessions. Passing file tests does not establish teaching quality or learning effectiveness.

Before a stable release, exercise the [acceptance cases](tests/acceptance-cases.md) in real chats, especially these:

- A beginner who cannot start and does not know a needed term.
- An experienced learner who should skip basic questioning.
- A limited-time cram session with incomplete exam scope.
- In-depth learning where a fluent explanation fails on a new problem.
- A valid alternative answer or a credible challenge to wrong tutor feedback.
- A fresh-chat resume that preserves the exact task and earlier hints.

Record the model, available tools, input, actual response, and deviations. These checks assess workflow, not improved learning outcomes. A dedicated repository can host the experimental version while testing continues.

The [14-case live instrument](tests/live/cases.json) and [rubric](tests/live/rubric.md) are included. Check its frozen holdout with `python -B tests/live/check_cases.py --verify-holdout`. `tests/live/check_run.py` checks complete judge annotations and quoted transcript evidence; it cannot decide whether the judge is right, verify unrecorded tool calls, or measure learning. A refusal-only response cannot pass merely by avoiding violations. Fixture passes are parser/scorer checks, not live tutoring results.

To evaluate learning, prepare independently checked criteria/answer keys and comparable unseen tasks before tutoring. Check unaided performance before, immediately after, and after a meaningful gap; keep hints and allowed aids separate. Use matched tasks and a controlled comparison before attributing a gain to this skill. Judge accuracy, transfer, and later recall rather than confidence or fluent explanations. Keep any voluntary learner records outside this repository; no automatic collection is provided. Successful file tests or a few synthetic model conversations establish none of those outcomes.

## Improvement process and results

We started with reproducible reliability bugs, then tested teaching behavior rather than assuming that more tutoring instructions would help. Failures and rejected changes are included in the [published evidence archive](handoff/PUBLICATION.md).

### 1. Reproduce bugs before fixing them

Independent code audits and failing regression tests guided the reliability pass. Fixes cover stale saves changing the graph before refusing, lost review obligations, pause durability, chronology, bounded reads, and honest reporting of partial saves. A minimal state-format migration preserves the original v1 backup before upgrading. The package suite grew from 30 to 74 tests; those tests validate software behavior, not student learning. See the [implementation report](handoff/IMPLEMENTATION_RESULTS.md) for the changes, executed checks, and remaining single-writer/nontransactional limits.

Teaching safeguards were also tightened: check numerical examples and grading, distinguish assisted success from independent work, correct tutor errors transparently, and treat instructions embedded in supplied documents as data rather than permission to run commands. These remain model instructions, not guarantees.

### 2. Freeze questions, preserve actual replies, and compare alternatives

Synthetic learner/tutor runs used DeepSeek V4.1 Flash at low effort. Earlier code audits used DeepSeek V4 Pro at maximum effort. Low effort was not treated as a human-novice model. Task facts were independently checked, protocols and scoring were fixed before runs, and unsuccessful replies were kept.

| Experiment | Observed result | What we learned |
| --- | --- | --- |
| [Novel invented rules](handoff/benchmarks/novel-rules/RESULTS.md): 12 learner sessions, 48 replies | Tutoring and worked-example self-study each got 32/32 valid unseen items correct; no instruction got 0/32 | The task was at ceiling. It showed no incremental tutoring benefit. |
| [Harder concept pilot](handoff/benchmarks/time-to-transfer/RESULTS.md): 4 learners, 12 replies | All final task answers were correct, but the explanation-plus-transfer criterion was met by tutoring **1/2** and self-study **2/2** | Correct numbers can hide incorrect explanations. The pooled 3/4 was not a tutoring advantage. |
| [Tutor versus competent ordinary chat](handoff/iterations/tutor-vs-chat/RESULTS.md): 17 actual tutor replies | On three fixed confirmation cases, original skill passed **3/3**, candidate **2/3**, ordinary chat **2/3** | The new timing paragraph was not an improvement worth shipping; we rejected it and kept the original core. |

These small, exploratory checks do not establish general superiority, statistical reliability, or human learning gains. They retain conversation context, and their internal tool traces are unavailable. Review annotations and quote checks are not independently calibrated human judgments.

### 3. Optimize useful learning time, not message count

The harder pilot checked workload under explicit reading/attempt-time assumptions. Most paths did not fit a ten-minute reference budget even before live tutor waiting. Those were **unvalidated timing scenarios**, not measured student learning times. Useful extra exchanges can be worthwhile; fewer prompts alone do not mean more efficient learning.

That finding informed a [shorter human lesson draft](handoff/benchmarks/time-to-transfer/HUMAN_LESSON.md): repair the affected step, check it, then use a changed case instead of repeating an entire assessment. Its core is explicitly narrower than the full pilot outcome and has not been validated with people. Worked acceptance case AC-26 records the time-budget requirement. The rejected candidate remains archived, not installed as the current policy.

### 4. Keep the boundary between engineering and learning evidence

Reliability and evaluation coverage improved. We also hardened report capture so prompts, grades, session continuity, and quoted judgments can be checked against recorded evidence. We have **not** shown that students learn faster, retain more, or should prefer this skill over regular chat. The next meaningful evidence would be a voluntary, timed human comparison on real course material, with independently graded unfamiliar questions and a later recall check.

To reproduce the published software checks and recorded reports without calling any models:

```text
python -B scripts/check_research.py
```

This runs **92 tests**: 74 package tests and 18 research/oracle/recorder tests, followed by archive, holdout, and report-integrity checks. The [publication guide](handoff/PUBLICATION.md) explains historical workspace paths, source hashes, privacy redactions, and reproduction. The [research notes](research.md) are historical, unverified authoring material, not a source of validated efficacy claims.

## Installation

Nothing has been globally installed. For automatic discovery, copy the folder containing `SKILL.md` to your configured OpenCode skill location, commonly `~/.config/opencode/skills/adaptive-learn`. Check for an existing skill before copying, and keep learner files elsewhere. No installer is required.

## Sources and license

See [PROVENANCE.md](PROVENANCE.md) for the reference projects, research guide, and reuse limits. They are not runtime dependencies, and their licenses do not automatically license this project.

The project's original code and documentation are licensed under the [Apache License, Version 2.0](LICENSE). Copyright 2026 hirokoyama75. See [NOTICE](NOTICE) for attribution and keep learner records out of uploads.
