# claim.md — 20260907-chernoff-neuralode-nd-multiseed-multin

**Graph node:** `H-B2-1m` (bridge `B2-CHERNOFF-UDE`) · **Tier:** Standard (reuses existing,
already-verified pipeline pieces byte-identically; no new stochastic-draw machinery)
**Parent:** `H-B2-1l` (kappa(V) CONFIRMED-with-weakening: the seed-ensemble leg, n=30 real
independent seeds at fixed N_DIM=8, survives — rho=0.453, p=0.012, ~20% of rank variance
explained. The N-sweep leg, rho=0.917, was WEAKENED/discredited by the session's own FL Step 8a
skeptic pass: `SEED=0` was hard-coded across all 9 N_DIM values, making that leg one deterministic
curve, not 9 independent draws — it never independently corroborated the seed-ensemble result.)

## Why This Experiment, Specifically

`H-B2-1l`'s own Relaxation Map (and the session's post-sweep next-steps table) named the correct
fix explicitly: a **genuinely** independent second population needs BOTH seed AND N_DIM to vary
with fresh random draws at every point — not seed varying with N fixed (already done, H-B2-1i),
and not N varying with seed fixed (the discredited leg). This experiment is that fix: for each of
`H-B2-1k`'s own 9 `N_DIM` values, draw multiple independent seeds and re-measure `(kappa(V), M1)`
pairs — replacing the discredited N-sweep leg with a real one, and testing whether the
seed-ensemble's partial finding (kappa(V) explains ~20% of M1's variance) generalizes across
dimension, not just at the one N_DIM=8 the original ensemble tested.

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE** (same as parent `H-B2-1l`/`H-B2-1i`/`H-B2-1k` — a correlational
claim about a measured mathematical quantity, no causal intervention framing).

## FL Step 0a — Mechanism Claim Gate (run BEFORE Step 1, per the rule just added to
`~/.claude/rules/falsification-ladder.md` this same session)

**Triggering sentence in this design:** "pooling `(kappa, M1)` pairs across DIFFERENT `N_DIM`
values still reflects a real kappa→M1 link" — a claim about how the pooled statistic *behaves*,
used to justify treating a single pooled Spearman correlation as the headline result.

**Check (run before writing this claim.md's kill criterion, script deleted after use):**
constructed synthetic `kappa'(N)` and `M1'(N)`, each an increasing function of `N_DIM` plus
independent random noise, with **NO direct link between kappa' and M1' by construction** — only
a shared N-trend. Pooled across the same 9 `N_DIM` values used here (10 synthetic seeds/N):

| Statistic | Result |
|---|---|
| Naive pooled Spearman | rho=0.948, p=2.1e-45 — spuriously "significant" despite zero real link |
| Within-N-slice Spearman (mean across the 9 slices) | rho=0.223 — correctly near the true (zero) relationship, appropriately noisy at n=10/slice |
| Rank-residualized partial correlation (N regressed out) | rho=0.290, p=0.0055 — still inflated; linear residualization does not fully remove a strongly heteroscedastic, nonlinear N-trend |

**Outcome: FAILS.** A naive pooled correlation across `N_DIM` is confounded and must NOT be the
headline statistic — confirmed directly, not assumed. **Design corrected before running the real
experiment:** the PRIMARY analysis is per-`N_DIM`-slice Spearman correlation (kappa vs. M1 across
seeds, at each fixed `N_DIM` separately), combined across slices via the fraction with the
predicted sign and via Fisher's method on the slice p-values. The naive pooled number is still
reported, explicitly labeled `[CONFOUNDED — NOT the claim under test]`, for transparency only.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `(kappa(V), M1)` pairs measured on `N_DIM x seed` matrices, `N_DIM` from `H-B2-1k`'s own 9-point set `(3,4,8,12,16,24,32,40,50)`, 15 seeds per `N_DIM` (seeds `0..14`). **RNG independence across `(N_DIM, seed)` pairs was CLAIMED here initially but was FALSE as first implemented** — `build_matrix_with_seed_and_n` originally seeded `np.random.default_rng(seed)` on `seed` alone, so the raw uniform stream was shared across every `N_DIM` for a matching seed index (independently verified by direct computation: `default_rng(0).uniform(size=(3,3)).ravel() == default_rng(0).uniform(size=(4,4)).ravel()[:9]`). Caught by the FL Step 8a skeptic pass, fixed to `default_rng(np.random.SeedSequence([n_dim, seed]))` before this claim.md was finalized — the numbers below are from the FIXED, genuinely independent version |
| **Falsifiable predicate** | The within-`N_DIM`-slice Spearman rho(kappa, M1) is positive in a majority of the 9 slices, generalizing `H-B2-1i`'s single-`N_DIM` partial finding |
| **Measurable outcome** | Count of slices with rho>0 (and separately, rho>=0.2 per `H-B2-1l`'s own pre-registered threshold), combined p-value via Fisher's method across the 9 independent slice tests |

## FL Step -3: Novelty Check

`grep` of `pearl_registry/INDEX.md` / `null_results/INDEX.md` / all `H-B2-1*` graph nodes: this
exact multi-seed-multi-N design is explicitly named as the correct fix in `H-B2-1l`'s own
CORRECTION ADDENDUM and the session report's next-steps table — not previously run. Confirmed
novel relative to this project's own prior attempts (which varied seed XOR N_DIM, never both).

## Kill Criterion (set BEFORE running; REFINED after FL Step 8a skeptic pass — see note)

- **CONFIRMED (generalizes across the FULL tested range):** majority of the 9 within-`N_DIM`-
  slice rhos are positive, AND Fisher's combined p-value across slices < 0.05, AND at least one
  slice at `N_DIM >= 24` is individually significant at alpha=0.05.
- **WEAKENED (partial, N_DIM-dependent):** majority positive with combined p < 0.05 but driven
  by small-N slices only (no large-N slice individually significant) — OR majority positive with
  combined p >= 0.05 — OR fewer than majority positive but the positive slices at/above
  `rho>=0.2` (H-B2-1l's own threshold).
- **REJECTED (does not generalize):** fewer than majority of slices positive, and combined p-value
  provides no evidence of a systematic positive relationship.

**Refinement note (FL Step 8a, run before this claim.md was finalized — not a post-hoc
correction to a committed verdict):** the original criterion above ("majority positive AND
combined p<0.05") does not distinguish a relationship that truly holds across the whole `N_DIM`
range from one that is real only at small `N_DIM` and vanishes at large `N_DIM`, because Fisher's
method can be dominated by a small number of extreme small-N p-values. Added the explicit
large-N individual-significance requirement for CONFIRMED specifically to close that gap — this
changes what "generalizes" is allowed to mean, not the underlying data.

## What This Does NOT Mean

1. Does NOT retroactively re-validate the discredited N-sweep leg of `H-B2-1l` — that leg stays
   WEAKENED/discredited regardless of this experiment's outcome; this is an independent, new test.
2. Does NOT establish causality — `kappa(V)` and `M1` are both functions of the same random
   coupling matrix; this tests correlation/explanatory power, not a causal mechanism.
3. A REJECTED or WEAKENED verdict here does NOT undo `H-B2-1i`'s own surviving n=30 finding at
   `N_DIM=8` specifically — that result stands on its own regardless of whether the relationship
   generalizes across dimension.
4. Even a CONFIRMED verdict would not establish `kappa(V)` as *the* dominant mechanism — per
   `H-B2-1l`'s own finding, it explained only ~20% of rank variance at `N_DIM=8`; this experiment
   tests generality of a partial, not total, explanatory relationship.

## MCID

Whether a majority of the 9 independent `N_DIM`-slices show `rho(kappa,M1) > 0`, reported as an
exact count and combined p-value — not rounded to a binary pass/fail on a single pooled number
(which Step 0a already showed is not a trustworthy statistic for this design).
