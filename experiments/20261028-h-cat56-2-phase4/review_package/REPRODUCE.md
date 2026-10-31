# REPRODUCE — minimal verification instructions (H-CAT56-2)

All commands are run from the folder `experiments/20261028-h-cat56-2-phase4/`. Python 3 with numpy, scipy and python-flint (for `fmpz`, `fmpq`, `arb`). Do not re-run long jobs unless a defect is found; the expected outputs below are what the existing logs contain.

Paths to the instance and to the direction file are absolute in the code (`stage_e_v1/code/ys_space.py`, `INST`). They refer to the project directory on the author's machine and must be edited to reproduce elsewhere.

## 1. Integrity

```
sha256sum -c review_package/SHA256SUMS.txt
```
Every line must print `OK`. This file lists the reviewed files, the exact logs and the input files (instance, direction file) by SHA-256.

## 2. S₊: certificate checks

| Step | Command | Expected | Cost |
|---|---|---|---|
| 2a. Exact Y_S membership (1484 × 12, Fraction) | `python stage_e_v1/code/audit_ys_exact.py` | 0 violations (`stage_e_v1/logs/audit_ys_exact.json`) | minutes |
| 2b. Linearisation of A | `python stage_e_v1/code/audit_lift_rows.py` | max diff 3.3·10⁻¹⁶ (`audit_lift_rows.log`) | minutes |
| 2c. Lemma D (numerical check) | `python stage_e_v1/code/check_decomposition_v5.py` | error ≈ 10⁻¹⁵ | seconds |
| 2d. Integer re-verification of 484 + 280 | `python stage_e_v1/code/verify_exact_integer_v3.py` | `rows_violated_exactly: 0`, `all_blocks_positive_definite_exact: true`; compare with `stage_e_v1/logs/verify_exact_integer_v3.json` | ≈ 81 min, one process, ≈ 17 GB RAM (not re-run for this package) |
| 2e. Rational original run | `python stage_e_v1/code/exact_cert.py` | `rows_violated_exactly: 0`; compare with `stage_e_v1/logs/exact_cert_result.json` | ≈ 3.2 h (not re-run for this package) |

Shared inputs of 2d and 2e: `exact_bases2.pkl`, `exact_povm_y_checkpoint.pkl`, `indep_rows.npy`. Verifying these inputs independently is an open item (see `PROOF_OBLIGATIONS.md` A8).

## 3. S₊: numerical reference

```
python stage_e_v1/code/control_differential.py
```
Expected: positive reference relative deficit ≈ 2·10⁻¹² (`stage_e_v1/logs/control_differential.json`). Numerical only.

## 4. O3 (separator certificate)

```
python o3_v2/code/audit_o3_journal_2026-10-31.py
python o3_v2/code/audit_leaves_coverage_2026-10-31.py
```
Expected: `AUDIT_PASS`; coverage consistent (`o3_v2/metrics/o3_summary.json`: `final_gap_trR_minus_20s = 0.030405245308261095`, `final_gap_positive = true`). The full re-run (≈ 6.1 h) exceeds the 4 h budget and is not repeated; the journals `o3_v2/metrics/o3_progress.jsonl` and `o3_failures.jsonl` (empty) are the record.

Tiling check (exact): `code/verify_tiling_exact.py` → `metrics/tiling_exact_check.json` (exact match with the bisection tree, 5 274 284 nodes), as recorded in `STAGE_C_FINAL_PROOF.md` §10.

## 5. Theorem N and the family F_U

```
python checks/fu_normalization_and_Y_2026-10-31.py > checks/fu_normalization_and_Y_2026-10-31.out
```
Expected (from the stored output):
- `sld_equation_max_residual_at_0 ≈ 4·10⁻⁷` (finite-difference limit; the identity L_ss = 0 is exact),
- `FQ0_vs_closed_form_max_abs_diff ≈ 7·10⁻¹²`,
- `two_outcome_sum_N_minus_FQ0_max_abs ≈ 7·10⁻¹²`,
- `random_povm_sum_N_minus_FQ0_relative ≈ 1.6·10⁻¹⁵`,
- `max_rank_real_gram_Qh_A^H_y_over_Y_S_basis = 1`, `generic_y_rank_distribution = {"4": 200}`.

## 6. Toy counterexample (synthetic, not the instance)

```
cd toy_rank_jump
python rank_jump_check.py > rank_jump_check.out
python povm8_jump.py > povm8_jump.out
```
Expected: at s = 0.003, tr F^Q(s) − tr F^Q(0) ≈ 3.998 (analytic 4·tr τ = 4), hᵀF_E(sh)h ≈ 16.40 with the rank jump versus 12.40 without it.

## 7. Proof text

`PROOF_RECONSTRUCTION_THEOREM_N_2026-10-31.md` (steps 1–12, second critical pass). `THEOREM_NATURAL_D2_NOGO_v8.md` (statement and status table). `S_PLUS_CERTIFICATE_FINAL_v2.md` (S₊ chain, inputs, limitations). `ARTICLE_DRAFT_v4_2026-10-31.md` (article). `EVIDENCE_LEDGER_2026-10-31_v5.md` (detailed ledger).

## 8. What a reviewer should not expect

- The `.out` logs were produced on the author's machine and are not bitwise-reproducible across platforms (floating point in the numerical checks).
- The exact integer and rational runs are long; the logs are the record. Re-running them is not required to check the S₊ logic.
- No external review has been performed.
