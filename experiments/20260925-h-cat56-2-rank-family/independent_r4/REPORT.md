# Independent-code check of the r = 4 certificate (d = 31, s = 13): report and verdict

Verdict against `PREREG.md` (fixed before any run): **PASS**. Label: `[VERIFIED-independent-implementation, same-briefing-author]`, at most Medium. Not U3.

## What was run
The blind implementer's library from the r = 3 check (`../independent_r3/cx_modp.py`, `run_float.py`), **unchanged**, driven by `run_r4.py` and `run_float_r4.py` (parameters and printing only).
Not fresh blindness: I knew my own value (30) and I wrote the driver; the prediction was registered before the run, and a plumbing sanity (d=23, r=3, s=12 -> 22, already known) passed first.
Everything below was produced by me in one run of each script (no agent report in this step, so there was nothing to take on trust).

## Results (d = 31, r = 4, k = 27, s = 13)
| check | independent code | my saved `fp_certify` / registered value | agree |
|---|---|---|---|
| plumbing sanity d=23, r=3, s=12 | dim V-perp 22 | 22 | yes |
| exact, p = 998244353, seeds 1, 2 | SLD ok, PCC ok (full 31 x 31 commutators), det QFIM != 0, dim V 931, dim V-perp **30** (both) | 30 | yes |
| exact, p = 1000000007, seeds 1, 2 | same, dim V-perp **30** (both) | 30 | yes |
| float complex128 SVD, seeds 1, 2 | dim V-perp 30; gap ratio 1.04e13 and 1.49e13; next-largest ratio 16, 19 (unique gap) | 30 | yes |
| stage solution-space dims j = 2..13 | 200, 184, ..., 24 (= 216 - 16(j-1)) | identical list | yes |
| N1 corrupt one entry of B_5 | PCC fails on exactly the 12 pairs containing block 5 | (control) | detected |
| N2 B_13 := B_12 | det QFIM = 0 (rank 12); dim V-perp = 41 | equals my registered below-crossing value at (31,4,12) = 41 | consistent |
| N3 s = 14 | stage-14 nullity 13 < 14, det QFIM = 0, dim V-perp 30 (exact and float) | claim.md addenda: singular QFIM, value at s* | consistent |

N2 is a small extra independent consistency: duplicating the last block collapses the state to an effective s = 12 tower and gives 41, the same integer my pre-registered
control (31, 4, 12) produced with entirely different code.

## What this does and does not show
Shows: for r = 4 the value 30 is reproduced by code that never saw `fp_certify.py`, on two other primes, four exact runs, and in float, with negative controls behaving as predicted.
Does NOT show: independence of the definitions (my write-up of arXiv:2601.21801, shared with the implementer); author independence; an explicit Q(i) instance (generic mod-p points,
lifting lemma unreviewed); novelty; anything for r = 5. Weaker than the r = 3 check in one respect: the library is the one already validated at r = 3, and the driver author knew the expected value.
