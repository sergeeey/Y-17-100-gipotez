# H-CAT30-2 — claim.md (redesign of H-CAT30-1 per its own Relaxation Map)

## Origin

H-CAT30-1 (`experiments/20260918-tensor-concentration-injective-norm-cat30/`) was REJECTED: its
fixed-`n=20`, scan-over-`d` pilot was proven mathematically DEGENERATE — the search was confined
to an at-most-`n`-dimensional subspace regardless of `d`, so the observed "plateau" was really an
order statistic (`E[max_i|g_i|]`), not evidence about tensor dimension. Its own decision.md named
a specific Relaxation Map: the ONE necessary change is `n=n(d)` scaling, so the search space is
genuinely `d`-dimensional (`span{a_i}=R^d` generically once `n≥d`).

This experiment implements that one necessary change, plus two of the Relaxation Map's secondary
items (between-family variance, a certified upper bound) — NOT the full list (adversarial search
and an SDP-certified bound are deliberately deferred, see "What this does NOT mean").

## The conjecture (same as H-CAT30-1, restated for self-containedness)

Bandeira et al., `arXiv:2603.29571`, Entry 8, Conjecture 16: for symmetric tensors `T_1,...,T_n ∈
(R^d)^⊗r`, i.i.d. Gaussian `g_i`, `p≥2`: `E||Σg_iT_i||_{I_p} ≤ Õ_{r,p}(d^{1/2-1/p}·sqrt(Σ||T_i||_{I_p}^2))`.
Proven for `p≥2r`. OPEN for `p<2r`. `r=3,p=2` (open, since `p=2<2r=6`) makes the rate dimension-free
(`d^0`).

## EstimandOps L0

**Question type:** Descriptive. "Does `R(d) := E||Σg_iT_i||_{I_2}/sqrt(Σ||T_i||_{I_2}^2)` grow with
`d` for a genuinely `d`-dimensional random rank-1 construction (`n=n(d)≥d`), on two independent
`n(d)` scalings?" No causal claim, no claim about the conjecture's general truth.

## Redesign changes from H-CAT30-1 (one assumption changed at a time, per Minimal Relaxation Rule)

1. **`n=n(d)` scaling (THE necessary fix).** Two independent scales tested: Scale A (`n=d`, the
   boundary case) and Scale B (`n=round(d^1.5)`, `n` growing faster than `d`). Independently
   re-verified `rank(A)=d` (full rank, `span{a_i}=R^d`) at every tested point
   (`verify_no_span_confinement.py`) — the specific mechanism that produced H-CAT30-1's degeneracy
   is now structurally absent (`x*` is no longer provably confined to a proper subspace).
2. **Between-family variance.** ≥8 independent draws of the tensor family `A` per `(scale,d)`
   point (H-CAT30-1 used exactly ONE family draw per `d`, a gap the reviewer explicitly flagged).
   Error bars use the variance of PER-FAMILY MEANS across families, not just within-family Monte
   Carlo noise.
3. **Certified upper bound as a validity check.** `σ_max(M)` of the mode-1 matricization `M∈R^{d×d²}`
   is a genuine, exact upper bound on `||S||_{I_2}` (proof: the matricization operator norm
   maximizes over independent `(u,W)` with `||u||_2=1,||W||_F=1`, a strict superset of the
   constrained `(x,x⊗x)` pairs the injective norm maximizes over — so `σ_max(M)≥||S||_{I_2}`
   always). Independently verified numerically on 4 cases before use
   (`verify_matricization_upper_bound.py`): sandwich holds in every case, ratio `1.04-1.13`.
   Computed on a small subset of draws per family as a spot-check on the power-iteration lower
   bound's reliability, not as the primary estimate.

## The claim (falsifiable, pre-registered BEFORE this run's numbers were seen)

Weighted power-law fit `log(R(d)) = α + β·log(d)` on each scale independently:
- **LEAD**: 95% CI on `β` excludes 0 AND is bounded away from `[-0.1,0.1]` in the POSITIVE
  direction (real growth beyond what polylog(d) could plausibly explain) on BOTH scales.
- **INFORMATIVE-NEGATIVE**: `β`'s CI is consistent with 0 or NEGATIVE on both scales (no growth
  — trivially consistent with the conjecture's upper bound, since the conjecture only requires
  `R(d)` to stay bounded, not to grow).

## What this does NOT mean

1. Does NOT attempt the full Relaxation Map — adversarial (optimization-driven) search over the
   `a_i` configuration, and a full SDP-certified upper bound, are both still absent. This
   redesign fixes ONLY the specific degeneracy H-CAT30-1's skeptic review found, per the Minimal
   Relaxation Rule (one assumption changed at a time) — not every named improvement at once.
2. A RANDOM (still non-adversarial) construction is known in advance to be a weak test for an
   UPPER-BOUND conjecture's tightness — H-CAT30-1's own skeptic review already flagged this
   ("Худший случай vs случайная реализация... ненатянутый инстанс ничего не говорит о валидности
   оценки"). A DECREASING or flat `R(d)` here is trivially consistent with the conjecture and
   provides NO evidence toward stress-testing whether the bound can be approached or violated —
   only a result showing UNEXPECTED GROWTH would be informative (a real, surprising finding);
   the absence of growth is close to a foregone conclusion for a non-adversarial construction and
   is stated here as a pre-registered fact, not spun as a discovery either way.
3. Does NOT prove Conjecture 16 in any sense, on either scale, regardless of outcome.
