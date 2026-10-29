# Intermediate candidate smoke — L-09, run 1

Actual replies, including errors; setup, source hash, and limitations are in `MANIFEST.md`.

## Learner 1

Explain quickly why 0.999... equals 1. Don't save anything.

## Tutor 1

**Short version:** they're two names for the same number.

The quickest way to see it is that there's no gap between them. If 0.999… were less than 1, there'd have to be some number strictly between them, but you can't name one — any number smaller than 1, like 0.99999, still has room for 0.999999… to pass it. No gap means same point on the number line.

If you want the classic algebra route:

Let x = 0.999…

Multiply by 10: 10x = 9.999…

Subtract: 10x − x = 9.999… − 0.999… = 9

So 9x = 9, and x = 1.

The "…" is doing the work: it means the 9s go on forever, so subtracting shifts the endless part away completely. With any *finite* string like 0.999, the trick fails (9.99 − 0.999 ≠ 9), which is why people sometimes feel it's cheating — but for the infinite decimal it's airtight.

Nothing saved, as requested. Want a deeper route (what "…" formally means as a limit), or another argument?

## Learner 2

I don't buy it. It's always a tiny bit less.

## Tutor 2

Your instinct is right — for every decimal you can actually write down. 0.999 is a tiny bit less. So is 0.99999999. Add as many 9s as you like and it's still less than 1. No argument there.

The catch is that 0.999… isn't any of those. The "…" means the 9s never stop — and that changes everything, because the "tiny bit" needs a place to live.

Try to name the gap. Say the difference is 0.0001. But 0.99999 (five 9s) is already bigger than 0.9999, so it's within 0.0001 of 1. Say the gap is 0.0000001. Seven 9s beats it. Whatever positive gap you name — no matter how tiny — there's a finite string of 9s that's closer to 1 than that. And 0.999… goes past *all* of those finite strings, since its 9s never run out.

So the difference can't be 0.001, or 0.0001, or any positive number at all. The only number that's smaller than every positive number is zero. Gap of zero = same number.

Another way to feel it: if 0.999… were less than 1, the difference would be 0.000…1 — a 1 after infinitely many zeros. But there's no "after" infinitely many zeros. There's no last decimal place to put the 1 in. The difference has nowhere to exist.

Where the weirdness comes from is the definition of infinite decimals: 0.999… isn't a process you finish, it's the number the sequence 0.9, 0.99, 0.999, … gets arbitrarily close to. Every *term* of that sequence is less than 1 — your "always a tiny bit less" is exactly right — but the number the sequence defines is its limit, and that limit is exactly 1.

Want me to unpack that limit idea, or is the "name the gap" argument enough to chew on?

## Learner 3

Okay, one more way to see it, then I have to go.

## Tutor 3

Fast one, using something you already accept:

1/3 = 0.333…

Multiply both sides by 3:

3 × 1/3 = 1

3 × 0.333… = 0.999…

Same operation on the same number, so both results are the same number. If 1/3 really is 0.333…, then 0.999… really is 1. The only escape is declaring 1/3 ≠ 0.333…, which kicks the same problem one level down.

What's nice about this one: it's a different route reaching the same destination as the others — no subtraction trick, no "name the gap" — and they all agree. That's usually a good sign the result isn't a parlour trick.

See you next time — if the limit framing ever nags at you, we can pick it up there.
