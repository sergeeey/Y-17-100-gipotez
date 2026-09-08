# claim.md — 20260908-chernoff-neuralode-nd-tighter-predictor-robustness (H-B2-1x)

**Graph node:** `H-B2-1x` (bridge `B2-CHERNOFF-UDE`) · **Tier:** Standard (robustness follow-up
to an already-confirmed predictive result, no new theory, no new algorithm)
**Parent:** `H-B2-1w` (K_MODEL_WINS, decisively, on `log(M1) = -8.03 + 1.943*log(K(A)) +
1.330*log(N)`, fitted on 20 points, evaluated on 30 fresh points)

## Why This Experiment, Specifically

`H-B2-1w`'s own decision.md named two honest limitations of its result: (1) the fitted
coefficients carry no reported uncertainty (no confidence intervals), and (2) 20 training points
for a 3-parameter model is thin — the RESULT (12x/2.6x RMSE gaps) is large enough to trust the
DIRECTION, but not necessarily precise enough to trust the EXACT exponent (~1.94, "close to 2") at
face value. Before investing in Option B (deriving WHY M1 might scale as K(A)^2 analytically —
the user's own named next-level question), the cheapest differentiating step is to check whether
the exponent is a stable, well-estimated quantity or a noisy artifact of a small sample —
per this project's own Cheapest Differentiating Test Protocol (a test that could kill the "K^2"
observation is more valuable right now than either doing nothing or committing to a full
analytical derivation of a possibly-noisy number).

## EstimandOps L0 Gate

**Classification: PREDICTIVE** (same as `H-B2-1w` — this experiment refits the SAME model form
on a LARGER training set and validates on a FRESH held-out set; no new predictive claim type).

| L1 attribute | Value |
|---|---|
| Population | Same matrix family (`build_matrix_with_seed_and_n`), `N_DIM` in {40, 50} |
| Intervention/predictor | `K(A)`, `N_DIM` — unchanged from `H-B2-1w` |
| Comparator | `H-B2-1w`'s own fitted model (20-point TRAIN) — does the LARGER TRAIN set change the exponent meaningfully, or confirm it within a tighter CI? |
| Endpoint | `M1`, same definition as `H-B2-1w`/`H-B2-1t`/`H-B2-1r` |
| Summary measure | (a) 95% CI on the `log(K(A))` exponent (via OLS standard errors); (b) out-of-sample RMSE on a GENUINELY FRESH test set (not `H-B2-1w`'s own 400-414, to avoid re-using already-revealed test data for what is functionally a new validation) |
| MCID | The refit exponent's 95% CI should be reported honestly regardless of where it falls — "does it still bracket ~2, or does more data pull it toward 1 (matching the naive bound) or somewhere else" is itself the finding |

## Population / Split — Pre-Registered

**EXPANDED TRAIN:** `H-B2-1t`'s full 40-seed population per `N_DIM` (seeds 300-339, `N_DIM` in
{40, 50}) — 80 matrices total. `alpha_eps`/`M1` already stored in `H-B2-1t`'s own
`metrics/run.json` for all 80; `K(A)` already computed for the first 10 seeds per `N_DIM`
(300-309, from `H-B2-1u`) — this experiment computes `K(A)` fresh ONLY for the remaining 30 seeds
per `N_DIM` (310-339), 60 new computations, reusing `H-B2-1u`'s `kreiss_constant_estimate`
unchanged.

**FRESH TEST:** seeds 420-434 (15 seeds), `N_DIM` in {40, 50} — 30 matrices, genuinely new (zero
overlap with ALL prior ranges: 0-39, 40-99, 0-59, 100-159, 300-339, 400-414). `K(A)`, `alpha_eps`,
`M1` all computed fresh.

## FL Step 0a — Mechanism Claim Gate

No new mechanism claim — same discipline as `H-B2-1w` (standard regression tooling, not a new
algorithmic behavioral claim).

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `(K(A), alpha_eps, N_DIM, M1)` tuples on 80 EXPANDED-TRAIN + 30 FRESH-TEST matrices |
| **Falsifiable predicate** | The `log(K(A))` exponent's 95% CI, refit on the larger TRAIN set, either (a) still brackets a value near 2 (consistent with `H-B2-1w`'s observation), or (b) shifts meaningfully toward 1 or elsewhere (the original ~1.94 was a small-sample artifact) |
| **Measurable outcome** | Refit coefficients + standard errors; RMSE on the fresh 30-point TEST set for the refit model, compared against `H-B2-1w`'s original 20-point-trained model evaluated on the SAME fresh test set (does more TRAIN data actually improve out-of-sample accuracy?) |

## FL Step -3: Novelty Check

No prior confidence-interval reporting or TRAIN-set-size sensitivity check anywhere in this arc.
Confirmed novel (as a robustness check, not a new predictive claim type).

## Kill Criterion (set BEFORE running)

- **Exponent CI still brackets ~2, RMSE improves or holds with more TRAIN data:** the K^2 pattern
  is a real, stable feature of this matrix family — a solid basis to invest in Option B (analytic
  derivation).
- **Exponent CI shifts substantially (e.g., excludes 2, includes 1) or widens uninformatively:**
  the original ~1.94 was a fragile, small-sample estimate — do NOT invest in deriving "why K^2"
  for a number that isn't robust; report honestly as a corrected/weakened finding.

## What This Does NOT Mean

1. Does NOT retroactively change `H-B2-1w`'s `K_MODEL_WINS` verdict — that comparison (K-model
   vs. alpha_eps vs. naive ceiling) stands regardless of the exact exponent value.
2. Does NOT itself constitute an analytical derivation — even a robust, tightly-bounded ~2
   exponent remains an empirical observation for this matrix family, not a proven scaling law.
3. Does NOT establish causality.

## MCID

95% CI half-width on the `log(K(A))` coefficient (narrower = more confident); RMSE on the fresh
test set for both the original (20-point) and expanded (80-point) models, reported side by side.
