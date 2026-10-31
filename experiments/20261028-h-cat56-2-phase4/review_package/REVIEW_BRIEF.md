# Review brief: saturability of the SLD quantum Cramér–Rao bound for one fixed rank-2 model in C²² (H-CAT56-2)

**Status.** Internal research draft, prepared for an external specialist. **No external review has been performed.** All proofs and audits were carried out by the same model family that wrote the texts, in isolated contexts. These are internal verifications, not independent review. Nothing has been sent to anyone.

**Scope of this brief.** One fixed model, one fixed instance, one fixed family. Claims are stated only for that setting. No general theorem is claimed.

---

## 1. Model and conventions

- Hilbert space ℂ² ⊕ ℂ²⁰. State at the reference point ρ₀ = Q ⊕ 0, Q = diag(1/3, 2/3). Rank 2.
- Sixteen instance blocks A_a = −2i·B_a, B_a ∈ ℤ[i]^{20×2} (instance file `instance_d22_r2_s16.jsonl`, seed 701082). Indices are 0-based: a ∈ {0,…,15}.
- Subsets S₊ = {0,…,11} and S₋ = {4,…,15}. Each is a 12-parameter subfamily. **The other four generators are known and fixed**: they are set to zero in the family below. This is not a nuisance-parameter problem (see §6).
- Family used in proofs (exponential, "F_U"): ρ_θ = U_θ ρ₀ U_θᴴ, U_θ = exp(Σ_{a∈S} θ_a X_a), X_a = [[0, −G_aᴴ],[G_a, 0]], G_a = A_a/2. Convention C2 (accepted by the project owner, not derived): the SLD at θ = 0 is L_a = [[0, A_aᴴ],[A_a, 0]]. It satisfies ∂_aρ = (ρL_a + L_aρ)/2 exactly at θ = 0, since ∂_aρ(0) = ½[[0, QA_aᴴ],[A_aQ, 0]] and the supp×supp block of L_a(0) vanishes.
- **QFIM:** F^Q_ab(θ) = Re tr(ρ_θ L_a L_b). At θ = 0, F^Q_ab(0) = Re tr(Q A_aᴴ A_b) (verified to 7·10⁻¹², `checks/…out`).
- **Classical Fisher information (D1, at each point θ):** for a POVM {E_k}, p_k(θ) = tr(ρ_θ E_k), F_E(θ) = Σ_{k: p_k(θ)>0} ∇p_k ∇p_kᵀ / p_k. Outcomes with p_k(θ) = 0 contribute 0.
- **Borel CFIM:** for a Borel POVM M, F^C_M(θ) is the Löwner limit of the net of finite-partition CFIMs. Its trace is sup over finite partitions of tr F_P(θ).
- **D2 (directional limit):** for a finite POVM and a curve θ(t) → 0, the limit of the outcome-wise terms. For F_U with finite POVMs the sum of limits equals the limit of sums, so the D2 trace is lim tr F_E(θ(t)).
- **Directional quadratic form:** hᵀF_E(th)h (or its Hellinger-type limit). This is a different object from the matrix CFIM. It is saturable (§4).

## 2. Positive result (S₊)

**Theorem S₊.** There is a finite POVM with 1764 rank-one regular outcomes E_j = ω_j u_j u_jᴴ, u_j = (x_j; Σ_a ĉ_a B_{j,a}), supported on 280 directions x_j ∈ ℂ² (182 directions with N_j = 7 and 98 with N_j = 5, Σ N_j = 1764), such that ΣE = I₂₂ and the 12×12 classical information at θ = 0 equals the QFIM F^Q_{S₊}(0). All outcomes are regular: Tr(ρ₀E_j) > 0 because x_j ≠ 0.

**Chain.**
1. YPZJ (arXiv:1806.07337, thm:reg) for regular outcomes: saturation ⇔ A_aᴴy = ξ_a x with real ξ_a, for a suitable choice of kernel basis. This is applied with the Stage-E kernels Y_{S₊}(x_j).
2. Lemma 3: the 484 real coordinates of Herm(22) and the completeness condition ΣE = I ⇔ A·M = b.
3. Lemma D: each positive definite block M_j = ω Σ ĉĉᵀ with last coordinate 1 (Cholesky + Householder).
4. Exact moments M_j* with A·M* = b (484 identities) and M_j* ≻ 0 (280 blocks).

**Status.** Logic: PROVED (internal). Exact identities and positivity: VERIFIED-EXACT in two independent arithmetics (ℚ and ℤ), on shared inputs (§5). **CONDITIONAL** on the shared inputs: bases `exact_bases2.pkl`, checkpoint y, and row list `indep_rows.npy` were not regenerated independently.

## 3. Positive numerical reference

At θ = 0, the POVM of §2 (float version) gives relative deficit 2.4·10⁻¹² (`stage_e_v1/logs/control_differential.json`). This is a numerical reference, not a proof.

## 4. Negative result (S₋): what is proved and what is not

**Theorem S₋ (matrix and trace, uniform).** For the family F_U and S₋ = {4,…,15}, there are c > 0 and s₁ > 0 such that for every finite complete POVM, every Borel POVM M, every unit h and every |s| ≤ s₁:

  tr(F^Q(sh) − F_E(sh)) ≥ c   (finite POVMs, D1 at sh), and
  tr F^C_M(sh) ≤ tr F^Q(sh) − c   (Borel POVMs).

Consequences:
- No finite or Borel POVM satisfies F_E(θ) = F^Q(θ) (matrix saturation) at any |θ| ≤ s₁, including θ = 0 under D1.
- For a finite POVM and each fixed direction h, the D2 limit along the ray θ = th exists, and its trace is ≤ tr F^Q(0) − c. For an arbitrary curve θ(t) → 0 only limsup tr F_E(θ(t)) ≤ tr F^Q(0) − c is claimed: outcome-wise null limits depend on the direction, so the D2 limit need not exist along general curves. The matrix D2 limit along a ray cannot equal F^Q(0), because the traces differ.

**Constants.** c = (γ/(2C₂))^{1/θ₀}, C₂ = 22C₁C₀, C₁ = 4‖R‖ + 2|s*|. γ = tr H − 20 s* with H = (R₀+R₀ᴴ)/2 (exact in arb), t := Σ Re(R₀)_ii = tr H, and s* := fl(fl(0.9·t)/20) = 0x1.c057f53368882p−7 = 0.01368236038871751 (see `../ERRATA_STAGE_C_FINAL_PROOF.md` E1–E3) (binary64, the value the certificate actually checks; the exact real 0.9·tr R/20 differs from it by 1.8·10⁻¹⁸, which is irrelevant once s* is defined as s_float); O3 gives γ ≥ 0.0304 (interval-verified; strict v3 re-certification over all 7 912 chunks, `O3_AUDIT_RECORD.md` §9; conditions C-O3-3 and C-O3-4 remain open). C₀, θ₀ come from the Łojasiewicz inequality for f₀ and are **not explicit**. s₁ is **not explicit**: it must satisfy ω(s₁)^{θ₀} ≤ γ/(2C₂), where ω is the Riesz-projector modulus (not the modulus of the full N_v, which is false under rank jumps). For F_U with ω(r) ≤ L·r one may take s₁ = min(t₀, (γ/(2C₂L^{θ₀}))^{1/θ₀}); the earlier formula without L was wrong (found by audit).

**Where the proof lives.**
- Riesz projector bound f_θ ≥ f₀ − ω(|θ|), with ω → 0 under continuity of ∂ρ at 0 (analytic; PROOF_RECONSTRUCTION §2–5).
- Lemma 2: N_E ⪰ F_E for each outcome, with N_E = Re tr(E L_a ρ L_b) and Σ_k N_k = F^Q. For p_k = 0 one has N_k ⪰ 0 but N_k ≠ 0 in general; F_k := 0 there (checked numerically, §7).
- Łojasiewicz on f₀ = λ₂(N_v(0)) over the sphere; zero set ℂ² × 𝒴.
- Separation: y^H(R − s*)y ≤ C₁ dist(y, 𝒴), with 𝒴 = ∪_x Y_{S₋}(x). The equality 𝒴 = ∪_x Y_{S₋}(x) is exact (§7). The separator certified by O3 is the Hermitian part H = (R + Rᴴ)/2 of the stored matrix (the stored R is Hermitian to 5.2·10⁻¹⁷; Re(yᴴRy) = yᵀHy exactly), with sup_{𝒴¹} Re(yᴴRy) ≤ s_target (Codex audit 2026-11-01, defect D1: state the separator via H, not yᴴRy for the stored R).
- Lemma 6: γ ≤ 22C₁C₀[(tr Δ)^{θ₀} + ω^{θ₀}] by subadditivity and Hölder, giving the bound.

**Status.** Theorem S₋ for F_U: PROVED-hand (internal, single model family) with the separator from O3 (VERIFIED-INTERVAL: strict v3 re-certification on all 7 912 chunks, internal only, independently audited 2026-11-01 by Codex (cross-model, read-only, not external review): CONDITIONAL on textual fixes D1, D3, D4 — see `../O3_V3_INDEPENDENT_AUDIT.md`). The Borel transition is PROVED-hand (Proposition 7). The D2 trace limit is PROVED-hand.

**Not claimed.**
- The general C¹-family extension is **CONDITIONAL** on an existing separator R with γ > 0. Without the separator the statement is not proved.
- The limit form of the trace bound along rays for families with rank jumps is **FALSIFIED** (toy counterexample, §4 of the proof file): tr F^Q is discontinuous at 0 when the rank jumps, and the analytic limit is tr F^Q(0) + 4 tr τ.
- Without the continuity of ∂ρ at 0, the general uniform statement is false (explicit counterexample), but minimality of this condition is not established.

## 5. Shared inputs and provenance

- Direction and basis construction: `build_exact_dirs.py`, `exact_kernel.py`, `exact_bases.py`, `transform_bases.py`, from `s14_povm_prefix12.npz` (SHA 8ab6f458…) and the instance (SHA 05289920…).
- Shared by both exact runs (`exact_cert.py` in ℚ; `verify_exact_integer_v3.py` in ℤ): bases `exact_bases2.pkl` (SHA fbca57fa…), checkpoint y `exact_povm_y_checkpoint.pkl` (SHA 1d6cdf94…), row list `indep_rows.npy` (SHA 0b0f3a4f…). **These are not regenerated independently.**
- Independent between the two runs: the construction of A (in the integer run A is rebuilt from the lift definition), the arithmetic, and the verification code.
- O3: input matrix R is from float column generation (`../20261027-h-cat56-2-discovery/metrics/s14_R_4-5-6-7-8-9-10-11-12-13-14-15_nx250.npz`, listed in `SHA256SUMS.txt`); the certificate applies to the recorded exact binary matrix. A reviewer needs this input file together with the primary certificate `o3_v3/code/interval_cells_v3.py`, its driver `o3_v3/code/o3_run_v3.py`, and the journal `o3_v3/metrics/o3v3_progress.jsonl` to check the separator (the v2 code `o3_v2/code/interval_cells_v2.py` is kept as history); the reviewed text alone does not contain R or the cell list. Its origin does not matter for the criterion (STAGE_C §7). Enclosures are arb, 192 bits; float cell bounds are converted exactly; the code adds a margin of 10⁻¹² to the radius of each cell and uses upper bounds (`o3_v2/code/interval_cells_v2.py` lines 138, 200–243). The journal audit passes (`o3_v2/metrics/o3_journal_audit_2026-10-31.json`). A full re-run took ≈6.1 h, above the 4 h budget, and is not repeated here.

## 6. Relation to Nurdin's work and to nuisance-parameter estimation

- Nurdin (arXiv:2402.11567 v5) gives a composite-matrix criterion for single-copy saturability, with Condition 2 corrected in a Corrigendum; the published correction is in IEEE Control Systems Letters, doi 10.1109/lcsys.2024.3451468. **We have not read the published correction.** Our statements use the arXiv v5 text only.
- In our instance, the composite criterion is applied to 16 generators: the span of traceless Hermitian 20×20 matrices has real dimension 399, and the criterion yields no kernel POVM for the full set (PROVED-hand, Proposition 5). For S₋ there are 4·C(12,2) = 264 generators, fewer than 399; **the criterion does not apply to S₋.** This is a statement about the criterion, not about saturation.
- In nuisance-parameter estimation the bound for a subset is the Schur complement of the full QFIM, and the classical information is for the subset with the others unknown. Our setting differs: the other generators are known and fixed at zero, so the relevant matrix is the 12×12 block of the 16×16 QFIM at the fixed point.
- The professor's matrices of size 20×3 are not the same as our 20×2 blocks. The mapping between the two parametrisations is **UNKNOWN** to us until the professor's construction is specified.

## 7. New, and not new

- **Known (cited, not claimed):** YPZJ thm:reg for regular outcomes; Nurdin composite criterion; the single-copy saturability literature (2602.12097 hierarchy, 2601.21801 geometric criterion) read by abstract or search excerpt only.
- **New for this instance (internal, not literature-checked):** S₊ existence with 1764 regular outcomes on 280 directions; S₋ trace-level non-saturation with uniform constants for finite and Borel POVMs for F_U; D2-trace limit bound; the separation between matrix non-saturation and quadratic-form saturation along a single direction (Proposition 6). **Priority is not claimed.** A complete literature search has not been carried out.

## 8. Three questions for an external specialist

1. **Convention.** Is the zero-probability convention D1 (outcomes with p_k = 0 excluded at each point) the convention used in the single-copy saturability literature, or is the D2 directional limit of YPZJ thm:null the intended one? Our trace bound holds under both for finite POVMs of the family F_U, but matrix equalities at the reference point depend on the convention.
2. **Parametrisation.** Are our SLD and QFIM conventions (C2 for A_a = −2iB_a; F^Q = Re tr(ρLL)) equivalent to the parametrisation in the professor's construction, in particular for the 20×3 matrices?
3. **Applicability of the composite criterion.** Does the composite criterion (in the published correction) say anything about POVMs that are not separated? Our trace bound quantifies over all finite and Borel POVMs, and we want to know whether any published condition on separated POVMs would change the S₋ conclusion.

---

*Companion files: PROOF_OBLIGATIONS.md (obligations and refutation points), REPRODUCE.md (verification commands and expected output), EVIDENCE_LEDGER.md (statuses), SHA256SUMS.txt (integrity), DRAFT_TO_NURDIN.md (unsent draft).*
