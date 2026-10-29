## Learner turn 1
There are three minutes left in my practice block. For x(x-2)=0, I got the solution set {0,2}. I divided both sides by x to get x-2=0 and x=2, then noticed x=0 also works in the original equation. I wrote that dividing by x is always legal here because the right side is zero. The final set is right, so is my justification right too? Help me understand the issue without starting the whole equations unit again. This is ungraded; do not save anything.

## Assistant turn 1
Your final set is right, but the justification isn't.

Dividing by \(x\) is legal only **when \(x \neq 0\)**. It has nothing to do with the right side being zero. Division by zero is undefined, period.

So this step:

\[
x(x-2)=0 \quad\Longrightarrow\quad x-2=0
\]

silently throws away the possibility \(x=0\). You noticed that afterward and checked it in the original equation, which is exactly why your final answer is still correct.

A sound version:

> If \(x \neq 0\), dividing gives \(x-2=0\), so \(x=2\). Separately, \(x=0\) makes the original equation true. Therefore the solutions are \(0\) and \(2\).

Cleaner still: use the zero product property directly:

\[
x(x-2)=0 \implies x=0 \text{ or } x-2=0 \implies x=0 \text{ or } x=2.
\]

The key habit: before dividing by a variable expression, ask whether it could be zero. If it could, split that case off or factor instead. Your instinct to check the original equation saved the answer here—keep that instinct.
