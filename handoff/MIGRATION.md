# Migrating v1 to v2

> Historical four-evidence-field candidate, superseded by the approved pause-only state v2 on 2026-10-29. Do not execute this candidate procedure. See `../adaptive-learn/references/persistence.md` for the implemented in-memory migration, `state.v1.json` backup, unchanged graph format, and recovery limits.

**Scope:** `state.json` and `graph.json` under `<root>/<subject>/.learning/`.
**Rule:** migration happens **in memory on read**. Nothing is written until a save succeeds. A load that only migrates must leave both files byte-identical.

## 1. What migration does

- Sets `format_version: 2` on both files.
- Adds four fields to every evidence record: `hint_level: 0`, `task_id: null`, `error_kind: null`, `transfer: null`.
- `graph.json` gets the version bump only.
- Untouched: nodes, edges, arguments, links, plan, checkpoint, constraints, `revision`, `saved_at`, `reviews`.

`hint_level: 0` is honest for v1: any hint that mattered had to appear in `assistance[]`, which makes the record `assisted` and ineligible for growth anyway. A rung count cannot be recovered; do not call migrated records "unaided".

## 2. Version gate and `_migrate`

Validate the v1 shape **before** adding fields, so a stray v2 field in a v1 file is still an error.

```python
V2_EVIDENCE_DEFAULTS = {"hint_level": 0, "task_id": None,
                        "error_kind": None, "transfer": None}

def _migrate(raw, from_version):
    _require(isinstance(raw, dict), "Expected a JSON object.")
    _require(type(from_version) is int, "format_version must be an integer.")
    _require(from_version in (1, 2),
             "Unsupported learning format; existing data was not reinitialized.")
    if from_version == 2:
        return deepcopy(raw)                     # idempotent
    out = deepcopy(raw)
    out["format_version"] = 2
    for event in out.get("evidence", []):        # state file only
        _require(isinstance(event, dict), "Invalid evidence record.")
        for key, default in V2_EVIDENCE_DEFAULTS.items():
            event.setdefault(key, default)       # fills absence, never overwrites
    return out
```

```python
def _read_versioned(path, v1_keys, v2_keys):
    raw = _read_json(path)
    version = raw.get("format_version") if isinstance(raw, dict) else None
    if version == 1:
        _fields(raw, v1_keys, v1_keys)           # strict v1 shape first
        return _migrate(raw, 1), True            # (data, migrated)
    if version == 2:
        _fields(raw, v2_keys, v2_keys)           # v2 fields required, not defaulted
        return raw, False
    raise LearningError("Unsupported learning format; existing data was not reinitialized.")
```

Then `_validate_state()` / `_validate_graph()` run on the migrated copy. `_load()` returns the `migrated` flag so `resume` can warn. `_validate_graph(root=...)` must use `_read_versioned` for neighbour graphs, or a v1 neighbour breaks validation of a v2 subject.

## 3. Single subject: step by step

1. **Confirm** root and subject. Migration is not a reason to reinitialize; records gain hint, task, error-category, and transfer fields, and nothing is deleted.
2. **Stop other writers.** No concurrent save, no second chat on this subject.
3. **Dry run.** `resume` (read-only). Success proves both files parse, migrate, and validate. Hash both files before and after; they must match.
4. **Record `revision`** from the resume output; the write needs it.
5. **Back up before any write.** Copy `state.json` bytes to `state.prev.json` (atomic temp + `os.replace`). If the update contains `withdrawals`, also copy `graph.json` to `graph.v1.json`: withdrawals are the one non-additive graph change.
6. **Validate** the proposal and the 16 MiB bound before any file write. Abort on failure.
7. **Submit the no-op save** `{"expected_revision": n}`; it is the only step that changes bytes.
8. **Write `graph.json`** if changed, re-read it, revalidate, and re-check that the on-disk state revision is still `n`. The stale check must run **before** the graph write (P-01).
9. **Write `state.json`** at version 2, atomically. Read it back: `format_version == 2`, `revision == n + 1`, all four fields on every evidence record.
10. **Refresh derived views** (`plan.md`, `sessions/`). Failure here is a warning; the canonical save stands.

Taking `state.prev.json` before the graph write means a failed graph write leaves a redundant copy of live state. Harmless.

**Do not** expect identical review output. P1 and P2 change intervals by design, so `due_at` moves. Compare target sets and `last_evidence`; a new interval is intended behavior, not a migration error.

## 4. Existing root with several subjects

1. Enumerate `<root>/*/.learning/state.json`. Ignore `LEARNER.md`, `.gitignore`, `plan.md`, `sessions/`.
2. **Dry-run every subject** before writing any. Cross-subject `links` mean validating B reads A's graph, so a malformed neighbour surfaces here. Fail fast; write nothing.
3. Run `init` for each subject first. It is idempotent, does not reset progress, and is the only operation calling `_privacy()`; `save` does not add ignore rules.
4. Convert **one subject per `save`**, each with its own `expected_revision`. Do not batch.
5. Order does not matter once the loader accepts v1 and v2: after a partial run, converted subjects are v2 and the rest v1, and every reader still works.
6. Report subject, old revision, new revision, warnings. Do not report "all migrated" until every `resume` returns `format_version: 2`.

A failure at subject 4 of 7 leaves 1–3 at v2 and 4–7 at v1. Both are valid; resume each before retrying, and never hand-edit `revision`.

## 5. Rollback

- `state.prev.json` holds the pre-write state, v1 on the first v2 save. Restore it over `state.json` with no writer running, then use the v1 helper.
- `graph.json` needs no rollback for additive changes. If withdrawals were saved, restore `graph.v1.json`.
- Re-running migration is safe and idempotent; after a rollback the retry starts from v1.
- Mid-way failure: `state.json` is old or new bytes, never a hybrid, because replacement is atomic. `graph.json` may be ahead; a retry with the same IDs and `expected_revision` completes it.
- **Downgrade** is unsupported. An older helper refuses `format_version: 2` and leaves the file intact; restore v1 only from a backup.

## 6. Edge cases

| Case | Behavior |
|---|---|
| `format_version` 3+, or a non-integer | Refuse with "Unsupported learning format". No write, no downgrade. The data is newer than the helper. |
| Malformed v1 (bad JSON, duplicate key, unknown key, missing field) | Parse/shape error names the file and key. Nothing written; bytes unchanged. |
| Partially migrated: v2 marker, event missing `transfer` | Reject. A missing value under a v2 marker means a hand edit or interrupted conversion. Restore `state.prev.json`. |
| Partially migrated: v1 event carrying `hint_level` | Reject as an unknown v1 field. Same repair. |
| Duplicate evidence IDs | `_validate_state` rejects. Migration never dedupes; dedupe destroys history. |
| `provisional:<id>` targets | Unchanged. `task_id` is not a target and needs no node. |
| Paused reviews | Carried through untouched. Phase 1 adds a state-level `suspensions` map so a pause survives invalidation of its last evidence (P-04); migration preserves the map, or seeds it from any paused review when the key is absent. |
| v1 state already containing `suspensions` (written after Phase 1) | Accept it: the key is optional and known to this helper. Do not strip it. A previous release's strict reader would reject it, which is why `state.prev.json` exists. |
| Invalidated evidence | Kept verbatim, gains the four defaults, excluded from recomputation. |
| File near 16 MiB | Migration adds roughly 55 bytes per event; a file within a few percent of the cap can fail the size check on save. Condense first; never truncate. |
| Future-dated evidence | Rejected at save by the `at > now + 5 minutes` check (P-07). Migration does not re-timestamp. |
| Mixed versions across files or subjects | Readable. Migration is a pure per-file function. |

## 7. Verification

```text
python -B <skill>/scripts/learn_state.py init   --root <root> --subject algebra
python -B <skill>/scripts/learn_state.py resume --root <root> --subject algebra
python -B <skill>/scripts/learn_state.py save   --root <root> --subject algebra --input -
py -3.10 -B <skill>/scripts/learn_state.py resume --root <root> --subject algebra
```

Expected at a high level, not measured results:

- `init` on existing v1 data returns `initialized: false` and the unchanged revision.
- `resume` returns `format_version: 2`, evidence carrying the four fields, and a migration warning. On-disk bytes are unchanged.
- `save` with `{"expected_revision": n}` on stdin returns `saved: true` and `revision: n + 1`; repeating it exits 2 with a stale-revision error and writes nothing. Afterwards both files report `format_version: 2` and `state.prev.json` exists.
- Python 3.10 and 3.13 give the same shapes; no syntax above 3.10, no new dependency.
- Run the existing suite plus the schema-v2 tests on both interpreters; do not trust a count.

## 8. Do not

- Migrate on load by writing files.
- Rewrite `revision`, `saved_at`, or evidence timestamps.
- Dedupe IDs, drop reviews, or renumber tasks.
- Derive `hint_level` upward from `assistance[]`; prose does not map to rungs reliably.
- Delete v1 backups until a full `resume` cycle has passed on every subject.
