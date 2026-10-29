# Lessons

A dated log of prompt-level changes justified by observed live behavior. One entry per lesson. An entry that cannot be checked later is not a lesson.

## Entry template

Copy this block. Keep it short.

```
### L-<nnn> — <one-line claim>

- **Date:** YYYY-MM-DD
- **Trigger:** <case ID>, <run number>, <transcript path>
- **Observed:** <what the tutor actually did, in one or two sentences>
- **Expected:** <what the case required, quoted from the case's `must`/`must_not`>
- **Gap:** <the specific instruction that failed, or its absence, with file:line>
- **Proposed rule:** <the sentence to add, change, or remove>
- **Landed:** <file:line, commit, or `not applied`>
- **Verification:** <case re-run and result, or `unverified`>
- **Falsifier:** <what observation would show this lesson is wrong>
```

Field notes:

- **Observed** describes behavior, not character. "Asked four questions before posing a task" — not "was too Socratic".
- **Gap** must name an instruction or its absence. If no instruction failed, the lesson is about the case, not the skill; say so.
- **Verification** is `unverified` until the triggering case, plus at least one non-triggering case, has been re-run. One clean re-run is not verification; note the run count.
- **Falsifier** is required. If nothing could disprove the lesson, rewrite it as a hypothesis until something could.

## Index

| ID | Date | Claim | Status |
| --- | --- | --- | --- |
| — | — | No lessons recorded. Live runs have not been executed. | — |

## Do not record

- **Learner quotes.** Paraphrase to the behavior. No verbatim personal statements.
- **Names, handles, schools, employers, locations, ages, or anything that identifies a person.**
- **Absolute root paths or host usernames.** Write `<root>`, not a real directory.
- **Unverified generalizations.** "Models always dump hints" is not a lesson; "in L-03 run 2, the second hint turn contained three rungs" is.
- **Model blame without a case.** "The model was lazy" is not evidence and cannot be acted on.
- **Scores without transcripts.** A number with no run behind it cannot be checked.
- **Anything that would let a reader reconstruct a real learner's problem.** Rewrite the case.

## Maintenance

- Append only. Do not rewrite history when a lesson turns out wrong; add a superseding entry and mark the old one `superseded by L-<nnn>`.
- Mark a lesson `rejected` if its falsifier was observed.
- Keep the log under 40 entries. Beyond that, merge duplicates and summarize by failure class.
- Review the log before editing `SKILL.md`. A rule that no lesson supports needs a different justification.
