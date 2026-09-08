# decision.md — 20260908-chernoff-neuralode-nd-tighter-predictor-m1 (H-B2-1w)

## Result

**K_MODEL_WINS — decisively, on genuinely held-out data.** The `K(A)`-based log-linear model,
fit ONLY on `H-B2-1u`'s existing 20 `(K(A), M1)` pairs and evaluated on 30 fresh, never-before-
touched matrices (seeds 400-414, N_DIM in {40, 50}):

| Model | RMSE on log(M1), TEST set | Relative to K-model |
|---|---|---|
| **K(A)-based (K, N)** | **0.3046** | 1x (best) |
| alpha_eps-only (arc's established correlational predictor) | 0.7950 | 2.6x worse |
| naive ceiling e·n·K(A) (point prediction) | 3.7101 | 12.2x worse |

This is the first PREDICTIVE-tier result in this arc, and the pre-registered kill criterion
("K-model beats both comparators, by a visible margin") is satisfied cleanly — not a marginal
or ambiguous call.

## Fitted Model

```
log(M1) = -8.03 + 1.943 * log(K(A)) + 1.330 * log(N_DIM)
```

**Notable, checkable pattern:** the fitted exponent on `K(A)` is ~1.94, close to **2**, not 1.
The naive theoretical ceiling `e*n*K(A)` implicitly assumes M1 scales LINEARLY with `K(A)`
(exponent 1) — the fitted data instead suggests M1 scales closer to **K(A) SQUARED**. This is a
genuinely new, quotable empirical regularity distinct from the theorem's own (linear, loose)
bound — stated as an observation from THIS fit on THIS matrix family, not a general theorem.

## Why the comparators lose — mechanistic, not just numeric

Inspecting the TEST data directly: `alpha_eps` (pseudospectral abscissa at `eps=1`, computed via
`H-B2-1r`'s grid search) repeats the SAME few values across many different matrices (e.g.
`8.313131313131315` appears for 3 of the first 4 test seeds) — a direct consequence of grid-search
discretization at a fixed, coarse resolution (same mechanism flagged in `H-B2-1u`'s and `H-B2-1v`'s
own convergence caveats). `K(A)` (from `H-B2-1u`'s multi-eps local-grid estimate) has much finer,
more continuous resolution across matrices. Part of `alpha_eps`'s weaker predictive performance is
therefore an INFORMATION-CONTENT limitation of the coarse `eps=1` grid, not only a "wrong feature"
issue — consistent with, not contradicting, this arc's established understanding of grid-search's
resolution limits.

## FL Step 8a — Skeptic-Style Self-Check (informal)

**Concern anticipated:** "the TRAIN set (K range 30-262) and TEST set (K range 30-161) don't fully
overlap in range — is the K-model's win partly an artifact of interpolation vs extrapolation
being easier for one model than another?" **Response:** Both models are evaluated on the EXACT
SAME 30 test points — any interpolation/extrapolation asymmetry would need to differentially favor
the K-model specifically, and there's no structural reason `alpha_eps`'s regression would face a
harder extrapolation problem than `K(A)`'s (both are single-feature-plus-N fits over comparable
train ranges). The `alpha_eps` model's failure is better explained by its coarse-grid tied values
(see above) than by range mismatch.

**Concern:** "20 training points for a 3-parameter model is thin." **Response:** True, and stated
explicitly in `claim.md` as an acceptable first-pass scope (Cheapest Differentiating Test
discipline) — the RESULT (12x and 2.6x RMSE gaps) is large enough that thin training data is an
unlikely full explanation; a future follow-up with a larger TRAIN set (more of `H-B2-1t`'s already-
collected 40-seed population, computing `K(A)` for the remaining 30 seeds per N_DIM) would firm
this up further, named below as a next step, not required to trust THIS result's direction.

## Kill Analysis

**What this experiment killed:** the possibility (implicit in treating `K(A)` as "just a
theoretical curiosity behind a loose bound") that `K(A)` adds no PRACTICAL predictive value beyond
the arc's already-established `alpha_eps` correlation. It clearly does, on this population.

**What this experiment did NOT kill:** nothing about prior verdicts — `H-B2-1u`'s
`MECHANISM_VERIFIED` and `H-B2-1v`'s independent cross-validation both stand; this experiment
answers a narrower, additional question (predictive value ADDED).

## What This Does NOT Mean

1. Does NOT retroactively change any prior verdict in this arc.
2. Does NOT mean the fitted model generalizes beyond `N_DIM` in {40, 50} or beyond this specific
   matrix family (diagonal + strictly-upper-triangular random coupling).
3. Does NOT establish causality — `K(A)` and `M1` are both properties of the SAME matrix.
4. The `~K²` exponent is an empirical observation from THIS fit, NOT a derived theorem — it is a
   candidate for future theoretical investigation (Option B of the user's own original Step 3
   framing), not itself a proof.
5. Does NOT mean `alpha_eps` (pseudospectral abscissa) is a bad descriptor generally — it remains
   the established, twice-independently-verified CORRELATIONAL predictor from `H-B2-1r/1s/1t`;
   this experiment only shows `K(A)` adds MORE precision as a magnitude predictor specifically.

## Relaxation Map / Next Steps (not auto-launched)

- Expand TRAIN set using `H-B2-1t`'s remaining 30 seeds per N_DIM (already has `alpha_eps`/`m1`
  stored; only needs fresh `K(A)` computation) — would firm up the fitted coefficients and their
  uncertainty (currently unreported — a natural next addition: confidence intervals via
  bootstrap or OLS standard errors).
- Investigate the `~K²` pattern theoretically (Option B from the original Step 3 framing) — is
  there a derivable reason `M1 ~ K(A)^2 * N^{4/3}`-ish for this matrix family specifically?
- Test generalization to other N_DIM values (currently only 40, 50 — the arc's established
  primary regime) or other matrix families (would require new `build_matrix_with_seed_and_n`-
  style constructions, out of scope here).

## Pearl Registry Update

New, general finding: for this matrix family, `M1` scales empirically closer to `K(A)^2` than
`K(A)^1` (fitted exponent ~1.94) — a candidate regularity worth checking analytically. Separately:
`alpha_eps` at the arc-wide grid's `eps=1` resolution shows visible value-repetition (discretization
ties) across distinct matrices — worth remembering as a limitation when `alpha_eps` (not `K(A)`) is
used as a fine-grained ranking feature in any future work.
