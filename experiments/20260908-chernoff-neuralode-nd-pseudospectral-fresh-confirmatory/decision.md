# decision.md — 20260908-chernoff-neuralode-nd-pseudospectral-fresh-confirmatory (H-B2-1t)

## Result

Pre-registered primary criterion: **CONFIRMED**. Pseudospectral abscissa individually
significant, positive, at BOTH N=40 and N=50 on completely fresh seeds (300-339) — the first
replication of `H-B2-1r`/`H-B2-1s` on data this arc has never touched, in any form.

| N_DIM | descriptor | rho | p | significant? |
|---|---|---|---|---|
| 40 | kappa(V) | 0.323 | 0.0423 | yes (marginal) |
| 40 | omega(A) | 0.312 | 0.0503 | no |
| 40 | **pseudospectral abscissa** | **0.731** | **8.69e-8** | **yes, very strong** |
| 50 | kappa(V) | -0.106 | 0.514 | no |
| 50 | omega(A) | 0.091 | 0.578 | no |
| 50 | **pseudospectral abscissa** | **0.638** | **9.33e-6** | **yes, very strong** |

The differentiation between descriptors is large at both slices — pseudospectral abscissa's
effect (rho 0.64-0.73) is roughly double the comparators' at N=40 and unambiguous where they
are null at N=50. This directly supports the user's own "stronger claim": at large N,
pseudospectral abscissa predicts M1 more reliably than `kappa(V)` and `omega(A)`, now shown on
data independent of every prior confirmation.

## Comparator Prediction Partially Broken — Investigated, Not Glossed Over

`claim.md` pre-registered that an unexpected comparator hit would be flagged, not silently
absorbed. `kappa(V)` at N=40 gave p=0.0423 — marginally significant, breaking the null pattern
`H-B2-1q` established across TWO prior independent seed ranges (0-59, 100-159).

## FL Step 8a — Skeptic Pass

**Verdict: `[CONFIRMED-REAL]`** for the primary criterion, with one investigated caveat.

1. **Is the primary result robust, or could shared structure spuriously favor pseudospectral
   abscissa specifically?** Skeptic: no — if a shared confound (matrix norm, spectral radius,
   dimension) drove a spurious M1 correlation, all three descriptors would inherit it similarly.
   The observed differentiation (0.731 vs 0.323 vs 0.312 at N=40; 0.638 vs -0.106 vs 0.091 at
   N=50) is too large and too descriptor-specific for that. One residual, unverifiable-from-
   outside-the-code caveat the skeptic raised: definitional leakage between `pseudospectral_
   abscissa` and `measure_m1`. **Resolved directly (skeptic could not check this without code
   access, I can):** `measure_m1` computes `max_t ||expm(t*A)|| / exp(w*t)` over a time grid
   (H-B2-1k); `pseudospectral_abscissa` computes `max{Re(z) : sigma_min(zI-A) <= eps}` via a
   grid search over the complex plane (H-B2-1r). These share only the INPUT matrix `A` — no
   intermediate computation, no code, no derived quantity in common. No leakage.
2. **Is the comparator anomaly (`kappa(V)` p=0.0423) statistically surprising given 2 prior
   clean-null seed ranges?** Skeptic, computed directly: with 4 comparator tests at alpha=0.05
   under a true null, `P(>=1 hit) = 1 - 0.95^4 ~= 18.5%`. Getting exactly 1 marginal hit is
   unsurprising — NOT evidence against `H-B2-1q`'s `hard_killed` verdict. Also corrected my own
   framing: `omega(A)`'s p=0.0503 is not meaningfully a "near-miss" — statistically indistinguishable
   from p=0.08 or p=0.15; only the actual hit (`kappa(V)`, p=0.0423) counts.
3. **Does the N=40-specific pattern (both comparators strongest there) suggest something real?**
   Skeptic's hypothesis: `kappa(V)`/`omega(A)` could show "spillover" correlation with M1 simply
   because they are correlated BY CONSTRUCTION with pseudospectral abscissa (same matrix), not
   because they carry independent signal — predicting their raw correlation should weaken/vanish
   when controlling for pseudospectral abscissa via partial correlation.

## Direct Follow-Up: Partial Correlation (cheap, on already-collected data, walled off from the
pre-registered primary verdict per Anti-Overfitting Gate discipline — does NOT change CONFIRMED)

| N_DIM | descriptor | raw rho, p (vs M1) | partial rho, p (vs M1, controlling for pseudospectral abscissa) |
|---|---|---|---|
| 40 | kappa(V) | 0.323, 0.0423 | **0.365, 0.0207** — signal SURVIVES, slightly strengthens |
| 40 | omega(A) | 0.312, 0.0503 | **-0.099, 0.542** — signal VANISHES |
| 50 | kappa(V) | -0.106, 0.514 | -0.154, 0.344 — remains null |
| 50 | omega(A) | 0.091, 0.578 | -0.005, 0.974 — remains null |

**This resolves the skeptic's spillover hypothesis differently for the two comparators.**
`omega(A)`'s weak N=40 signal behaves exactly as predicted by spillover — it disappears once
pseudospectral abscissa is controlled for, meaning `omega(A)`'s raw correlation was riding on
its own correlation with pseudospectral abscissa, not independent information. `kappa(V)`'s
signal does the OPPOSITE — it survives, and slightly strengthens (p: 0.042 -> 0.021) — NOT
consistent with pure spillover. This does not revive `kappa(V)`'s `hard_killed` status (a single
modest hit in a third seed range, still well within chance-level per the skeptic's own binomial
calculation) but IS a genuine, specific, walled-off observation worth a Pearl Registry entry
for future investigation, not a change to any current verdict.

## Kill Analysis

**What this experiment killed:** the possibility that `H-B2-1r`/`H-B2-1s`'s pseudospectral
abscissa result was somehow specific to the one 15-seed sample used in both — it replicates
cleanly, and more strongly, on entirely fresh data.

**What this experiment did NOT kill:** `H-B2-1q`'s `hard_killed` verdict for `kappa(V)`/`omega(A)`
at N>=40 — the one marginal comparator hit is within chance-level expectation, confirmed by
direct binomial calculation, not evidence of a revival.

## What This Does NOT Mean

1. Does NOT retroactively change `H-B2-1q`'s `hard_killed` verdict for `kappa(V)`/`omega(A)` —
   the partial-correlation finding is walled off, reported for transparency, not promoted to a
   claim.
2. Does NOT constitute publication-grade evidence by itself — this is one strong, independent
   replication among what would ideally be several before any external claim.
3. Does NOT establish causality.
4. The `kappa(V)`-survives-partial-correlation observation does NOT establish that `kappa(V)`
   carries real independent information at N=40 specifically — a single result in a third seed
   range, at a modest effect size, is suggestive at most.

## Relaxation Map / Next Steps (not auto-launched)

- **Priority 3 (user's own plan, now the correct next step):** mechanistic analysis of WHY
  pseudospectral abscissa succeeds where `kappa(V)`/`omega(A)` fail (resolvent amplification ->
  Kreiss constant -> transient growth -> Chernoff bound constant M1) — this experiment's clean,
  twice-independent-seed-range replication is exactly the evidentiary base that analysis should
  build on.
- A fourth independent seed range specifically testing whether `kappa(V)`'s N=40 partial-
  correlation survival replicates — named as a Pearl Registry entry, not launched (would need a
  specific trigger: another `kappa(V)` marginal hit at N=40 in unrelated future work).

## Pearl Registry Update

New finding, walled off from any current verdict: `kappa(V)`'s weak N=40 signal (p=0.042, this
seed range) SURVIVES partial correlation controlling for pseudospectral abscissa (p=0.021,
slightly stronger) — unlike `omega(A)`'s equivalent signal, which vanishes under the same
control (consistent with spillover). One point is noise; two would be a pattern worth revisiting
`H-B2-1q`'s `hard_killed` status for `kappa(V)` specifically (not `omega(A)`, which behaved as
expected).
