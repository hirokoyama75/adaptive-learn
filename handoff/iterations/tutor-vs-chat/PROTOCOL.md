# Local repair: skill versus ordinary chat

This bounded iteration tests **actual tutor replies**, not student learning, human preference, or elapsed study time. It does not recruit people or alter earlier frozen experiments.

## Frozen comparison

- Same verified model throughout: `opencode-go/deepseek-v4.1-flash#low`.
- Three development cases, original skill versus competent ordinary chat: six fresh one-reply tutor sessions. The ordinary-chat baseline gets the same student message, source facts, time budget, and permission to check calculations; it is not asked to fail or taught a weak persona.
- Original-skill tutors read the captured full core and primary math playbook. The baseline gets a competent tutoring request without those files. Loading overhead and additional context differ; no pure-latency or equal-token claim is made. File access is instruction-restricted, not sandboxed, and internal tool traces are unavailable.
- Freeze all six student messages and review expectations before any session. Confirmation runs wait until the revision/no-revision decision is recorded. The orchestrator authored the entire new case bank and is not blinded; these are fixed fresh checks, not an independently hidden holdout. Do not change their messages or criteria after seeing development. No existing package holdout is opened or changed.
- At most one small policy revision, only for an observed gap or an explicit user requirement that current instructions do not cover. Prefer replacing ambiguous wording over adding a checklist or a new reference. Do not revise just because the control performs well.
- If revised: rerun the triggering development case with original and revised skill (two fresh sessions), then run all three confirmation cases with original, revised, and ordinary chat (nine sessions). Maximum **17 actual tutor replies**. If no change is justified, confirmation compares original and chat only, for twelve replies total.
- Stop after this pass. No retries, escalation to a more favorable model, repeated revision, silent case changes, or positive-result fishing. Preserve failed/unhelpful replies. One reply per condition/case is exploratory and cannot separate stochastic variation from a policy effect.

## What is assessed

Independent arithmetic/algebra checks establish the case facts before runs. Each case requires: (1) accurate diagnosis or acceptance of a valid alternative, (2) preservation of sound work and a correct local explanation, (3) a proportionate next action that respects the stated remaining time. It forbids false endorsement/new math errors, unrelated foundation resets/full-battery reassessment, and invented timing/permanent mastery/automatic saving.

The orchestrator judges the actual replies against those frozen expectations, with literal assistant quotes for positive observations and violations. The existing package `check_run.py` validates annotations and derives their verdict; it does **not** independently judge semantics. The reviewer is not the tutor session, but is not blinded or independently calibrated. Absent required behavior fails; fabricated or incomplete annotations are invalid. Report all criteria and failures, not only an aggregate score.

Word counts, question counts, or message counts are not learning-efficiency scores. A concise wrong correction fails; a useful extra question may be appropriate. Distinguish one connected local probe from an unrelated test battery. Do not invent how many minutes the response took a student to read or grasp.

## Implementation and claims

Before-state source, prompts, actual replies, session IDs, annotations, and hashes remain outside the skill package. A confirmed small behavior improvement may justify a local implementation, not a claim of faster human learning or superiority over regular chat. When both methods meet expectations, report the tie. A human time-to-transfer comparison remains necessary for the user's broader preference goal.

No dependencies, automatic learner-data collection, persistence-schema change, global install, commit, or publication. Preserve all prior uncommitted work. Integrity checks run without Python `-O`.
