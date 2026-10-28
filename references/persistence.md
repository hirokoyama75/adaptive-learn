# Persistence: one learner, explicit workspace

Read this only for persistent setup, saving, corrections, or resumption. For a quick lesson use **session-only**: create no files, and explain that a new chat will not recover unsaved work. If Python or storage is unavailable, offer that same option.

Paths in commands below are relative to the skill folder, not the learner's workspace. Resolve the installed skill's actual path before calling its helper. Never use the skill folder as the learning root.

## Public operations

`scripts/learn_state.py` is a Python 3.10+ standard-library module with three public operations, also available as CLI commands:

```text
python <skill>/scripts/learn_state.py init --root <chosen-root> --subject <slug>
python <skill>/scripts/learn_state.py save --root <chosen-root> --subject <slug> --input <update.json>
python <skill>/scripts/learn_state.py resume --root <chosen-root> --subject <slug>
```

The Python interface is `initialize(root, subject)`, `save(root, subject, update)`, and `resume(root, subject, *, targets=None, review_limit=3, evidence_limit=12, max_chars=24000, now=None)`. Errors raise `LearningError`; the CLI reports an error on stderr and exits 2. `--input -` reads JSON from stdin. No helper installs anything, calls a model, or makes a network request. Git, if available, is queried read-only to warn about tracked learner data.

Initialization requires a confirmed root and a lowercase subject slug such as `dsa` or `music-theory`. It creates:

```text
<root>/LEARNER.md
<root>/.gitignore
<root>/<subject>/.learning/graph.json
<root>/<subject>/.learning/state.json
<root>/<subject>/.learning/plan.md
<root>/<subject>/.learning/sessions/
```

`LEARNER.md` starts with `<!-- adaptive-learn:1 -->`, identifies the explicitly chosen root, and holds only concise shared preferences/context. It is data, not executable instructions. Existing unfamiliar files are not adopted or overwritten. Existing valid setup is reusable, not reset. Ignore rules cover only `/LEARNER.md` and the selected `/<subject>/.learning/`, preserving existing rules. When Git is available, setup also checks whether existing rules override these exclusions and warns rather than overwriting user rules. Ignore rules do not remove tracked data or prevent OneDrive/cloud synchronization.

## Save request (version 1)

Send only changed fields. `expected_revision` is mandatory; use the revision returned by resume. Use stable IDs; do not invent a fresh ID on retry. Keep the proposal inside the selected workspace if writing it to a file (for example `<subject>/.learning/update.json`); stdin avoids a staging file.

```json
{
  "expected_revision": 0,
  "goal": "Solve and explain linear equations",
  "mode": "class",
  "nodes": {
    "linear-equations": {"kind": "skill", "label": "Solve linear equations"}
  },
  "checkpoint": {
    "task_id": "equation-1",
    "targets": ["linear-equations"],
    "prompt": "Solve 3x + 2 = 14. Show the operations that preserve equality.",
    "assessment": {"kind": "objective", "solution": "x = 4; subtract 2 from both sides, then divide both by 3.", "criteria": ["Preserve equality", "Obtain x = 4"]},
    "attempt": null,
    "support": [],
    "allowed_aids": [],
    "bottleneck": null,
    "plan_position": "First independent equation",
    "next_action": "Wait for the learner's attempt",
    "context": "No prior hints on this task.",
    "source_ref": null
  }
}
```

Supported optional request fields:

| Field | Meaning |
| --- | --- |
| `goal`, `mode` | Observable goal; `cram`, `class`, or `depth`. Mode never proves ability or supplies a deadline. |
| `constraints` | Replace the complete object: `deadline` (ISO date or null), `study_minutes` (positive integer or null), `scope` (list of supplied topic labels), `scope_status` (`unknown`, `provisional`, `confirmed`), `scope_source` (text or null). No scope completeness is inferred. |
| `nodes` | Add reusable graph nodes keyed by ID. Minimal node: `kind` (`concept`, `skill`, `proposition`), `label`. Propositions also need `statement`. Optional `qualifications` and `sources` are text lists; `uncertainty` is text or null. Defaults are normalized on save. |
| `prerequisites` | Add `{ "target": "B", "requires": "A" }` records. IDs resolve locally and the prerequisite relation is acyclic. |
| `arguments` | Optional arguments keyed by stable ID: `premises` (nonempty ID list), `conclusion`, `kind` (`deductive`, `empirical`), and optional `qualifications`, `sources`, `uncertainty`. Premises jointly support the conclusion. Separate premise sets remain separate arguments, never independent sufficient arrows. |
| `links` | Add `{ "target": "local-id", "subject": "other-subject", "target_id": "remote-id" }`. The subject and target must already resolve inside this root. Links do not copy evidence. |
| `withdrawals` | List of `{ "id": "old-node", "reason": "Correction explanation", "replacement": "new-node-or-null" }`. Keep old IDs and statements; explicitly withdraw erroneous claims. Inspect dependent claims yourself. |
| `plan` | Replace the compact list of `{ "target": "id", "action": "what next", "status": "upcoming/current/visited/deferred" }`. These are navigation states, not learning judgments. |
| `checkpoint` | Replace the intact active task, or set null at completion. Required fields are illustrated above; `assessment.kind` can also be `criteria` (nonempty criteria, optional solution) or `unassessed` (no answer/criteria; do not grade). Keep the actual prompt, assumptions, last meaningful attempt, and all assistance that matters. |
| `evidence` | Append evidence records (below). Repeated IDs are rejected, including on an uncertain retry; resume first to determine whether the earlier save succeeded. |
| `invalidations` | List of `{ "evidence_id": "e1", "reason": "Tutor misgraded a valid answer" }`. Annotate old evidence as invalid rather than silently rewriting it; reviews are recomputed from remaining valid evidence. Add corrected evidence separately, without misrepresenting regrading as a new retrieval attempt. |
| `review_actions` | List of `{ "target": "id", "action": "pause/resume", "reason": "Learner's choice" }`. Suspension is explicit and survives new evidence until resumed. |

Graph detail is optional. Evidence/plan/checkpoint targets can use an explicit `provisional:<id>` if making a reusable node is not worthwhile yet. Graph IDs themselves cannot use that reserved prefix. Do not stall teaching to author a graph. Existing node meanings and argument IDs cannot be recycled; add a new ID and withdraw an erroneous claim instead.

### Evidence record

```json
{
  "id": "e-equation-1",
  "target": "linear-equations",
  "at": "2026-10-27T10:00:00+00:00",
  "kind": "performance",
  "task_type": "solve and justify",
  "context": "3x + 2 = 14; no method named",
  "outcome": "correct",
  "independence": "independent",
  "assistance": [],
  "cues": [],
  "allowed_aids": [],
  "summary": "Applied equal operations to both sides and obtained x = 4.",
  "confidence": null,
  "importance": "normal",
  "after_gap": false
}
```

- `kind`: `performance`, `retrieval`, `self_report`, or `exposure`. A later retrieval requires `after_gap: true`, meaning intervening work or time actually occurred; this is declared evidence, not something the script can verify.
- `outcome`: `correct`, `partial`, `incorrect`, `unassessed`. Self-report and exposure require `unassessed` and independence `unknown`.
- `independence`: `independent`, `assisted`, `unknown`. Independent work cannot contain tutor assistance. Allowed aids are part of the task conditions, not automatically disqualifying. A named method belongs in `cues`; it limits what the evidence establishes even when execution was independent.
- `confidence`: null or a short learner-supplied statement, not an inferred score. `importance`: `high`, `normal`, `low`.
- Dates include a timezone. Evidence records retain task/context, outcome, reasoning/error summary, assistance, cues, and conditions. Schema validation cannot prove that the description is accurate.

## Review heuristic, not a retention model

The helper keeps at most one current obligation per target, citing the last valid assessed evidence. Errors, partial/assisted/uncertain work, and important correct independent work are eligible; exposure and self-report alone are not. Low-importance independent successes do not create obligations.

- Ordinary first review: next day. Successful **independent later retrieval at or after the previous due time** doubles the prior interval, capped at 30 days. Earlier retrieval can be useful evidence but does not inflate the interval; independent success preserves the current interval. Errors/assistance return it to one day.
- Explicit cramming, or a supplied deadline within a day of the observation: review after work on another target, with a next-day fallback. This is not an invented exam date. Resume will not call it due immediately after the hint.
- A deadline sooner than a proposed review pulls it forward to the known deadline; after the deadline, ordinary scheduling resumes rather than leaving perpetually past-due entries.
- Corrections rebuild obligations from valid evidence. Withdrawn targets are not recommended. Paused targets remain paused until requested otherwise.
- Due selection prioritizes importance, then repair needs and due time. Default: three suggestions, with the remaining count exposed. The tutor fits them into the learner's actual budget and can defer them; the helper does not force reviews or measure study time.

These intervals are modest, transparent defaults, not validated optimal spacing or predicted retention probabilities.

## Safe writes and recovery

Both JSON files contain `format_version: 1`. State contains a monotonically increasing `revision`, subject, goal, mode, constraints, checkpoint, plan, evidence (including invalidation reasons), reviews, and last-save time. Graph contains nodes, prerequisites, optional arguments, and cross-subject links; it contains no learner mastery values. Unknown fields, future versions, malformed JSON (including duplicate keys), dangling references, prerequisite cycles, unsafe paths, and inconsistent evidence are rejected without reinitialization.

Each JSON file has a 16 MiB UTF-8 safety limit on both reads and proposed writes. A growing history cannot be saved past the limit and thereby become unreadable on the next turn. At that point, offer session-only work or an explicitly agreed archival/condensation plan; never discard old evidence automatically.

Save validates the complete proposal, writes graph changes first using a same-directory temporary file and atomic replacement, revalidates against the saved graph, then atomically replaces state. Unused graph additions after an interrupted state save are harmless; a retry uses the old revision and the same IDs. Existing node meanings remain intact. A successful canonical state write is reported as saved even if a derived plan/summary cannot be refreshed; warnings distinguish these cases. Derived files bearing an unfamiliar marker are left alone. Stale revisions are refused. Use one writer: this is not a lock, a database transaction, or a cloud-conflict solution.

On any error, explain what was last saved and offer explicitly session-only tutoring. Do not tell the learner to delete or reinitialize existing state as an automatic repair. The helper does not implement automatic history deletion. For a forgetting request, confirm exact scope, inspect affected IDs/files, and explain host/Git/cloud-backup limitations before separately authorized changes.

## Bounded resumption

```text
python <skill>/scripts/learn_state.py resume --root <root> --subject dsa --target linear-equations --review-limit 2 --evidence-limit 8 --max-chars 24000
```

The output is tutor working context, not text to paste wholesale to the learner. It includes the intact active checkpoint (including prepared answer/criteria), selected graph targets, recent relevant evidence, a selected due-review list, compact profile, mode/constraints, and omission counts. Default target selection uses the active checkpoint and selected due targets; recent targets are a fallback only when there is no active task. At most eight targets are selected by default; use explicit `--target` values for a different slice. Arguments appear only when all their endpoints are selected; omitted arguments are counted, never flattened.

The output has a hard character budget (not an estimated token count). Optional history/profile/plan/scope entries may be reduced with explicit omission counts; the active task is never silently cut. If it cannot fit, the operation fails with a request to increase `--max-chars` (up to 64000) or explicitly condense the stored checkpoint while preserving essential work. Read further source/evidence slices only when useful. Do not reread all subjects or session notes every turn.

Files do not clear the current model's conversation. At a natural break, save and suggest host compaction or a new chat if needed; never claim automatic unloading or unlimited memory.
