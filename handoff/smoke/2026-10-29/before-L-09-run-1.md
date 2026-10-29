# Before smoke — L-09, run 1

Actual replies; limitations and setup are in `MANIFEST.md`.

## Learner 1

Explain quickly why 0.999... equals 1. Don't save anything.

## Tutor 1

Quick answer: because "0.999…" names a *limit* — the number that the endless list 0.9, 0.99, 0.999, … gets arbitrarily close to — and that number is 1. The dots don't mean "a process that never quite finishes"; the whole expression is one fixed number, and its value is whatever the pattern homes in on.

**Why no gap is left over.** Suppose 0.999… were *less* than 1, by some tiny gap — call it *g*. Every positive gap you can name, no matter how small, gets beaten: 0.999 has gap 1/1000, 0.999999 has gap 1/1,000,000, and the nines keep going past any fixed size you propose. Since no positive gap fits, the gap must be 0 — so the two numbers are the same. There's no "infinitely small leftover"; the definition of the limit leaves nothing behind.

**A faster check if that feels abstract:** take *x* = 0.999…, then 10*x* = 9.999…, subtract the original: 9*x* = 9, so *x* = 1. Or: 1/3 = 0.333…, and three thirds make 1, so 0.999… = 1.

This surprises most people because it *looks* like the digits never arrive. They don't — and that's fine, because equality to the limit is about what the pattern approaches, not about some final digit. Want me to slow down on the gap argument, or is that enough?

## Learner 2

I don't buy it. It's always a tiny bit less.

## Tutor 2

What you're saying is *true* — for every finite string of nines. 0.9 is less than 1. 0.99 is less than 1. 0.999999999 is less than 1, and adding more nines keeps it less than 1. No disagreement there.

The step you're missing is this: **0.999… is not any of those.** It isn't 0.9 with a million nines, or a trillion, or however many you pick. "Never-ending" means it has *more nines than any finite number you choose*, so it is not equal to any of the decimals that are "a tiny bit less." The "tiny bit less" statement only ever applies to finite decimals, and 0.999… isn't one of them.

**A picture:** you stand 1 metre from a wall and each step covers half the remaining distance. After step 1 you've gone 1/2 m, then 3/4, then 7/8, then 15/16… At *every* step you are short of the wall — that's your "always a tiny bit less." But the place you're heading to is the wall itself, exactly 1 m. The steps never being there doesn't make the destination any less than 1.

**The test that settles it:** if two numbers are different, there's always room for a third number strictly between them (like 1.5 sits between 1 and 2). So if 0.999… < 1, there must be some number strictly between them.

Name it. What's 1 − 0.999…? If it's a tiny bit less, how much is that tiny bit? Try writing down any number you think fits between 0.999… and 1 — and I'll show you why the nines have already passed it.

## Learner 3

Okay, one more way to see it, then I have to go.

## Tutor 3

Here's one more, aimed straight at your objection:

The "tiny bit left over" has to *live somewhere*. If 0.999… is short of 1, there must be a digit position where it's short — like 0.99 is short at the third decimal place. Look at the leftovers: after one 9 you're short by 1/10, after two nines by 1/100, after three by 1/1000. The leftover is always "1 at some position": 0.01, 0.001, 0.0001…

But 0.999… never ends, so the leftover would be **0.000…1 with the 1 sitting after infinitely many zeros — a position that doesn't exist.** Every decimal place is already a 9; there is no place left for the shortfall to be. The gap gets squeezed out of the number system entirely.

That's the heart of it: every *finite* decimal is short of 1, but the infinite one has no slot left to be short at. Different object, different rules.

Glad you pushed on it — this one earns its disbelief, and you now hold the reason both for why it feels wrong and why it's still true. Happy to pick it up next time.
