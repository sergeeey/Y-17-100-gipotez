# claim.md — 20260908-chernoff-neuralode-nd-tighter-predictor-m1 (H-B2-1w)

**Graph node:** `H-B2-1w` (bridge `B2-CHERNOFF-UDE`) · **Tier:** Standard (empirical predictive
model over already-established, twice-independently-verified quantities; no new theory)
**Parent:** `H-B2-1u`/`H-B2-1v` (Kreiss mechanism MECHANISM_VERIFIED + independently
cross-validated; efficiency ratio established as low — the loose `e*n*K(A)` ceiling is valid but
far from a tight predictor of M1's actual magnitude)

## Why This Experiment, Specifically — User's Own Step 3, Option A (Chosen via AskUserQuestion)

The whole `H-B2-1` arc established a CORRELATIONAL chain (pseudospectral abscissa predicts M1's
existence/direction) and a THEORETICAL chain (Kreiss theorem bounds M1, loosely). Neither answers
a genuinely new, more useful question: **can a fitted empirical model, using the SAME already-
computed quantities (`K(A)`, `N_DIM`), predict M1's actual MAGNITUDE more precisely than either
(a) the naive theoretical ceiling `e*n*K(A)`, or (b) the established but cruder correlational
predictor (`alpha_eps` at `eps=1` alone)?** User explicitly chose the empirical-regression path
(Option A) over deriving a new analytic bound (Option B) — lower risk, reuses existing
infrastructure, fast result.

## EstimandOps L0 Gate

**Classification: PREDICTIVE.** This is the arc's FIRST predictive-tier claim (everything through
`H-B2-1v` was descriptive: correlation, or a proven-theorem computation check). A predictive claim
requires, per `estimand-ops.md`: population, intervention/predictor, comparator, endpoint, summary
measure, MCID — filled below — and a PRE-REGISTERED train/test split, decided BEFORE any test-set
value is examined (Anti-Overfitting Gate discipline, `falsification-ladder.md`).

| L1 attribute | Value |
|---|---|
| Population | Matrices from `build_matrix_with_seed_and_n` (H-B2-1m), `N_DIM` in {40, 50} (arc's established primary large-N regime) |
| Intervention/predictor | `K(A)` (Kreiss constant estimate, `H-B2-1u`'s `kreiss_constant_estimate`, reused unchanged) and `N_DIM` |
| Comparator | (a) naive ceiling `e*N_DIM*K(A)` as a point prediction; (b) simple log-linear regression on `alpha_eps` (pseudospectral abscissa at `eps=1`) ALONE, the arc's own established correlational predictor, reused from already-collected `H-B2-1t` data |
| Endpoint | `M1` — the SAME `w`-normalized transient growth constant (`max_t ||exp(tA)|| / exp(w*t)`, `w=0.5`) used throughout `H-B2-1r/1s/1t`'s own correlational tests (NOT `H-B2-1u`'s raw, non-normalized `raw_transient_growth` — different quantity, kept separate for continuity with the arc's established M1 definition) |
| Summary measure | Out-of-sample RMSE of `log(M1)` on the TEST set, for each of the 3 candidate predictors (K(A)-based regression, alpha_eps-only regression, naive ceiling) |
| MCID | K(A)-based regression's test RMSE must be lower than BOTH comparators' by a real, visible margin (not a coin-flip difference) to count as "tighter" — no numeric threshold pre-fixed beyond "strictly and visibly better on the actual numbers," reported honestly either way |
| ICE | None — no post-baseline events, this is a pure numerical fit/predict pipeline |

## Population / Split — Pre-Registered BEFORE Touching Test Data

**TRAIN set:** `H-B2-1u`'s own already-computed 20 `(K(A), M1)` pairs (seeds 300-309, `N_DIM` in
{40, 50}) — ZERO new compute, reused exactly as-is (Minimal Relaxation Rule). `alpha_eps`/`m1` for
the comparator model reused from `H-B2-1t`'s own stored `metrics/run.json` for the SAME 20
(N_DIM, seed) pairs.

**TEST set:** seeds 400-414 (15 seeds), `N_DIM` in {40, 50} — 30 matrices, GENUINELY FRESH (never
appeared in ANY prior experiment in this arc — checked against all prior ranges: 0-39, 40-99,
0-59, 100-159, 300-339). Requires fresh computation of BOTH `K(A)` (reusing `H-B2-1u`'s
`kreiss_constant_estimate` + `KREISS_GRID_KWARGS` unchanged) and `M1`/`alpha_eps` (reusing
`H-B2-1r`'s `pseudospectral_abscissa` and `H-B2-1k`'s `measure_m1` unchanged).

## FL Step 0a — Mechanism Claim Gate

No new "X targets/discriminates Y" behavioral sentence — the model form (log-linear regression on
already-validated quantities) is a standard statistical tool, not a claim about a specific
algorithm's behavior. The Kreiss theorem's own validity was already checked (`H-B2-1u`/`H-B2-1v`);
this experiment does not re-derive or re-assert it, only asks whether it (via `K(A)`) is a useful
PREDICTOR feature.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `(K(A), alpha_eps, N_DIM, M1)` tuples on 20 TRAIN + 30 TEST matrices |
| **Falsifiable predicate** | The `K(A)`-based log-linear regression, fit ONLY on TRAIN, achieves LOWER out-of-sample RMSE on `log(M1)` (TEST set) than both comparators (naive ceiling, `alpha_eps`-only regression) |
| **Measurable outcome** | Three RMSE numbers (K(A)-model, alpha_eps-only-model, naive-ceiling) on the same 30 TEST points, computed once, reported honestly regardless of which wins |

## FL Step -3: Novelty Check

`grep` of `pearl_registry/INDEX.md` and `null_results/INDEX.md`: no prior fitted predictive model
for M1 anywhere in this arc — every prior experiment tested CORRELATION (rho, p-value) or a
PROVEN INEQUALITY (Kreiss theorem check), never a fitted regression with an out-of-sample test.
Confirmed novel.

## Kill Criterion (set BEFORE running)

- **K(A)-model wins on TEST RMSE, by a visible margin:** genuinely useful new predictor found —
  `K(A)` (not just its correlational cousin `alpha_eps`) adds real predictive value beyond what
  was already established. Promotable finding.
- **K(A)-model does NOT beat `alpha_eps`-only on TEST:** the extra machinery (Kreiss constant
  estimation, expensive to compute, structurally limited per `H-B2-1u`'s Convergence Caveat) adds
  no practical value over the simpler, already-established `alpha_eps` correlation — a genuine,
  informative null result for the "tighter predictor" question, NOT evidence against anything
  established so far (the correlational and theoretical findings stand either way).
- **Neither model beats the naive ceiling:** would be surprising given the ceiling's known
  looseness (H-B2-1u: efficiency 3.7-6.3% median) — if this happens, investigate before reporting
  (same discipline as `H-B2-1u`'s own kill criterion for the proven-theorem check).

## What This Does NOT Mean

1. Does NOT retroactively change any prior verdict in this arc (`H-B2-1r/1s/1t/1u/1v` all stand
   regardless of this experiment's outcome).
2. A K(A)-model win does NOT mean the model generalizes beyond `N_DIM` in {40, 50} or beyond this
   specific matrix family (`build_matrix_with_seed_and_n`) — no claim about other matrix families.
3. Does NOT establish causality — `K(A)` is a property of the SAME matrix that generates M1, not
   an independent intervention.
4. A K(A)-model loss (does not beat `alpha_eps`-only) does NOT mean `K(A)`/the Kreiss theorem is
   "wrong" or "useless" — it answers a narrower question (practical predictive value ADDED beyond
   the simpler correlational predictor), separate from the theorem's own validity (already
   established) or from `alpha_eps`'s own correlational value (already established).

## MCID

Three RMSE values on `log(M1)`, TEST set only, reported as a table — no single pass/fail number,
the comparison itself IS the result.
