# Implementer brief: adaptive-learn

**Use only after a human approves `handoff/PROPOSAL.md`.** Implement the accepted rows, not the full D-list. If a row is marked Defer or Reject, it is not work.

You are the implementing model. Make the smallest set of verified changes that improves teaching behavior in `adaptive-learn/` without weakening its epistemic honesty. The review is finished; do not re-derive strategy. Execute the approved changes and prove each one.

## Read order

Read in this order. Stop when the next file cannot change your next edit.

1. `handoff/AGENT_BRIEF.md` — scope, ownership, authority.
2. `handoff/DECISIONS.md` — settled decisions. Do not relitigate them.
3. `handoff/NON_GOALS.md` — explicitly out of scope.
4. `handoff/WORK_ORDER.md` — ordered change IDs; this is your queue.
5. `handoff/IMPLEMENTATION.md` — per-change anchors and proposed text.
6. The specific skill files named by the change ID. Nothing else by default.
7. `adaptive-learn/tests/live/` — the cases and rubric that will judge you.

Study the house style before editing. `SKILL.md` uses short declarative rules with concrete fallbacks. `references/` carry nuance. `playbooks/` carry subject specifics. Preserve that division.

## Hard constraints

- **No global install.** Do not copy the skill to `~/.config/opencode/skills/`, `~/.claude/skills/`, or any host skill directory. Do not modify the host configuration.
- **No new dependencies.** Standard library only for Python. No packages, no network calls, no build step, no YAML/JSON schema libraries. If a change seems to need one, stop and report.
- **No whole-file rewrites.** Use targeted edits. Never regenerate `SKILL.md`, a playbook, or `learn_state.py` from scratch. If a file needs more than roughly a third of its lines changed, that is a design problem: stop and report.
- **Preserve voice.** Second person or imperative, short sentences, no marketing adjectives, no emoji, no "simply/just/obviously". Do not add rhetorical questions to instructions. Do not add headings the surrounding file does not already use.
- **No mastery claims.** Never write or imply "mastered", "proficient", percentage mastery, retention probability, or that a single success generalizes. Provisional advancement language only.
- **No learning styles.** No VAK, no "visual learner", no personality or ability labels. Accessibility accommodations are allowed and are not learning styles; do not conflate them.
- **No subject playbooks.** Do not add, split, rename, or delete playbooks. At most two new references, each ≤45 lines, if `WORK_ORDER.md` says so.
- **No schema change without a migration hook.** Any field addition to `state.json` requires the migration path named in `IMPLEMENTATION.md`. A change that bricks an existing workspace is a blocker.
- **No learner data.** Do not create `LEARNER.md`, `.learning/`, or any state file inside the skill directory or the repository. Test fixtures go in temp directories.
- **No unverified factual claims.** Do not add efficacy numbers, study citations, or "research shows" sentences unless `DECISIONS.md` supplies the exact wording and the caveat. Do not claim a test passed unless you ran it.

## Output format

Report one block per change, in the order applied:

```
CHANGE <ID>
file:      <path>
anchor:    <quoted line or nearest heading; line number if stable>
before:    <exact removed text, fenced>
after:     <exact inserted text, fenced>
test:      <command or manual check, and its observed result>
rollback:  <git checkout path | revert hunk description>
```

After all blocks, print:

```
SUMMARY
changes applied:   <IDs>
changes skipped:   <IDs + reason>
tests run:         <command → pass/fail/count>
deviations:        <anything not matching IMPLEMENTATION.md, and why>
open questions:    <only items that block the next phase>
```

Never summarize a change you did not make. Never claim a test you did not run.

## Checkpoints

Stop and report at each phase boundary. Do not start the next phase without an explicit go-ahead.

- **Phase 1 — correctness.** Helper defects, save atomicity, review computation, input validation. Verify with the existing `unittest` suite plus the new regression tests. All prior tests must still pass. Phase 1 changes must not alter prompt text.
- **Phase 2 — teaching.** Answer-key and verification rules, hint ladder, feedback after error, transfer item, self-explanation, precedence ladder, turn-1 block, router. Re-read every edited paragraph against the acceptance cases; name the case IDs that support each rule.
- **Phase 3 — schema and content.** Front matter, privacy and injection text, new references, documentation sync. Confirm `README.md` and `references/` no longer contradict code. Confirm no orphan links.

At each checkpoint report: files touched, tests run, changes deferred, and anything you believe is wrong with the plan.

## Stop conditions

Halt immediately and report, without attempting a workaround, if:

- Two instructions conflict and neither `DECISIONS.md` nor `WORK_ORDER.md` resolves the order.
- A test fails in a way you cannot explain from the diff.
- The fix requires more than the stated line budget, a new file type, or a new dependency.
- The change would delete existing behavior that an acceptance case protects.
- You cannot verify a factual claim the text would assert.
- You find a defect outside the assigned scope. Record it; do not fix it.

## Ask the human before

- Editing `SKILL.md` front matter `description` or `name` — this changes skill discovery.
- Removing or merging any playbook, or reordering the routing table.
- Changing privacy, retention, or data-deletion wording.
- Changing the meaning of an existing test assertion.
- Adding any claim about learning outcomes.
- Touching anything under `adaptive-learn/.git/`.

## Definition of done

Every assigned change has a diff, a check, and a rollback. The full suite passes on the documented Python versions. No constraint above is violated. Deviations are listed, not hidden. Baseline results are cited only if `BASELINE.md` was actually executed; otherwise say "baseline not run".
