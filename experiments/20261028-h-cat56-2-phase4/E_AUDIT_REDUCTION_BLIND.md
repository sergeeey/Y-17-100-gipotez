# E_AUDIT_REDUCTION_BLIND — context-blind falsification audit of the cone criterion

Date: 2026-10-28. Auditor: skeptic agent, context-blind.
Objects audited: `experiments/20261028-h-cat56-2-phase3/PHASE3_PROOF.md` §§1–6 (with §7 and §11 read
because they state claims about §§1–6) and `experiments/20261028-h-cat56-2-phase4/CONVENTION_RESOLUTION.md`.
Not read: ADVERSARIAL_REVIEW.md, DISCOVERY_LEDGER.md, FINAL_DECISION.md, C_NOTES.md, the instance file, any metrics.

**Substrate limit, stated first (affects items 5 and 6).** This audit ran with Read/Write/Edit only:
no shell, no Python, no web fetch. So no script was run (the scratch folder `audit_red\` was not
created) and no arXiv paper was opened. Every tag below is therefore `[INFERRED]` (hand derivation,
step by step), `[TEXT-of-audited-file]` (what the audited file says), `[MEMORY]` (capped LOW), or
`[UNKNOWN]`. No `[VERIFIED-tool]` and no `[DOCS]` tag appears anywhere in this report. That is not an
oversight to fill in later by assumption: items 5 and 6 are CANNOT-CHECK for this reason.

## Summary table

| # | Item | Verdict |
|---|---|---|
| 1 | Lemma 1, Lemma 2, realness of λ, complex λ ⇒ strictly positive deficit | HOLDS |
| 2 | Theorem A (general POVMs, Radon–Nikodym, closure, null outcomes) | HOLDS (one wording repair in (vi), one stale sentence in §7) |
| 3 | Theorem B (explicit finite POVM) | HOLDS |
| 4 | Matrix vs scalar saturation | HOLDS: matrix equality is used; one unstated hypothesis (F^Q invertible) for the inverse-covariance form in CONVENTION §4 |
| 5 | Hypotheses of cited theorems against primary sources | CANNOT-CHECK (no web access); one attribution discrepancy flagged |
| 6 | Counterexample search | CANNOT-CHECK numerically; four hand-derived controls all agree with the criterion; a new exact necessary condition is derived that should be run on the instance |
| — | CONVENTION T4 ("same saturable class under the limit convention") | GAP (repairable, repair given below); scope is constant-rank families only |

---

## 1. Lemma 1 and Lemma 2 — HOLDS

Checked: PHASE3 §2 lines "b = (√Q A_c† y ; 0), a = (√Q x ; 0)" through "Consequences (a)–(c)", and §3 in full.

Re-derivation `[INFERRED]`, from the setting in §1 (ρ = Q ⊕ 0, Q = diag(1/3, 2/3), L_i = [[0, A_i†],[A_i, 0]], ∂_iρ = ½{ρ, L_i}):

- For π = (x; y): L_c π = (A_c† y; A_c x). With ρ^{1/2} = √Q ⊕ 0: a = ρ^{1/2}π = (√Q x; 0), b = ρ^{1/2}L_cπ = (√Q A_c† y; 0). Correct.
- p = w π†ρπ = w|a|². q_c = w π† L_c ρ L_c π = w|b|². Tr(ρ L_c m) = w π†ρ L_c π = w⟨a, b⟩. Since m is Hermitian, Tr(Lρm) = conj Tr(ρLm), so Tr(∂_cρ m) = Re Tr(ρ L_c m) = w Re⟨a,b⟩. Correct.
- Per-outcome classical term (∂_c p)²/p = w (Re⟨a,b⟩)²/|a|². Deficit G_c = w(|b|² − (Re⟨a,b⟩)²/|a|²) ≥ w(|b|² − |⟨a,b⟩|²/|a|²) ≥ 0. Correct.
- Equality: the second inequality is equality iff b = t a for some t ∈ C; the first iff additionally Im t = 0. Because √Q is invertible on C², b = t a ⟺ A_c† y = t x. Correct, and this is the only place Q enters: the criterion is independent of the spectrum of Q as long as Q > 0 on C². (This is consistent with the YPZJ-type regular-outcome condition "same real ξ for every support eigenvector", see item 5.)
- Linearity / realness of t_c: for fixed x ≠ 0, t_c is uniquely determined by A_c† y = t_c x and A_c† y is linear in c, so t_c is linear; t_{e_i} = λ_i real gives t_c = Σ c_i λ_i real for all real c. Conversely real λ_i give real t_c. Correct.
- Complex constant ⇒ strictly positive deficit: if A_c† y = t x with Im t ≠ 0, then b = t a, |b|² = |t|²|a|², Re⟨a,b⟩ = (Re t)|a|², so G_c = w|a|²(|t|² − (Re t)²) = w|a|²(Im t)² > 0 (for w > 0, x ≠ 0). Correct; the claim (b) is exact, not only "generically".
- Null case x = 0: a = 0, so p = 0 and a_c = 0; under P-reg the outcome contributes 0 to F^C while it contributes q_c = w|√Q A_c† y|² to F^Q, so G_c = q_c, zero for all c iff A_i† y = 0 ∀i. Correct.

Lemma 2 `[INFERRED]`: p, a_c, q_c are additive over a finite decomposition; null pieces have a_k = 0 (their a-vector is 0); for p(m) > 0, (Σa_k)²/Σp_k ≤ Σ_{p_k>0} a_k²/p_k is the Cauchy–Schwarz (Sedrakyan/Engel) inequality. If p(m) = 0 every piece is null and G_c(m) = q_c(m) = Σ q_k. Correct, including for non-orthogonal decompositions. Corollary (each positive-weight piece admissible or pure when G_c(m) = 0 ∀c) follows because every term is ≥ 0. Correct.

No gap.

---

## 2. Theorem A — HOLDS (two wording defects, neither affects validity)

Checked: PHASE3 §4 steps (i)–(vii) and the Remark.

(i) Radon–Nikodym `[INFERRED]`. ν = Tr M(·) is finite (ν(Ω) = 22). If ν(E) = 0 then M(E) is PSD with zero trace, hence 0, so every entry of M is ν-absolutely continuous; the matrix density m is PSD ν-a.e. (test against a countable dense set of vectors) and ∫ m dν = I. Correct. Note: only finiteness of ν is used; "standard Borel" is not needed for this step (harmless extra hypothesis, not a gap).
- θ-derivative: in finite dimension p_θ(ω) = Tr(ρ_θ m(ω)) with m θ-independent, so ∂_i p = Tr(∂_iρ m) pointwise and the density is w.r.t. the θ-independent ν. Correct.
- {p = 0}: Tr(Q m₀₀) = 0 with Q > 0 forces m₀₀ = 0, and PSD then forces the off-diagonal blocks to vanish, m = 0 ⊕ K. Then ρL_i(0 ⊕ K) = [[0, Q A_i† K],[0, 0]] has zero trace, so ∂p = 0 there. Correct.

(ii) c^T F^Q c = Tr(ρL_c²) = Tr(ρ L_c (∫m dν) L_c) = ∫ q_c(m) dν (linear in m). Integrability of a_c²/p follows from 0 ≤ a_c²/p ≤ q_c pointwise. Correct.

(iii) G_c(m(ω)) = c^T D(ω) c with D(ω) ⪰ 0 a quadratic form in c (true for p > 0 and for p = 0). ∫ G_c dν = 0 for each c in a countable set (e.g. e_i and e_i + e_j suffice) gives a single null set off which D(ω) = 0. Correct.

(iv) Spectral pieces of m(ω) are admissible or pure by the Lemma-2 corollary; the kernel block of m(ω) is Σ_k w_k y_k y_k† ∈ 𝒞_S. Different pieces may use different x_k; this is fine because 𝒴_S is the union over x. Correct. **This is the "reduction to rank-one outcomes"**: it is not a reduction of the POVM but a pointwise spectral decomposition of the density, legitimate because the deficit is additive and Lemma 2 holds for any finite decomposition. Correct.

(v) ∫ K dν = (∫ m dν)₁₁ = I₂₀. Correct.

(vi) Closure `[INFERRED]`. Result correct, one wording repair needed:
- Z must be shown closed jointly in (x, y). The text defines Z through "the real-linear form Φ_x y = 0 … (phi_rows of the code)". If Φ_x is built from a basis of the real complement of R·x, that basis need not depend continuously on x. Repair (one line): for |x| = 1, "A_i† y ∈ R x" ⟺ A_i† y − (x† A_i† y) x = 0 and Im(x† A_i† y) = 0, both continuous in (x, y); so Z is closed in S³ × S³⁹, compact, and its projection 𝒴¹ is compact. Pure unit vectors and all special points are included automatically.
- Cone closedness: conv{yy† : y ∈ 𝒴¹} is compact (Carathéodory) and lies in {tr = 1}, so 0 ∉ conv; the cone over a compact convex set not containing 0 is closed. Correct.
- **Stale sentence:** §7 bullet "Closure" still says "𝒞_S is closed because 𝒴¹ is compact", which §4(vi)'s own audit note says is insufficient. Text inconsistency, not a logic gap.
- Finite sums vs closure: since 𝒞_S (finite sums) is already closed, there is no distinction. And Theorem A concerns one POVM, not a limit of POVMs, so no "limit of POVMs" closure issue arises. A limit-of-POVMs question would arise only for an infimum/asymptotic notion of attainability, which the text does not claim.

(vii) Separation of I₂₀ from a closed convex cone gives Hermitian R with tr R > 0 and tr(RX) ≤ 0 on 𝒞_S; ∫ tr(R K) dν ≤ 0 contradicts. Correct (equivalently: an integral of a measurable function valued in a closed convex cone lies in the cone).

Null-outcome handling: correct under P-reg (null outcomes contribute 0 to F^C, contribute q_c to F^Q, so saturation forces them pure). Under any other convention Theorem A as written does not apply; see the T4 row below.

Remark (finite, countable, general POVMs): correct.

---

## 3. Theorem B — HOLDS

Checked: PHASE3 §5 construction, completion, and the rational-compatibility paragraph.

`[INFERRED]`:
- π_j^± = (±√ε x_j; y_j): A_i† y_j = λ_ij x_j = (±λ_ij/√ε)(±√ε x_j), real coefficient. Admissible. Pure y_j (y_j ∈ C_S) are in Y_S(x) for every x, so any x_j ≠ 0 may be assigned; the theorem therefore covers all of 𝒴_S, not only non-pure vectors.
- Σ_± (c_j/2) π_j^± π_j^{±†} = c_j [[ε x_j x_j†, 0],[0, y_j y_j†]] (cross blocks cancel). Total (εX, 0; 0, I₂₀). Correct.
- X ≠ 0 since x_j ≠ 0 and c_j > 0, so λ_max(X) > 0, ε = 1/(2λ), I₂ − εX ⪰ ½I₂ ≻ 0. Completion by (u_k; 0) with y = 0: admissible trivially. Sum = I₂₂. Correct.
- Every element has x-part ≠ 0, hence p > 0 because Q ≻ 0. No null outcome. Lemma 1 gives G_c = 0 per element for every c, and c^T(F^Q − F^C)c = Σ G_c = 0 for all c ⇒ F^C = F^Q **as matrices**. Correct.
- Condition on the C² part: the only conditions used are Q ≻ 0 on C² (so x ≠ 0 ⇒ p > 0, and √Q invertible in Lemma 1) and that the support block of every L_i is zero (built into the model; the kernel-kernel block of the SLD is arbitrary in general but drops out because ρ^{1/2} kills it). Both hold for A0. No missed condition.
- Rational version: LDL form R₂ = (1/a) v v† + diag(0, d − |b|²/a) with v = (a; b̄) checked: (1/a)vv† = [[a, b],[b̄, |b|²/a]]. Correct. Rational s with s² ≤ ε keeps s²X ⪯ ½I₂. Correct.

No gap.

---

## 4. Matrix vs scalar saturation — HOLDS, with one unstated hypothesis

Checked: PHASE3 §1 "Saturation: F^C(M) = F^Q as real symmetric matrices on S"; §5 last line; CONVENTION §4 (H*), §3 T5.

- The text uses the **matrix** equality, all parameters of S jointly. Theorem A uses c^T(F^Q − F^C)c = 0 for all c; Theorem B proves it for all c. `[TEXT-of-audited-file]` + `[INFERRED]`.
- CONVENTION T5 correctly separates the single-direction scalar (D3), which is always attainable (eigenbasis of L_u), from the matrix statement. `[INFERRED]`: correct and important; D3 cannot discriminate S+ from S−.
- **Unstated hypothesis:** CONVENTION §4 equates SAT(S) with Tr(W F^{-1}) = Tr(W (F^Q)^{-1}) for W ≻ 0. This needs F^Q (12×12) invertible. The criterion itself (Fisher-matrix equality) does not, but any phrasing as "QCRB attained", i.e. covariance = (F^Q)^{-1}, does. Neither file states that F^Q_{S±} is nonsingular or gives its smallest eigenvalue. Repair: report λ_min(F^Q_{S+}), λ_min(F^Q_{S−}) (exact over Q for the integer instance). `[UNKNOWN]` whether it holds; generically yes (Gram matrix of 12 vectors in a real 80-dim space).

---

## 5. Hypotheses of the cited theorems — CANNOT-CHECK

No web tool was available, so none of arXiv:1806.07337, 2402.11567, 2601.21801 was opened. I give no quotes and no equation numbers: anything I wrote would be from memory, and the rules forbid that.

What can be said without the sources:
- **Attribution discrepancy.** The audit prompt calls 1806.07337 "Yang–Pezzè–Zhou–Jing". PHASE3 §11 and CONVENTION §6 call it "Yang, Pang, Zhou, Jordan" (PRA 100, 032104, 2019). My recollection agrees with the files (Jing Yang, Shengshi Pang, Yiyu Zhou, Andrew N. Jordan) `[MEMORY, LOW]`. The prompt's paraphrase is the likely error. Check it against the arXiv abstract page before anything is sent out.
- **Internal consistency of the authors' quotes** `[INFERRED]`. The regular-outcome condition the files attribute to YPZJ (Π_k L_i|ψ_n⟩ = ξ_i Π_k|ψ_n⟩, ξ real, independent of the support eigenvector n), specialised to a rank-one Π_k = ππ† with π = (x; y), reads conj(A_i† y)_n = ξ_i conj(x_n) for n = 1, 2, i.e. A_i† y = ξ_i x with ξ_i real. That is exactly Lemma 1's admissibility. So if the quote is accurate, Lemma 1 agrees with it. Whether the quote is accurate is `[UNKNOWN]`.
- **Hypotheses for this model** `[INFERRED]`: ρ is rank-deficient (rank 2 of 22). At first order the data are compatible with constant rank (CONVENTION F_U), so a constant-rank hypothesis like the one attributed to Nurdin is satisfiable by a choice of family, but A0 itself does not fix a family. The QFIM is singular only if F^Q_S is (item 4, unknown). The support is parameter-dependent at first order (the L_i rotate support into kernel), so any cited theorem that assumes a fixed support would not apply. I cannot say which, if any, of the three theorems assumes that.
- The files themselves say the null-outcome conventions of YPZJ and of YIP were not read in full (`[UNKNOWN]` in CONVENTION §6, "[INFERRED], full text not read" in PHASE3 §11). This audit does not change that status.

Note: Theorems A and B as proved in PHASE3 do not depend on any cited theorem; they are self-contained (items 1–3). The literature matters for novelty and for the convention cross-walk, not for validity.

---

## 6. Counterexample search — CANNOT-CHECK numerically; hand controls agree

No Python was run (no shell tool). Instead, four small models solved in closed form `[INFERRED]`, each compared against an independent known criterion:

| Control | Model | Criterion says | Independent check | Agree |
|---|---|---|---|---|
| C1 | any single parameter, any Q ≻ 0 | every y admissible (take x = A†y) ⇒ I in cone ⇒ saturable | Braunstein–Caves: one parameter always attainable | yes |
| C2 | pure support C¹ ⊕ C¹, A₁ = 1, A₂ = i (L₁ = σ_x, L₂ = σ_y on \|0⟩) | y = λ₁x, −iy = λ₂x with real λ ⇒ y = 0 ⇒ not saturable | Matsumoto: Im⟨0\|L₁L₂\|0⟩ = 1 ≠ 0 ⇒ not saturable | yes |
| C3 | pure support C¹, general A_i ∈ C^{m×1} | saturable ⟺ B†B real (B = [A₁…A_k]): if real, I = P_{V⊥} + B G⁺ B† with real eigenvectors of G = B†B gives admissible y = B c; the converse follows from the identity below | Matsumoto (pure states: iff Im⟨ψ\|L_iL_j\|ψ⟩ = 0) | yes, both directions |
| C4 | support C² (Q ≻ 0), kernel C¹, A₁† y = (y, 0), A₂† y = (0, y) | y must be ∝ both (1,0) and (0,1) ⇒ 𝒴_S = {0} ⇒ not saturable | Tr(ρ[L₁,L₂]) = 0 here (weak commutativity holds), but the support block of [L₁,L₂] is [[0,1],[−1,0]] ≠ 0 (partial commutativity fails) ⇒ not single-copy saturable | yes, and it shows the criterion is strictly stronger than weak commutativity, as it must be |

**New exact necessary condition derived from the criterion** `[INFERRED]`: if I₂₀ = Σ_j c_j y_j y_j† with A_i† y_j = λ_ij x_j (λ real), then

    A_a† A_b = Σ_j c_j (A_a† y_j)(A_b† y_j)† = Σ_j c_j λ_aj λ_bj x_j x_j†,

which is Hermitian. So **saturability of S implies A_a†A_b = A_b†A_a (equivalently P[L_a, L_b]P = 0, P the support projector) for every pair a, b ∈ S.** This is the partial-commutativity condition the files attribute to YPZJ, and it falls out of the criterion in one line, an independent consistency check of the whole reduction.

Why it matters for the downstream claim: PHASE3 §1 says the instance entries are "integer Gaussian entries times −2i". If the A_i are (−2i)·(real integer matrix G_i), then A_a†A_b = 4 G_a^T G_b, and Hermiticity reduces to G_a^T G_b symmetric: one integer equation per pair, which random integer G fail generically. Two consequences, both cheap and exact:
1. If some pair in S+ violates it, S+ is **not** saturable, contradicting the §8 numerical POVM (which would then have to be a numerical artefact). This is a direct falsification test of the S+ claim.
2. If some pair in S− violates it, S− non-saturability has a **one-line exact proof** in integer arithmetic, and the computer-assisted Lipschitz certificate of §9 becomes unnecessary.
3. If all pairs in S+ ∪ S− pass, the instance is structured (not "generic random"), and that structure should be stated.

I could not run this check (no shell, and the instance file is outside the permitted reading set). It is the single most informative next computation: exact, integer, a few seconds.

No counterexample to the equivalence was found, and given that items 1–3 hold step by step, none should exist under P-reg. Numerical search was not performed.

---

## CONVENTION_RESOLUTION T4 ("same saturable class under the other convention") — GAP, repairable

Checked: CONVENTION §3 T2, T4 and §7 residual risk 2.

- T4 (ii) is stated "for a family with A1" (any constant-rank family), but the per-null-outcome limit Ψ_h(N_E) = (N_E h)(N_E h)^T/(h^T N_E h) (T2) is proved only for the specific family F_U; §7 item 2 admits this. As written, (ii)⇒(iii) for a general constant-rank family rests on an unproved step. **This is a gap.**
- **Repair (verified by hand, `[INFERRED]`):** for any smooth family of constant rank 2 with ρ_θ = [[P_θ, C_θ],[C_θ†, D_θ]] in the fixed C² ⊕ C²⁰ split and P_θ ≻ 0 near θ₀, rank 2 forces D_θ = C_θ† P_θ^{-1} C_θ exactly (Schur complement zero). With C_θ = ½ Q A_θ† + O(|θ|²) (first-order data) and P_θ = Q + O(|θ|), this gives y†D_θ y = ¼|√Q A_θ† y|² + O(|θ|³) = ¼ θ^T N_E θ + O(|θ|³) and ∇p = ½ N_E θ + O(|θ|²), which gives the same limit as F_U. So T2, and with it T4, extends to every constant-rank family. Add this paragraph and the gap closes.
- I also re-derived T2's F_U expansion: for null w = (0; y), w†[X,[X,ρ]]w = 2(Xw)†ρ(Xw) (using X† = −X, ρw = 0), so p = (B_θ† y)† Q (B_θ† y) = ¼ θ^T N_E θ. Correct.
- Rest of (ii)⇒(iii): a PSD sum of rank ≤ 1 terms with a common one-dimensional range forces each term into that range, and N_{y} rank ≤ 1 ⟺ all √Q A_i† y are real multiples of one vector ⟺ y ∈ Y_S(v). Correct.
- **Scope, not softened:** "the set of attainable S is the same under the other convention" holds only for D2 with a constant-rank family and a direction h with h^T N_E h > 0 for every non-pure null element. For rank-increasing families (T3) D2 is not a function of the A0 data, and nothing is claimed. The files say this; any summary that drops "constant rank" overclaims.

---

## What this audit does NOT establish

- It does not verify that S+ is saturable or that S− is not; only the reduction (criterion) was audited. §§8–9 numerics were not examined.
- It does not verify any literature quote or the novelty statement (item 5).
- It is a same-model, isolated-context review (weak–medium independence on the verification ladder). Hand derivations are not code-checked.

## Files

- This report: `E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments\20261028-h-cat56-2-phase4\E_AUDIT_REDUCTION_BLIND.md`
- No scratch scripts were created (no execution tool available).
