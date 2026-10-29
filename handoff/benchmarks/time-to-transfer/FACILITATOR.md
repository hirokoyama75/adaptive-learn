# Ten-minute facilitation: spend time on the actual obstacle

This is a **post-pilot lesson-design revision**, not a tested faster intervention. It has not been rerun on agents or tried with people. It implements the existing skill's local-slip and budget principles; the published skill did not need another rule.

## Scope and clock

Core target: independently distinguish recoverable from erased information, undo a changed composition, and correctly track the **original** information after reordering. Program construction and universal-equivalence arguments are extensions. This narrower target is **not equivalent to the pilot's four-part criterion**; if those extensions are required outcomes, agree on extra time or different scope rather than silently omit them.

Start an actual clock when the learner first sees the material. Count reading/listening, thinking, answering, feedback, and tutor/service waiting. Reuse a known goal/budget; do not add an intake interview. Ask for a different pace or remaining time only when it changes the next move. Do not infer understanding from response speed.

| Latest checkpoint | Action; move earlier when ready |
| --- | --- |
| 0:30 | Agree the core target and reuse any known background. |
| 1:45 | Finish section A; model one missing move if the learner cannot start. |
| 3:15 | Hear the two attempts in B and their short reasons. |
| 4:30 | Repair only the blocking step and ask **one local check**, not the whole battery again. |
| 7:00 | Finish the two changed cases in C, with no new help during the attempt. |
| 9:00 | If needed, repair the affected concept and use one reserve case. Otherwise stop or offer the requested extension. |
| 10:00 | Stop. State what was independently shown and what is still unresolved; do not claim completion merely because time ran out. |

These are planning checkpoints, not measured completion times. If the learner is still blocked, reduce scope or agree on more time. Do not rush them through an answer to manufacture a pass. More short exchanges are fine when they save total time; if response waiting dominates, combine related work into one coherent block rather than splitting it into needless micro-turns.

## Checked keys — do not display before attempts

All arithmetic is mod 5. Accept different valid witnesses and explanations.

1. Start `(2,1)`: W gives `(1,4)`; N gives `(0,4)`. Undo N, then W. N inverse is `(u−v,v)`; W inverse is `(v−2u,u)`.
2. All starts `(a,3)` work. S,C maps `(x,y)` to `(y,y)`. Original y survives; original x is lost. For example `(0,3)` and `(1,3)`.
3. Start `(2,3)`: N gives `(0,3)`; W gives `(3,1)`. This time undo W, then N. Choosing the order matters more than reciting an inverse formula.
4. All starts `(a,4)` work: N,S,C maps `(x,y)` to `(y,y)`. Original y=4 survives, original x is free. Exactly five valid starts; non-unique does not mean infinite.
5. Extension: S,C and W,C both map every `(x,y)` to `(y,y)`. Either is a valid construction. The explanation must follow a generic pair, not just one successful example.

## Local repairs, selected from the actual attempt

- **Wrong W inverse:** point to which old value is stored in the new first slot. Ask the learner to recover `(1,2)` from W's result `(2,0)`. Do not reteach copying or equivalence if those parts were sound.
- **Wrong written order, correct calculation:** ask them to reverse the operation list once and reconcile it with their own states. Treat a transcription slip as provisional, not a global misconception.
- **Wrong original value called “lost”:** label the original pair `(x₀,y₀)` and track `S,C: (x₀,y₀) → (y₀,x₀) → (y₀,y₀)`. Ask which original value can still vary.
- **“Infinite” in this finite domain:** ask how many choices the free number has, then distinguish “more than one” from “infinitely many.”

Reserve cases, only for the repaired dimension: W,S gives `(2,2)` with unique start `(3,2)`; S,N,C gives `(1,1)` with exactly the five starts satisfying `x+y=1 mod 5`, including `(0,1)` and `(1,0)`. The latter preserves a sum, not either original coordinate individually.

## Human validation still needed

For a voluntary human trial, record actual start, first adequate independent attempt, transfer-check completion, and budget expiry; note aids and user-visible waiting. A correct answer copied after feedback is assisted evidence, not independent transfer. Check the explanation for contradictions as well as the final numbers. No recording, upload, or learner-file creation is automatic.

The pilot revealed the cost of rechecking all four tasks after local slips. This draft instead checks the affected step and then a changed case. That is a defensible design correction; its effect on actual human learning time remains unmeasured.
