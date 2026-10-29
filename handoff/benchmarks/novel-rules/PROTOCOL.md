# Novel-rule benchmark — frozen protocol v1

This is a controlled **synthetic, open-context rule-application experiment**, not a human learner study, retention test, or claim that model weights changed.

## Design fixed before sessions

- Learners: `opencode-go/deepseek-v4.1-flash#low`, same model/effort throughout. The user authorized high or low after medium was unavailable. Low effort is not a human-novice proxy.
- Four independently generated fictional sorting worlds: development seeds 43 and 107; confirmation seeds 211 and 509. Confirmation tasks and scoring are frozen before development runs, not chosen after seeing results.
- Three arms per world, twelve fresh learner sessions total: orchestrator tutoring, worked-example self-study, and no instruction. Launch order within each world is randomized with seed 20261029. No forced errors or pretend-human personalities.
- Each session has four actual learner replies: four-item pretest without the rulebook; one practice item after condition material; another practice item after feedback; ten-item posttest after final feedback. No pretest feedback. The two instruction arms receive exactly the same rulebook and initial worked example. Both see checked practice solutions after attempting them; only tutoring targets feedback to the submitted intermediate values. No-instruction receives no rules or answer feedback.
- Tutoring follows the current skill's prepared-key, local-error, bounded-feedback, and no-mastery principles. The orchestrator uses program-checked templates to avoid teaching an incorrect key. This tests that bounded teaching implementation, not all possible executions of the skill.
- Same learner prompts/questions and turn count across matched arms. Feedback is capped at 110 whitespace words. Actual prompt/response words are reported; token usage and wall-clock effort are not equated. The tutor arm can receive different feedback length/content. No claim isolates adaptivity from those differences.
- Learners are told not to use tools, read files, or consult outside sources. The harness cannot technically disable child tools or export full internal tool traces; isolation is instruction-based, not sandbox-proven. The orchestrator, not learner self-report, records actual replies.

## Measures and grading

- **Primary:** correct final value **and** route on eight well-defined, previously unseen posttest inputs, reported as counts per matched world/arm.
- **Secondary:** two paraphrased surface-transfer items (subset of those eight); two underspecified/invalid inputs requiring `UNKNOWN`; intermediate-trace accuracy; protocol-invalid replies; feedback exposure and clarification questions.
- The unknown-rule pretest is a manipulation check, not a meaningful estimate of prior human knowledge or a learning gain. No-instruction agents can correctly abstain on invalid items while knowing none of the rules; these counts are separate from the primary measure.
- Rule execution is checked against a second implementation exhaustively over all valid inputs for every world before runs. JSON must contain every requested ID exactly once; invalid output is retained and scores zero for the relevant stage, never silently repaired. A single fenced JSON block is accepted; extra prose is not.
- The learner retains conversation context, including rules and feedback. Posttest means **no new help**, not closed-book recall, durable learning, or delayed retention. No model judge or personality score is used.
- Teacher sees practice keys but does not inspect posttest items/keys until the two teaching turns are fixed. Posttest tasks are sent only after instruction is complete. No answer feedback during the posttest.

## Adaptation and stopping rule

Run development worlds first and report all their results. Before opening confirmation prompts, record whether a concrete, attributable teaching defect warrants at most one small revision. No automatic skill edit for a null result, ceiling effect, stochastic difference, or purely benchmark-specific weakness. Keep the original primary measure and confirmation questions unchanged. If a skill revision is warranted, it is exploratory; a separate matched comparison of original/revised teaching is required before claiming improvement.

Stop after the twelve planned sessions, one analysis, and at most one documented evidence-supported improvement. Record failures and deviations; do not fish for a positive finding or run indefinitely. No human efficacy claims, mastery percentages, telemetry, dependencies, installation, publication, real learner data, or changes to the existing fourteen-case holdout.
