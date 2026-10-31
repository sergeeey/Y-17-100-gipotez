# C_NOTES — stage C working notes: reformulation of the S− obstruction (phase 4)

Status: working notes, not a final claim. Markers: `[PROVED]` author's argument (audit pending, stage E); `[VERIFIED-float]` numerics; `[UNKNOWN]` open.

## 1. Reformulation (Lemma R) `[PROVED]`

Notation: B_S = [A_i]_{i∈S} ∈ C^{20×2|S|}; M_S = B_S†B_S ∈ Herm(2|S|), blocks (M_S)_{ik} = A_i†A_k ∈ Herm(2) (Hermitian because of PCC, hence symmetric in (i,k)). Cone_sep := cone{ λλᵀ ⊗ xx† : λ ∈ R^{|S|}, x ∈ C² }.

**Lemma R.** Assume rank B_S = 20. Then I₂₀ ∈ cone{yy† : y ∈ 𝒴_S} ⇔ M_S ∈ Cone_sep.
Proof. (⇒) Let I₂₀ = Σ_j c_j y_jy_j†, y_j ∈ 𝒴_S, c_j > 0. A nonzero y ∈ 𝒴_S has B†y = λ⊗x with λ ∈ R^{|S|} (A_i†y = λ_i x); y pure would give B†y = 0, impossible for y ≠ 0 since B† is injective. Then M = B†I₂₀B = Σ c_j (λ_j⊗x_j)(λ_j⊗x_j)† = Σ c_j λ_jλ_jᵀ ⊗ x_jx_j†.
(⇐) Let M = Σ q_jq_j†, q_j = λ_j⊗x_j. Ran q_j ⊂ Ran M = Ran B†, so q_j = B†y_j for a unique y_j, and y_j ∈ 𝒴_S by construction. Then B†(Σ y_jy_j† − I)B = M − M = 0; B surjective gives Σ y_jy_j† = I₂₀. ∎
Consequence: the obstruction question is a separability-type question for a **fixed integer matrix** M_S (entries of A_i are Gaussian integers times −2i). No SVD, no kernel parametrisation, no condition number 10⁴.

## 2. The PPT test carries no information here `[PROVED]` + `[VERIFIED-float]`

Cone_sep ⊂ {M ⪰ 0, M^{T₂} ⪰ 0} (T₂ = transpose on the C² factor). For every PCC model the blocks G_ik are Hermitian, so G_ikᵀ = conj(G_ik) and M^{T₂} = conj(M), which has the same spectrum as M. Hence PPT is automatic for every subset (floats: min eig M = min eig M^{T₂} to 4 digits for all prefixes, S+, S−, all 16; `code/c1_ppt_probe.py`). The obstruction is therefore genuinely beyond PPT-type relaxations (as expected: PCC is exactly the structure that makes the first-level condition vacuous).

## 3. Dual certificate in (λ, ξ) variables

Write x = (ξ₀+iξ₁, ξ₂+iξ₃). Variety V = {(λ, ξ) : λ⊗x ∈ Ran B†} is cut out by 2(2|S|−20) real bilinear equations ℓ_r(λ, ξ) = 0 (8 for |S| = 12). For a symmetric family of Hermitian blocks W_ik put f_W(λ, ξ) = Σ_{ik} λ_iλ_k x†W_ik x and ⟨W, M⟩ = Σ_{ik} tr(W_ik G_ik).
**Dual lemma** `[PROVED]`: if f_W ≥ 0 on V and ⟨W, M_S⟩ < 0 then M_S ∉ Cone_sep, hence (Lemma R) S is not saturable.
Positivity on V is certified by an identity
   |λ|^{2a}|ξ|^{2b} f_W + Σ_r ℓ_r h_r = mᵀ G m,  G ⪰ 0, m = (λ-monomials of degree 1+a) ⊗ (ξ-monomials of degree 1+b),
with polynomial multipliers h_r. This is a sum-of-squares (SOS) identity: exact rational data can be verified by exact linear algebra.

## 4. Levels tried (code/c2_sos_dual.py; maximise τ with G ⪰ τI, ⟨W,M⟩/tr M = −1, τ ≤ 1)

| level (a, b) | set | status | best τ | seconds |
|---|---|---|---|---|
| (0, 1) | S− | optimal | −1.43 (no certificate) | 446 |
| (0, 1) | S+ | optimal | −1.47 (no certificate; correct, S+ is saturable) | 66 |
| (0, 0) | both | not run; the primal point M itself is feasible for the moment relaxation (PSD, satisfies the range constraints), so no dual certificate exists | — | — |
First run of the script produced `unbounded` for both sets: the pairing for off-diagonal blocks carried an extra factor 2 not present in f_W. Fixed before the table above; the bad run is not used.
| (0, 2) | S− | optimal | −2.38 (no certificate; 5854 s, Gram 240, 6552 monomials) | 5854 |
| (1, 0) | S− | killed: ~75 GB working set | — | — |

Decision (after (0,2)): the SOS hierarchy is not pursued further as the primary route (no completeness in the λ-degree, cost grows quickly). Pivot: rigorous cell-wise certificate of the Phase-3 separation inequality (section 5).

## 5. Route 2: rigorous cell-wise certificate of the Phase-3 separation inequality (S−)

Statement certified (float64 with explicit safety margins; interval arithmetic NOT used): for every unit x ∈ C² and every unit y ∈ Y_{S−}(x) = ker Φ_x, y†Ry ≤ s_target = 0.9·trR/20 = 0.0136824. Since tr R − 20 s_target = 0.0304 > 0, the Phase-3 criterion gives I₂₀ ∉ cone{yy†: y ∈ 𝒴_{S−}} ⇒ S− not saturable (conventions D1/D2, T4).

Method (code/c3d_cell_certificate_adapted.py). Φ(u) = Σ u_j Φ_j is real-linear in u = (Re x₀, Im x₀, Re x₁, Im x₁). Cell with centre u₀, |Δu| ≤ du (Bloch rectangle with half-widths hθ, hφ; speed bound du = ½hθ + sin(θ_hi/2)·hφ; the first version had ½·sin and under-estimated the φ term by 2×, found by a blind audit, see below). With Φ₀ = Φ(u₀), 36 rows, σ₃₆(Φ₀) > 0: any y ∈ ker Φ(u) is y = z + w, z ∈ K = ker Φ₀, w ∈ rowspace, w = −Φ₀⁺Φ(Δ)(z+w), so |w| ≤ ρ|z|, ρ = κ_K/(1−κ), κ = du·√Σ_j|Φ₀⁺Φ_j|², κ_K = du·√Σ_j|Φ₀⁺Φ_j Z|² (< 1 required). Then yᵀMy ≤ max(λ_K,0) + 2|MZ|ρ + |M|ρ², λ_K = λ_max(ZᵀMZ). Failing cells are bisected.

Dead ends before it worked (kept as findings, not hidden): the cruder bound |Φ(Δ)|/σ₃₆ with L_Φ = 506 certified 0 cells at depth 5 (2.1M cells); the (λ, x) formulation y = (BB†)^{-1}B(λ⊗x) certified 0 cells at depth 6 because σ_min(B) = 0.037 vs σ_max(B) = 253 (cond BB† = 4.6e7), absolute |W₀| ≈ 14 vs σ_min(W₀Z) ≈ 0.01. The adapted norms κ, κ_K remove that loss.

**Invalidated first run (kept, renamed `*_INVALID_du-bug`).** The first run (2 060 207 cells, depths 4–9, 2251 s) used du with the φ term under-estimated by a factor 2 (|∂u/∂φ| = sin(θ/2), not ½ sin(θ/2)). A blind skeptic (could not run code) found it by hand derivation. Fixed in c3, c3d, c3e; every result computed with the old formula is discarded. `c3b_cell_certificate_lambda.py` still has the old factor but was never used for any claim.

Result (corrected du, margin MARGIN_REL = 1e-8): `CERTIFIED_all_cells`, 3 955 841 certified cells (depths 0–10), 0 uncertified; failed counts per level 512, 2048, 8192, 32768, 116752, 216757, 194808, 219782, 373977, 152847, 0 (sum of cells 5 274 284 − failed 1 318 443 = 3 955 841, recomputed). Certified area 19.739208802178712 vs 2π² = 19.739208802178716 (relative −2.2e-16). Min σ₃₆ over certified cells 0.010076; worst certified-cell bound 0.0136824 ≤ s_target 0.0136824 (this is the bisection threshold, not a measured sup). Run time ≈4295 s (metrics/c3d_S-_f090_v2.json, logs/c3d_S-_f090_v2.log). Label: [VERIFIED-float-with-margin], not interval arithmetic.

Checks (all with the corrected du):
- c3e_validate_bound.py (independent loop implementation with pinv): 1500 random cells, 0 violations of g_true ≤ B, min slack 1.53e-4, median 1.23e-2 [VERIFIED-float] (metrics/c3e_validate_v2.json). A min slack of 1.5e-4 against a bound ≈1.4e-2 is about 1%: this check would detect a systematic bound error of order 1%, not smaller.
- Negative control S+ (same code, same R, depth ≤ 6): `NOT_CERTIFIED`, 0 cells certified at any depth (cells 512…2 097 152, all uncertified, area 2π²) (metrics/c3d_Splus_control_f090_v2.json). L_Φ(S+) = 23.16 vs 506.16 for S−, so the failure is not caused by a crude radius. Expected, since R was built for S− and S+ is saturable; it shows the code does not accept everything, not that it can separate S+.
- Auditor's independent falsification (`falsify_c3d.py`, kernel built from the 48×52 real system in (Re y, Im y, λ), not from `phi_rows`): grid 181×360 = 65 160 points, kernel dim 4 at every point, min σ₄₈ = 0.0056, grid max of y†Ry = 0.002927 at (θ, φ) = (2.670, 1.606), Nelder–Mead refinement from 41 starts 0.002978, ratio to s_target 0.218 (logs/falsify_c3d_run1.log) [VERIFIED-float]. The true supremum found by search is ≈0.0030, about 4.6× below the bisection threshold and about 5× below trR/20 = 0.0152. The 10% gap (trR − 20·s_target = 0.0304) is the gap of the certificate threshold, not of the true supremum. A search is not a proof: it can miss a narrow peak; the cell certificate covers the whole sphere.
- Cell radius check on three cells (including the pole): sup|Δu| / du_code = 0.745, 0.730, 0.943, all ≤ 1, so du in the code bounds the true radius.
- Margin 1e-4 rerun (MARGIN_REL = 1e-4, 10 000× the base margin): `CERTIFIED_all_cells`, 3 977 762 certified cells (depths 0–10), 0 uncertified, uncertified area 0.0; worst certified-cell bound 0.0136823570 ≤ s_target 0.0136823604; min σ₃₆ 0.010075; ≈5500 s (metrics/c3d_S-_f090_margin1e-4_v2.json). Count recomputed: cells 5 303 512 − failed 1 325 750 = 3 977 762. Only 21 921 more cells than at margin 1e-8 (+0.55%), so the verdict is insensitive to float round-off at this level [VERIFIED-float-with-margin].

- mpmath re-verification (40 digits, Φ rebuilt from the integer instance data, float R taken as exact and Hermitized exactly; scratchpad script `mp_check_constants.py`, logs/mp_check_constants.log): L_Φ = 506.1644905 (the code's 506.2151 at margin 1e-4 equals 506.16449·(1+1e-4), as designed); ‖M‖ = λ_max(M) = 0.2897488185 (code 0.28975 at 1e-8, 0.28978 at 1e-4); trR = 0.3040524531. At 6 random cell centres σ₃₆ agrees with float to relative 3e-16…4e-14, far below the 1e-8 margin; the 4 smallest eigenvalues of ΦᵀΦ are ≤ 1e-36 (kernel dim exactly 4 within 40-digit precision), and λ_K(mp) = −0.0011…−0.0134 < 0 at all 6 points [VERIFIED-mp at the sampled points]. Not verified: λ_K and ‖MZ‖ inside the certificate against mp at the same cells (only σ₃₆ was compared), and the full chain at all 3.9M cells.

Not yet: context-blind skeptic audit of the corrected certificate, audit of the reduction (saturable ⇒ I₂₀ ∈ cone{yy†: y ∈ 𝒴_S}: T4, closedness, Radon–Nikodym step, convention D3, assumptions of Nurdin/YIP), positive certificate for S+ (stage D), SHA-256 sums.

## 6. Blind audit of the reduction (stage E, first pass) — E_AUDIT_REDUCTION_BLIND.md

Auditor: `skeptic` agent, given only PHASE3_PROOF.md §§1–6 and CONVENTION_RESOLUTION.md (no history, no certificate results). It had Read/Write/Edit only: no shell, no web. Independence rung: same model family, isolated context = weak–medium. All verdicts are hand derivations, no `[VERIFIED-tool]`, no `[DOCS]`.

| Item | Auditor verdict | My status |
|---|---|---|
| Lemma 1, Lemma 2 (complex constant gives deficit w·|a|²·(Im t)² > 0; independent of spectrum of Q for Q ≻ 0) | HOLDS | hand-derived by auditor [INFERRED]; not re-derived by me |
| Theorem A (general POVM, Radon–Nikodym, null outcomes under P-reg, closure of finite-sum cone) | HOLDS; two wording fixes: define the set Z in §4(vi) by visibly continuous conditions; §7 still says "closed because compact" which §4(vi) calls insufficient | wording fixes open |
| Theorem B (finite POVM, CFIM = QFIM as a matrix) | HOLDS (needs only Q ≻ 0, zero support blocks of SLDs) | [INFERRED] |
| Matrix vs scalar saturation | HOLDS; unstated hypothesis: 12×12 QFIM invertible (needed for the Tr(W F⁻¹) form) | **closed by me**: QFIM_ij = Re Tr(P A_i†A_j), P = diag(1/3, 2/3), min eigenvalue 2.611 (S+), 2.723 (S−), 2.341 (all 16); cond 45 / 2.2e4 / 2.5e4 [VERIFIED-float; QFIM formula is the standard SLD one, taken as INFERRED from the model definition] |
| Hypotheses of YPZJ 1806.07337 / Nurdin 2402.11567 / YIP 2601.21801 | CANNOT-CHECK (no web) | **still open**; the three primary sources must be opened and quoted; note: authors of 1806.07337 are Yang–Pang–Zhou–Jordan (as in the project files), my audit brief had the wrong names |
| Counterexample on small models | CANNOT-CHECK numerically; four hand controls agree with the criterion | **still open** (needs a numerical POVM search on small C²⊕C^m models) |
| CONVENTION T4 ("same saturable class under the limit convention") | GAP, repairable: T2 limit formula proved only for family F_U though stated for every constant-rank family; repair via Schur complement D = C†P⁻¹C; even repaired, covers constant-rank families only; rank-increasing families (T3): D2 not a function of A0 data | **scope restriction to adopt**: the final statement is for convention D1/P-reg (and D2 for constant-rank families); no claim for rank-increasing families |

Auditor's suggested exact necessary condition: if S is saturable then A_a†A_b is Hermitian for every pair a, b ∈ S (block (a,b) of M_S = Σ c λ_aλ_b xx†). I checked it in exact integer arithmetic on all 256 ordered pairs of the instance: **0 violations** (script check_hermitian_qfim.py). So the condition is vacuous here (it is the PCC property already noted in section 2); it neither refutes S+ nor gives a one-line proof for S−. That shortcut is closed.

Consequence for the claim: the reduction passed a first blind pass on the algebra (items 1–4) without a gap, with one repairable gap and one scope restriction on the convention equivalence, and two checks (primary-source hypotheses, small-model counterexample search) still not done. The S− result stays [VERIFIED-float-with-margin] on top of a reduction that is [PROVED by authors + hand-audited once], not independently tool-verified.

### 6b. Check against primary sources (arXiv LaTeX via the arxiv tool, 2026-10-28) [DOCS], closes the "full texts not read" limitation of PHASE3_PROOF §12 for the parts listed

Read: YPZJ 1806.07337 §3.2 (null operators, first 9000 chars) and §4.1 (both saturation theorems); Nurdin 2402.11567v5 §6 (Corrigendum, complete); YIP 2601.21801v1 (statement of conditions (2), (3) and Theorem 1, PCC remark). Not read: Nurdin main-paper Theorem 2 and its lemmas, YIP supplementary proofs, YPZJ §3.3 and §4.2.

1. **YPZJ.** Regular operator: Π_k L_i|ψ_n⟩ = ξ_i Π_k|ψ_n⟩ with ξ_i real, independent of n. Null operator: Π_k L_i|ψ_n⟩ = η_ij Π_k L_j|ψ_n⟩ with η_ij real, independent of n. Hypotheses visible in the text: ρ positive definite on its support (all p_n > 0); a null operator is one whose kernel contains every |ψ_n⟩; the Fisher information of a null operator is DEFINED as a 0/0 limit λ′→λ and expanded to second order, so it depends on the approach direction δλ and needs ρ twice differentiable and a positive denominator.
   My derivation from their expression (hand, not tool-checked) [INFERRED]: with T_ij = ¼ Re Tr(ρ L_i Π L_j), the null contribution is F_ij = 4 (Tδλ)_i (Tδλ)_j / (δλᵀTδλ) while the null QFIM contribution is 4T, so F ⪯ 4T with equality iff rank T ≤ 1 (for δλᵀTδλ > 0). For Π = |π⟩⟨π|, π = (0; y), T = Σ_n p_n (Re a_n Re a_nᵀ + Im a_n Im a_nᵀ) with (a_n)_i = (A_i†y)_n, so rank T ≤ 1 iff all Re a_n, Im a_n lie on one real line, i.e. A_i†y = λ_i x with real λ_i (λ_i = 0 allowed). That is exactly the null part of 𝒴_S. It also shows the direction dependence that T4 handles: for δλ ⟂ λ the expression is 0/0 again.
   For π = (u; y) regular: y†A_i e_n = ξ_i u†e_n for n = 1, 2 gives A_i†y = ξ_i u, the regular part of 𝒴_S (ξ_i = 0 allowed).
2. **YIP v1.** Per-outcome conditions (2), (3) and Theorem 1 (simultaneous hollowization) are as quoted in PHASE3_PROOF §11; PCC is stated as necessary (their Eq. 8). One discrepancy between the two papers: YIP's printed Eq. (2) puts the real coefficient on the other side (⟨π|ψ_a⟩ = ξ⟨π|L_i|ψ_a⟩) from YPZJ's regular theorem (⟨π|L_i|ψ_a⟩ = ξ⟨π|ψ_a⟩). They differ exactly when some ξ_i = 0. Our 𝒴_S follows the YPZJ form and the direct deficit identity (Lemma 1, re-derived by the auditor with t any complex number, including 0). OPEN: whether any element of the S+ POVM, or the S− analysis, actually needs λ_i = 0 (not checked).
3. **Nurdin v5 with Corrigendum.** The original Condition 2 was found insufficient. Corrected theorem: Conditions 1 and 2′ are necessary and sufficient; Condition 3 is necessary; Conditions 1 and 4 are sufficient. Setting: smooth constant-rank family (rank r_+, kernel dimension r_0). Condition 4 asks for a UNITARY W (orthonormal basis of the kernel with columns real-proportional across parameters), a projective measurement, and is only sufficient. Condition 2′ asks, for the null part, for a POVM {E_k} on the kernel with Σ E_k = I_{r_0} and E_k Y†(∂_lṼ − c^k_lm ∂_mṼ) = 0 with real c.
   Since Y†V = 0, Y†∂Ṽ = Y†∂V U†, so the null part does not depend on U and uses only first-order data L_{+0} = 2∂V†Y. For A0: L_{++} = 0 (Condition 1 trivial) and ∂ρ = ½[[0, PA†],[AP, 0]] is off-diagonal, so V†∂V = 0 to first order and U = I, D = 0 solve the PDE system (the corrigendum's own Example 3). Then Condition 2′ reduces to: there is a POVM on C^20 summing to I_20 whose elements satisfy the null condition, i.e. I_20 ∈ cone 𝒴_S [INFERRED, my reading]. So in the limit convention the same cone appears as a necessary and sufficient condition; the saturating POVM there is projective on the support plus a null POVM on the kernel, while under P-reg it uses mixed regular outcomes. This matches the claim of PHASE3 ledger P3-D11 (same saturable set) and the T4 scope restriction. Caveat: whether the PDE system is integrable for a full family around θ₀ is not fixed by the A0 first-order data (the family-dependence the auditor flagged).
4. Our S+ certificate is a non-orthogonal POVM with 280 elements, so Nurdin's Condition 4 (orthonormal basis) does not cover it; consistent with Condition 4 being only sufficient.

Net: the criterion is corroborated by the primary sources in both conventions at the level of the null/regular conditions; remaining caveats are the λ_i = 0 discrepancy between YIP Eq. (2) and YPZJ, the family-dependence of the limit convention, and the unread parts listed above.

### 6c. The λ_i = 0 question (YIP Eq. 2 vs YPZJ), closed on data + source

- **Source [DOCS].** YIP 2601.21801v1, supplement §8.2 ("Regular POVM basis") defines the coefficient as the ratio ξ^(a)_{ω,i} = ⟨ψ_a|L_i|π_ω⟩ / ⟨ψ_a|π_ω⟩ and requires it real and independent of a; i.e. ⟨ψ_a|L_i|π⟩ = ξ⟨ψ_a|π⟩, which is the YPZJ form and allows ξ = 0. The main-text Eq. (2) is printed with ξ on the other side (⟨π|ψ_a⟩ = ξ⟨π|L_i|ψ_a⟩), inconsistent with their own proof exactly when ξ_i = 0. Their Theorem 1 (conditions via W_{ij,ab}, M_{i,ab}) needs no division and is unaffected. Operative form for our 𝒴_S: YPZJ / YIP-supplement form, λ_i = 0 allowed. (The discrepancy was also pointed out in an external review pasted by the owner; I re-read the supplement myself before recording it.)
- **Direct check of the 280-element S+ POVM** (`metrics/inputs/s14_povm_prefix12.npz`; my own script `check_povm280_direct.py` in the scratchpad, written independently of `splus_numerical_check.py`; layout v = (x ∈ C²; y ∈ C^20), ρ = diag(1/3, 2/3) ⊕ 0, L_i = [[0, A_i†],[A_i, 0]], i = 0..11) [VERIFIED-float]:
  - completeness max|ΣwE − I| = 9.6e-10; weights 2.4e-8…0.556; all 280 elements regular (|x| ≥ 0.217, none null, all p > 1e-14).
  - **2 elements have y = 0 exactly (support-only vectors), total weight 1.0557; for them all λ_i = 0 identically.** So the ξ_i = 0 case is realised in the S+ POVM, and these two elements violate YIP's printed Eq. (2) while satisfying the YPZJ form.
  - the other 278: direct residual |A_i†y − λ_i x| / (|y|·‖A_i‖) with λ_i = Re(x†w_i)/|x|²: max 1.8e-10, median 1.9e-16. λ_i ≈ 0 numerically (|A_i†y| ≤ 1e-8·scale) in 6 (element, i) pairs; ≤ 1e-3·scale in 22, ≤ 1e-2·scale in 124 of 3336.
  - F^C computed from probabilities p = w⟨v|ρ|v⟩, dp_i = w⟨v|∂_iρ|v⟩ vs F^Q = Re Tr(ρ L_iL_j): max|F^C − F^Q| / max|F^Q| = 3.3e-10 (max|F^Q| = 114.67); eig(F^Q − F^C) in [−4.9e-8, 1.5e-8]. Same numbers as phase 3; the formula path is different (probabilities, not the SLD-derivative path).
- **Reading.** The positive S+ evidence is a numerical candidate with 1e-10 residuals, not an exact certificate; nothing here changes that. The check shows the λ_i = 0 case is not hypothetical and that the YPZJ form is the right operative one.
- **Not reproduced:** the external review's 4-dimensional two-parameter exact counterexample (six outcomes): the explicit POVM was not provided. The same structural point (an optimal POVM with a regular element whose ⟨π|L_i|ψ⟩ = 0 while ⟨π|ψ⟩ ≠ 0) is realised by our own POVM above.

## 6d. Stage C, lemma and coverage audit (2026-10-29) — see LEMMA_CELL_AUDIT.md

- **Lemma (L1–L4):** re-derived by hand step by step (LEMMA_CELL_AUDIT.md §1–4). No error found. Kernel = Y_S(x) (phase-3 rows), speed bound du, the decomposition y = z + w with |w| ≤ ρ|z|, and the quadratic bound B. L_Φ is not used by the current certificate (only by the historical c3 script); κ, κ_K, ‖M‖, ‖MZ‖, λ_K are.
- **Coverage:** leaves tile [0,π_f]×[0,2π_f] exactly (children share float midpoints); the float seams (θ = π, φ = 2π) are covered by L2, because the lemma holds for every unit u with |u − u₀| ≤ du, not only for points in the rectangle. Degenerate points (σ₃₆ = 0 inside a leaf) need no separate treatment: the bound uses only the centre's data. Checked numerically: `code/sliver_check.py`, 20 000 polar and 20 000 seam leaves, max ratio 1 − 9·10⁻⁹ < 1 (logs/sliver_check.log).
- **Sampling audit:** `code/lemma_audit.py`, 40 leaves × 6000 points on the sphere ball (metrics/lemma_audit_40x6000.json): NO_COUNTEREXAMPLE_IN_SAMPLES; max g/B_up = 0.111, max |w|/(ρ|z|) = 0.83, max du-ratio = 0.91. Sampling can refute, not prove.
- **Corrected in this stage:** (i) my first version of LEMMA_CELL_AUDIT claimed the seam check was zero on the audit sample; no audit leaf touched θ = π, so that claim was withdrawn and the seam was tested separately. (ii) Full interval run estimated at ~3.2 h on 24 cores (not 77 h single-core as first stated); not started.
- **Not done (open):** strict interval evaluation for all ~3.96·10⁶ leaves or a proved float-error bound for all of them; formal verification of the decomposition; the S− result stays [VERIFIED-float-with-margin] plus interval on 5630 leaves; not PROVED.
- **Alternative threshold b = 0.0145** (task contract, item 2 of the S− section): tr R − 20·0.0145 = 0.014052 > 0, legitimate because the criterion needs only sup < tr R/20 (for any unit-normalised cone decomposition: tr R = Σc_j y_j†Ry_j ≤ b·Σc_j = 20b). Run `c3d_S-_b0145_v2` (frac = 0.9537828) launched in background; result pending (metrics/c3d_S-_b0145_v2.json).

### 6e. Alternative threshold b = 0.0145 (result, 2026-10-29)
- `c3d_S-_b0145_v2`: CERTIFIED_all_cells, 3 413 399 leaves (vs 3 955 841 at 0.9·trR/20: −14%), 0 uncertified; worst certified bound 0.01449999637 ≤ 0.0145; tr R − 20·0.0145 = 0.01405245 > 0; min σ₃₆ 0.010076 (metrics/c3d_S-_b0145_v2.json). [VERIFIED-float-with-margin]
- Assessment: the threshold change is legitimate and does give a valid certificate, but saves only ~14% of leaves. The bound stays tight (bisection stops at the threshold), so the interval cost of a full strict check barely drops (≈2.8 h instead of 3.2 h on 24 cores). Not a cheap route to rigor.
- PROOF_CERTIFICATES/SHA256SUMS.txt covers 65 files (inputs, code, metrics, logs, notes); REPRODUCIBILITY.md lists the commands.

### 6f. Full strict interval pass over all leaves of S− (2026-10-29)
- **Run 1** (`code/interval_full_parallel.py`, 12 workers): 3 595 000 of 3 955 841 leaves processed, 0 failures in its journal (`metrics/interval_full_progress.jsonl`, 7 190 chunks). Stopped with `FLINT exception: Unable to allocate memory (1441151890153799712)` (`logs/interval_full_parallel.log`). No summary written. **Cause not established.** The number looks like an arb size or precision blow-up on one cell, or memory pressure at 12 workers. The first run did not record the leaf index, so this is unresolved.
- **Run 2** (`code/interval_resume_parallel.py`, 8 workers, `logs/interval_resume_parallel.log`): the 722 chunks absent from run 1 (360 841 leaves). Per-leaf exceptions are caught and recorded with leaf index and cell; none occurred. 0 failures. Journal `metrics/interval_resume_progress.jsonl`, summary `metrics/interval_resume_summary.json` (`min_slack_abs_this_run = 6.14·10⁻³`, `max_B_up_this_run = 7.54·10⁻³`, threshold `s = 1.368·10⁻²`, `final gap = 3.04·10⁻²`).
- **Independent coverage check** (`code/verify_interval_coverage.py` → `metrics/interval_coverage_check.json`, verdict `COVERAGE_CONSISTENT`): both journals together cover the 7 912 chunk indices with no duplicates and no gaps; each line has `n` equal to the expected chunk size and `ok + fails = n`; the sum is 3 955 841 leaves; 0 failures. The leaves array has 3 955 841 rows, and some rows reach θ = π and φ = 2π. That last check only shows the terminal cells are present, not that none were lost.
- **Status [VERIFIED-interval for every leaf that the journals report; the journal of run 1 is the only evidence for its first 3 595 000].** The run-1 exception is a real gap in the record: those leaves were checked, but the one that triggered the exception is not identified. Run 2 does not reproduce it at 8 workers.
- **Not established by this step:** the geometric covering argument (L1–L4, `LEMMA_CELL_AUDIT.md`), the global separation chain (Lemma R, the bound y†Ry ≤ s on all admissible directions, the necessity of I₂₀ ∈ cone{yy†}), and the CFIM convention. A certificate that every leaf passes says nothing about these. Verdict stays: **not PROVED**. See `STAGE_C_FINAL_PROOF.md` (written 2026-10-29, verdict CONDITIONAL).

### 6g. Stage C final proof attempt (2026-10-29)
- Lemma-level re-derivation (L1–L4) done step by step; kernel equivalence `Y_S(x) = ker Φ(x)` now also covered at the pole x₀ = 0 (the earlier text handled only x₀ ≠ 0).
- **Code fix:** `code/interval_cells.py` set λ_K from the midpoint of the arb enclosure; now it uses the upper bound. Rechecked the 200 cells with smallest slack (`code/recheck_closest_leaves.py`, `metrics/recheck_closest_leaves.json`): 200/200 below s, B_up unchanged. The full run (6f) used the old rule; a full re-run with the corrected code was done later as `o3_v2` (6j).
- Verified exactly: R is exactly Hermitian after symmetrisation, M is its exact real form, `final_gap = 0.030405 > 0`.
- Still open: literature convention check (O4). Closed later: O1 (6i), O2 (6h), O3 (6j).

### 6j. Full re-run with corrected rule (O3, 2026-10-30)
- Code: `code/interval_cells_v2.py` (+ `code/o3_run_v2.py`, `code/preflight_v2.py`). v1 `interval_cells.py` unchanged. Snapshot and SHA-256: `SHA256SUMS_o3v2.txt`. Design and kernel certificate: `PRECHECK_KERNEL_v2.md`.
- Result: 7 912 / 7 912 chunks, 0 duplicates, 0 failures; 3 955 841 leaves; `final_gap_positive` true; min slack in this run 8.4·10⁻⁹ (positive, narrow).
- Found during pre-check: `np.array_equal(R, R^H)` is False (max diff 5.2·10⁻¹⁷, 298 entries). R is now symmetrised in arb. The earlier sentence "R exactly Hermitian" in 6g was wrong as stated.
- Run was interrupted by a PC restart at chunk ~3420 and resumed from the progress journal (chunks are written only after full processing, so no chunk was lost or counted twice).
- Per-leaf `B_up` maximum and slack minimum are recorded only for chunks 3421–7911 (summary of this run). For chunks 0–3420 only the per-leaf `ok` status is in the journal.

### 6h. Exact tiling check (O2, 2026-10-29)
- `code/verify_tiling_exact.py` rebuilds the partition tree from the 16×32 root grid with the same float split as `c3h_dump_all_leaves.py` and matches every accepted leaf by IEEE-754 bit pattern. Result: 3 955 841 leaves = 3 955 841 distinct = 3 955 841 matched tree nodes; stop at depth 10; 0 uncovered cells (`metrics/tiling_exact_check.json`, verdict `TILING_EXACT`).
- Negative controls: dropping one leaf → 1 048 576 uncovered cells; duplicating one leaf → distinct ≠ length. Both give `TILING_PROBLEM` (`logs/verify_tiling_exact.log`, controls run in scratchpad).
- Scope: the tiling is exact on the float rectangle [0, π_f] × [0, 2π_f]. The gap to π and 2π is handled by L2 (LEMMA_CELL_AUDIT §4).

### 6i. Independent check of the reduction (O1, 2026-10-29)
- An agent without the history of this work re-derived PHASE3 Lemma 1 (G_c ≥ 0 and the equality case), Lemma 2, the Corollary, Theorem A steps (i)–(vii) and the separation step. Verdict: VALID (`audit/O1_independent_report.md`).
- Numeric check reproduced: `code/o1_check.py` → `logs/o1_check.log` (min normalised G = 0.0067 random, 0.0088 on A0; admissible rank-one max |G|/(q·p) = 1.4·10⁻¹² and 3·10⁻⁹).
- Refinement found, not an error: PHASE3's equality condition is weaker than the exact one (the exact one needs one real t shared by all pieces). Sufficient for Theorem A.
- Independence is weak–medium (same model family, no shared history). PROVED still needs a check by a human or a different model family.

## 6k. Сверка D1 по первоисточникам (O4, 2026-10-30)

- Результат: формулировка «D1 — соглашение, принятое в литературе» неверна. YPZJ (1806.07337) для нулевых исходов использует многомерный предел, то есть D2 (направленно зависящий). Nurdin (2402.11567 v5) и YIP (2601.21801) наследуют конвенцию YPZJ. D1 — выбор этого проекта. `[TEXT]`, часть текстов не прочитана (см. CONVENTION_RESOLUTION §6).
- Теорема C ограничена D1 (STAGE_C_FINAL_PROOF §2). Переход D1 → D2 не доказан.
- Открыто два пункта: квантор по направлениям (T4 требует одно направление h, YPZJ thm:null требует все; CONVENTION_RESOLUTION §7.2) и точная постановка D2.
- Новых вычислений не запускалось. Стадия C остаётся CONDITIONAL. Стадия D не начиналась.
