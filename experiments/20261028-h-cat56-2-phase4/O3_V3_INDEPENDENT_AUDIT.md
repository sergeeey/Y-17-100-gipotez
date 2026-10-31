# O3 v3 independent audit (2026-11-01)

**Scope.** Mathematics and implementation of the interval certificate for the separator of S₋ = {4,…,15} (`o3_v3/`): the cell bound `cell_bound`, the arb decision logic, `phi_rows`, the threshold s*, coverage of the 3 955 841 leaves, and integrity against the SHA-256 manifests.

**Independence, stated precisely.** Two independent checks were made:
1. A **cross-model read-only audit** by Codex CLI (`codex-cli 0.153.4`, `-s read-only`), given primary files only and no earlier verdicts. Prompt: `review_package/codex_logs/o3v3_codex_prompt_2026-11-01.txt`; full log: `review_package/codex_logs/o3v3_codex_audit_2026-11-01.txt` (SHA-256 83e6d616…). **This is not external scientific review.** The packet excluded `review_package/`, `O3_AUDIT_RECORD.md`, the ledgers, and `audit_run*.json`.
2. **My own numerical tests**, which do not use the certificate: a dense grid over the Bloch sphere and a cell-level validity test on the 1 000 tightest certified cells. Scripts and outputs are in `o3_v3/audit_tests/`.

Neither check is a proof. The certificate's correctness for all 3 955 841 cells rests on the audited lemma and on the arb implementation.

## 1. Verdicts by estimate

| # | Estimate | Codex | My check | Final | Evidence |
|---|---|---|---|---|---|
| 1 | Lemma behind `cell_bound`: displacement du, decomposition y = Py + (I−P)y, bounds κ, ρ, mz, division by 1−δ, sign of λ_K | PASS (a)–(g) | Re-derived du (path argument: φ-leg at θ_c, then θ-leg; length hθ/2 + sin(θ_c/2)·hφ) — valid | **PASS** | `interval_cells_v3.py:147–256`; Codex §1 |
| 2 | Real form: y^†Ry = [r;s]^T [[A,−B],[B,A]] [r;s] | CONDITIONAL (stored R not exactly Hermitian) | Random-y check: max error 1.8·10⁻¹⁵ for the Hermitian part | **PASS for H = (R+R^†)/2; wording CONDITIONAL** (see D1) | `interval_cells_v3.py:82–107`; `dense_sup_grid.py` |
| 3 | `phi_rows` encodes A_a^†y ∈ ℝx; real-linearity in (Re x₀, Im x₀, Re x₁, Im x₁) | PASS | Confirmed by hand: g₁ = x₀a₁ − x₁a₀ and g₃ = x̄·a encode λ real; kernel vectors satisfy A_a^†y = λx to 3.6·10⁻¹⁴ | **PASS** | `s8_admissible_span.py:46–58`; `dense_sup_grid.py` (kernel check) |
| 4 | Arb soundness: every decision is an arb comparison; no float on a bound path | PASS | Confirmed: float conversions occur only at seed vectors (eigh, SVD) and reporting; bounds use arb `·.upper()`, `arb_max`/`arb_min` | **PASS** | `interval_cells_v3.py:64–71, 130–136, 163–165` |
| 5 | Threshold s* = fl(0.9·tr R/20) and γ = tr R − 20 s* ≥ 0.0304 | PASS, with note | γ = 0.030405…, s* = 0.01368236038871751 (`0x1.c057f53368882p-7`). Exact rational 9/10 with one rounding gives the adjacent float 0.013682360388717509 | **PASS** as sequential binary64 evaluation; definition must state it (D4) | `interval_cells_v3.py:56–59, 110–112` |
| 6 | Coverage: 7 912 chunks, 3 955 841 leaves, tiling of [0,π]×[0,2π) | PASS (sampled and full count) | Journal: 7 912 unique chunks, 3 955 841 records, 0 failures | **PASS** (count and journal); exact tiling proof not re-done | `o3v3_progress.jsonl`; Codex §6 |
| 7 | Integrity: code and inputs match manifests; record SHA-256 matches journal | CONDITIONAL (manifests cover runs C, D only in its packet) | Manifests runs A–D **all** carry identical SHA-256 for `interval_cells_v3.py`, `o3_run_v3.py`, `leaves.npy`, `R_input.npz`; all record files match the journal (Codex streaming check: 7 912 files, 0 bad hashes, 0 bad leaf positions, 0 non-ok lines) | **PASS** (D2 resolved by runs A and B manifests) | `o3_v3/metrics/run_manifest_run{A,B,C,D}.json`; Codex §7 |
| 8 | Counterexample search | PASS (no violating cell or x found) | Dense grid: sup over x ≈ 0.00212 (31×61), far below s*; cell test on 1 000 tightest cells, 5×5 and 9×9 samples: 0 violations, worst ratio sup/B_up = 0.159 | **PASS** (sampled only) | `grid_small.json`; `cell_validity_top1000_n{5,9}.json` |
| 9 | Full recomputation of all 3 955 841 cells | not done (Codex residual risk) | not done | **not verified** | — |

**Overall O3 v3 verdict: CONDITIONAL.** The mathematics and the arb implementation pass. The conditions are textual and provenance items (D1, D3, D4) and one unperformed check (row 9). None of them is a numerical failure.

## 2. Defects and conditions

**D1 — stored R is not exactly Hermitian** (Codex, `[VERIFIED]`). `max |R − R^†| = 5.2·10⁻¹⁷`. The certificate uses H = (R+R^†)/2, which is correct. The separator statement must therefore use `Re(y^†Ry) = y^†Hy` (identical for every R) or name H, not `y^†Ry` for the stored matrix. **Condition for PASS:** correct the statement in `REVIEW_BRIEF.md`, `PROOF_OBLIGATIONS.md` B8 and `STAGE_C_FINAL_PROOF.md`.

**D2 — provenance of chunks 0…3420** (Codex, `[VERIFIED]` in its packet). Codex was given only runs C and D manifests. Runs A and B manifests exist and carry the same SHA-256 for code and inputs (checked by me, see table row 7). **Resolved.**

**D3 — STAGE_C_FINAL_PROOF.md line 73** (Codex, `[CODE]`). It asserts bitwise Hermiticity of the float symmetrisation, contradicting its own line 103 and the data. This is C-O3-4, still open. **Condition for PASS:** correct the line.

**D4 — threshold definition** (Codex, nuance). s* is the sequential binary64 value of `0.9*trR/20` as the code evaluates it. An exact-rational one-rounding definition differs by one ulp (≈1.8·10⁻¹⁸). The certificate proves the bound for the stored value, so this changes nothing, but every document must define s* as that value. **Condition for PASS:** state the definition in the brief and the ledger.

**Still open, from earlier work:** C-O3-3 (the driver records expected input hashes but does not enforce them). Codex did not raise it again; it stays open.

## 3. Counterexample attempts

- Dense grid over the sphere (31×61 points): sup ≈ 0.00212. A finer grid (361×721) was not run in this pass.
- Cell test on the 1 000 tightest certified cells (784 of them have th_lo > 3.0, i.e. near the pole θ ≈ π; the rest are elsewhere): sampled supremum never exceeds B_up. Worst ratio 0.159 (row 616). 5×5 and 9×9 samples gave identical worst cases, which suggests the supremum is attained at a cell corner. That is an inference, not checked.
- Codex found no counterexample to any lemma inequality on the sampled cells.

**Limits of my own tests (from a read-only logic review of the four scripts, 2026-11-01; no logic errors found, P2 items only):**
- The cell test is weak: the worst sampled sup (0.00218) is far below B_up (≈ 0.01368), so it can only reveal a bound that is wrong by more than about 6×. It has no positive control (a deliberately shrunk B_up that it would flag).
- `dense_sup_grid.py` reports `min_sigma_36_over_grid` but does not assert rank 36. The reviewer checked σ₃₆ ≥ 0.0104 over 9 000 cell-sample points, so the last four right singular vectors are the full kernel there; the assertion is not in the script.
- `check_D1_D4.py` prints values and has no assertions. Its sequential threshold s* is the larger of the two candidates (…882 against …881), which is the non-conservative direction; it is immaterial because the minimum slack is 8.4·10⁻⁹.

**Interpretation.** The certified bounds are valid on every sample but loose by a factor of about 6 or more (sampled sup ≈ 0.002 against B_up ≈ 0.0137). The separator holds with a large margin in fact, and the certificate's tightness is a property of its estimates, not of the separator.

## 4. What this audit does not establish

- Full independent recomputation of all 3 955 841 cells. Only the closest leaf and samples were recomputed.
- Correctness of python-flint / Arb beyond its documented interval semantics.
- Any external review. Codex is a cross-model read-only audit and is reported as such.

## 5. Next steps (not started)

1. Edit the separator statement to name H or Re(y^†Ry) (D1).
2. Correct STAGE_C line 73 (D3, C-O3-4).
3. Add the definition of s* (D4) to the brief and ledger.
4. Keep C-O3-3 open or add driver-side hash enforcement (a code change; not started).
5. Optional: finer dense grid and a full recomputation, only if a concrete defect is found.
