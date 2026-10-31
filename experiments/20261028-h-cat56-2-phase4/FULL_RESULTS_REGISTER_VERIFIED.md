# H-CAT56-2: independent verified results register (2026-11-01)

**Status of the source register.** `H-CAT56-2_FULL_RESULTS_REGISTER_2026-11-01.md` (ChatGPT draft) was **not found** on this machine (searched: the repository, Downloads, Desktop, Documents, D:, the Obsidian vault) and its text was not supplied. Every item of that document is therefore **BLOCKED**. This register is built from primary evidence only, and cannot claim item-by-item coverage of the missing document. When the file is supplied, it must be diffed against this register (open obligation OB-1).

**History of changes.**
- v0: ChatGPT register — unavailable, BLOCKED.
- v1 (this file): independent register from primary sources. Corrections to earlier project texts found while building it are listed in `FULL_RESULTS_AUDIT.md` §5.

## Conventions

Verdicts: **VERIFIED** (confirmed by my own execution, derivation or reading of primary output), **CONDITIONAL** (internal proof or certificate whose basis I did not independently re-derive, or which depends on an unread/unchecked premise), **REFUTED** (a claim shown false), **UNKNOWN** (no basis either way). Model agreement alone (Claude, Codex) never raises a status.

How I checked (in LIMITATIONS): `exec` = I ran it in this audit; `read` = I read the primary output but did not re-execute; `derive` = I derived it by hand; `cite` = taken from a project document.

Evidence class (CLASS): **M** math proof (internal), **X** exact computational certificate, **N** numerical experiment, **I** internal/cross-model audit, **D** definition or data, **L** literature, **P** process. **External expert review: none exists.**

Paths are relative to `experiments/20261028-h-cat56-2-phase4/` unless stated. `DISC` = `experiments/20261027-h-cat56-2-discovery/`.

Notation: S₊ = {0..11}, S₋ = {4..15} (blocks of the 16), other parameters known and fixed at 0. ∣θ∣ is the Euclidean norm.

## A. Model, definitions, exact identities

| ID | CLAIM | SOURCE | PROOF / TEST | LIMITATIONS | CLASS | VERDICT |
|---|---|---|---|---|---|---|
| A1 | Model ρ_θ = U_θρ₀U_θᴴ, ρ₀ = Q⊕0, Q = diag(1/3,2/3) on C²² = C²⊕C²⁰; 16 integer blocks A_a ∈ C^{20×2}, A_a = −2iB_a; instance SHA-256 05289920…0044 | `THEOREM_NATURAL_D2_NOGO_v8.md` §0; `DISC/code/s8_admissible_span.py:35–43`; `o3_v3/metrics/run_manifest_runD.json` | exec: loader returns 16 blocks of shape (20,2) (`novelty_checks/partial_commutativity_check.out:1`); SHA equal in 4 manifests | convention C2 is an owner-accepted assumption; the exact form of U_θ was not re-read | D | VERIFIED |
| A2 | At θ=0 an SLD is L_a = [[0, A_aᴴ],[A_a, L_kk]] with L_kk arbitrary | `checks/fu_normalization_and_Y_2026-10-31.out:17`; `novelty_checks/partial_commutativity_check.py:1–10` | derive: ρL+Lρ = [[0,QAᴴ],[AQ,0]] gives QL₁₁+L₁₁Q = 0 ⇒ L₁₁ = 0, L₁₂ = Aᴴ, L₂₁ = A; exec: finite-difference residual 4.4·10⁻⁷ | needs ∂ρ(0) = ½[[0,QAᴴ],[AQ,0]] (C2) | M | VERIFIED |
| A3 | F^Q(0)_ab = Re tr(Q A_aᴴ A_b) | A2 | derive: tr(ρL_aL_b) = tr(Q·(L_aL_b)_ss) = tr(Q A_aᴴA_b) | none beyond A2 | M | VERIFIED |
| A4 | For a complete POVM Σ N_k = F^Q; a zero-probability outcome can have N_k ≠ 0 (kernel-outcome trace 60005.33) | `checks/fu_normalization_and_Y_2026-10-31.out:20–24` | exec by project: ΣN−F^Q ≤ 7.3·10⁻¹², relative 1.6·10⁻¹⁵; read | numeric; the identity is also elementary | M+N | VERIFIED |
| A5 | The real-linear map Φ_x (36×40) encodes exactly Y_S(x) = {y : A_aᴴy ∈ ℝx, a ∈ S}; the 40×40 form H = [[A,−B],[B,A]] gives yᴴRy = [Re y; Im y]ᵀ H [Re y; Im y] | `DISC/code/s8_admissible_span.py:46–58`; `o3_v3/code/interval_cells_v3.py:82–107` | derive: rows Re(g₁·y), Im(g₁·y), Im(g₃·y) with g₁ = x₀a₁−x₁a₀, g₃ = x̄₀a₀+x̄₁a₁; exec: real-form error 1.8·10⁻¹⁵, kernel residual 3.6·10⁻¹⁴ | none | M+N | VERIFIED |
| A6 | Y_S(e^{iα}x) = e^{iα}Y_S(x), so x = (cos(θ/2), sin(θ/2)e^{iφ}) suffices for sup of a phase-invariant quantity | `o3_v3/code/interval_cells_v3.py:155` | derive | none | M | VERIFIED |

## B. S₊: existence of a saturating POVM

| ID | CLAIM | SOURCE | PROOF / TEST | LIMITATIONS | CLASS | VERDICT |
|---|---|---|---|---|---|---|
| B1 | Theorem S₊: from exact moments M_j ≻ 0 with A·M = b there is a finite POVM of 1764 rank-one regular elements (Σ E = I₂₂, Tr ρE > 0 at θ=0) whose 12×12 CFIM equals the QFIM | `stage_e_v1/THEOREM_S_PLUS_EXISTENCE_v6.md` §2–4; `S_PLUS_CERTIFICATE_FINAL_v2.md` §1 | read statement; Codex S₊ audit PASS WITH CONDITIONS (`review_package/codex_logs/splus_codex_audit_2026-10-31.txt`) | Lemma D and the lift were not re-derived by me | M+I | CONDITIONAL |
| B2 | 484 coordinate equalities A·M* = b hold exactly in ℚ; G_I invertible; all 280 blocks positive definite | `stage_e_v1/logs/exact_cert_result.json` | read: rows_violated_exactly 0, independent_rows 175, all_M_positive_definite_exact true | not re-executed (11 387 s); shares inputs with B3 | X | VERIFIED |
| B3 | Same equalities hold exactly over ℤ with A rebuilt from the lift definition; 280 blocks PD | `stage_e_v1/logs/verify_exact_integer_v3.json` | read: rows_checked 484, blocks_checked_PD 280, columns 6566, violated 0 | y loaded from a checkpoint, not recomputed; not re-executed (4 839 s) | X | VERIFIED |
| B4 | Counting is consistent: 280 blocks of sizes 7 and 5 give 1764 outcomes and 6566 columns; 484 = 22² | B2, B3 | exec arithmetic: 182·7+98·5 = 1764; 182·28+98·15 = 6566 | the 182/98 split is solved from the two totals; the second total is an independent check | X | VERIFIED |
| B5 | Inputs are shared between the two runs (bases `exact_bases2.pkl`, start moments, row list); y recomputed in run A, only loaded in run B; no independent regeneration | `S_PLUS_CERTIFICATE_FINAL_v2.md` §4 | read | the stated grid's validity depends on these inputs | I | CONDITIONAL |
| B6 | CFIM = QFIM at θ=0 for that POVM, via YPZJ thm:reg (saturation ⇔ A_aᴴy = ξ_a x, ξ real) | `stage_e_v1/logs/control_differential.json` | read: relative trace deficit 2.4·10⁻¹², matrix error 1.5·10⁻¹⁰, completeness 1.8·10⁻¹¹ | external theorem not checked by Codex or by me against its primary proof; numeric control is float | M+N | CONDITIONAL |
| B7 | An explicit exact (rational) POVM is written out | `S_PLUS_CERTIFICATE_FINAL_v2.md` §5–6 | not done | irrational ĉ from Cholesky; not needed for existence | X | UNKNOWN |

## C. S₋: no-go for the matrix CFIM

| ID | CLAIM | SOURCE | PROOF / TEST | LIMITATIONS | CLASS | VERDICT |
|---|---|---|---|---|---|---|
| C1 | Theorem N (family F_U): ∃ c, s₁ > 0 ∀ finite complete POVM ∀ h ∀ ∣θ∣ ≤ s₁: tr(F^Q(θ) − F_E(θ)) ≥ c, convention D1 (outcomes with p_k = 0 contribute 0) | `THEOREM_NATURAL_D2_NOGO_v8.md` §2; `PROOF_RECONSTRUCTION_THEOREM_N_2026-10-31.md` | read quantifier; Codex skeptic corrections applied | Riesz, Łojasiewicz and Lemma 6 steps not re-derived by me; c, s₁ implicit (non-effective); needs C7 | M+I | CONDITIONAL |
| C2 | Corollary N₁: for Borel POVM M, tr F^C_M(θ) ≤ tr F^Q(θ) − c for ∣θ∣ ≤ s₁ | `THEOREM_NATURAL_D2_NOGO_v8.md` §2 | read | depends on C1, C3 | M | CONDITIONAL |
| C3 | Proposition 7: for θ-independent μ = tr M, F^C_M = ∫ ∇m∇mᵀ/m dμ (net of finite partitions = integral) | `THEOREM_NATURAL_D2_NOGO_v8.md` §2 | read | proof chain (density of simple functions, orthogonal projection) not re-derived | M | CONDITIONAL |
| C4 | Refinement monotonicity: G ⊂ G′ ⇒ F_G ⪯ F_G′ | `THEOREM_NATURAL_D2_NOGO_v8.md` (Lemma 1′) | derive: Cauchy–Schwarz (Titu): (Σg)ᵀ(Σg)/Σp ≤ Σ ggᵀ/p | none | M | VERIFIED |
| C5 | D2 trace bound along each fixed ray: limit trace ≤ tr F^Q(0) − c | `review_package/PROOF_OBLIGATIONS.md` B15 | read | follows from C1 | M | CONDITIONAL |
| C6 | The D2 limit exists along arbitrary curves θ(t) → 0 | earlier drafts | refuted by the project: outcome-wise null limits depend on direction; only limsup holds (PROOF_OBLIGATIONS B15) | counterexample not re-derived by me | M | REFUTED |
| C7 | Separator R with γ > 0: sup over unit y ∈ 𝒴 of Re(yᴴRy) ≤ s* — see E7 | E-series | E-series | E-series | X | CONDITIONAL |
| C8 | 𝒴 = ∪ₓ Y_S(x) exactly, via the real-line argument with Q^{1/2} | `review_package/EVIDENCE_LEDGER.md` row 8; `checks/fu_normalization_and_Y_2026-10-31.out:32–33` | read: rank 1 on 120 vectors, generic y rank 4 on 200 | "forward inclusion numerical; converse analytic" (ledger); converse not re-derived | M+N | CONDITIONAL |
| C9 | Riesz bound f_θ ≥ f₀ − ω(∣θ∣), ω → 0 under continuity of ∂ρ at 0 | `PROOF_RECONSTRUCTION…` §2–5 | read | not re-derived | M | CONDITIONAL |
| C10 | Łojasiewicz inequality on the semialgebraic f₀ = λ₂(N_v(0)) | `THEOREM_NATURAL_D2_NOGO_v8.md` §4 | read; reference Bochnak–Coste–Roy §2.6 at section level | corollary number not used; constants non-effective | M | CONDITIONAL |
| C11 | Lemma 6: γ ≤ 22C₁C₀[(tr Δ)^{θ₀} + ω^{θ₀}] | `review_package/PROOF_OBLIGATIONS.md` B-series | read | not re-derived | M | CONDITIONAL |
| C12 | Proposition 8: for F_U the directional quadratic form hᵀF_E(th)h → hᵀF^Q(0)h is saturable (E₀ = I₂⊕0, E_k = 0⊕e_ke_kᴴ). So the no-go is **specific to the matrix (and trace) CFIM** | `THEOREM_NATURAL_D2_NOGO_v8.md` §3 | read | proved by hand for F_U only | M | CONDITIONAL |
| C13 | Theorem N for general C¹ families (modulus ω): holds under conditions 1–3 and a separator R* with γ > 0 | `THEOREM_NATURAL_D2_NOGO_v8.md` §0, §4 | read | no separator exists for other families | M | CONDITIONAL |
| C14 | Limit form N₁ for general C¹ families with a rank jump | `toy_rank_jump/rank_jump_check.out:3–4`; `povm8_jump.out:6` | exec by project: tr F^Q(s) = 65.5134 vs tr F^Q(0) = 61.5137 at s = 0.001 (jump 3.9997 for tr τ = 1) | toy 5×3 synthetic; factor 4 checked only for tr τ = 1 | N | REFUTED |
| C15 | Proposition 8 for general C¹ families | `toy_rank_jump/povm8_jump.out:6` | exec by project: hᵀF_E h = 16.3991 vs hᵀF^Q(0)h = 12.3991 | same toy | N | REFUTED |
| C16 | Without continuity of ∂ρ at 0 the uniform statement fails | `THEOREM_NATURAL_D2_NOGO_v8.md` §0 (explicit φ(θ)) | read | construction not re-derived; minimality of the condition not established | M | CONDITIONAL |

## D. Structure of S₊ and S₋ (new in this milestone window)

| ID | CLAIM | SOURCE | PROOF / TEST | LIMITATIONS | CLASS | VERDICT |
|---|---|---|---|---|---|---|
| D1 | P[L_a,L_b]P = A_aᴴA_b − A_bᴴA_a = 0 for every pair: 66 in S₊, 66 in S₋, 120 in all 16 | `novelty_checks/partial_commutativity_check.out:2–4` | exec: defect 0.0 (integer data); an independent reviewer re-derived the formula and ran a control (random A gives 23.1) | θ = 0 only | M+N | VERIFIED |
| D2 | tr(ρ[L_a,L_b]) = 0 for every pair (independent of L_kk) | same | exec | θ = 0; the consequence "Holevo bound = SLD-CR bound" (Suzuki Lemma 4.4) is D6 | M+N | VERIFIED |
| D3 | The composite generators i(A_i σ A_jᴴ − A_j σ A_iᴴ) (σ ∈ {1,X,Y,Z}) have numerical rank 261 (S₊, 264 rows), 264 (S₋, 264 rows), 399 (all 16, 480 rows); 399 = dim of traceless Hermitian 20×20; max trace 0 | `novelty_checks/composite_rank_check.out` | exec (SVD, tolerance 10⁻⁹σ₁) | numerical rank | N | VERIFIED |
| D4 | Rank 399 means Nurdin's composite criterion excludes a kernel POVM for the full 16-parameter model | `review_package/EVIDENCE_LEDGER.md` rows 23–24 | read | criterion taken from arXiv v5; corrigendum unread; not re-derived | M | CONDITIONAL |
| D5 | For S₊ and S₋ the rank is below 399, so that sufficient exclusion condition does not apply; it neither proves nor refutes either subset | D3, D4 | derive from D3 | depends on the criterion text (D4) | M | CONDITIONAL |
| D6 | Both subsets are asymptotically classical at θ = 0 in the sense of Suzuki–Yang–Hayashi eq. (104) | D2; `arXiv:1911.02790` §5.4, Lemma 4.4 | read the lemma | their definitions are written for general states; applicability to a rank-deficient state not checked | L+M | CONDITIONAL |
| D7 | The S₊ / S₋ contrast is therefore a single-copy effect, not explained by partial commutativity or by asymptotic classicality | B-series, C-series, D1, D2, D6 | derive | inherits the conditions of B1, B5, C1, C7, D6 | M | CONDITIONAL |

## E. O3 v3 interval certificate (separator)

| ID | CLAIM | SOURCE | PROOF / TEST | LIMITATIONS | CLASS | VERDICT |
|---|---|---|---|---|---|---|
| E1 | t = Σ Re R_ii = tr H = 0.3040524530826113; s* = fl(fl(0.9t)/20) = 0x1.c057f53368882p−7 = 0.01368236038871751; γ = tr H − 20s* = 0.030405245308261095 ≥ 0.0304 | `o3_v3/code/interval_cells_v3.py:56–59, 110–112`; `o3_v3/audit_tests/check_D1_D4.py` | exec (exact rational sum of the binary64 diagonal) | the exact 9t/200 rounded once is …881, 1.73·10⁻¹⁸ lower | N | VERIFIED |
| E2 | The certified object is the exact Hermitian part H = (R₀+R₀ᴴ)/2; the stored R₀ is Hermitian only to 5.2·10⁻¹⁷ (max imaginary diagonal 1.2·10⁻¹⁷) | `o3_v3/code/interval_cells_v3.py:82–107`; `ERRATA_STAGE_C_FINAL_PROOF.md` E1–E3 | read code; exec | none | N | VERIFIED |
| E3 | Cell lemma: for y ∈ ker Φ_x, x in a cell, yᵀHy/∣y∣² ≤ (λ_K⁺ + 2·mz·ρ + ∥H∥ρ²)/(1−δ) with ρ = κ_K/(1−κ), κ = du·√Σ∥A_j∥², du = hθ/2 + sin(θ_c/2)hφ + 10⁻¹² | `o3_v3/code/interval_cells_v3.py:147–256` | derive: displacement of u via the φ-then-θ path; (I−P)y = −ΣΔu_jA_jy; ∣w∣ ≤ κ_K∣c∣/(1−κ); quadratic expansion; ∣y∣² ≥ (1−δ)∣c∣²; Codex PASS (a)–(g) | not machine-checked | M | VERIFIED |
| E4 | lam_max_upper: Gershgorin rows of V⁻¹BV (arb) bound the largest eigenvalue of symmetric B for any invertible V | `interval_cells_v3.py:120–136` | derive: similarity preserves eigenvalues | a poor seed V can only cause a recorded failure | M | VERIFIED |
| E5 | Every decision (>, <, max, min, sign) is an arb comparison; float is used only to seed eigenvectors/SVD and for reporting | `interval_cells_v3.py:64–71, 117, 163–166, 233` | read (grep of float/max/min) | arb soundness is a library contract (python-flint 0.9.0) | I | VERIFIED |
| E6 | 7 912 chunks, 3 955 841 leaves, runs A 0–1710, B 1711–3420, C 3421–5600, D 5601–7911; no duplicates, gaps or failed leaves | `o3_v3/metrics/audit_run{A,B,C,D}.json`; `o3v3_progress.jsonl` | exec: audit of run D by me; read A–C; arithmetic 1711+1710+2180+2311 = 7912 and 855 500+855 000+1 090 000+1 155 341 = 3 955 841; last chunk 341 | audit script reads records and journal only; no recomputation | N | VERIFIED |
| E7 | For all x, sup over unit y ∈ ker Φ_x of Re(yᴴRy) ≤ s* (the separator over the whole sphere of directions) | E3–E6 | strict v3 run; cross-model audit; sampled checks (E11) | internal; python-flint trusted; no independent full recomputation; bounds ≈ 6× looser than the sampled sup | X+I | CONDITIONAL |
| E8 | Minimum certified slack [8.40e-9 ± 5.2e-12] (run C); maximum B_up [0.01368235198 ± 6.1e-12] | `audit_runC.json` | exec/read | slack is ≈ 6·10⁻⁷ of s* | X | VERIFIED |
| E9 | Tiling: 3 955 841 leaves matched in the tree, 5 274 284 nodes, 0 uncovered cells at depth 10 (accepted by depth sum to 3 955 841) | `metrics/tiling_exact_check.json` | read; exec arithmetic of the depth counts | verifier code not re-read; produced for the v2 leaf file, identical (SHA 29ab7b14…) to the v3 input | X | VERIFIED |
| E10 | Run manifests A–D carry identical SHA-256 for code, R, instance, s8 and leaves, equal to the files on disk | `o3_v3/metrics/run_manifest_run{A,B,C,D}.json` | exec | the driver does not enforce them (E14) | P | VERIFIED |
| E11 | Dense grid (31×61): sup ≈ 0.00212 < s*; 1 000 tightest cells at 5×5 and 9×9 samples: 0 violations, worst ratio 0.159 | `o3_v3/audit_tests/*` | exec | sampled; weak test with no positive control | N | VERIFIED |
| E12 | "R is an exact rational Hermitian matrix; R_sym = R bitwise" (STAGE_C lines 71–73) | `STAGE_C_FINAL_PROOF.md:71–73` | exec: max ∣R−Rᴴ∣ = 5.2·10⁻¹⁷ (also STAGE_C:103) | corrected in the ERRATA | N | REFUTED |
| E13 | "s* = 0.9·tr R/20" as an exact real number | `STAGE_C_FINAL_PROOF.md:74` | exec: differs from the binary64 value by 1.73·10⁻¹⁸ | corrected: s* is the sequential binary64 value | N | REFUTED |
| E14 | The driver records expected input hashes but does not enforce them (C-O3-3) | `o3_v3/code/o3_run_v3.py` | read | open | P | VERIFIED |

## F. Literature and novelty

| ID | CLAIM | SOURCE | PROOF / TEST | LIMITATIONS | CLASS | VERDICT |
|---|---|---|---|---|---|---|
| F1 | Nurdin arXiv:2402.11567: partial commutativity is necessary for single-copy QCRB saturation; its sufficiency was open; the paper gives necessary and sufficient conditions | arXiv abstract | read | full text read only in an earlier pass (composite criterion) | L | VERIFIED |
| F2 | Yang–Pang–Zhou–Jordan arXiv:1806.07337: matrix bound per measurement operator; SLDs must commute on the support for separable or few-copy saturation | arXiv abstract; Lemma 3 excerpt | read | full text not read | L | VERIFIED |
| F3 | Suzuki–Yang–Hayashi arXiv:1911.02790 §5.4: D-invariance (eq. 102), quasi-classical and asymptotically classical models (eqs. 103–104) for parameters of interest, with Lemmas 4.3–4.4; the authors say these results are new | full HTML text | read the section | their claim of novelty is theirs | L | VERIFIED |
| F4 | Suzuki §4.1: commuting SLDs give single-copy attainability for strictly positive ρ | full HTML text | read | our ρ is rank-deficient, so this route does not apply directly | L | VERIFIED |
| F5 | Nurdin arXiv:2405.01471 is withdrawn (v2, 22 Dec 2024): "irreparable error in Lemma 2 in Section 4", Corollaries 2, 3 and Theorem 3 incorrect, Section 3 examples unaffected; points to DOI 10.1109/LCSYS.2024.3451468 | arXiv page, read 2026-11-01 | read | an earlier version of the novelty matrix cited its abstract as live: now corrected | L | VERIFIED |
| F6 | Content of the IEEE CSL correction (DOI 10.1109/LCSYS.2024.3451468) | OpenAlex W4401990536 (title only) | blocked: text not accessible | any statement about its scope (e.g. "separated POVMs") is relayed, not verified | L | UNKNOWN |
| F7 | Whether Nurdin's corrected conditions (1) and (2′) decide S₊ or S₋ | — | not checked | needs F6 | L | UNKNOWN |
| F8 | "Dependence of attainability on the chosen parameter subset is new" | Suzuki §5.4 | derive: the framework of parameters of interest versus fixed or nuisance parameters already contains such dependence | as a claim of novelty, not as a computed fact | L | REFUTED |
| F9 | The explicit pair (equal-size subsets of one rank-deficient model, others fixed; one attainable, one not for the matrix CFIM) is new | `NOVELTY_MATRIX.md` | limited search, no prior example located | no systematic literature search | L | UNKNOWN |
| F10 | The literature (YPZJ) treats zero-probability outcomes through a limit (D2), whereas this project uses D1 | `STAGE_C_FINAL_PROOF.md:104` ([TEXT, partially read]) | not verified here | affects comparability with the literature | L | UNKNOWN |

## G. Preservation and process facts

| ID | CLAIM | SOURCE | PROOF / TEST | LIMITATIONS | CLASS | VERDICT |
|---|---|---|---|---|---|---|
| G1 | Commits f0c6df5ccef9a5c7612f7436b4e64eed7f8c4a32 (306 files) and 77114897c02548681e48e6a849d34d6c174c48bb (5 files), local, not pushed | git log | exec | local only | P | VERIFIED |
| G2 | Large archive (SHA-256 411d9721…43e30): 7 938 files OK; text snapshot (96105b63…ebfa): 305 files OK; D: copy 10/10 OK | `RESTORATION_TEST_2026-11-01.md` | exec | same machine (two SSDs) | P | VERIFIED |
| G3 | Git normalised CRLF to LF in 135 of 305 text files, so SHA-256 of 37 manifest files differ from the git checkout by CR bytes only | `RESTORATION_TEST_2026-11-01.md` F2 | exec (byte counts) | fixable by `.gitattributes`; not done | P | VERIFIED |
| G4 | No external expert review of any result exists | — | fact | — | E | VERIFIED |

## Addendum v1.1 (2026-11-01, after OB-1): the source register was supplied

The text above is unchanged. The statement in the header that the source register was not found is historical: the file was supplied later and copied to `review_package/H-CAT56-2_FULL_RESULTS_REGISTER_2026-11-01.md` (SHA-256 `32650d10…a760e`). Its 44 items were compared with this register in `OB1_REGISTER_DIFF_2026-11-01.md`: 28 VERIFIED, 12 CONDITIONAL, 3 CORRECTED, 1 UNKNOWN, 0 REFUTED.

Entries added or changed by that comparison (the numbering of v1 is not changed):

| ID | CLAIM | PROOF / TEST | CLASS | VERDICT |
|---|---|---|---|---|
| H1 | A₁₄ᴴA₁₅ = [[136, 144i], [−144i, −132]], Hermitian | `novelty_checks/register_diff_checks.py` (exec) | N | VERIFIED |
| H2 | For E = {I₂⊕0, 0⊕I₂₀}: N(I₂⊕0) = 0 and N(0⊕I₂₀) = F^Q (error 1.5·10⁻¹¹), independent of L_kk; tr F^Q (16×16) = 60152 | same (exec) | N | VERIFIED |
| H3 | Rank-jump toy rerun reproduces the recorded output byte for byte | `novelty_checks/toy_povm8_rerun.out` (exec) | N | VERIFIED |
| H4 | Ruff exemption hides no real undefined name in the certified code: 20 findings (14 F821 in `toy_rank_jump/povm8_jump.py`, names defined by `exec`; 6 F841) | `ruff --isolated --select F821,F811,F841` (exec) | N | VERIFIED |
| H5 | The restoration test was completed (supersedes "no result reported" in the source register) | `RESTORATION_TEST_2026-11-01.md` | P | VERIFIED |
| D6 (changed) | Wording narrowed: both subsets satisfy Suzuki's eq. (104) as an equation; "asymptotically classical" and Lemma 4.4's consequence are not claimed until OB-8 (rank-deficient ρ₀, D-invariance eq. 102) is done | OB-1 item U03 | L+M | CONDITIONAL |
