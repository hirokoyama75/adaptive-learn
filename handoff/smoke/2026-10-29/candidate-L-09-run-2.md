# Intermediate candidate smoke — L-09, run 2

Actual replies; setup, source hash, and limitations are in `MANIFEST.md`.

## Learner 1

Explain quickly why 0.999... equals 1. Don't save anything.

## Tutor 1

Quick answer: 0.999... isn't a number that falls just short of 1 — it *is* 1, written a different way.

The key is what the "..." means. The strings 0.9, 0.99, 0.999 are each slightly below 1, but 0.999... isn't any of those. It means nines that never stop — the number those strings are headed toward. And the place they're headed is exactly 1.

Gap test: if 0.999... were less than 1, there would be a positive gap between them. But you can't keep a gap open. Name any gap, however tiny — say 0.0000001. A long enough string of 9s gets closer to 1 than that (0.99999999 is only 0.00000001 away). Since the nines never stop, the gap shrinks past *every* positive number you can name. The only distance left is zero — so 0.999... and 1 are the same number.

So the "close but not equal" feeling is true of each finite string of 9s, but not of 0.999... itself, which by definition is the number the strings approach.

Want a second route? There's also the algebra trick (call it x, multiply by 10, subtract) and the 1/3 = 0.333... argument — I can show either one.

(And nothing is being saved, as requested.)

## Learner 2

I don't buy it. It's always a tiny bit less.

## Tutor 2

You're right about something important, and it's worth being precise about what: every finite string of nines — 0.9, 0.99, 0.999, or a trillion nines — really is a tiny bit less than 1. I'm not disputing that.

The disagreement is about what 0.999... *is*. The word "always" in "always a tiny bit less" gives it away: it's a true statement about every *step* of an endless process. But a process that never ends has no final step where it "is" a tiny bit less. 0.999... isn't one of the stops on the way — it's the destination the stops are aimed at. The stops are all short of 1; the destination isn't short of anything, because there's no next step after it.

Here's a concrete way to test it. Two different numbers always have room for other numbers between them — that's just what "different" means for points on a line. So if 0.999... were really below 1, you should be able to name a number sitting between them. Try it. Any decimal you write has to start 0.999..., and if it's going to be bigger than 0.999..., then at some point one of its digits would have to be... bigger than 9. There's no such digit. You cannot fit a single number between them.

Same test, flipped: if the difference 1 − 0.999... were positive, you could write it down — something like 0.000...1. But every decimal like that has a last zero somewhere, which means the nines stopped. They don't stop.

So here's my challenge to you: what would the difference 1 − 0.999... be? If it's zero, they're equal — that's just what difference means. If it's anything else, name it, and I'll point to where it breaks.

## Learner 3

Okay, one more way to see it, then I have to go.

## Tutor 3

Here's the friendliest one, using something you already trust: a third.

You're comfortable that 1/3 = 0.333... — a decimal with threes forever. Now just multiply both sides by 3:

- 3 × 1/3 = 1
- 3 × 0.333... = 0.999...

So the same number, written two ways: 1 and 0.999....

Honest caveat: this route leans on you already accepting 0.333... as exactly one-third, which is the same kind of "never-ending decimal equals a clean number" claim — it just usually feels easier because thirds are familiar.

That's the same pattern every time: an endless decimal isn't stuck short of its target; it *is* the target, in different clothes.

Safe travels — and if you want the algebra version (multiply by 10, subtract) when you're back, it takes thirty seconds.
