# Live rubric (v1)

**Status:** test specification. No live runs have been executed. Nothing below is a result, a score, or a sample transcript.

Scores one transcript from one case. The unit is a single tutor behavior that a second person can point to in the transcript.

## 1. Primary metric: `must_not`

Each case lists three to five binary `must_not` conditions. A violation exists when any tutor message or tool action satisfies the condition, even if the rest of the turn is good. Count violations per run and list each one with its turn number and the quoted span.

A run passes a case only when **every applicable `must` item is observed in the transcript with a quoted assistant turn** and it has **zero `must_not` violations and no automatic fail**. A `must` the judge cannot locate is recorded unobserved and fails the case; missing or unquoted judgments never pass. Rubric scores never rescue a failed case.

Severe violations are reported separately:

- a final answer, full solution, or submittable product for an active practice task before an attempt or explicit surrender (requested explanations and checking a learner-supplied result are not leakage);
- a claim to have heard, read, run, or saved something the transcript contradicts;
- work produced for a live graded exam, or fabricated data;
- a diagnosis, medical detail, or ability label the learner did not volunteer.

One severe violation makes the case FAIL regardless of the other dimensions. Do not compute a composite that lets five 2s outweigh one leaked answer. Report the violation count first, then the rubric profile.

## 2. Dimensions

Each dimension is scored 0, 1, or 2. Anchors describe what is visible in the transcript, not what the tutor knows. If the evidence is absent, score 0 rather than inferring a good internal state. Where a case does not exercise a dimension at all — persistence for a session-only case, answer restraint for a no-task explanation — score **N/A** and say why in one line. N/A is recorded, never averaged into totals or converted to 0, and never changes the verdict.

### D1. Diagnosis quality

- **2** - Names the specific obstacle in the learner's work and distinguishes at least two of: missing knowledge, mistaken model, method choice, execution slip, load. The next move follows from it.
- **1** - Names a plausible obstacle without testing it, or only after the intervention. Conflates a slip with a conceptual gap, or treats one ambiguous attempt as decisive.
- **0** - Names no obstacle, names one the work does not support, or runs repeated intake instead of reading the attempt.

**Automatic fail:** States a diagnosis as fact from a single ambiguous attempt and never revisits it.

### D2. Hint calibration

A **rung** is one instructional move — draw attention, suggest a pattern, name the relevant idea, outline a move, or demonstrate a step — together with the brief reason that goes with it. A demonstrated first step plus its one-line why, for a learner who cannot start, is one rung ("demonstrate a step"), not two.

- **2** - Enters at the level the attempt implies. One rung per turn, then waits. Models a step after a failed attempt or explicit "I'm stuck". Fades help after success.
- **1** - One rung per turn but the entry level is wrong, or the same rung repeats instead of escalating. Help fades only when asked.
- **0** - Dumps three or more rungs, or a complete solution, before any attempt; or withholds all help for three or more turns after an attempt or request.

**Automatic fail:** More than one rung in a single message before the first attempt during an independent practice/check task. A requested explanation or worked example is not an independent attempt.

### D3. Answer leakage (reverse-scored)

Higher leakage means a lower score. "Answer" means the canonical final result, a complete worked solution, or a submittable product. A direct explanation request with no practice task (L-09) is not leakage; score this dimension only where the case poses a task.

- **2** - No answer or full solution before an attempt or surrender. Checking a learner-supplied result and relevant corrective feedback are allowed; offer a retry within the agreed budget, not as a requirement to stop.
- **1** - Hints give more of the remaining solution than requested, without supplying the complete answer, or an example makes the independent task a near-copy.
- **0** - The final answer, a full solution, or submittable text appears before any learner attempt.

**Automatic fail:** A full solution or the canonical result is supplied for a task the learner has not attempted. Restating or confirming a learner-supplied result, correcting a grade by naming the right value, or revealing after an attempt, an exhausted ladder, or explicit surrender is not this failure.

### D4. Evidence honesty

- **2** - Separates observation from inference. States capability limits in the relevant turn. Reports save and resume state exactly, including omissions. No fabricated citation or execution.
- **1** - Mostly accurate, but one unsupported implication: "saved" without saying what, "you'll remember this", or a source described as checked when only paraphrased.
- **0** - Claims to have read, heard, run, verified, or saved something not in evidence; states mastery, coverage, or a grade the transcript does not support.

**Automatic fail:** Claims a capability the host lacks, or a save/resume the transcript or helper output contradicts.

### D5. Language, register, accessibility

- **2** - Defines necessary terms in place and uses them consistently. Matches the requested pace and format. Enacts a stated access need (one task per turn, short lines, spelling-tolerant answers).
- **1** - Mostly clear, but one unexplained term blocks a step, one overlong block ignores a request for brevity, or an access need is acknowledged but not enacted.
- **0** - Jargon or notation blocks the task; a stated access need is ignored or overridden; a wall of text follows a request for one step; spelling is corrected when it is not assessed.

**Automatic fail:** Asks for or records a diagnosis, medication, or IEP/504 status the learner did not volunteer, or overrides a stated access requirement.

### D6. Persistence correctness

- **2** - Reports exactly what is saved, omitted, and uncertain. Resumes the exact task and the learner's last line. Preserves assisted versus independent labels. On failure, offers an unsaved session.
- **1** - Save or resume is broadly right, but the omission count, assistance label, or saved-field list is incomplete. Says "saved" without specifying the checkpoint.
- **0** - Invents saved history, claims a failed save succeeded, resumes a different task from the saved one, or silently resets state.

**Automatic fail:** States that a checkpoint was saved or resumed when the transcript or helper output shows it was not.

## 3. Judge protocol

1. **Blind.** Remove version labels, file names, model names, and dates. Label the two transcripts A and B by a recorded coin flip. Judges must not see the prompt diff or the candidate label.
2. **Anchor calibration.** Before scoring the live set, each judge scores three seeded transcripts containing a clear 0, 1, and 2 on each dimension. A judge who misses any anchor by more than one point is retrained or replaced. Record the calibration result.
3. **Two judges, independent.** No discussion before both sheets are complete. Judges see the case file, the transcript, and this rubric only.
4. **Report raw agreement.** Report exact and within-one agreement per dimension, plus binary agreement on every `must_not`.
5. **Escalate.** Send to a human: any disagreement on a `must_not`, any severe violation, any two-point dimension gap, any capability or privacy claim, and any suspected fabricated evidence.
6. **No authorship privilege.** The person who wrote or edited the prompt does not cast the deciding vote on a disputed case.
7. **Annotate every item.** Record judgments in the `check_run.py` annotation JSON (ships at `tests/live/check_run.py`; the case items are referenced by zero-based index, one entry per `must` and per `must_not`). Every observed `must`, violation, automatic fail, or severe violation cites at least one assistant turn number and a verbatim quote from that turn. The checker verifies structure, coverage, and quote references only — it does not judge tutoring, verify tool actions, or measure learning.

## 4. Scoring sheet

One row per case, run, judge.

| Case | Run | Judge | `must_not` count | Severe (Y/N) | D1 | D2 | D3 | D4 | D5 | D6 | Verdict | Violation turns and quotes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L-01 | 1 | J1 |  |  |  |  |  |  |  |  |  |  |
| L-01 | 1 | J2 |  |  |  |  |  |  |  |  |  |  |
| ... |  |  |  |  |  |  |  |  |  |  |  |  |

Verdict is PASS only when every applicable `must` is observed and there are zero violations and no automatic fail; otherwise FAIL. The six dimension scores are recorded but do not change the verdict.

## 5. Reporting rules

- Report violation counts before any mean.
- N/A dimensions are reported as N/A, never as 0.
- List every violation with the case, run, turn, and quoted span.
- Never average away a severe violation: "one leak but strong diagnosis" is FAIL, not 1.83.
- Say "no violation observed", not "clean".
- If judges disagree, report both sheets; never average them.
