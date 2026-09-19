# H-CAT31-4 — decision.md

## Verdict

**Locked category: `P-MINUS-ONE`.** The pre-registered claim ("on primes the log-log slope CI
excludes `-1` and overlaps the composite band") is **killed as registered**, by a margin of 0.007
in slope. Not `UNDERPOWERED` (half-width 0.0836 < 0.10), not a substrate failure.

| quantity | value | source |
|---|---|---|
| weighted slope `b_P` (8 primes, 67..4093) | **-0.9231** | `metrics/analysis.json` |
| 95% t-interval (locked rule, dof 6) | **[-1.0067, -0.8396]** | same |
| contains `-1` | yes, by 0.0067 | same |
| contains composite slope `-0.9126` | yes | same |
| independent re-derivation (`verify.py`, `curve_fit` path) | slope differs by 1.7e-9, CI by 4.0e-9 | `metrics/verify.json` |

Read honestly: the prime sweep **cannot reject `n^-1`** on its own, and it is **statistically
indistinguishable from the composite sweep**. Both statements are equally supported; neither
"primes confirm the sub-`n^-1` law" nor "primes refute it" is licensed.

## Result table (`metrics/analysis.json`)

| n (prime) | reps | Var(X_n) | 95% bootstrap CI of Var | n·Var | z of mean(X_n) |
|---|---|---|---|---|---|
| 67 | 300 | 5.5208e-2 | [0.04619, 0.06414] | 3.699 | +1.54 |
| 127 | 300 | 3.5049e-2 | [0.02947, 0.04049] | 4.451 | +0.27 |
| 251 | 300 | 1.8853e-2 | [0.01594, 0.02192] | 4.732 | -1.10 |
| 509 | 250 | 9.4288e-3 | [0.00778, 0.01109] | 4.799 | -0.27 |
| 1021 | 200 | 5.1658e-3 | [0.00421, 0.00617] | 5.274 | +0.16 |
| 2053 | 200 | 3.2737e-3 | [0.00261, 0.00396] | 6.721 | +0.71 |
| 3001 | 200 | 1.4754e-3 | [0.00121, 0.00174] | 4.428 | +0.77 |
| 4093 | 100 | 1.3037e-3 | [0.00096, 0.00165] | 5.336 | -0.74 |

`n·Var` is not monotone: Spearman `rho = 0.595`, `p = 0.120` (no significant trend up or down).
The 95% intervals at `n = 2053` and `n = 3001` do not overlap; the independent seed block
(control 7) gives `Var(2053) = 0.00281` against `0.00327` in the main block (ratio 0.859), so the
main-block value at 2053 was on the high side by chance, not a sampler artefact.

## Controls (all pre-registered in `controls.md`; all passed)

| control | requirement | result |
|---|---|---|
| Substrate Gate | `theta(C5)=sqrt5`, `theta*theta_bar = n` at `n=67`, zero variance at `p=0` | READY (`metrics/substrate_gate.json`) |
| solver failures | `nan` rate <= 2% | 0 of 1850 |
| positive control (truth -1, 2000 simulated sweeps) | CI covers -1 in 92-98% | 95.35% |
| power control (truth -0.9126) | CI excludes -1 in >= 60% | 85.35% |
| symmetry (`E[X_n] = 0` at `p=1/2`) | max abs z <= 3.5 | 1.54 |
| independent verification | slope and CI agree to 1e-6 | agree (1.7e-9 / 4.0e-9) |
| seed block 2 (`n` = 509, 1021, 2053) | point estimates replicate | Var ratios 1.068, 0.890, 0.859 |

Because the power control passed (0.85), the `P-MINUS-ONE` result is not an artefact of a weak
design: had the true prime slope been `-0.913`, the design would have excluded `-1` about 85% of
the time. It did not, which is mild evidence that the prime slope is not far from `-1`, without
excluding `-0.913`.

## No-collapse / sensitivity variants (all reported; none changes the locked category)

| variant | slope | 95% CI |
|---|---|---|
| primary (weighted, t-interval) | -0.9231 | [-1.0067, -0.8396] |
| unweighted OLS | -0.9232 | [-1.0088, -0.8377] |
| robust variance (MAD) | -0.9424 | [-1.0047, -0.8800] |
| drop two smallest primes | -0.9624 | [-1.1342, -0.7906] |
| drop two largest primes | -0.8585 | [-0.9260, -0.7911] |
| `n <= 509` only | -0.8743 | [-1.0643, -0.6844] |
| `n >= 1021` only | -1.0779 | [-1.9809, -0.1748] |
| leave-one-out | -0.8837 to -0.9508 | (slopes only) |
| instance-resampling bootstrap of the slope | | [-0.9650, -0.8716] |

Two things to state plainly. (1) The instance-resampling bootstrap interval **excludes `-1`**
while the locked t-interval does not; the locked rule (claim.md) is the t-interval, so the
category stands, but the result sits on the boundary and depends on the interval construction.
(2) The large-`n` half alone has a very wide interval, so no drift can be read from the split.

## Post-registration analyses (labelled; not part of the verdict)

1. **Operational change after the first launch.** The first launch used 12 unpinned workers and
   the machine rebooted under load (measured: one LP at `n = 4093` peaks at 3.56 GB and starts 16
   HiGHS threads, `OMP_NUM_THREADS=1` does not limit them). The run was resumed with 4 workers,
   each pinned to 2 cores at below-normal priority. Statistical design, seeds and repetition
   counts are unchanged; 34 already-finished `n = 4093` solves were kept (same seeds, same
   deterministic computation).
2. **Joint fit with the composite sweep** (`analyze_post.py`, `metrics/analysis_post.json`),
   asked only after seeing the locked result: common slope `-0.9183`, 95% CI `[-0.9629, -0.8737]`
   (excludes `-1`); prime-minus-composite slope difference `-0.0106`, CI `[-0.1039, +0.0828]`;
   prime level shift `+0.0709`, CI `[-0.0556, +0.1974]`. This supports "primes and composites
   follow one law" but assumes a common slope and was chosen after the fact; it is a hypothesis
   for a pre-registered follow-up, not a result.

## Kill Analysis

**Killed:** the specific pre-registered claim, "prime-`n` slope CI excludes `-1`".

**Not killed:**
* the sub-`n^-1` decay observed on composites (`H-CAT31-3`), which primes neither confirm nor
  refute;
* the possibility that `Var(X_n) = C/n * L(n)` with a slowly varying `L`, which no finite-range
  slope can exclude;
* `Var(X_n) = O(1/n)` as an asymptotic statement.

**Relaxation Map** (one assumption per variant, separate experiment ids):
* V1: extend primes to `n = 8009+` (LP cost grows steeply; needs a specialised solver);
* V2: pre-register the joint prime-plus-composite common-slope fit and repeat with fresh seeds;
* V3: replace the variance target by a structurally motivated model (`C/n + D/n^2`) and compare
  models on the same rows.

## What this does NOT mean

1. It does not show `n^-1` is the true law; it shows this design cannot reject it on primes.
2. It does not show primes and composites differ: the estimated difference is `-0.011 +/- 0.09`.
3. It says nothing about `p != 1/2`, non-circulant graphs, or `n > 4093`.
4. The joint-fit exclusion of `-1` is post-registration and assumes a common slope.

## Claim Entropy (Perelman)

Before: 1 unresolved blocker (prime-`n` behaviour unknown), 1 hidden assumption (composite sweep
representative of primes). After: blocker cleared; the hidden assumption became an estimated
quantity (slope difference `-0.011 +/- 0.09`); new open item: interval construction sensitivity at
the `-1` boundary. Net change: 0 (one cleared, one created), so per Perelman this step does not
count as reducing entropy.

## Pearl Gate

Observation: on a boundary case the t-interval and the instance-bootstrap interval disagree about
`-1`. Falsifiable prediction: in a repeat with fresh seeds the bootstrap interval will again
exclude `-1` and the t-interval will again contain it (i.e. the disagreement is structural, from
only 8 points and dof 6). Impact 3 (local to variance-law reporting). Trigger: any future
pre-registration of a slope test with fewer than 10 design points. next_check: at V2 above.
Not written to the pearl registry.

## Files

`claim.md`, `controls.md` (pre-registered), `run.py`, `analyze.py`, `verify.py`,
`analyze_post.py`, `metrics/` (`thetas_main.jsonl`, `thetas_block2.jsonl`, `analysis.json`,
`analysis_post.json`, `substrate_gate.json`, `verify.json`), `sweep_main.log`,
`sweep_block2.log`.
