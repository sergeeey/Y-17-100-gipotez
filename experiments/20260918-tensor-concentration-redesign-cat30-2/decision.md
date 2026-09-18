# H-CAT30-2 — decision.md

## Result

**REJECTED — foreordained-null, not INFORMATIVE-NEGATIVE.** The redesign successfully removed
H-CAT30-1's span-confinement degeneracy (`n=n(d)` scaling, `rank(A)=d` confirmed at every point),
but a context-asymmetric skeptic proved the measured quantity has a DIFFERENT closed-form,
foreordained answer for ANY isotropic random rank-1 tensor family, regardless of the `n(d)`
scaling chosen. Independently re-verified before writing this record.

## The mechanism (proven, then independently re-derived and numerically confirmed)

`||S||_{I_2}=max_{||x||_2=1}|Σg_i⟨a_i,x⟩³|` is invariant under rotation of `R^d` — it depends on
`x` and the `a_i` only through the Gram matrix `G=AA^T` (n×n) and the projection `u=Ax`. As `d`
grows with `n` fixed OR growing more slowly (or comparably, for i.i.d. random unit `a_i`), `G`
concentrates toward `I_n`. **At exactly `G=I` (orthonormal `a_i`), a KKT argument gives
`||S||_{I_2}=max_i|g_i|` EXACTLY** — a simple order statistic of `n` Gaussians, carrying zero
information about tensor structure or dimension.

**Independently re-verified, three ways, before accepting (`verify_gram_identity_closed_form.py`):**
1. For `a_i=e_i` (exactly orthonormal, `G=I`), the power-iteration estimator recovers `max_i|g_i|`
   EXACTLY (`0.0000%` deficit) at `n∈{5,10,20}`, confirmed against an independently-implemented
   brute-force Nelder-Mead search (different code, not calling `estimate_injective_norm`).
2. At the skeptic's proposed "budget canary" (`n=80,d=200`, matching H-CAT30-2's actual restart
   budget of 40), the estimator STILL recovers the exact value with `0.0000%` deficit, even with
   200 restarts giving an identical answer — the restart-budget concern (their own MEDIUM-confidence
   item) does not change the result at this scale, though it remains untested for the true
   near-but-not-exactly-`I` Gram matrices the actual experiment used.
3. A free, non-optimization certified lower bound `max_i|(G³g)_i|` matches the exact value exactly
   in the orthonormal case, confirming the closed form algebraically, not just numerically.

**Fit against this closed form, using tabulated/asymptotic `E[max_i|g_i|]` values (skeptic's own
table, independently spot-checked): predicted `β = -0.376` (Scale A) vs observed `-0.3673`
(2.5% gap); predicted `β = -0.585` (Scale B) vs observed `-0.5613` (4% gap) — ZERO fitted
parameters.** Two full experiments (`n_families=8` × `n_gaussian_draws=15`, 4-8 `d` points each)
reproduced a Gaussian order statistic to within a few percent — the same outcome as H-CAT30-1,
via a different mechanism (there: span-confinement; here: Gram-matrix concentration).

## Additional confirmed issues (all independently checked, not accepted on the skeptic's word alone)

| Skeptic finding | Independent check | Verdict |
|---|---|---|
| `run.py` never calls the "independent cross-check" its own docstring promises | `grep -n "scipy_cross_check" run.py tensor_injective_norm.py` — zero matches in `run.py` | **CONFIRMED** — real methodology gap |
| The two `n(d)` scales (A: `n=d`, B: `n=d^1.5`) are not actually independent tests — if `R` depends on `d` only through `n`, the ratio `β_B/β_A` is forced to exactly `1.5` | `0.5613/0.3673 = 1.528` vs forced `1.5` — 2% gap | **CONFIRMED** — the "two independent scales" framing in claim.md was misleading |
| Scale B's reported 95% CI used the raw (unscaled) `se_beta` despite `chi2=13.48,p=0.0012` rejecting that model (same class of error as H-CAT30-1's own first-round CI mistake) | Recomputed: `scale=sqrt(13.48/2)=2.60`, `se_scaled≈0.039`, CI `≈[-0.638,-0.484]` — sign unchanged, but the originally-reported precision was unjustified | **CONFIRMED** |
| No positive control with a genuinely NON-decreasing `R` to establish the measurement pipeline's dynamic range | Skeptic's own proposed control (`a_i≡a` for all `i`, giving `R=E|Σg_i|/√n=sqrt(2/π)≈0.798` exactly, flat in both `n` and `d`) not implemented in this experiment | **ACCEPTED GAP** — not re-run here, named as a requirement for any future attempt |

## Kill Analysis (FL Anti-Overfitting Gate) — broadened per the skeptic's own recommendation

**What is killed:** not just this specific `n=n(d)` redesign, but the ENTIRE approach of "isotropic
random rank-1 tensor family + normalize by `sqrt(Σ||T_i||²)`" for probing Conjecture 16's open
`p<2r` regime — across BOTH attempts (H-CAT30-1's fixed-`n` design and H-CAT30-2's `n=n(d)` design),
the measured quantity reduced to a closed-form Gaussian order statistic unrelated to the
conjecture, for two different underlying reasons (span-confinement, then Gram-concentration).
This is now a general, twice-confirmed structural fact about this construction family, not a
one-off design flaw.

**What is NOT killed:** Conjecture 16 itself remains completely untouched — genuinely open. The
numerical pipeline (power iteration, matricization upper bound, span/rank verification) is
correct and reusable. The specific closed-form calibration found here
(`E||S||_{I_2} ≈ E[max_i|g_i|]·(1+ε(n/d))`, `ε≈0.02-0.21` in the tested range) is itself a genuine,
if modest, byproduct — it retroactively explains why NEITHER H-CAT30-1 NOR H-CAT30-2 could ever
have produced a LEAD, independent of any implementation detail.

**Relaxation Map (necessarily different in KIND from the previous one, not just degree):**
- **Non-isotropic / structured tensor families** — e.g. coherent frames (tightly correlated `a_i`,
  Gram matrix deliberately far from `I`), or a deterministic construction where the Gram spectrum
  does not concentrate — required so the "G→I" collapse mechanism cannot recur regardless of any
  `n(d)` scaling choice.
- **Genuine adversarial search** over the tensor family itself (optimizing the `a_i` configuration
  to maximize `R(d)`, not just drawing them randomly), matching the catalog's OWN originally
  suggested "First Research Experiment" — never actually attempted in either H-CAT30-1 or
  H-CAT30-2.
- If attempted: fix `run.py`'s dead cross-check (either call `scipy_cross_check` for real, or
  remove the docstring's false claim); add the flat positive control; use a bootstrap (not `t`
  or normal-approximation) CI given only 8 families; verify the injective-vs-Frobenius norm
  identification directly against the primary source's own definition (flagged `[UNKNOWN]` by
  the skeptic, not yet resolved in either experiment).

## Verdict

**REJECTED — foreordained-null / zero-signal**, per the skeptic's own proposed reclassification,
adopted here after independent verification. Not "the conjecture withstood a real stress test" —
the test never had statistical power to touch the conjecture's actual open content, by
construction, for a reason now understood and documented rather than merely suspected.

## What this does NOT mean

1. Does NOT mean Conjecture 16 is true, false, or that either random construction attempted
   provides any evidence either way.
2. Does NOT mean numerical/computational approaches to this conjecture are hopeless — only that
   isotropic random sampling (in either of the two forms tried) is structurally the wrong tool.
3. Does NOT invalidate the reusable numerical pipeline, which passed every direct correctness
   check applied to it (gradient, cross-checks at small scale, exact recovery on the orthonormal
   canary).

## FL Step 8a

Context-asymmetric skeptic (`claim.md` + core code + results, no session reasoning) — verdict
`FALSIFIED`, with a specific, independently-reproducible closed-form mechanism (not merely a
statistical critique). Every load-bearing claim in the skeptic's report was independently
re-derived with fresh code (`verify_gram_identity_closed_form.py`) before acceptance — exact
agreement on the orthonormal canary (0.0000% deficit, both against the closed form and an
independently-implemented brute-force search), confirmed dead cross-check via direct `grep`,
confirmed the forced `1.5` ratio via direct arithmetic on the already-reported numbers.

## Methodology lesson — this window's dominant pattern, now generalized across TWO consecutive experiments on the same catalog item

Not one design flaw caught twice by luck — two STRUCTURALLY DIFFERENT flaws (subspace
confinement, then Gram-matrix concentration), both independently discovered by context-asymmetric
skeptic review, both hiding behind a superficially reasonable "the plateau/decay looks consistent
with the conjecture" narrative. The generalizable lesson for any future numerical probe of a
concentration-inequality conjecture in this project: **before trusting an apparent trend (flat,
growing, or decaying) as evidence about an open bound, ask whether the SPECIFIC random
construction used has a closed-form, deterministic reduction — check the limiting/degenerate case
of the construction (here: `G→I`) analytically BEFORE running the full Monte Carlo sweep**, not
after. This would have caught both H-CAT30-1 and H-CAT30-2's core defect for a fraction of the
compute actually spent.
