> Historical planning bundle: the status and sibling-workspace paths below describe the original before-state, not the current release. Start with [PUBLICATION.md](PUBLICATION.md) for the published evidence and current reproduction commands.

# Adaptive Learn — Improvement Handoff

A self-contained bundle for a stronger model (or a careful human) to improve `../adaptive-learn/` without eroding what makes it good.

**Nothing here is installed.** `adaptive-learn/` is unmodified at commit `1485e0b` (clean tree, `main...origin/main`). This folder sits outside that repository.

## Status, stated plainly

| Item | Status |
|---|---|
| Skill code and tests | Verified locally: 30/30 pass on Python 3.13.14 and 3.10; no skips |
| Research findings | Written up, not peer-verified; DOIs and page numbers were not re-resolved |
| Live baseline | **Not run.** No transcripts, scores, or improvement claims exist |
| Case harness | Specified and structurally validated; no case has been executed |
| Citations | Every entry in `CITATIONS.md` is `unverified` or explicitly `likely` |
| Decisions D1–D14 | **Recommendations.** The reviewer may accept, amend, or reject each with evidence |
| Drafts | Written, marked draft, not installed |

If you need a number that proves the skill got better, there isn't one yet. Phase 0 and Phase 4 exist to produce it.

## Start here

1. `AGENT_BRIEF.md` — scope, binding constraints, evidence rules.
2. `SYNTHESIS_TASK.md` — the assignment: verdicts, output template, what a good proposal looks like.
3. `../research.md` — evidence base.
4. `NON_GOALS.md` — what must be preserved.
5. `DECISIONS.md` — the 14 recommendations being judged.
6. `../adaptive-learn/SKILL.md` — the actual skill; read it before believing any description of it.

Then write `handoff/PROPOSAL.md` and stop. Implementation starts only after a human approves it.

## What is in the bundle

| File | Purpose |
|---|---|
| `AGENT_BRIEF.md` | Context, binding constraints, read order, evidence rules |
| `SYNTHESIS_TASK.md` | **The assignment:** decide what to adopt; required `PROPOSAL.md` format |
| `MANIFEST.json` | Every file with purpose, status, read order, byte size, SHA-256; bundle-wide claim flags |
| `DECISIONS.md` | Recommended D1–D14 with rationale, rejected options, evidence pointers, revisit triggers |
| `NON_GOALS.md` | Hard prohibitions, preservation checklist, diff budget, done gate |
| `WORK_ORDER.md` | Gate A (proposal approval), then Phases 0–4 with budgets, commands, gates, rollback |
| `IMPLEMENTATION.md` | Change manifest and proposed patch text; advisory line numbers |
| `SCHEMA_V2.md` | Field contract for `hint_level`, `task_id`, `error_kind`, `transfer`; scheduler rules |
| `MIGRATION.md` | v1→v2 migration, ordering, failure handling, rollback |
| `CONTENT_PLAN.md` | Subject fold/ignore table, task-verb router, reference outlines, access and integrity blocks, AC-26–29 |
| `SECURITY_PRIVACY.md` | Threat model, injection defenses, privacy wording, minors note, supply chain, red-team checklist |
| `BASELINE.md` | Protocol for capturing the before-state (protocol only — no results) |
| `LESSONS.md` | Template for dated, falsifiable post-run lessons |
| `CITATIONS.md` | Verification ledger; nothing marked verified |
| `tests/live/cases.json` | 14 executable scenarios, 4 holdout |
| `tests/live/rubric.md` | Six dimensions, observable anchors, automatic-fail rules |
| `tests/live/README.md` | Baseline capture, run layout, blind comparison, power limits |
| `tests/live/check_cases.py` | Stdlib validator; `--freeze` / `--verify-holdout` for the holdout hash |
| `tests/live/holdout.json` | Frozen holdout IDs and SHA-256 (`9afaefb8…a658b`) |
| `tests/adversarial/cases.md` | 12 inert injection fixtures with expected and forbidden behavior |
| `drafts/exam-craft.md` | 45-line draft reference, not installed |
| `drafts/study-skills.md` | 45-line draft reference, not installed |
| `drafts/accessibility-block.md` | 10-line paste-ready access block |
| `prompts/implementer.md` | Copy-paste brief for the model doing the work |
| `prompts/reviewer.md` | Adversarial review prompt; defaults to reject |
| `prompts/judge.md` | Blind pairwise transcript judge |
| `../research.md` | Evidence base outside this folder; never ship as citation |

## Authority on conflict

1. **Binding:** `AGENT_BRIEF.md` §3 and `NON_GOALS.md` invariants. A proposal that violates one is rejected.
2. **Arguable:** `DECISIONS.md`, `WORK_ORDER.md`, `IMPLEMENTATION.md`, and the research. The reviewer decides, and records the verdict in `PROPOSAL.md`.
3. **Ground truth:** the current skill source. If a document and the code disagree about what the skill does, the code wins.

The bundle has been internally reconciled on the known conflicts: schema field count (four, no `attempt`), P2 file budget (8, not 12), scheduler scope (no stability/difficulty parameter), baseline results filename, and the AC-26–29 ↔ L-11–L-14 mapping. If you find another contradiction, record it; do not silently pick a side.

## Quick check

From the workspace root:

```powershell
python -B handoff\tests\live\check_cases.py --cases handoff\tests\live\cases.json --verify-holdout
```

From `adaptive-learn/`:

```powershell
git status --porcelain          # expect empty
python -B -m unittest discover -s tests -v
py -3.10 -B -m unittest discover -s tests -v
```

Both suites should report 30 tests, all passing, on the untouched tree.

## Scope reminders

- Do not add dependencies, global installs, telemetry, dashboards, gamification, mastery percentages, learning-style matching, or new subject playbooks. A reviewer may recommend one, but only with an explicit "needs human approval" flag.
- Do not rewrite whole files.
- Do not edit `LICENSE`, `NOTICE`, or remove ignore rules.
- Do not put learner data in either repository.
- Do not repeat the "2× learning" headline. One field RCT (unverified here) reports that unguarded chat access lowered unassisted exam scores while a tutor condition with held-back answers was neutral. That is a reason for caution, not a claim about this skill.

## Not legal advice

`SECURITY_PRIVACY.md` summarizes FERPA, GDPR, COPPA, and UK children's-code considerations for a local single-user tool. A school or employer deployment creates obligations this skill does not satisfy.
