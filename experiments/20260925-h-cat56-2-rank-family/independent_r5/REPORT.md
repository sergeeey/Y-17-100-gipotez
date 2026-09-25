# Independent-code check of the r = 5 certificate (d = 41, s = 14): report and verdict

Verdict against `PREREG.md` (fixed before any run): **PASS**. Label: `[VERIFIED-independent-implementation, same-briefing-author]`, at most Medium. Not U3.

## What was run
The blind implementer's library from the r = 3 check (`../independent_r3/cx_modp.py`, `run_float.py`), **unchanged**, driven by `run_r5.py` and `run_float_r5.py` (copies of the r = 4 drivers with parameters and
printing only). Same standing as r = 4: no fresh blindness (I knew my own value and wrote the drivers); all predictions were registered before the run; a plumbing sanity (d=23, r=3, s=12 -> 22) passed first.
All numbers were produced by me in one run of each script; no agent report was involved in this step.

## Results (d = 41, r = 5, k = 36, s = 14)
| check | independent code | my saved `fp_certify` / registered value | agree |
|---|---|---|---|
| plumbing sanity d=23, r=3, s=12 | dim V-perp 22 | 22 | yes |
| exact, p = 998244353, seeds 1, 2 | SLD ok, PCC ok (full 41 x 41 commutators), det QFIM != 0, dim V 1641, dim V-perp **40** (both) | 40 | yes |
| exact, p = 1000000007, seeds 1, 2 | same, dim V-perp **40** (both) | 40 | yes |
| float complex128 SVD, seeds 1, 2 | dim V-perp 40; gap ratio 5.9e12 and 6.8e12; next-largest ratio 26, 27 (unique gap) | 40 | yes |
| stage solution-space dims j = 2..14 | 335, 310, ..., 35 (= 360 - 25(j-1)) | identical list | yes |
| N1 corrupt one entry of B_5 | PCC fails on exactly the 13 pairs containing block 5 (4 earlier + 9 later) | registered | detected |
| N2 B_14 := B_13 | det QFIM = 0 (rank 13); dim V-perp = **61** | **registered in advance**: equals my pre-registered below-crossing value at (41,5,13) = 61 | yes (prospective hit) |
| N3 s = 15 | stage-15 nullity 14 < 15, det QFIM = 0, dim V-perp 40 (exact and float) | registered | yes |

The N2 hit is the informative one: at r = 4 the same equality was noticed after the fact, here it was written down before the run and came out exactly (61), with code that never saw the (41,5,13) run.

## What this does and does not show
Shows: for r = 5 the value 40 is reproduced by code that never saw `fp_certify.py`, on two other primes, four exact runs and in float, with all registered controls behaving as predicted. Together with
`independent_r3` and `independent_r4` this covers r = 3, 4, 5 by the same independent library.
Does NOT show: independence of the DEFINITIONS (my write-up of arXiv:2601.21801, shared with the implementer); author independence (a different model instance briefed by me; for r = 4, 5 the driver author
also knew the value); an explicit Q(i) instance (generic mod-p points, lifting lemma unreviewed); novelty; anything for r >= 6. Runtime note: the largest exact run took 801 s (d = 41, p = 1000000007, seed 2).
