# Worked acceptance cases

These are concrete solutions to the 25 design acceptance cases, identified as AC-01 through AC-25. They are **worked design walkthroughs, not transcripts from executed live tutoring sessions**. Sample wording is illustrative; equivalent concise responses meeting the criteria are valid.

For a future live check, load the skill in a fresh chat with the given setup, compare actual behavior with the response/action and record expectations, and save the observed result separately. Do not mark a learning outcome as validated just because a file test passes. Automated mechanical support lives in [test_state.py](test_state.py); it cannot validate the tutor's judgment or the truthfulness of supplied evidence.

## AC-01 — Novice cannot begin

- **Given:** “I don't know where to start” on `3x + 2 = 14`.
- **Response/action:** “We want x on its own. Subtract 2 from both sides, giving 3x = 12. What operation would undo multiplying by 3?” If that is still inaccessible, demonstrate division rather than repeating guesses. Later fade support on a comparable task.
- **Record/check:** Save the task and demonstrated move; completion is assisted. A later changed task after intervening work/time can establish independent retrieval. Reject endless questioning, a foundation reset, or an independent-success label for this attempt.

## AC-02 — Experienced learner

- **Given:** A learner correctly solves and justifies a representative equation without help, including relevant restrictions.
- **Response/action:** “That reasoning is sound. Let's move to a case where you need to decide whether the same method applies.” Advance provisionally; do not search for a forced failure ceiling or replay beginner questions.
- **Record/check:** Record observed independent performance and its conditions; important targets receive later review. Response speed is unnecessary unless genuinely part of the target. Reject a permanent mastery claim or compulsory discovery sequence.

## AC-03 — Slip versus misconception

- **Given:** Learner correctly chooses subtracting 2 from both sides but writes `14 - 2 = 11`; compare with subtracting from only one side.
- **Response/action:** For the first, “Check 14 minus 2,” preserving the demonstrated equality reasoning. For the second, model why the same operation must affect both sides and give a small continuation.
- **Record/check:** Distinguish execution slip from a provisional conceptual error. Ask one discriminating question if the written work is ambiguous. Reject treating both as identical missing foundations.

## AC-04 — Practice paper only

- **Given:** “Help me prepare,” with one paper and no deadline or syllabus.
- **Response/action:** “We'll use this paper to start class-aligned practice; it may not cover the whole exam. Let's try this representative task.” Ask about a deadline only when it changes prioritization.
- **Record/check:** Goal `class`; scope `provisional`; deadline null. A paper does not establish weights or complete scope. Reject an invented exam date, automatic cramming, or a long intake before useful work.

## AC-05 — Scope exceeds effort

- **Given:** Twenty supplied objectives, 45 minutes available, and an explicit cram request.
- **Response/action:** “We cannot reliably cover all twenty in this block. I'll prioritize the supplied high-weight areas and prerequisites that unlock several question types, then check them with unseen tasks. These other areas will remain untested.” If weights are absent, say so rather than estimating them as facts.
- **Record/check:** Persist the supplied scope/source, actual available effort, priorities, and deferred risks. Keep retrieval active. Reject guaranteed coverage/passing, silent omissions, or unrelated depth.

## AC-06 — Hint-assisted success

- **Given:** Learner solves an integral after the tutor names integration by parts and demonstrates the first move.
- **Response/action:** Credit the result and explain the remaining independent target. Continue with intervening work; later present a changed integral without naming the technique if method selection is being assessed.
- **Record/check:** First event is assisted with explicit cues/support. Same-session cramming review becomes eligible after other meaningful work, not immediately after the hint. Reject treating an immediate near-copy as independent retention. Automated support: review-spacing and cramming tests.

## AC-07 — Qualified claims and joint premises

- **Given:** A philosophical argument: under a particular framework, P1 says virtue is sufficient for happiness; P2 says wisdom implies virtue; together they support a conclusion about wisdom and happiness.
- **Response/action:** Present the conclusion conditionally and distinguish validity from acceptance of the premises. If saving this structure is worthwhile, preserve the framework/source and uncertainty.
- **Record/check:** One argument has premises `[P1, P2]`, not two arrows claiming either premise alone suffices. An alternative argument remains separate. Detailed graphs may be omitted entirely when not useful. Automated support: joint-argument/prerequisite tests.

## AC-08 — No audio capability

- **Given:** “Judge my singing intonation,” but the host cannot inspect a recording.
- **Response/action:** “I can't assess the sound here. I can help analyse the notation or design a practice exercise, but that won't establish your actual intonation.” Do not claim to have heard anything.
- **Record/check:** Actual performance is unassessed. Any text/notation task has its own target and criteria. Reject invented pronunciation, tone, or timing feedback.

## AC-09 — End mid-problem

- **Given:** The equation above is active, the learner has written `3x = 12`, and one subtraction hint was supplied.
- **Response/action:** At handoff/checkpoint save the exact prompt, checked solution/criteria, partial attempt, hint, allowed aids, obstacle, and next action. On resumption say “You had reached 3x = 12 after a subtraction hint. Continue from there.” Do not reveal the prepared answer unnecessarily.
- **Record/check:** The new chat uses the saved checkpoint, not a reconstructed similar equation or a full transcript. Do not invent unsaved work. Automated support: exact-task handoff test.

## AC-10 — Visited is not understood

- **Given:** A plan item was read and an explanation displayed, but no learner performance occurred.
- **Response/action:** Mark navigation as visited if useful. Invite an appropriately sized attempt when the learner is ready; do not announce competence.
- **Record/check:** Exposure/self-report is unassessed with unknown independence. It creates no observed-performance or mastery claim. Automated support: visited/exposure/self-report test.

## AC-11 — Invalid or unsafe files

- **Given:** Dangling targets, cyclic prerequisites, inconsistent hint metadata, duplicate JSON keys, a future format, an unsafe path, or failed replacement.
- **Response/action:** Refuse the persistent update with a clear reason and last-save uncertainty; preserve existing files and offer explicitly session-only tutoring. Never silently drop unknown fields or reinitialize.
- **Record/check:** No proposed graph additions are written when complete proposal validation fails. State remains valid after an interrupted replacement. Automated support: invalid-format/update, path, and interruption tests. These are not power-loss or multi-writer guarantees.

## AC-12 — Git setup and tracked data

- **Given:** The selected learning root is in a Git repository with existing ignore rules; some learner records may already be tracked.
- **Response/action:** Append only the profile and chosen subject's private-state ignore rules, preserving user rules. Warn that tracked data stays tracked and that local files may sync to a cloud folder. Do not automatically untrack anything.
- **Record/check:** No global skill installation or unrelated ignore changes. Inspect effective ignore/tracking status before sharing. Automated support: repeated-setup/privacy and Git integration checks where Git is available.

## AC-13 — Cross-subject task

- **Given:** A business decision requires discounted cash-flow calculations.
- **Response/action:** Use decision criteria/business guidance as primary; add the relevant mathematical check only if needed. Choose one subject home for the attempt and link to reusable math targets.
- **Record/check:** Math evidence elsewhere is a starting signal, not proof of making the business decision. Do not duplicate the attempt or load every STEM guide. Automated support: cross-subject-link test; routing judgment still needs a live check.

## AC-14 — Long productive session

- **Given:** A productive multi-block chat is becoming long.
- **Response/action:** At a natural break, save the active checkpoint and say that compaction or a new chat may help. Explain that writing files does not clear previous model context. Continue the useful block if interrupting would be worse.
- **Record/check:** New-chat resumption uses the selected view; no full-history replay, automatic context-clearing claim, fabricated token meter, or unlimited-memory promise.

## AC-15 — Unfamiliar term

- **Given:** A fraction explanation needs “denominator,” which the learner has not shown they understand.
- **Response/action:** “In 3/4, the bottom number, 4, means one whole is divided into four equal pieces. We call that bottom number the denominator.” Then use the name consistently and continue the actual task.
- **Record/check:** No compulsory vocabulary interview/database. A later terminology slip is distinguished from the underlying fraction concept. Reject unexplained labels or permanently hiding assessed terminology.

## AC-16 — Exam months away

- **Given:** Supplied course objectives and an exam three months away; no cram request.
- **Response/action:** Use Learning for class, with explanation, independent application, and spaced retrieval across the known scope. Ask before adding substantial unrelated depth.
- **Record/check:** Keep the supplied date separate from mode/support. Do not infer low time availability from exam relevance. Reject automatic compression, rote-only learning, or deadline invention.

## AC-17 — Important independent success

- **Given:** An important target is solved correctly without help, not yet retested after a gap.
- **Response/action:** “That supports moving on. We haven't checked later recall yet; we'll revisit it.” Do not keep probing merely to obtain certainty.
- **Record/check:** Performance event is independent under declared aids/cues. Schedule later review even though the answer was correct; later independent retrieval can extend the heuristic interval. Automated support: successful-target review test.

## AC-18 — Defensible alternative

- **Given:** A literary task asks for an interpretation supported by a passage. The learner argues for a different defensible interpretation than the tutor prepared.
- **Response/action:** Judge against the preselected criteria—textual support and reasoning—not agreement with the tutor's thesis. Explain why the alternative meets or misses those criteria, checking the passage rather than inventing a quote.
- **Record/check:** No misconception recorded merely for disagreement. A new grading assumption must be disclosed, not invented after seeing the response to force a preferred answer. Also applies to equivalent proofs/code/designs.

## AC-19 — Tutor misgraded

- **Given:** Learner answers `2x + 2` for `2(x + 1)`; tutor incorrectly expected `2x + 1`.
- **Response/action:** “Your answer was correct. I failed to multiply both terms by 2.” Invalidate the misgraded evidence with this reason; remove the false active misconception and rebuild reviews. If recording the corrected performance, retain the original observation conditions/time; it is not a second attempt.
- **Record/check:** Inspect and withdraw any saved erroneous rule and dependent claims. Old IDs/records remain identifiable; corrections are explicit. Automated support: evidence-invalidation and node-withdrawal tests.

## AC-20 — Large-history resumption

- **Given:** Many old targets/evidence records and an active mid-problem checkpoint.
- **Response/action:** Read the bounded selected view containing the intact task, criteria, attempt, hints, and relevant context. Respect omitted counts; fetch another slice if it materially affects the next action or a coverage claim.
- **Record/check:** Under a small character budget, optional history may be omitted explicitly; the task is never silently truncated. If the intact task cannot fit, request a larger budget or an explicit safe condensation. Automated support: bounded-resume test.

## AC-21 — Stop between graph and state

- **Given:** Graph additions save successfully, but state replacement fails.
- **Response/action:** Report the failed canonical save; resumption uses the previous state/revision. Reuse the same graph IDs when retrying after checking actual state.
- **Record/check:** Old state bytes remain intact, any unused graph additions are harmless, temporary files are cleaned up, and retry succeeds without duplicate IDs. A failed plan/summary refresh after a successful state commit instead reports “saved” with a warning. Automated support: interrupted-state and derived-view tests.

## AC-22 — Session only

- **Given:** “Explain this quickly; don't save anything.”
- **Response/action:** Teach immediately without asking for a learning root or invoking setup/save. If continuity becomes relevant, explain that a new chat cannot recover this unsaved work automatically.
- **Record/check:** No learner files, hidden profile, global installation, or automatic notes. This is a tutoring-behavior check, not something helper tests alone can establish.

## AC-23 — In-depth activities

- **Given:** “I want to understand why dividing by a fraction works, in depth.”
- **Response/action:** Use a concrete sharing/measurement example, introduce necessary vocabulary, repair the exact gap, then try a changed independent case. When useful, examine assumptions such as the divisor being nonzero. Skip already-demonstrated activities and model missing steps when needed.
- **Record/check:** A fluent explanation alone is insufficient if application fails. Activities are not mastery levels or a compulsory Socratic sequence. Later retrieval still matters after a successful new case.

## AC-24 — Named-method drill

- **Given:** “Use breadth-first search to find the shortest number of edges in this unweighted graph,” with documentation allowed.
- **Response/action:** Treat this as useful focused execution practice. Define the algorithm's name before relying on it if unfamiliar; assess the trace/implementation and conditions. Later give a task without naming the method if method selection is a target.
- **Record/check:** Record the method cue and allowed documentation separately from tutor hints. Do not claim independent method selection or treat normal documentation use as hidden assistance by default.

## AC-25 — Review backlog

- **Given:** Seventy eligible due targets; learner agrees to at most two reviews before returning to current coursework.
- **Response/action:** Offer two high-value relevant suggestions and disclose that more remain. Let the learner suspend a low-relevance target or choose to continue coursework without clearing the backlog.
- **Record/check:** One current obligation per target, explicit remaining count, suspension respected across eligible new evidence, no compulsory catch-up. Automated support: bounded-resume selection, review merge/spacing, and suspension tests. The helper does not measure time spent or force the two reviews.
