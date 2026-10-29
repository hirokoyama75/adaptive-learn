# Schema v2: four evidence fields

> Historical candidate, not the implemented format. On 2026-10-29 the user approved a smaller pause-only state v2. It adds only `suspensions`; graph/profile remain v1. The actual contract and recovery limits are in `../adaptive-learn/references/persistence.md`. The four evidence fields below were not adopted.

**Applies to:** `adaptive-learn/scripts/learn_state.py`, `references/persistence.md`, `tests/test_state.py`.
**Status:** the single field contract for v2 *if v2 is adopted*. No other fields in this version.

## 1. What changes

`format_version` goes from 1 to 2 in both `state.json` and `graph.json`, and exactly four fields are added to **evidence records**. One state-level key, `suspensions` (target → reason), ships earlier in Phase 1 as an optional forward extension; it is not an evidence field and does not change the four-field count. Everything else keeps its shape: graph keys, review keys, ID grammar, 16 MiB cap, strict unknown-field rejection.

`suspensions` exists because a pause is a learner decision, not evidence: when invalidation removes the last evidence for a target, the derived review disappears and the pause with it. Absence of the key means `{}`. A file containing it is readable by this helper, but a previous release with strict v1 validation will reject it; `state.prev.json` is the rollback for that case.

Two invariants survive. `reviews` stay **derived**: recomputed from evidence on read and on save, never trusted as truth. No review field is added; a re-teach obligation lives in the existing free-text `reason` plus `interval_days`. No mastery value, retention probability, latency, or confidence score is stored or claimed.

## 2. Fields

| Field | Type | Constraint | Request default | Migration default | Stored v2 |
|---|---|---|---|---|---|
| `hint_level` | integer | `type(x) is int`, `0..5` | `0` | `0` | required |
| `task_id` | string or null | `_id` grammar `[A-Za-z][A-Za-z0-9_.:-]{0,79}` | `null` | `null` | required |
| `error_kind` | string or null | one of 7 exact literals | `null` | `null` | required |
| `transfer` | string or null | `same`, `related`, `novel` | `null` | `null` | required |

`error_kind`: `missing_knowledge`, `mistaken_model`, `method_selection`, `execution_slip`, `ambiguous_wording`, `cognitive_load`, `tutor_or_item_error`. Lowercase, no aliases.

`transfer`: `same` = same task repeated, not transfer; `related` = same structure, new surface, method unnamed; `novel` = unfamiliar surface, no method cue; `null` = unclassified, never inferred.

`hint_level` counts ladder rungs delivered **on this task before the recorded attempt**: 0 none, 1 draw attention, 2 suggest pattern, 3 identify relevant idea, 4 outline a move, 5 demonstrate a step. It is an ordinal, not a measurement; a named method belongs in `cues`.

## 3. Validation rules

Enforced in `_evidence()` for appended records and again in `_validate_state()` for stored ones.

1. **Exact types.** `type(hint_level) is int`; reject `True`, `2.0`, `"2"`. The other three are `str` or `None`.
2. **Requests may omit; stored files may not.** Missing keys are filled with the request defaults before validation, as `_node()` does. A stored v2 record missing any of the four is a partially migrated file (§7).
3. **Range.** `0 <= hint_level <= 5`.
4. **`error_kind` requires a negative outcome.** Non-null only when `outcome in ("incorrect", "partial")`. A corrected attempt is a new record.
5. **Diagnosis is provisional.** Nothing validates that the label is right. `tutor_or_item_error` is the escape hatch and normally accompanies an `invalidations` entry.
6. **Unassessed kinds carry none of it.** `kind in ("self_report", "exposure")` requires `hint_level == 0`, `error_kind is None`, `transfer is None`.
7. **`novel` means the method was not supplied.** `transfer == "novel"` requires `cues == []`. `same` and `related` are unconstrained.
8. **`task_id` is not a target.** No graph lookup, no `provisional:` prefix rule. Evidence from the active checkpoint reuses `checkpoint.task_id`; earlier tasks keep their own IDs, so a mismatch is legal.
9. **No coupling with `independence`.** `hint_level > 0` with `independence: "independent"` is accepted, because a hint may be offered and unused. §6 makes the scheduler conservative instead of rejecting the record.

## 4. Where each field is used

| Field | Teaching use | Evidence it changes | Scheduling use |
|---|---|---|---|
| `hint_level` | Enter the ladder at the rung the attempt implies; one rung per turn; stop laddering after an error and give the answer plus a why. | Separates unassisted production from guided success. | Growth gate (`== 0`). `>= 1` shortens spacing without counting as a lapse. |
| `task_id` | Groups attempts at one item so "third try" is visible. | A within-task trend, not independent samples. | Attempt count in `reason` only; no interval effect. |
| `error_kind` | Chooses the repair: teach, confront with a discriminating case, interleave confusables, one targeted redo, restate the item, shrink the load, or correct yourself. | One auditable label instead of an unrecorded diagnosis. | Non-learner kinds do not increment the lapse streak and cannot trigger re-teach. |
| `transfer` | One `related`/`novel` item before "move on". | Separates repeat success from transfer. | `null`/`same` grows the interval but never satisfies the move-on gate. |

## 5. Example

`state.json` fragment at v2:

```json
{
  "format_version": 2,
  "revision": 7,
  "subject": "algebra",
  "goal": "Solve and justify linear equations",
  "mode": "class",
  "constraints": {"deadline": "2026-11-14", "study_minutes": 45, "scope": ["one-variable equations"],
                  "scope_status": "provisional", "scope_source": "Supplied practice paper"},
  "checkpoint": {
    "task_id": "eq-4", "targets": ["linear-equations"],
    "prompt": "Solve 7(x - 1) = 4x + 5 and justify each step.",
    "assessment": {"kind": "objective", "solution": "x = 4; expand, subtract 4x, add 7, divide by 3.",
                   "criteria": ["Preserve equality"]},
    "attempt": null, "support": [], "allowed_aids": [],
    "bottleneck": null, "plan_position": "Uncued transfer item after one sound success",
    "next_action": "Wait for the learner's attempt", "context": "No rungs given on this task.",
    "source_ref": null
  },
  "plan": [{"target": "linear-equations", "action": "Uncued transfer item", "status": "current"}],
  "evidence": [
    {
      "id": "e-eq-3", "target": "linear-equations", "at": "2026-10-28T09:40:00+00:00",
      "kind": "performance", "task_type": "solve and justify",
      "context": "4(x - 1) = 2x + 6; no method named",
      "outcome": "correct", "independence": "independent", "assistance": [], "cues": [],
      "allowed_aids": [], "summary": "Expanded, collected terms, divided, checked by substitution.",
      "confidence": "fairly sure", "importance": "normal", "after_gap": true,
      "hint_level": 0, "task_id": "eq-3", "error_kind": null, "transfer": "related",
      "invalidated": null
    }
  ],
  "reviews": [],
  "saved_at": "2026-10-28T09:41:12+00:00"
}
```

Derived review after that save (not stored truth):

```json
{"target": "linear-equations", "reason": "Review: independent success", "last_evidence": "e-eq-3",
 "due_at": "2026-10-29T09:40:00+00:00", "after_evidence_id": null, "interval_days": 1,
 "importance": "normal", "paused": false, "pause_reason": null}
```

An earlier review due 2026-10-27 would double to 2.

## 6. Review and scheduler implications

Recomputed in `_reviews()` from evidence:

- **sound** = `outcome == "correct"`, `independence == "independent"`, `hint_level == 0`, not invalidated, target not withdrawn.
- **guided** = `outcome == "correct"` but not sound.
- **lapse** = `outcome in ("incorrect", "partial")` with `error_kind` not in `("tutor_or_item_error", "ambiguous_wording", "cognitive_load")`.

1. **P1 — growth on any sound event.** Double when sound, a previous review exists, the observation is at or after the previous `due_at`, and (for `kind == "retrieval"`) `after_gap` is true. This replaces `and event["kind"] == "retrieval"` at `learn_state.py:285`.
2. **P2a — 90-day cap.** `interval = min(previous * 2, 90)`, so growth passes 30 → 60 → 90 instead of stopping at 30. `_validate_state` relaxes the bound from `1..30` to `1..90`.
3. **P2b — lapse scales down.** `interval = max(1, int(previous * 0.4))`; with no prior review it is 1.
4. **P2c — guided success shortens without counting.** Same arithmetic, but it does not increment the lapse streak. Deliberate change from the v1 one-day reset.
5. **Re-teach.** Count consecutive lapse events since the last sound event. At three: `interval_days = 1`, `reason = "Review: re-teach after 3 lapses"`. The streak resets only on a sound event. Re-teach means instruction plus a worked example, not another quiz; the helper cannot enforce that.
6. **Unchanged.** Errors, partial, assisted, and important independent successes create obligations; exposure and self-report do not. Deadline pull-forward, cram urgency, pause, and importance ordering are untouched.
7. **Move-on gate (teaching, not code).** Require one sound `transfer in ("related", "novel")` success before "ready to move on". The helper cannot verify the item was unfamiliar.
8. **Not claimed.** `hint_level` is not a learning measure. `error_kind` is provisional. `transfer` is a declared classification. 90 and 0.4 are policy constants, not fitted parameters. No retention probability, optimal interval, or FSRS. Three lapses is heuristic. v1 data cannot recover rung counts, so migrated records read `hint_level: 0` and are not "unaided" on that basis.

## 7. Compatibility

- **Unknown fields.** Still rejected, naming the keys; do not ignore them in v2.
- **v1 reading.** `_read_json` → strict v1 shape check → `_migrate(raw, 1)` in memory → semantic validation. `resume` returns v2-shaped records and writes nothing. While the file is v1, `resume` warns that evidence was migrated and `hint_level` defaults to 0.
- **v2 writing.** The first successful `save` writes both files at version 2. A read-only session leaves v1 bytes intact. Migration does not bump `revision`; the save does.
- **Mixed files.** A v2 graph with a v1 state is readable: migration is a pure per-file function, so matching versions are not required.
- **Future versions.** `format_version > 2` or a non-integer raises `Unsupported learning format ...` and rewrites nothing. Never migrate downward.
- **Downgrade.** Unsupported. An older helper refuses a v2 file at its version check and leaves it intact. Restoring v1 requires `state.prev.json` or an operator copy; the helper never does it.
- **Cross-subject links.** `_validate_graph(root=...)` reads the neighbour's graph; use the same version-aware loader so a v1 neighbour stays readable beside a v2 subject.

## 8. Test plan

1. `test_v1_state_migrates_on_read_without_touching_bytes` — v1 fixture; `resume` reports `format_version: 2`; file bytes identical.
2. `test_migration_fills_all_four_defaults_on_every_event` — every event, invalidated ones included, gets `0`/`None`/`None`/`None`.
3. `test_v2_round_trip_preserves_fields_and_bumps_version_once` — values equal after save; revision +1.
4. `test_partially_migrated_file_is_rejected` — v2 event missing `transfer`; v1 event carrying `hint_level`. Both raise; neither writes.
5. `test_invalid_enum_and_type_values_are_rejected_before_writes` — `error_kind: "careless"`, `transfer: "far"`, `hint_level: 6`, `True`, `"2"`, `2.0`; both files byte-identical after each.
6. `test_hint_level_blocks_growth_and_shortens_without_a_lapse` — independent + `hint_level 2` yields `max(1, prior*0.4)` and validates.
7. `test_sound_performance_at_or_after_due_doubles` — P1 regression; a same-day early attempt holds at 1.
8. `test_interval_saturates_at_ninety_days` — chain yields 30, 60, 90, 90; validator accepts 90.
9. `test_lapse_scales_by_point_four_with_floor_one` — 10 → 4; 2 → 1; 1 → 1.
10. `test_three_lapses_produce_re_teach_then_reset` — three `incorrect` events give interval 1 and a `re-teach` reason; a later sound event restores growth.
11. `test_non_learner_error_kinds_do_not_count_as_lapses` — the three excluded kinds never reach three; an invalidated `tutor_or_item_error` creates no obligation.
12. `test_review_recomputation_is_idempotent_and_ignores_stored_values` — save → resume → no-op save → identical reviews; a hand-edited `due_at` is overwritten; `novel` with a cue rejected.

Run under Python 3.10 and 3.13. No new dependency, no network, no clock beyond the injected `now`.
