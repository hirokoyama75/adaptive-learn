# Published improvement evidence

Start with the repository [README](../README.md#improvement-process-and-results). This directory preserves the project-specific research, proposals, actual synthetic replies, rejected candidate, graders, and result reports behind that summary. It is not learner memory, a live teaching service, or proof of improved human learning.

## Current reports

| Work | Report | Outcome |
| --- | --- | --- |
| Reliability fixes and minimal migration | [Implementation results](IMPLEMENTATION_RESULTS.md) | Reproduced defects fixed; 74 package tests pass |
| Invented-rule experiment | [Novel-rule results](benchmarks/novel-rules/RESULTS.md) | Tutor and worked-example self-study tied at 32/32 valid posttest items each |
| Harder concept/time pilot | [Time-to-transfer results](benchmarks/time-to-transfer/RESULTS.md) | Full criterion: tutoring 1/2, self-study 2/2; human time unmeasured |
| Actual tutor versus ordinary chat | [Comparison results](iterations/tutor-vs-chat/RESULTS.md) | Confirmation: original 3/3, candidate 2/3, chat 2/3; candidate rejected |

The original core and rejected candidate snapshots remain separate. The retained skill includes the earlier reliability/teaching changes, not the rejected timing paragraph. Worked AC-26 is an expected-behavior example, not an automatic timer or a measured learning result.

## Reproduce the publication

From the repository root, with Python 3.10 or newer:

```text
python -B scripts/check_research.py
```

On the Windows environment used for the original runs, the second supported interpreter was checked with:

```text
py -3.10 -B scripts/check_research.py
```

The entry point runs the 74 package tests plus 18 research/oracle/recorder tests, checks archive hashes and the unchanged four-case holdout, and recomputes all three recorded reports. It makes **no model calls**, changes no recorded evidence, and writes test fixtures only to a temporary directory. Run without Python `-O`; assertion-based evidence checks must remain enabled.

Some frozen scripts and historical commands assume the original workspace layout, where `handoff/` and `adaptive-learn/` were siblings. The publication entry point supplies the existing annotation-checker import path and isolated test-temporary-directory environment; it does not edit those frozen scripts. Use this entry point for the published layout rather than blindly rerunning the old workspace commands. Starting a new experiment needs a new protocol and capture, not overwriting a frozen run.

Historical implementation links and frozen source snapshots also retain their original sibling/package-relative paths. Browse the current [playbooks](../playbooks/) and [references](../references/) here; the archived copies are evidence, not additional installed skills.

## Provenance and privacy

[PUBLICATION_MANIFEST.json](PUBLICATION_MANIFEST.json) lists every imported artifact with its original and published SHA-256. All frozen protocols, graders, questions, replies, and run metadata were copied byte-for-byte. Publication-only differences are explicitly listed:

- A historical-context banner was added to the original handoff README.
- Eleven machine-local traceback path prefixes were replaced with `<workspace>/` in one red-test log.
- The historical [research notes](../research.md) received a context/citation warning and one local interpreter path was redacted.

Original local files were not rewritten. `.gitattributes` prevents Git from changing archived evidence line endings. Host-local planning files, credentials, caches, unrelated skills, and real learner records are not included. Opaque synthetic-run session identifiers are attribution metadata, not independently authenticated provider traces.

The old `MANIFEST.json`, agent briefs, proposals, schemas, drafts, and status statements are historical authoring inputs. Their original dates, counts, constraints, and sibling paths do not describe the current release. Proposed evidence fields or scheduler changes are not implemented merely because a draft describes them. Current source and the reports above govern implementation status. Full internal model tool traces, earlier external before-source snapshots, and independently verified external literature citations are not supplied by this archive.

## What this does not establish

The synthetic work exposed incorrect explanations, misleading timing assumptions, and an unsuccessful candidate. It did not establish student preference, faster human understanding, durable retention, or superiority over competent ordinary chat. Explanation judgments were not independently blinded/calibrated. Any such claim needs a voluntary human study with independently checked tasks and actual elapsed time, including reading, thinking, feedback, and waiting.
