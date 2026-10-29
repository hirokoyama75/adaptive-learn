# Reliability implementation results — 2026-10-29

## Outcome and authorization

Completed the local reliability pass, preserving the earlier approved changes. The user explicitly approved the minimal pause migration and expansion beyond the initial 150-line starter budget. DeepSeek V4 Pro at maximum effort (`opencode-go/deepseek-v4-pro#max`) performed independent audits, evaluation-tool implementation, and a read-only migration review. The parent reviewed and amended those changes.

No dependencies, global installation, telemetry, new subject playbooks, extra reference files, commits, tags, or publication were added. No real learner files were migrated or collected. The original proposal remains a dated historical review, not a current test report.

## Implemented

- **Save honesty and review preservation:** retained P-01, D5's ordinary-practice gap correction, P-03's minimal preservation rule, and explicit graph-ahead failure disclosure.
- **P-04, approved minimal state v2:** only required `suspensions` was added. Graph/profile remain v1. Pauses survive invalidation, withdrawal, and mode changes; a standing pause can be resumed without an extant review. No hint, confidence-score, error-kind, or transfer fields were added.
- **Migration/recovery:** v1 is validated strictly and migrated in memory on read. First upgrade saves byte-identical `state.v1.json`; conflicting backups are refused. Tests cover interrupted upgrade/retry, BOM/CRLF preservation, invalid suspensions, and old-reader refusal. Cached reviews are not canonical pause decisions.
- **P-05/P-06/P-08:** unselected reviews are omitted and counted; checkpoint context is retained; same-session eligibility scans timestamps, not insertion position; derived schedules rebuild on read. Future clock-slack observations do not count as intervening work before their time.
- **P-07/P-09/P-10/P-11/P-12:** new timestamps beyond five-minute slack are refused; UTC deadline semantics are explicit; reads and stdin use UTF-8 byte bounds; privacy checks repeat read-only without hiding successful saves; oversized profiles are refused. **P-13 was rejected as unreachable**, not patched speculatively.
- **Tutoring:** retained prepared criteria, direct explanations, assisted/independent distinctions, provisional advancement, stop/skip, and transparent corrections. Added concrete grading/example verification, a usable hint/feedback boundary, document-command restrictions, task-appropriate access support, distress handling, and assessed-work boundaries. These are prompt mitigations, not guarantees.
- **Evaluation:** shipped the unchanged 14-case/four-holdout instrument, repaired contradictory grading/leakage rules, required positive behaviors, and added a stdlib annotation checker with synthetic fixtures. Missing judgments, fabricated quotes, malformed inputs, and boolean numeric fields cannot silently pass. The checker validates annotations; it does not judge tutoring or measure learning.

## Executed verification

| Check | Observed result |
|---|---|
| `python -B -m unittest discover -s tests -v` | 74 passed, zero skips; 35.613 s |
| `py -3.10 -B -m unittest discover -s tests -v` | 74 passed, zero skips; 37.306 s |
| New helper regressions before fixes | Nine initial reliability tests failed; later clock-slack and interrupted-upgrade message tests also failed before their fixes |
| New evaluation regressions | Scorer initially absent; later strict-type/path/case-shape regressions failed before fixes; all are now green |
| Actual released v1 helper loaded in memory | Refused v2 without writes; v1 read-only migration, exact backup, and synthetic state-only recovery verified |
| Suspension budget sweep | 2,048/4,096/8,192-character packets retained checkpoint, consistent target slices and nonnegative omissions; canonical state unchanged |
| Case/holdout integrity | Staged/package cases, checker, holdout and amended rubric byte-match; frozen hash unchanged |
| Package audit | 33 local Markdown destinations checked; Python 3.10 syntax valid; no learner/cache artifacts; license/notice/provenance unchanged |
| Diff whitespace | `git diff --check` passed |

Frozen holdout SHA-256: `9afaefb8241bfd5db8a57b28b232fcaf259d58df10cfcb7abbfdfb6f735a658b`.
Final core SHA-256: `4741578910c18e412a9f4d6c5c8c019cfb2964a38803971cce11ad678b991260`.

## Actual tutoring evidence and limits

`smoke/2026-10-29/` preserves two before-source L-09 conversations, two intermediate-candidate L-09 conversations, and one final targeted numeric reply. These were actual separate tutor sessions, not authored sample answers. They are demos: there are no independent judge scores, complete tool traces, full 14-case runs, or learner outcomes.

One candidate reply contained a numerical side-example error; the transcript is preserved, not silently corrected. An exact Python check established the error, and the final rule explicitly covers intermediate numerical examples as well as grading. A fresh targeted reply gave the correct gap. This does not establish causality or general reliability, and the targeted question's wording was ambiguous.

Nothing here makes the skill perfect or proves improved learning. Establishing that requires independently checked, comparable unaided pre/post and delayed tasks with real consenting learners and a controlled comparison. No such study was run. External research citations remain unverified in this pass.

## Remaining operational limits and rollback

Use one writer. Graph/state replacement remains nontransactional; partial graph commits are disclosed, not automatically reversed. Prompt injection and model mistakes remain possible. Pause choices already erased by old v1 writers cannot be inferred. UTC deadlines are not learner-timezone-aware.

Rollback code through inverse edits by behavior; retain test artifacts as historical evidence. Never reset unrelated changes or automatically restore learner files. After any real format upgrade, old helpers refuse v2; recovery needs stopped writers, inspection, and separately authorized restoration. `state.v1.json` restores only original state, not graph withdrawals or later evidence. Keep it private.
