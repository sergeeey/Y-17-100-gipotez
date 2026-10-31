# CONVENTION_RESOLUTION — which CFIM, and what the main hypothesis says (phase 4, stage B)

Date: 2026-10-28. Scope: canonical A0 instance (`instance_d22_r2_s16.jsonl`, unchanged), S+ = {0..11}, S− = {4..15}.
L0 class: Descriptive (exact statements about a fixed finite-dimensional model). Ladder tier: Full.
Evidence markers: `[PROVED]` argument written here; `[VERIFIED-float]` numerics (metrics/ files); `[TEXT]` read in a primary source; `[UNKNOWN]` not read or not checked. Independent audit of these proofs is stage E, not done yet, so every `[PROVED]` below is "proved by the author, audit pending".

## 1. What A0 actually specifies

A0 gives ρ = diag(1/3, 2/3) ⊕ 0 on C²⊕C²⁰ and Hermitian generators L_i = [[0, A_i†],[A_i, 0]] with ∂_iρ|θ0 = ½{ρ, L_i}. It gives **first-order data only**. It does not give ρ_θ for θ ≠ θ0.

Consequence `[PROVED]`: any quantity that needs ρ_θ near θ0 beyond first order is not a property of A0 unless a family is chosen. Two families with the same first-order data (both checked, `metrics/b2_conventions_A0.json`, first-order residual 0.0):
- F_U (constant rank 2): ρ_θ = U_θ ρ U_θ†, U_θ = exp(Σ θ_i X_i), X_i = [[0, −B_i†],[B_i, 0]], B_i = A_i/2. Then [X_i, ρ] = ½{ρ, L_i}. It exists for every A, so the data are realisable at constant rank.
- F_R (rank increasing): ρ'_θ = (1 − c|θ|²) ρ_θ + c|θ|² σ with σ a kernel projector. The change is quadratic, so first-order data are unchanged.

## 2. Three definitions of "the classical Fisher information at θ0"

For a finite θ-independent POVM {E_k}, p_k(θ) = tr(ρ_θ E_k). Regular outcome: p_k(θ0) > 0. Null outcome: p_k(θ0) = 0 (equivalently E_k supported in ker ρ; Nurdin Lemma 1 `[TEXT]`).

- **D1, point (P-reg) CFIM.** F¹ = Σ_{p_k(θ0)>0} ∂p_k ∂p_kᵀ / p_k; null outcomes contribute 0. Depends only on (ρ, L_i).
- **D2, limit-matrix CFIM.** F²(h) = lim_{t→0} F^C(θ0 + t h), null outcomes included at their own probabilities. Depends on the family and on the direction h.
- **D3, directional scalar.** F³(u) = uᵀF^C u compared with uᵀF^Q u for one fixed u (or the limit analogue). Attainability of the scalar bound for one direction.

Quantum side: F^Q_ab = Re tr(ρ L_a L_b) = Re tr(Q A_a†A_b) (Q = diag(1/3, 2/3)). Per-outcome QFI share N_E,ab = Re tr(E L_a ρ L_b); Σ_k N_{E_k} = F^Q for every complete POVM. For a rank-one null E = ww†, w = (0; y): N_E,ab = Re(a_a† Q a_b) with a_i = A_i†y ∈ C². So N_E has rank ≤ 1 iff all a_i are real multiples of one vector v ∈ C², i.e. y ∈ Y_S(v) = {y : A_i†y = λ_i v, λ_i ∈ R}, or y is pure (all a_i = 0).

## 3. Results

**T1 (regular outcomes; no convention dependence)** `[PROVED]`. If every outcome of a finite POVM has p_k(θ0) > 0, then F^C(θ) is continuous at θ0 for every smooth family, so D1 = D2 (all h). The value D1 depends only on first-order data.

**T2 (null outcomes at constant rank)** `[PROVED]` for F_U. For a null E = ww†, w = (0; y), |w| = 1: ρ_θ = ρ + [X,ρ] + ½[X,[X,ρ]] + …, X = Σθ_iX_i. Using ρw = 0: tr(E[X,ρ]) = 0 and tr(E[X,[X,ρ]]) = −2 tr(E Xρ X). Hence p_E(θ) = ¼ θᵀN_Eθ + O(|θ|³) with N_E as above (checked, `[VERIFIED-float]`: p/t² = 0.1274 at t = 0.01 against the prediction 0.1276 from hᵀNh/4). Therefore, for hᵀN_Eh > 0,
  CFIM_E(θ0 + t h) → (N_E h)(N_E h)ᵀ / (hᵀN_E h) ≤ N_E (Cauchy–Schwarz), with equality iff rank N_E ≤ 1.
For hᵀN_Eh = 0 the limit is 0 for F_U (checked: 9e-9 at t = 0.01, `[VERIFIED-float]`), not N_E. This agrees with the repository result Z3/Z5/Z6 with hypothesis A1 (`null_results/20261021-h-cat56-2-cfim-zero-prob-convention-general-identities.md`, `[VERIFIED-mp]`).
For a pure null outcome (N_E = 0), elementary bound |∇p|² ≤ 2 p sup‖Hess p‖ for p ≥ 0, with Hess p → 0, gives CFIM_E → 0.

**T3 (D2 is not a function of the A0 data)** `[PROVED]` + `[VERIFIED-float]`. For F_R with σ = E, p'_E ≈ t²(hᵀN_Eh/4 + c|h|²). In the check (c = 0.5, same null element, same h): the limit contribution is ≈ [[2.09, 1.01],[1.01, 0.49]] (trace 2.57) against N_E with trace 0.83, and along h ⊥ range(N_E) it is nonzero (≈ [[1.34, −0.94],[−0.94, 0.66]]) while F_U gives 0. So a null element can contribute more than its N_E, and D2 changes with the family although (ρ, L_i) do not. Statements about D2 are statements about (A0 + a chosen family). Only constant rank (A1, assumed explicitly in Nurdin: dim ker ρ_θ fixed `[TEXT]`) is used below.

**T4 (saturability class is the same for D1 and D2)** `[PROVED]`. Let S ⊂ {0..15} and 𝒴_S = ∪_x Y_S(x) (including pure vectors). TFAE:
 (i) some finite POVM has F¹ = F^Q_S (D1);
 (ii) for a family with A1, some finite POVM has lim_{t→0} F^C(θ0 + t h) = F^Q_S for at least one direction h with hᵀN_Eh > 0 for every non-pure null element (D2);
 (iii) I₂₀ ∈ cone{yy† : y ∈ 𝒴_S}.
Proof. (iii)⇒(i): phase-3 Theorem B (explicit POVM). (iii)⇒(ii): the same POVM; if |S| is such that no pure vector exists, all outcomes are regular and T1 applies; pure null outcomes contribute 0 by T2. (i)⇒(iii): phase-3 Theorem A. (ii)⇒(iii): Σ_k N_{E_k} = F^Q and, per outcome, F^C_E(θ0) ≤ N_E for regular E (YPZJ Eq. (9) `[TEXT]`, also phase-3 Lemma 1) and Ψ_h(N_E) := (N_Eh)(N_Eh)ᵀ/(hᵀN_Eh) ≤ N_E for null E (T2). Equality of the sums of PSD differences forces each difference to vanish. For null E this means rank N_E ≤ 1, and since N_E = Σ_j N_{y_j} is a sum of PSD terms of rank ≤ 1 with one common range, every rank-one piece y_j has a_i = c_i v, i.e. y_j ∈ 𝒴_S. For regular E every rank-one piece is admissible or pure (phase-3 refinement inequality). Hence I₂₀ = Σ_k (E_k)₀₀ is a sum of yy† with y ∈ 𝒴_S. ∎
Key point: a null outcome in D2 is allowed to use a vector (0; y) with y ∈ Y_S(v), v ≠ 0, which D1 forbids. But the **same y** is already available in D1 inside the regular outcome (±s x; y)(…)† with x = v. Only the kernel-block vectors y enter I₂₀, so the cone is identical.

**T5 (D3 is trivial and cannot carry the hypothesis)** `[PROVED]` + `[VERIFIED-float]`. For every direction u, projective measurement in an eigenbasis of L_u = Σu_iL_i gives uᵀF^C u = uᵀF^Q u (Braunstein–Caves; null eigenvectors have zero support part, so zero QFI share). On S−: 5 random u, relative directional deficit ≤ 7e-16, while the matrix deficit of the same measurement is 0.5%–3.4% in Frobenius norm and max eigenvalue 287–2037 (`metrics/b2_conventions_A0.json`). So D3 holds for S− and for S+ alike; it says nothing about the S+/S− difference.

**T6 (S+ POVM is regular)** `[VERIFIED-float]`. All 280 outcomes of the saved S+ POVM have p_k > 0: min p_k = 5.5e-10 (relative to weight: ≥ 0.0157), no outcome below 1e-12, every vector has ≥ 21% of its norm on the support (`metrics/b1_splus_regularity.json`). By T1, F^C_lim = F^C_pt, checked on F_U: ‖F^C(θ0+th) − F^C(θ0)‖ = 9.2e-3, 9.2e-5, 9.3e-7 at t = 1e-2, 1e-3, 1e-4 (linear in t); ‖F^C(θ0) − F^Q‖ = 5.2e-8 against ‖F^Q‖ = 125.3. This is float64, not an exact certificate (stage D).

## 4. Definition of the main hypothesis (fixed from here on)

**H\*.** Let SAT(S) mean: there exists a finite (equivalently, by phase-3 Theorem A, any standard-Borel) θ-independent POVM with F^C_pt(θ0) = F^Q_S as 12×12 matrices, with D1 (null outcomes contribute 0). Equivalent to the scalar bound Tr(W F^{-1}) = Tr(W (F^Q)^{-1}) for one (hence every) positive-definite W (F^C ≤ F^Q gives (F^C)^{-1} ≥ (F^Q)^{-1}, equality of a W-trace with W > 0 forces equality). Claim: **SAT(S+) is true and SAT(S−) is false** on the canonical A0.
Not covered: single-direction attainability (T5), multi-copy or asymptotic attainability, the Holevo bound, any statement needing a particular ρ_θ beyond first order, families without constant rank (T3).
By T4, H\* is equivalent to: I₂₀ ∈ cone{yy† : y ∈ 𝒴_{S+}} and I₂₀ ∉ cone{yy† : y ∈ 𝒴_{S−}}. This is the form stages C and D certify.

## 5. What this changes for earlier claims

| Item | Before | Now |
|---|---|---|
| P3-D11 (classification coincides for P-reg and limit conventions) | OPEN, "derived" | `[PROVED]` as T4 (A1, generic direction), audit pending in stage E |
| Cone criterion, S+ POVM, S− certificates | stated under P-reg | valid under D1; same class under D2 with A1 (T4); D3 does not apply (T5) |
| Nurdin Example 2 conflict (Z10) | CONFLICT, source-internal | unchanged; not needed for A0: A0's S+ POVM is regular (T6) |
| Claims about D2 for non-constant-rank families | unclear | out of scope for A0 (T3) |

## 6. Primary-source check (what was and was not read)

- Yang–Pang–Zhou–Jordan, arXiv:1806.07337 v3: `[TEXT]` the CFIM of a null POVM element contains 0/0 terms "understood in the sense of the multivariate limit" (introduction); per-outcome inequality uᵀF^k u ≤ uᵀI^k u for regular and null elements (Eq. 9); saturation for regular elements: Π_k L_i|ψ_n⟩ = ξ_i^k Π_k|ψ_n⟩ with ξ real and independent of n (Eq. 39). Their convention is D2 (multivariate limit: F^k = lim g/h along δλ, with the null-case formula depending on the direction; checked by hand: with T = N/4 it gives (Nh)(Nh)ᵀ/(hᵀNh)). Theorem null (eq:Fijk-null) read in part; its proof after the symmetrisation step not read in full `[UNKNOWN]`. Consequence: D1 is the repository's own choice, not the literature's convention (see STAGE_C_FINAL_PROOF O4).
- Nurdin, arXiv:2402.11567 v5 (corrigendum): `[TEXT]` dim ker ρ_θ = r₀ fixed (constant rank, our A1); Definition 1 regular/null; Theorem 1 (citing YPZJ Theorems 1–2): regular E_k L_l|ψ⟩ = c_l E_k|ψ⟩; null E_k L_l|ψ⟩ = c_lm E_k L_m|ψ⟩ with real c_lm. The pairwise form is the rank-one condition on N_E (it fails when a_m = 0 ≠ a_l, which is why the repository's earlier finding P1 says the literal form is unsatisfiable at D; irrelevant to A0 because T6).
- Yang–Imai–Pezzè, arXiv:2601.21801 v1: `[TEXT]` abstract and Theorem 1 passage (simultaneous hollowization of W_{ij,ab}, M_{i,ab}); Observation 2 (dim 𝒱⊥ < d−1 ⇒ not saturable). The null-outcome convention in their proof not read `[UNKNOWN]`.
- Read in part (2026-10-30, LaTeX sources via arXiv MCP): YPZJ ~40 000 of 96 189 characters; Nurdin ~26 000 of 58 339; YIP ~26 000 of 76 079. Not read: YPZJ null-case proof tail, Nurdin main-paper Theorem 2 proof and its lemmas, YIP End Matter and Supplemental Material. Nurdin v5 corrigendum (§6, Theorem 3, condition 2′) read in full (2026-10-30). Nurdin v5 has no labelled "Theorem 6": its Introduction cites "(Theorem 6)" as a dangling reference, so the earlier "Nurdin Theorem 6" is replaced by "Nurdin v5 Thm 2/3". Equation numbers (9), (39) are checked against LaTeX labels only, not against the published numbering.
- Statements above rely on the quoted passages and on the repository's earlier `[VERIFIED-mp]` identities.

## 7. Residual risks

1. T4 (ii)⇒(iii) uses the identity Σ N_E = F^Q and equality-forcing; stage E should re-derive it independently (different code path, exact control).
2. Direction quantifier (found 2026-10-30). T4 (ii) requires saturation for at least one direction h; YPZJ thm:null gives the condition for all directions δλ. For a null element with N_E ≠ 0 there is a subspace of directions h ⊥ range(N_E) where the YPZJ formula is 0/0, and T2 sets it to 0 (the F_U choice), which is a choice, not a consequence of the text. So "D1 and D2 have the same saturable class" is proved only for the one-direction variant of D2, not for the all-directions variant. Open until the exact D2 statement is fixed (O4).
2. T2 is proved for F_U; the general A1 statement is quoted from the repository's null result, not re-proved for arbitrary smooth families here.
3. T6 is float64; the minimum probability 5.5e-10 is far above machine precision but not an exact positivity proof.
