# Addendum A': pre-registration of the follow-up search, written BEFORE it is run

Refers to `claim.md` (frozen at commit `f8c365a`). `claim.md` is not edited. Same outcomes (PASS-SMALL, PASS-LARGE, FAIL), same verification checks, same resources, same stop rules.

## What triggered it (observed, exploratory, `explore_a2.py`, not pre-registered)

Approach A as frozen (one of the 3 shortest vectors) gives valid exact PCC tuples with entries in {-1,0,1} and float dim V about 290 to 318 (exact rank 267 on the first tuple). Combining several vectors from a larger pool raises dim V:
pool m=6, c=2: 345 to 395 at max entry bit-length 2 or 3; m=12, c=3: one tuple with dim V = 424 at bit-length 3 (the other seven degenerate: dim V 4 to 79, bit-length 26 to 395). m=25 and m=40 exceeded 400 bits in all 8 runs. So dim V rises with pool size while entries stay small, until growth breaks the construction. Target: 463.

## Search A' (frozen parameters)

- Grid: pool m in {8, 10, 12, 14, 16, 18, 20}; combination size c in {2, 3, 4}; 12 seeds per cell (252 runs). Seeds start at 50000 to stay disjoint from earlier runs.
- Same builder as `explore_a2.py` (unchanged code), abort a run at 400 bits. Record float dim V and max bit-length for every finished tuple.
- Any tuple with float dim V >= 463 goes to `verify_instance.py` (exact checks) and counts as a PASS candidate only after that.
- Also recorded: the maximum float dim V reached per cell, so a null result still shows how close the search gets.

## Budget and stop

Wall-clock 45 minutes for A' (on top of the time already spent; total experiment budget stays 90 minutes counted from the first run at 17:54). At most 3 processes, cores 16-23, below-normal priority. Stop at the first verified PASS, or when the 252 runs or the budget end. No extension without a new addendum.

## Outcome interpretation, fixed now

- Verified PASS: an explicit instance exists (PASS-SMALL if entries <= 2^31, which 400 bits would already violate but the observed entries are tiny). The statement then no longer depends on the lifting lemma for the Q(i) instance (it still uses Observation 2).
- Maximum float dim V below 463 in every cell: FAIL for A'. This says nothing about existence.
- A float dim V of exactly 463 that the exact verifier rejects: recorded as a discrepancy between float and exact and investigated, not as a PASS.
- Prior stated now: 15 percent that A' finds a verified PASS. The dim V of 424 at 3 bits shows the constraint is not a hard wall, but 463 is the generic value and the bound `dim V-perp >= 21` is tight there, so extra structure in small tuples is likely to cost the last 39 dimensions.
