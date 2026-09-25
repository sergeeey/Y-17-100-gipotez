# H-CAT56-2 rank family: F_p certificates for r = 4, 5 and sharpness controls (pre-registered 2026-09-25)

Written BEFORE any run in this folder. Question type (EstimandOps L0): **descriptive / existence** (a mathematical object with a
stated property); no causal layer. Tier: Standard (extension of an already-frozen Full-Ladder result; nothing here changes the
frozen r=2 claim or the sent email).

## What is already known (so nothing below is presented as new)
- `20260919-pcc-generic-quasipure-cat56-2/decision.md` (C-ID, C-LB, C-CEIL): `dim V-perp >= LB(k,r,s) = r^2 + max(s, 2kr - s r^2) + max(1, k^2 - C(s,2) r^2)`,
  and the first size where `min_s LB < d` is d = 22 (r=2), 23 (r=3), 31 (r=4), 41 (r=5).
- `metrics/fp_certify_d22_r2_s16.json` and `..._d23_r3_s12.json` (commit 8813a33): both F_p certificates fire (dim V-perp 21 and 22).
- So r = 2, 3 are DONE. This folder adds r = 4, 5 and the sharpness controls (s below / above the crossing).

## Claim (falsifiable)
The F_p-lifting certificate `fp_certify.py d r s` (same code, unchanged, primes 67108837 and 67108777, both 1 mod 4) gives
`all_ok = True` and `dimVperp_mod_p = r^2 + max(s, 2kr - s r^2) + 1` (the measured generic closed form) at:

| d | r | k | s | predicted dimVperp | fires (< d)? |
|---|---|---|---|---|---|
| 31 | 4 | 27 | 13 | 30 | YES |
| 41 | 5 | 36 | 14 | 40 | YES |

Controls (must NOT fire, and pin the formula from both sides):

| d | r | s | predicted dimVperp | fires? |
|---|---|---|---|---|
| 31 | 4 | 12 | 41 | no |
| 31 | 4 | 14 | 31 (= d) | no |
| 41 | 5 | 13 | 61 | no |
| 41 | 5 | 15 | 41 (= d) | no |
| 23 | 3 | 11 | 31 | no |
| 23 | 3 | 13 | 23 (= d) | no |

## Kill criteria (fixed now)
1. Any firing config with `all_ok = False` (a flag false on either prime, or kernel dims != float generic) => that rank is NOT certified.
2. Any config with `dimVperp_mod_p < LB` => C-LB is falsified (or the code is wrong): STOP and debug before anything else.
3. A predicted value off by more than 0 (integer equality) => the closed form is not general; record which, do not refit silently.
4. A control that fires => the sharpness statement is false.

## What this does NOT show
- No explicit Q(i) instance for these ranks (existence via the lifting lemma only; same status the r=2 claim had before seed 701082).
- Same author, same code path as r=2: this raises breadth, not independence. `verification_strength` stays medium.
- Nothing about minimality of d over ALL constructions: C-CEIL is a statement about this test (dim V-perp < d), not about counterexamples in general.
- Novelty is unchanged (U2 open).

## Addendum 2026-09-25 (written after reading (31,4,14) and BEFORE reading (41,5,15) and (23,3,13))

Result that triggers it: control (31, 4, 14) gave `dimVperp = 30` and `fires = True` on both primes, with `qfim_det_nonzero_mod_p = False`.
By kill criterion 2 this said "stop and debug". Debug outcome, checked in float with the project's own sampler
(`h2_core.sample_sequential`, seed 20260919): at s = 14 the QFIM has rank 13 < 14 (s = 12, 13 give full rank). So the 14th block is
real-dependent on the earlier ones, the state is outside the class (nonsingular QFIM is a hypothesis of both C-LB and the claim), and C-LB is
**not** violated (its precondition fails). The value 30 equals the s = 13 value, i.e. the extra block adds nothing.

Pre-registration error, stated plainly: I registered "s above the crossing" controls as if such states existed. The sequential tower has at most
`s* = ceil(2kr/(r^2+1))` non-degenerate blocks (decision.md, C-CEIL: "s* the largest non-degenerate s"), so for s > s* there is no admissible state
in this construction. Consequence: kill criterion 4 ("a control that fires") is NOT triggered in substance, because the object is not in the class.

Amended, prospective predictions for the still-unread above-crossing controls (41, 5, 15) and (23, 3, 13): same signature as (31, 4, 14),
namely `qfim_det_nonzero_mod_p = False` on both primes and the F_p rank equal to the value at s = s*, i.e. `dimVperp` = 40 and 22 respectively.
If instead a QFIM comes out nonsingular there, the "s* is the maximum" reading is wrong for that rank and this is recorded.

The below-crossing controls (31,4,12), (41,5,13), (23,3,11) and the four firing configs stand exactly as registered.
What the above-crossing controls can NOT support: any statement that larger s is impossible outside this tower; the sharpness is a statement about
`min_s LB` and about this construction only.

## Second addendum 2026-09-25 (after the independent reviewer pass; earlier text above is untouched)

1. **Kill criterion 3 (integer mismatch) also fired on (31,4,14)**, not only criterion 2: the registered value was 31, the result was 30. The addendum above discussed 2 and 4 only.
   Plain count: all three above-crossing rows registered in the table above (31, 41, 23) were wrong as predictions, i.e. **3 of the 10 registered predictions failed**;
   the 4 firing rows and the 3 below-crossing rows (7 of 10) held.
2. **The amended predictions are forced, not independently tested.** In the JSON the last kernel dimension of the tower equals `s - 1` in all three above-crossing
   configs (13 < 14, 14 < 15, 12 < 13). A nonsingular QFIM is a positive-weighted Gram matrix of the `s` blocks, and all of them lie in that kernel, so it needs
   `dim K_s >= s`. Singularity was therefore certain in advance, and the clause "if a QFIM comes out nonsingular there, the reading is wrong" could not have fired.
   What the match shows is that the bookkeeping agrees with a counting argument; it is not a risky test of `s*` being the maximum. The counting argument is the
   actual explanation of `s*` `[INFERRED]`.
3. **Limit on this file's own pre-registration claim:** the first half of this file was never committed before the runs, so "written before any run" rests on the
   author's word; only the timing of the first addendum is checkable (file mtimes versus JSON mtimes). Next time: commit the claim before the first run.
