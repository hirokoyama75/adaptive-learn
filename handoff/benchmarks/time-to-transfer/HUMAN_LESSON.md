# Recover the original, or show why you cannot

Draft for a ten-minute human lesson; not yet tested with people. Show one section at a time. The tutor keeps the [facilitator notes](FACILITATOR.md) separate.

## A. The idea

The goal is to tell whether a result preserves enough information to recover its starting point.

A machine holds two numbers, each 0–4. Wrap arithmetic around 5: 6 becomes 1; −1 becomes 4. Each operation uses both **old** numbers at once:

- **W:** `(x,y) → (y,x+2y)`.
- **N:** `(x,y) → (x+y,y)`.
- **S:** swap the numbers.
- **C:** copy the first number into both slots.

For example, W takes `(1,2)` to `(2,0)`. To undo W on a new pair `(u,v)`, old `y=u` and old `x=v−2u`, wrapped. Undo a chain **last operation first**.

Copying is different: several starting pairs can produce one result. Later swaps or additions cannot bring back a lost distinction. Track the original numbers through the chain: C does not always erase the original second number.

## B. Try it

1. W then N gives `(0,4)`. What was the starting pair? Explain your undo order.
2. S then C gives `(3,3)`. Give two different starting pairs. What original information survives?

If one step is unclear, ask about that step. You do not need to repeat a part you have already shown correctly.

## C. New cases, without a hint

For each case, decide whether the starting pair is uniquely recoverable. Recover it, or give two possible starts and explain what remains known.

3. N then W gives `(3,1)`.
4. N then S then C gives `(4,4)`.

## Extension, only if needed and time remains

Do S then C and W then C always agree? Explain for any starting pair, not just an example. Can you build a process that puts the original second number into both slots?
