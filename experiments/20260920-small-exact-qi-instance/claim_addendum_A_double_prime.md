# Addendum A'': pre-registration of a prefix-resampling search, written BEFORE it is run

Refers to `claim.md` (frozen `f8c365a`) and `claim_addendum_A_prime.md` (frozen `8aa060e`). Neither is edited.

## Results that trigger it (recorded, final for the previous stages)

- Approach A as frozen: 200 tuples with entries in {-1,0,1}; all pass exact PCC and QFIM nonsingularity; exact rank of the stack 229 to about 310 (need 463). Verdict for A: FAIL.
- Approach A' (252 runs, grid as registered): best float dim V = 456 (m=10, c=3, seed 51032, max entry 564), exact rank mod two primes 456 (float and exact agree), 0 tuples at >= 463. Verdict for A': FAIL by its own criteria, but 7 short of 463.
- Time used at this point: about 10 of the 90 minutes.

## Search A'' (frozen parameters)

- Start points: the 5 A' tuples with the highest float dim V (rebuilt deterministically from their recorded seeds).
- Move: keep the first t blocks of a start tuple, t in {6, 8, 10, 12, 14}, and rebuild blocks t+1..16 with the same short-vector builder (`explore_a2.build` logic), pool m in {8, 10, 12}, combination size c in {2, 3}, fresh seeds. 12 resamples per (start, t, m, c) cell: 5 x 5 x 3 x 2 x 12 = 1800 builds.
- Abort a build at 400 bits. Record float dim V and max bit-length for each finished build. Greedy: if a resample beats the start tuple, it replaces the start for the remaining cells of that start point.
- A tuple with float dim V >= 463 goes to the separate exact verifier and counts only after passing it.

## Budget, stop, outcomes

Budget 30 minutes wall-clock, at most 3 processes on cores 16-23, below-normal priority; total experiment budget stays 90 minutes from 17:54. Stop at the first verified PASS or when the 1800 builds or the budget end. Outcomes as in `claim.md` (PASS-SMALL / PASS-LARGE / FAIL). No extension without a new addendum; after A'' the search stops unless a new pre-registration is written with a new reason.

Prior stated now: 30 percent that A'' reaches 463 (the start tuples are within 7 of the target and resampling only the tail preserves most of the structure), and 20 percent that a hit is found while max entry stays below 2^31 (any tuple of at most 400 bits passes PASS-LARGE but not PASS-SMALL; the observed entries so far are tiny).
