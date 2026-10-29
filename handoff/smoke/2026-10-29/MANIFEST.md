# Actual tutoring smoke sessions — 2026-10-29

These are actual subagent replies, not authored sample answers. They are **demos**, not the full live baseline, independently judged results, or evidence of improved learning.

- Editable case: L-09, direct explanation with no saving. No holdout was used.
- Tutor: `opencode-go/deepseek-v4-pro#max`, separate fresh session per run.
- Before source: the approved 36-test working tree, not pristine commit `1485e0b`.
- Before `SKILL.md` SHA-256: `dfb9010ade931210a9885dfb66d2132e31e274ed0cfdebfcfbcb8dcffb363abd`.
- A copy and per-file hashes of all 23 tracked source files were retained in an external temporary source snapshot before further implementation.
- Run 1 session: `ses_e79efc8b4ffeZ9BjqCQY7Ir0zU`; run 2: `ses_e79efc8b2ffeZbPuQWMRky3GPG`.
- Export includes the actual conversational replies. Internal file-read/tool traces are not available in this export, so it cannot establish that the tutor loaded a particular support file or made no tool calls.
- No independent judges, calibrated anchors, learner tests, delayed retention checks, or learning outcomes were obtained. Do not put these demos in measured `runs/` or aggregate them as passes.
- Redaction: the setup's absolute source workspace was replaced with `<workspace>`. There was no learner root or real learner data.

Both tutors received this setup followed by the first learner turn:

```text
Act only as the tutor for this learning session. Working directory <workspace>. Before responding, read adaptive-learn/SKILL.md and only the support files its current instructions call for. Do not read handoff/, research.md, plans, or other agents' output. Do not create or edit any files. Do not use other subagents. Follow the shipped skill normally; answer the learner with your actual tutoring reply, not a simulated transcript or an analysis of the skill. Learner message: Explain quickly why 0.999... equals 1. Don't save anything.
```

The next two learner turns were sent verbatim as separate continuations. Responses in the adjacent files are preserved as returned, including inaccuracies or excessive wording; they are not corrected transcripts.

## Intermediate candidate demos

Two fresh sessions repeated the same setup and learner turns after the first focused core edits. Their core SHA-256 was `04c82b0f712f93fcb5add1d2327861a711d236cd70f260c3be7e8c0694c93f51`. Run 1: `ses_e79e1658dffelbSA409c5MuWuo`; run 2: `ses_e79e1657effe1RYOaDz1vfrUti`. Replies are in `candidate-L-09-run-1.md` and `candidate-L-09-run-2.md`.

These demos still contain verbosity and an incorrect numerical side example. In candidate run 1, tutor turn 2 says seven nines beat a gap of 0.0000001. An exact Python `Fraction` check confirmed `1 - 0.9999999 == 1/10000000`: equal, not smaller. This is not a passing learning result. It prompted one further rule clarification: verify numerical examples and intermediate steps in explanations, not just answers being graded. No holdout was inspected or tuned.

## Final targeted numeric smoke

Final core SHA-256: `4741578910c18e412a9f4d6c5c8c019cfb2964a38803971cce11ad678b991260`. A fresh tutor (`ses_e79d8749cffetuIxRvYLIsfaSe`) received the same tutor-only/no-file/no-handoff setup with this learner message: `I wrote that seven nines, 0.9999999, are closer to 1 than 0.0000001. Is that right? Check it briefly and don't save anything.` The actual reply is in `final-numeric-smoke.md`. It states the correct exact gap. The learner wording is ambiguous about a gap versus comparing two numbers; do not treat this single reply as a calibrated case pass or proof the new rule caused improvement.

All five sessions are recorded, including the numerical mistake. There are no judge scores, full tool traces, blind pairwise results, complete 14-case runs, or learner outcomes here.
