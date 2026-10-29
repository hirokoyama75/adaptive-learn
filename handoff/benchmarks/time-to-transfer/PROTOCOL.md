# Harder, time-focused concept pilot — protocol v1

Frozen before any new learner runs. This is a synthetic feasibility pilot, not a measurement of human learning speed.

## Objective and scope

Optimize **time to verified application and transfer**, not prompt count. A provisional ten-minute human lesson is the design target, not an observed outcome or a promised completion time. Short questions, feedback, and additional replies are useful when they repair an obstacle faster; no score rewards fewer turns or shorter text.

The concept is information preservation: undo a composed process in reverse order, distinguish recoverable from erased information, refute a universal claim with a counterexample, and construct a process with a specified effect. Fictional two-slot machines use small wrapped integers. This is harder concept work than the original forward-arithmetic benchmark, not merely larger numbers.

## Frozen pilot

- Learners: verified `opencode-go/deepseek-v4.1-flash#low`, unchanged across conditions. No deliberate errors, pretend-human personalities, or claims that low effort represents a human novice.
- Two matched worlds, seeds 617 and 1291; tutoring and self-study in each, **four fresh learner sessions maximum**. Both worlds run even if the first is at ceiling, so the stopping rule is not selected from favorable results. No no-instruction arm: the prior experiment already established that invented rules are unavailable without instruction.
- Both arms receive identical definitions and one forward worked example, followed immediately by four concept tasks. No pointless unknown-rule pretest. Every packet has exactly one recoverable chain, one ambiguous chain requiring two witnesses, one program-equivalence claim, and one short construction. Tasks and target effects are disjoint across packets, with coverage asserted before freezing.
- There are three pre-frozen checkpoint packets and one final transfer packet per world. A learner proceeds to final as soon as a checkpoint meets criterion; otherwise it may receive up to two feedback/checkpoint rounds. The four-reply cap is an execution/runaway guard, not the efficiency objective. All attempts, including invalid replies, remain recorded; no replacement sessions or repairs to returned JSON.
- The orchestrator actually applies the current skill and mathematics playbook to tutor feedback; it is not a fixed diagnostic-feedback template. It sees the current checked key and actual response, not future packet items/keys. Self-study receives the checked worked solutions to its attempted packet. Both receive feedback only after attempting the relevant items. Feedback may differ in content and length; this is a pragmatic workflow comparison, not an isolated causal test of adaptivity.
- No packet-specific help during a checkpoint or final. Prior conversation remains available: this is open-context performance, not retention. A clarification may be answered in the next permitted feedback turn; the response budget is not spent on repeated intake. Unresolved ambiguity or an invalid item is recorded as a deviation, not blamed on the learner.
- Stop after these four sessions and one analysis. No teaching-policy amendment during the pilot, extra task selection, retries to improve scores, or automatic harder-level escalation. This is exploratory, not a confirmatory efficacy study.

## Criterion and grading

Each packet has four executable certificates: a unique starting state, two distinct starting states giving the same observed output, an equivalence judgment with a counterexample when false, and a constructed program that realizes a requested mapping for **every** valid starting state. Alternative valid witnesses/programs are accepted. All computations are exhaustively checked against independent matrix composition before runs.

A checkpoint qualifies only if all four certificates are correct **and** the brief explanation satisfies three preregistered checks: (1) undo the last operation first, using the new pair to recover the old values; (2) a copy can merge distinct inputs and later reversible moves cannot recover the lost distinction; (3) one differing input refutes equivalence, while agreement on a sample alone does not prove universal equivalence. For a true equivalence claim, a valid general algebraic/operational justification is needed, not merely examples.

Explanation judgments are made by the orchestrator with literal supporting quotes preserved. Quote validation checks attribution, not semantic accuracy; there is no calibrated independent human judge. Report executable correctness and explanation judgments separately. Operational criterion is not a psychometric proof of understanding.

**Time-to-criterion** means the first qualifying checkpoint followed by a qualifying **unseen final transfer packet**. Report failures/censoring, not just successful times. First-attempt performance is a sensitivity check: if both arms solve everything immediately, this model/task pair still cannot assess repair efficiency. All future packets stay unopened until the current feedback decision is fixed; final stays unopened until teaching has ended for that session.

## Timing: keep observations and assumptions separate

1. **Observed:** recorded launch-to-capture wall-time envelopes for actual agent exchanges. These include tool dispatch, model/service waiting, and manual capture overhead; they are not pure inference latency, thinking time, or a human's study time. Offline benchmark construction and pauses between exchanges are excluded from those envelopes and are not hidden as a learning-speed benefit.
2. **Unobserved primary human outcome:** actual elapsed active lesson time (reading/listening, thinking, answering, useful back-and-forth, and user-visible tutor waiting) to the same transfer criterion, with a ten-minute deadline. No human is enrolled in this pilot, so this outcome is **not measured**. Do not substitute agent wall time for it.
3. **Workload sensitivity only:** for the human-facing material actually sent, calculate `60 * words / reading_wpm + items * attempt_seconds + packets * explanation_seconds`. Scenarios are fast `(240,30,20)`, reference `(180,45,30)`, and slower `(120,60,60)`. Attempt allowances include thinking and answering; explanation allowances cover the short spoken/written explanation. All rates are unvalidated assumptions, not forecasts for a person. They omit real human-specific difficulty and live tutor waiting; report how much waiting budget, if any, remains. Agent-only JSON/tool instructions are excluded from human-facing word counts and reported separately.

No intrinsic turn penalty, word-count winner, or composite "learning efficiency" score. Report certificate/transfer outcomes, criterion status, material workload, scenario fit to ten minutes, timing boundaries, and tradeoffs. If the scenario ordering changes, say so; if nothing fits, say the lesson is not yet ten-minute-ready. Provide a human-ready lesson with time checkpoints and a clear fallback when the learner remains blocked, but do not claim it has been validated on humans.

## Integrity and limits

Raw tool-returned replies, exact declared prompts, hashes, session continuity, launch/capture timestamps, checked grades, explanation quotes, and actual feedback are preserved outside the skill package. Local files cannot authenticate provider execution. Learners are instructed not to use tools or sources, but tools are not technically disabled and internal traces are unavailable. No sandbox or contamination-free claim is made.

The original frozen experiment, existing skill changes, and package holdouts remain untouched. No real learner data, telemetry, dependencies, installation, publication, or new persistence schema. Any later claim of actual human time efficiency requires a voluntary human trial and measured timing, not a synthetic rerun.
