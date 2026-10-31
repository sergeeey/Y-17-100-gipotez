# Novelty matrix for H-CAT56-2 (revised 2026-11-01)

Format per row: OUR CLAIM → PRIOR WORK → EXACT DIFFERENCE → SOURCE → CONFIDENCE.

## Sources, and how far each was read

- **[S1]** Yang, Pang, Zhou, Jordan, arXiv:1806.07337v3, "Optimal measurements for quantum multiparameter estimation with general states". **Abstract and a Lemma 3 excerpt read** (saturation of the matrix CFIM bound by a regular projector iff a condition on ∂p, ψ, π). Full text not read.
- **[S2]** Nurdin, arXiv:2402.11567v5, "Saturability of the Quantum Cramér-Rao Bound in Multiparameter Quantum Estimation at the Single-Copy Level". **Abstract read.** The composite criterion (rank 399 for 16 generators; 264 < 399 for S₋) was read in an earlier pass.
- **[S3]** Suzuki, Yang, Hayashi, arXiv:1911.02790v3, "Quantum state estimation with nuisance parameters". **Full HTML text fetched and the relevant sections read:** §4.1 (single-copy commuting-SLD attainability), §4.3 (SLD tangent space), and the section whose arXiv ID is 5.4 (text numbering 4.4), which defines *D-invariance* and *asymptotic classicality* for the parameters of interest with nuisance parameters, with Lemmas 4.3–4.4 and equations (102)–(104). The authors state that the results of that subsection "are not reported in literature" (their claim, not verified by us).
- **[S4]** Nurdin, "Corrections to 'Saturability of the Quantum Cramér-Rao Bound…'", IEEE Control Systems Letters, DOI 10.1109/LCSYS.2024.3451468. **DOI resolves to the title (OpenAlex W4401990536). Content not accessible** in this environment and not in the arXiv store. Every statement that depends on what the correction changed is **UNKNOWN**.
- **[S5] WITHDRAWN — NOT USABLE.** Nurdin, arXiv:2405.01471, "Saturation of the Multiparameter Quantum Cramér-Rao Bound at the Single-Copy Level with Projective Measurements". The arXiv page (read 2026-11-01) shows v2 of 22 Dec 2024 as withdrawn: "irreparable error in Lemma 2 in Section 4 that also renders Corollaries 2 and 3 and Theorem 3 in that section incorrect"; the examples of Section 3 are said to remain valid; the comment points to the correction DOI 10.1109/LCSYS.2024.3451468. An earlier version of this matrix cited its abstract as a live source; that was an error (the abstract text on the arXiv listing does not carry the withdrawal). Its claims are **not used** anywhere below.

Nothing here is a full literature search. Priority claims are therefore not made.

**Relevant structural fact about our model.** The state ρ = diag(1/3, 2/3) ⊕ 0 on C²² is **not full rank**. The commuting-SLD sufficient route in [S3] §4.1 is stated for strictly positive ρ and does not apply directly. The non-full-rank single-copy setting is the one treated by [S2] ([S5] is withdrawn).

---

## Row 1 — Existence of a saturating single-copy POVM on S₊ = {0,…,11}

- **OUR CLAIM.** For the fixed rank-2 instance A0 (d=22, r=2, s=16), a finite POVM of 1764 rank-one regular elements saturates the 12×12 QFIM at θ=0 on S₊, certified by exact rational and integer arithmetic (484 equalities, 280 positive definite blocks).
- **PRIOR WORK.** [S1] Lemma 3: saturation of the matrix bound by a regular projector. [S2]: necessary and sufficient single-copy conditions (projected SLD commutativity plus a PDE system) for non-full-rank states. ([S5] is withdrawn and is not used.) [S3] §4.1: commuting SLDs give attainability for strictly positive ρ.
- **EXACT DIFFERENCE.** We do not use these as a general theorem. We construct and verify an explicit instance certificate. **We did not check whether the instance satisfies the conditions of [S2]** (and [S5] is withdrawn), so we cannot say whether the existence follows from them. Our POVM is rank-one and not claimed to be projective.
- **SOURCE.** `S_PLUS_CERTIFICATE_FINAL_v2.md` §1–§4; [S1] Lemma 3 excerpt; [S2] abstract; [S3] §4.1.
- **CONFIDENCE.** Medium on the instance result (exact verification; Codex audit of the S+ chain: PASS WITH CONDITIONS). **Low on novelty:** the criteria are known, and the check against them is not done. Status for novelty: **UNKNOWN**.

## Row 2 — Impossibility of saturation for S₋ = {4,…,15} (uniform trace gap for F_U)

- **OUR CLAIM.** For the F_U family and all finite and Borel POVMs, tr(F^Q − F_E) ≥ c uniformly for |θ| ≤ s₁, D1 convention, given the separator with γ ≥ 0.0304.
- **PRIOR WORK.** [S2] composite criterion (rank counting) is a sufficient condition; 264 < 399 means the criterion does not apply to S₋. [S3] §5.4 (D-invariance; Holevo bound with nuisance parameters equal to the RLD bound, Lemma 4.3): a characterisation of when the parameters of interest are "classical". ([S5] is withdrawn and is not used.)
- **EXACT DIFFERENCE.** Failure of a sufficient condition is not a no-go, so the criterion count does not establish impossibility. Our statement is a quantitative trace gap for the instance family. **Checked 2026-11-01 (`novelty_checks/partial_commutativity_check.py`):** at θ=0 the SLDs are L_a = [[0, A_aᴴ],[A_a, L_kk]], so P[L_a,L_b]P = A_aᴴA_b − A_bᴴA_a. This is **exactly zero for all 66 pairs in S₊, all 66 pairs in S₋ and all 120 pairs of the 16 blocks** (integer matrices; maximum defect 0.0). The single-copy necessary condition of partial commutativity therefore does **not** exclude S₋, and the weak commutativity tr(ρ[L_a,L_b]) = 0 holds as well. D-invariance proper (eq. 102) needs the commutation operator, which is not uniquely defined for the rank-deficient state ρ = diag(1/3,2/3) ⊕ 0; it was **not** tested.
- **SOURCE.** `THEOREM_NATURAL_D2_NOGO_v8.md`; `O3_V3_INDEPENDENT_AUDIT.md`; [S2], [S3] §5.4.
- **CONFIDENCE.** Medium on the reduction; the separator is audited (CONDITIONAL). **Novelty NOT ESTABLISHED.**

## Row 3 — Subset dependence: S₊ saturable, S₋ not, for the same model

- **OUR CLAIM (central).** Whether the SLD-QCRB is reachable depends on which parameter subset is treated as the parameters of interest; shown on one fixed model, positive on S₊, no-go on S₋.
- **PRIOR WORK.** [S3] §5.4 is exactly this setting: parameters of interest versus nuisance parameters, with the attainability criteria D-invariance (eq. 102) and asymptotic classicality (eqs. 103–104) expressed through *effective* SLDs for the chosen subset. The authors claim these results are new in 2019. [S2] works with projected SLDs, which depend on the subset.
- **EXACT DIFFERENCE.** Our instance is a case of [S3]'s framework. The difference we can state is the explicit instance pair and the quantitative gap. We have **not** checked whether S₊ and S₋ satisfy D-invariance or asymptotic classicality, so we cannot say our contrast is new relative to [S3]'s conditions. We do not claim the phenomenon is new.
- **SOURCE.** Rows 1–2; [S2] abstract; [S3] §5.4 and Lemmas 4.3–4.4.
- **CHECK RESULT (2026-11-01).** Since all SLDs weakly commute at θ=0 (tr(ρ[L_a,L_b]) = 0 for every pair, independent of the arbitrary block L_kk), both S₊ and S₋ satisfy the *weak-commutativity equation* of [S3] eq. (104) at θ=0 (no nuisance parameters, so the effective SLDs are the SLDs themselves). *Correction 2026-11-01 (OB-1, register diff U03):* this checks the equation only. That [S3] Lemma 4.4 then gives "Holevo bound = SLD-CR bound" for these subsets is **not verified**, because [S3]'s definitions are written for general states and their applicability to the rank-deficient ρ₀ was not checked (OB-8); D-invariance (eq. 102) was not checked either. So the equation of [S3] eq. (104) and partial commutativity do **not** separate S₊ from S₋, but the full set of [S3] §5.4 conditions has not been tested. The contrast is therefore *probably* a **single-copy** effect rather than an asymptotic or collective-measurement effect (CONDITIONAL on OB-8). This is consistent with [S2], whose single-copy conditions are stronger than partial commutativity.
- **CONFIDENCE.** **PARTIAL** (instance contrast supported). The statement that subset dependence is not new stands for the general framework of [S3]. What the check adds: the pair is **not explained by partial commutativity or by the weak-commutativity equation of [S3] eq. (104)** (Lemma 4.4 and D-invariance are unchecked, OB-8), so a prior result covering it would plausibly come from the single-copy theory of [S2] (and [S4], whose text is unread and whose content is UNKNOWN). Whether [S2]'s conditions (1) and (2′) decide S₋ is **not checked**. **Novelty of the subset dependence: NOT ESTABLISHED. Novelty of an example that separates single-copy from asymptotic attainability inside one rank-deficient model: UNKNOWN, no prior example located.** All of this is at the single point θ=0.

## Row 4 — D2 directional limit: existence along rays, failure along general curves

- **OUR CLAIM.** For a finite POVM, the D2 limit of the CFIM exists along each fixed ray; along general curves only limsup is guaranteed, because outcome-wise null limits depend on the direction.
- **PRIOR WORK.** Not located in [S1]–[S5]. Classical Fisher information with vanishing probabilities is standard; no reference checked.
- **EXACT DIFFERENCE.** The ray/curve distinction is our precise statement about this limit.
- **SOURCE.** `PROOF_OBLIGATIONS.md` B15–B16; `THEOREM_NATURAL_D2_NOGO_v8.md`.
- **CONFIDENCE.** PROVED-hand (internal). **Novelty UNKNOWN.**

## Row 5 — Rank-jump counterexample to the naive N₁ limit form

- **OUR CLAIM.** For a general C¹ family with a rank jump, the limit trace is F^Q(0) + 4 tr τ, not F^Q(0); the N₁ limit form and Prop 8 fail for general families (toy counterexample 65.51 vs 61.51).
- **PRIOR WORK.** None checked. [S1] treats regular projectors under a fixed-rank assumption, consistent with the failure but not stating it.
- **EXACT DIFFERENCE.** A local analytic counterexample, not a universal theorem. The factor 4 was checked only with tr τ = 1 in the toy.
- **SOURCE.** `toy_rank_jump/rank_jump_check.out`, `povm8_jump.out`; `THEOREM_NATURAL_D2_NOGO_v8.md`.
- **CONFIDENCE.** High that the counterexample is correct as stated. **Novelty UNKNOWN.**

## Row 6 — Borel transition: sup over partitions equals the integral

- **OUR CLAIM.** For Borel POVMs with θ-independent μ = tr M, the CFIM equals the sup over finite partitions and the integral.
- **PRIOR WORK.** Standard measure-theoretic approximation; [S1] works with discrete measurements.
- **EXACT DIFFERENCE.** None beyond the setting. **Novelty not claimed.**
- **SOURCE.** `ARTICLE_DRAFT_v4_2026-10-31.md`, Prop 7.
- **CONFIDENCE.** PROVED-hand.

## Row 7 — Nurdin composite criterion does not apply to S₋

- **OUR CLAIM.** The composite criterion of [S2] (rank 399 needed for 16 generators) cannot be met for S₋ (264 < 399).
- **PRIOR WORK.** [S2].
- **EXACT DIFFERENCE.** An application of [S2] to one instance; the criterion is theirs.
- **SOURCE.** `EVIDENCE_LEDGER.md` rows 23–24.
- **CONFIDENCE.** PROVED-hand (counting). The version used is arXiv v5; [S4] was not read, so any dependence on the correction is **UNKNOWN**.

## Row 8 — Computer-assisted separator certificate

- **OUR CLAIM.** An arb (192-bit) interval certificate bounds the separator over all 3 955 841 cells.
- **PRIOR WORK.** Interval certification of matrix bounds is a general technique; not searched.
- **EXACT DIFFERENCE.** Methodological. **Novelty not claimed.**
- **SOURCE.** `o3_v3/`; `O3_V3_INDEPENDENT_AUDIT.md`.
- **CONFIDENCE.** VERIFIED-INTERVAL (internal; Codex CONDITIONAL, defects closed in `ERRATA_STAGE_C_FINAL_PROOF.md`).

---

## Strongest novelty statement the evidence supports

For one specific rank-2 model with 16 blocks (instance A0, d=22, r=2, s=16) we give:

1. an exact-arithmetic certificate that a 1764-element rank-one regular POVM saturates the QFIM at θ=0 on S₊ (Row 1);
2. a computer-assisted separator bound, from which a uniform trace-gap no-go follows for S₋ on the F_U family, under the stated conventions (Row 2);
3. explicit local counterexamples showing that the naive limit form of the trace bound is false for general C¹ families with rank jumps (Row 5).

**What we cannot claim:**
- that subset dependence is new: [S3] §5.4 is the same setting, and of its conditions only the equation (104) was tested against S₊ and S₋; D-invariance and Lemma 4.4 on a rank-deficient state were not (Row 3);
- that the criteria of [S1], [S2] (and its correction [S4], unread) do not already cover the instance (Row 1);
- that any result is first (no priority search);
- anything that depends on [S4], which is not accessible.

**Verdict: PARTIAL.** The instance-level results are supported. The central subset-dependence claim is NOT ESTABLISHED as new.

## Readiness for a conversation with Prof. Nurdin

**FIX FIRST.** Before sending anything: (a) obtain [S4] in full; (b) [partial commutativity and the weak-commutativity equation (104) of S₊ and S₋ were tested on 2026-11-01: both hold exactly for both subsets, so they do not separate them; asymptotic classicality as a consequence (Lemma 4.4), its applicability to the rank-deficient state, and D-invariance remain untested, OB-8]; (c) check the conditions of [S2] (and its correction [S4]) on the instance; [S5] is withdrawn; (d) keep `review_package/DRAFT_TO_NURDIN.md` unsent until (a)–(c) are done.
