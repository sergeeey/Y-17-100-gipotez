# Proof obligations and refutation points (H-CAT56-2)

Each row is a step an external reviewer can attack. "Where" points to the file and section. "Refutation" states what would falsify the step. Status values: PROVED (analytic), PROVED-hand (analytic, checked once internally by the same model), VERIFIED-EXACT, VERIFIED-INTERVAL, VERIFIED-NUMERIC (not a proof), CONDITIONAL, FALSIFIED, UNKNOWN.

## A. Positive part (S₊)

| ID | Obligation | Where | Status | Refutation point |
|---|---|---|---|---|
| A1 | Regularity: Tr(ρ₀E_j) = ω_j |Q^{1/2}x_j|² > 0 for every outcome | `S_PLUS_CERTIFICATE_FINAL_v2.md` §1; `THEOREM_S_PLUS_EXISTENCE_v6.md` | PROVED | x_j = 0 for some j |
| A2 | YPZJ thm:reg applies to these outcomes: saturation ⇔ A_aᴴy = ξ_a x, ξ real | `THEOREM_S_PLUS_EXISTENCE_v6.md` §2; YPZJ 1806.07337 (LaTeX text read) | PROVED (given the cited theorem) | a regular outcome that does not satisfy the stated condition in the cited text |
| A3 | Completeness ΣE = I ⇔ A·M = b (484 real coordinates of Herm(22)) | `THEOREM_S_PLUS_EXISTENCE_v6.md` lemma 3 | PROVED | a coordinate of Herm(22) not covered |
| A4 | Lemma D: M_j = ω Σ ĉĉᵀ with ĉ_N = 1 for every positive definite block | v6 lemma D; `check_decomposition_v5.py` (err ~10⁻¹⁵) | PROVED | a positive definite M with last coordinate ≠ 0 that cannot be so decomposed |
| A5 | 484 identities A·M* = b hold exactly over ℚ | `stage_e_v1/logs/exact_cert_result.json` (rows_violated 0), SHA 53a1f6d7… | VERIFIED-EXACT | a nonzero residual in the exact log |
| A6 | 484 identities hold exactly over ℤ, A rebuilt independently from the lift definition | `stage_e_v1/logs/verify_exact_integer_v3.json` (rows_violated_exactly 0), SHA f255dec4… | VERIFIED-EXACT | a nonzero integer residual |
| A7 | 280 blocks positive definite (ℚ: LDLᵀ; ℤ: Sylvester minors) | the two logs above | VERIFIED-EXACT | a non-positive minor |
| A8 | Shared inputs: bases `exact_bases2.pkl` (SHA fbca57fa…), checkpoint y (SHA 1d6cdf94…), rows `indep_rows.npy` (SHA 0b0f3a4f…) | `S_PLUS_CERTIFICATE_FINAL_v2.md` §4 | **CONDITIONAL** (not regenerated) | an error in the bases or in y that the two exact runs would not detect; **this is the main open point of A** |
| A9 | Float reference: relative deficit 2.4·10⁻¹² at θ = 0 | `stage_e_v1/logs/control_differential.json` | VERIFIED-NUMERIC | not a proof |

## B. Negative part (S₋), matrix and trace, F_U

| ID | Obligation | Where | Status | Refutation point |
|---|---|---|---|---|
| B1 | N normalisation: Σ_k N_E,k = F^Q for a complete POVM, N_E,ab = Re tr(E L_a ρ L_b) | `review_package/…` §1; `checks/fu_normalization_and_Y_2026-10-31.py` (part1) | PROVED; VERIFIED-NUMERIC (7·10⁻¹² on F_U) | a POVM with ΣN_k ≠ F^Q beyond rounding |
| B2 | Lemma 1/2: N_k ⪰ F_k for p_k > 0; N_k ⪰ 0 for p_k = 0 (F_k := 0) | `PROOF_RECONSTRUCTION_THEOREM_N_2026-10-31.md` (second pass, item 2) | PROVED | an outcome with p_k = 0 and N_k not PSD (none expected: N_k is a Gram matrix) |
| B3 | Riesz projector: N_v(θ) ⪰ Gram(P(θ)w_a(θ)); f_θ ≥ f₀ − ω(|θ|), ω → 0 | `PROOF_RECONSTRUCTION…` steps 2–5 | PROVED-hand (needs continuity of ∂ρ at 0) | a rank-changing family where the spectral gap closes; a θ-sequence with f_θ < f₀ − ω(|θ|) |
| B4 | Łojasiewicz on f₀ over the sphere (semialgebraic since N_v(0) is quadratic with real constant coefficients); exponent θ₀ ≤ 1 | PROOF_RECONSTRUCTION step 6; BCR §2.6 (section level) | PROVED-hand; citation at section level | a non-semialgebraic f₀ (excluded by construction) |
| B5 | Zero set of f₀ = ℂ² × 𝒴 (needs (∂ρ₀)_ss = 0; automatic for F_U) | PROOF_RECONSTRUCTION step 7 | PROVED-hand | a nonzero supp×supp block in the F_U derivative (excluded by the closed form) |
| B6 | 𝒴 = ∪_x Y_S(x) exactly (real-line structure preserved by Q^{1/2}) | PROOF_RECONSTRUCTION step 7; `checks/…out` part2 (120 vectors rank 1; 200 random y rank 4) | PROVED-hand + VERIFIED-NUMERIC (forward inclusion) | a y with rank_ℝ ≤ 1 not of the form Y_S(x); the converse is analytic |
| B7 | Lemma 6 constant 22C₁C₀ (Hölder over ≤ 22 eigen-terms and over k) | PROOF_RECONSTRUCTION step 8 | PROVED-hand | an exponent or count error (≤ 22 eigenvectors per outcome) |
| B8 | Separator (certified for the Hermitian part H = (R+Rᴴ)/2, since the stored R is Hermitian only to 5.2·10⁻¹⁷; independent audit 2026-11-01: CONDITIONAL on D1, D3, D4, see `../O3_V3_INDEPENDENT_AUDIT.md`): sup_{𝒴¹} Re(yᴴRy) ≤ s_float for all leaves, with s_float = fl(0.9·tr R/20) and tr H − 20 s_float = 0.0304 (recomputed exactly; s_float = fl(fl(0.9·tr H)/20) with tr H = Σ Re(R₀)_ii, see ERRATA E1–E2). Strict v3 re-certification 2026-10-31: all 7 912 chunks, 3 955 841 per-leaf records, arb-only decisions; closes v2 conditions C-O3-1 (per-leaf slack) and C-O3-2 (float selections). Still open: C-O3-3 (driver does not enforce external hashes), C-O3-4 (stale text in STAGE_C l.73) | `o3_v3/metrics/audit_run{A,B,C,D}.json` (all COMPLETE_STRICT); `o3_v3/metrics/run_manifest_run*.json`; `o3_v2/metrics/o3_summary.json` (history); `STAGE_C_FINAL_PROOF.md` §6–8 | VERIFIED-INTERVAL (arb, 192 bits; strict v3, internal only) | a leaf with B_up ≥ s_target (none in the journal); a missed cell (coverage check) |
| B9 | O3 coverage: all x ∈ S³ (Bloch parametrisation, phase reduction) covered by 3 955 841 leaves in 7 912 chunks | `STAGE_C_FINAL_PROOF.md` §4 P4, §8, §10 O2 (exact tiling) | VERIFIED-EXACT (tiling); PROVED-hand (principle) | a gap in the tree bisection |
| B10 | Rounding: arb enclosures; float cell edges converted exactly; margin 10⁻¹² in du; λ_K from upper bound | `o3_v2/code/interval_cells_v2.py` (lines 116–124, 138, 228–243) | VERIFIED-INTERVAL (the margin is an extra safety, not a directed-rounding proof) | a cell where du is underestimated by more than 10⁻¹² (arb enclosure would show it) |
| B11 | Theorem N (uniform trace bound), F_U, D1 at each θ, all finite POVMs, all unit h, |s| ≤ s₁ | PROOF_RECONSTRUCTION step 8 | PROVED-hand | a finite POVM with tr(F^Q − F_E) < c at some |s| ≤ s₁ |
| B12 | Uniformity: constants independent of POVM and h | steps 8; sums Σ tr E = 22, Σ tr(R̂E) = tr H, Σ tr(P_yE) = 20 | PROVED-hand | a constant that depends on the POVM |
| B13 | Borel transition: F^C_M(θ) = sup_P F_P = I_int for θ-independent μ = tr M | `THEOREM_NATURAL_D2_NOGO_v8.md` proposition 7 | PROVED-hand | a Borel M for which the partition sup is not I_int (approximation lemma) |
| B14 | Borel trace bound: tr F^C_M(θ) ≤ tr F^Q(θ) − c | corollary of B11 on finite partitions | PROVED-hand | a partition whose POVM is not complete |
| B15 | D2 trace bound: tr F_E(θ) ≤ tr F^Q(θ) − c at every |θ| ≤ s₁, hence (i) the D2 limit along each fixed ray has trace ≤ tr F^Q(0) − c; (ii) limsup along any curve θ(t) → 0 has the same bound. Existence of the D2 limit along arbitrary curves is **not** claimed (false: direction-dependent null-outcome limits) | pointwise bound + continuity of tr F^Q at 0 (constant rank 2) | PROVED-hand | a finite POVM with tr F_E(θ) > tr F^Q(θ) − c at some |θ| ≤ s₁ |
| B16 | Matrix D2 limit ≠ F^Q(0) | consequence of B15 | PROVED-hand | a POVM whose matrix limit equals F^Q(0) but whose trace is smaller than tr F^Q(0) − c (impossible if B15 holds) |

## C. Scope and negative results (must be stated in the paper)

| ID | Statement | Status | Note |
|---|---|---|---|
| C1 | Theorem N for general C¹ families | CONDITIONAL on separator R with γ > 0 | not a consequence of C0–C3 alone |
| C2 | Continuity of ∂ρ at 0 is needed for the general uniform statement | FALSIFIED as a necessary condition for the full class: without it Theorem N fails (counterexample); minimality not established | `THEOREM_NATURAL_D2_NOGO_v8.md` §0 |
| C3 | Limit form N₁ (tr F^C(sh) → ≤ tr F^Q(0) − c) for families with rank jumps | FALSIFIED | `toy_rank_jump/rank_jump_check.out` (trFQ(s) → 65.51 vs 61.51); analytic limit 4 tr τ |
| C4 | Directional quadratic form hᵀF_E(sh)h saturable for F_U and for the explicit POVM {I₂⊕0, 0⊕e_ke_kᴴ} | PROVED-hand (F_U) | the matrix F_E is not saturated (trace) |
| C5 | Stage C theorem C (matrix, D1 in the point θ = 0, reduction via Theorem A) | CONDITIONAL (O1, O4) | Theorem N does not depend on Theorem A |

## D. Points most likely to be wrong (ask the reviewer to attack these first)

1. **B3 + B6 together:** the Riesz bound and the identification of the zero set. If the separator is applied to a set larger than 𝒴 (e.g. a different real-line condition), Lemma 5 fails.
2. **B8 + B9:** whether the O3 coverage is over exactly the directions x that enter 𝒴, including phase and the pole x₀ = 0 (P2 in `STAGE_C_FINAL_PROOF.md` §4).
3. **A8:** the shared inputs of the S₊ runs. Two exact runs agree on A, but not independently on bases and y.
4. **D1 vs D2 in the literature (question for the specialist):** whether D1 is the intended convention. Our S₋ trace statement holds for both at the level of trace for finite POVMs of F_U.
5. **Borel D2 (B13–B15):** the order of limits. The bound is proved at each fixed θ with ≤ s₁ before any limit is taken.
