# Iteration outcome: candidate rejected

**Kept the existing core policy.** A candidate time-budget clarification was tested and rejected as an optimization. This pass adds a worked time-budget acceptance case and a reproducible ordinary-chat comparison, not a claimed teaching or human-learning improvement.

## Actual comparison

Seventeen fresh, actual tutor sessions used `opencode-go/deepseek-v4.1-flash#low`: six development replies, two D1 regression replies, and nine fixed confirmation replies. No retries or second candidate. Ordinary chat received a competent tutoring request with the same student messages, case facts, remaining-time statements, and permission to check mathematics.

The original/revised conditions were instructed to read captured full skill sources and the math playbook. All replies, declared prompts, session IDs, source hashes, transcripts, and annotations are retained under `runs/`. File loading and internal tool actions cannot be independently authenticated from the returned final replies; the tool boundary is instruction-based, not sandboxed.

### Development

| Condition | Cases meeting the frozen behavior criteria |
| --- | --- |
| Original skill | 3/3 |
| Ordinary chat | 2/3 |

Both conditions noticed the incorrect explanations and accepted the valid alternative method. Ordinary-chat D1 nevertheless introduced a false extra backward step: after undoing the copy, `(2,y)` must undo the first swap to `(y,2)`, not remain `(2,y)`. Its main forward trace was correct. The failure was retained.

No original-skill local-repair failure was reproduced. The [pre-confirmation decision](DECISION.md) therefore did not add a duplicate diagnostic branch. It tested one clarification of the user's explicit requirement: budget reading, thinking, answers, feedback, and waiting rather than a target number of turns; use measured/reported time rather than invented time. The candidate changed exactly one core line. AC-26 and the README count were updated alongside it.

### Fixed confirmation

| Case | Original skill | Candidate | Ordinary chat |
| --- | --- | --- | --- |
| C1: changed composition and original-variable tracking | PASS | **FAIL** | PASS |
| C2: correct probability with false independence explanation | PASS | PASS | PASS |
| C3: valid alternative operation order | PASS | PASS | **FAIL** |
| **Total** | **3/3** | **2/3** | **2/3** |

The additional D1 before/candidate reruns both passed. They were requirement/regression checks, not a reproduced original-policy failure turned green. Do not pool the unequal development/repeat counts into a misleading overall method ranking.

## What failed and what it means

- **Candidate C1:** its correct table was followed by prose claiming slot 2 contained `u+v` immediately after A. In fact A maps `(u,v)` to `(u+v,v)`, so slot 2 contains `v`. For example `(1,5)` becomes `(6,5)`, not a second-slot value of 6. Its unnecessary six-order discussion also duplicated DBA and omitted BDA. The optional explanation added errors after the main diagnosis was already correct.
- **Ordinary-chat C3:** it accepted the student's valid method, then instructed them to use the worksheet's order on the page despite no stated requirement. This violated the frozen alternative-method criterion.
- **Other concerns retained separately:** revised D1 speculated about why the learner stopped listing pairs; original C2 used imprecise opening probability labels before clarifying the conditional distinction; original C3 offered an unsupported five-second checking estimate and a loose analogy. These concerns were not silently turned into new scoring criteria after seeing the replies. Passing the narrow rubric is not a guarantee of ideal teaching.

This is a small, unblinded, one-reply-per-case check. The orchestrator authored all cases and reviewed the replies. Source context and loading overhead differ. The result does not establish that the timing wording caused the candidate error, that the original skill is generally superior to ordinary chat, or that any student would learn faster. There was no real learner, learner follow-up, delayed recall, preference measurement, or human time-to-understanding result.

The existing independent-check instruction already forbids unverified numerical side examples. A new timing paragraph did not reliably enforce that instruction. More prompt text is not automatically an improvement.

## What was retained

1. **Original core restored byte-for-byte** to the before snapshot, preserving all earlier approved reliability/teaching edits. Only this pass's one-line candidate change was undone; no Git reset or user-work discard.
2. **Worked acceptance case AC-26** in `adaptive-learn/tests/acceptance-cases.md`: time budget rather than a turn quota, preserve verified work, local repair, no invented time or latency-based ability inference. It is design documentation, not a measured result or a new automatic timer.
3. **README count updated to 26** worked cases; the document still explicitly distinguishes walkthroughs from live outcomes.
4. **New comparison and four oracle/audit tests:** exhaustive variable-loss checks, exact root/probability checks, captured-input integrity, and refusal to grade a reply under the wrong case.
5. **All negative evidence:** rejected candidate source, original decision, candidate manifest, failed replies, and literal review quotes. [OUTCOME.md](OUTCOME.md) records the rejection; [final-state.json](final-state.json) identifies the actual retained core. `revision.json` is historical evidence of the candidate at creation time, not the shipped source.

The core therefore has **no new policy change from this iteration**. It would be misleading to describe this as a validated improvement in teaching or a newly installed time-management feature.

## Verification and reproduction

Both Python 3.10 and 3.13 passed **92 automated tests each**:

- 74 existing package tests, zero skips;
- 9 original novel-rule benchmark tests;
- 5 harder-pilot/lesson tests;
- 4 new comparison oracle/audit tests.

The original 14-case instrument/four-case holdout validates unchanged. The earlier benchmark reports recompute exactly; their frozen inputs and actual replies were not changed. Current core SHA-256 is `4741578910c18e412a9f4d6c5c8c019cfb2964a38803971cce11ad678b991260`, matching the preserved before-source. The rejected candidate remains `889afe7b8245c4a47e8436064e2e0b5aceb63d6a8e152f28b18d79a82857a5eb`.

From the workspace root:

```text
python -B handoff/iterations/tutor-vs-chat/check.py
python -B -m unittest discover -s handoff/iterations/tutor-vs-chat -p "test_*.py" -v
py -3.10 -B -m unittest discover -s handoff/iterations/tutor-vs-chat -p "test_*.py" -v
```

The existing checker derives verdicts from complete, quoted annotations; it does not independently judge the reviewer. Run without Python `-O`, because integrity guards use assertions. No new dependency, global installation, commit, publication, persistence change, automatic recording, or real learner data was added.

## Next bounded investigation

Target verification of optional explanations and unsupported claims about the learner, rather than adding another generic local-repair rule. Require an actual reproduced failure, a narrowly motivated change, and fixed fresh checks before keeping it. Separately, a consenting human trial against competent ordinary chat is still needed to assess independent transfer within the learner's real deadline. Do not substitute these tutor-response scores for that outcome.
