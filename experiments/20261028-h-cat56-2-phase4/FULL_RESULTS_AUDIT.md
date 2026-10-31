# H-CAT56-2: full scientific results audit (2026-11-01)

Companion to `FULL_RESULTS_REGISTER_VERIFIED.md` (64 numbered results, each with CLAIM, SOURCE, PROOF/TEST, LIMITATIONS, CLASS, VERDICT).

**EstimandOps L0 classification.** The object of the audit is a list of mathematical and computational claims. It is descriptive and deductive, not a causal or predictive claim about the world. No intervention estimand applies, so the causal layer (DAG, identifiability) is not needed.

## 1. Blocker: the source register is missing

`H-CAT56-2_FULL_RESULTS_REGISTER_2026-11-01.md` was not found and its text was not supplied (searched: the repository, Downloads, Desktop, Documents, D:, the Obsidian vault). **Every item of that document is BLOCKED.** This audit therefore does not satisfy "each item of the original register received a verdict". It does give a primary-source register that the original can be diffed against.

**The audit is not complete** until the original is supplied and diffed (OB-1).

## 2. Counts (the independent register)

| Verdict | Count | Meaning |
|---|---|---|
| VERIFIED | 33 | confirmed by my execution, derivation or reading of primary output |
| CONDITIONAL | 20 | internal proof or certificate I did not re-derive, or depends on an unread premise |
| REFUTED | 6 | claim shown false (C6, C14, C15, E12, E13, F8) |
| UNKNOWN | 5 | no basis either way (B7, F6, F7, F9, F10) |
| BLOCKED | all items of the source register | document unavailable |
| Total | 64 | |

By section: A model/identities 6 (all VERIFIED); B S₊ 7 (3 V, 3 C, 1 U); C S₋ no-go 16 (1 V, 12 C, 3 R); D structure 7 (3 V, 4 C); E O3 14 (11 V, 1 C, 2 R); F literature 10 (5 V, 1 R, 4 U); G process 4 (all V).

**Reading the numbers.** Most VERIFIED items are identities, counts, arithmetic, code reading, recorded exact outputs, and my own executions. The main mathematical theorems (B1, C1–C3, C5, C9–C13) are CONDITIONAL: they are internal proofs, partly reviewed by Codex, that I did not re-derive. The word VERIFIED on a long exact run (B2, B3) means "primary output read", not "re-executed".

## 3. Evidence classes kept apart

- **Mathematical proofs (internal):** Theorem N chain, Prop 7, Prop 8, D2 bounds, Theorem S₊ logic. All CONDITIONAL.
- **Exact computational certificates:** 484 equalities and 280 positive definite blocks (ℚ and ℤ); tiling; the cell lemma implemented in arb. Output read; the cell lemma re-derived by me.
- **Numerical experiments:** dense grid, cell-bound validity, partial commutativity, composite ranks, toy rank-jump. Executed or read.
- **Internal audits:** Codex (S₊, O3 v2, O3 v3) and a reviewer pass on four scripts. These are the same-project cross-model checks; none raises a status here.
- **External expert review:** none exists.

## 4. Status vocabulary: ledger versus this register

`EVIDENCE_LEDGER.md` uses PROVED-hand, VERIFIED-EXACT, VERIFIED-INTERVAL, VERIFIED-NUMERIC. This register is stricter. A ledger "VERIFIED-INTERVAL (strict v3, internal)" is CONDITIONAL here (E7) because there is no independent full recomputation and the arithmetic library is trusted. The ledger's PROVED-hand is CONDITIONAL here unless I re-derived the step. This is a difference of standard, not a contradiction.

## 5. Errors, omissions and contradictions found

| # | Finding | Where | Action |
|---|---|---|---|
| 1 | arXiv:2405.01471 is **withdrawn** (irreparable error in Lemma 2 §4; Corollaries 2, 3 and Theorem 3 incorrect). The novelty matrix cited its abstract as a live source. The vault already recorded the withdrawal on 2026-10-27. | `NOVELTY_MATRIX.md` [S5], Row 1–3, readiness; `FINAL_CONSISTENCY_2026-11-01.md` | corrected in the working tree (uncommitted, see §8); F5 |
| 2 | Draft reply v2 and v3 wrote "120 × 4 = 480 ≥ 399", comparing a row count with a dimension. The right statement is a rank: 399 (all 16), 264 (S₋), 261 (S₊). Verified in this audit (D3). | `review_package/DRAFT_REPLY_TO_NURDIN_v3` (fixed), `v2` (marked superseded) | fixed |
| 3 | Draft v2 said "family of constant-rank states". The proven setting is the unitary-orbit model F_U and the matrix/trace CFIM. v3 now names the model and the matrix scope. | same | fixed |
| 4 | **Scope of the S₋ result.** The no-go is for the matrix (and trace) classical Fisher information under convention D1, near θ=0. Proposition 8 shows the directional quadratic form hᵀFh is saturable for F_U. Any text that says "S₋ is not attainable" without these qualifiers overstates it. The unqualified phrasing appears in the externally supplied draft letters ("single-copy non-attainability argument") and must be qualified before use. | `THEOREM_NATURAL_D2_NOGO_v8.md` §3; C12 | flagged |
| 5 | The pasted draft says "Our computational checks are complete" and "complete, rigorously bounded interval-arithmetic certificate". The strict v3 run is complete for the cell list; no independent recomputation exists, python-flint is trusted, and the certified bound is ≈ 6× looser than the sampled supremum. | pasted draft; E7, E11 | flagged |
| 6 | The S₊ result is **at θ=0** only, with shared inputs not regenerated independently (B5). The S₋ result is on ∣θ∣ ≤ s₁ with implicit constants. The contrast is stated at the reference point only. | B5, C1 | stated in the central formulation |
| 7 | Suzuki–Yang–Hayashi §5.4 is the closest prior framework for "attainability depends on the parameter subset". The dependence itself is therefore not a novelty claim (F8). The contrast cannot be explained by their conditions: both subsets are asymptotically classical and satisfy partial commutativity (D1, D2, D6). | NOVELTY_MATRIX Row 3 | consistent after the check |
| 8 | The convention for zero-probability outcomes (D1 here; the literature may use a limit, D2) is not verified against YPZJ. | F10; `STAGE_C_FINAL_PROOF.md:104` | open |
| 9 | STAGE_C lines 71–73 state exact Hermiticity of R and "s = 0.9·trR/20" as exact. Both are wrong at 5.2·10⁻¹⁷ and 1.7·10⁻¹⁸. | E12, E13 | ERRATA already issued |
| 10 | The CRLF normalisation by git means committed copies of 135 text files differ from their pinned hashes. | G3 | byte-exact snapshot exists |

No contradiction was found between the numerical values in the ledger, the milestone and the audit files for: s*, γ, run totals, S₊ counts, rank 399, toy-model values.

## 6. Strongest central statement the evidence supports

For the unitary-orbit model ρ_θ = U_θρ₀U_θᴴ on C²² with ρ₀ = diag(1/3, 2/3) ⊕ 0 and the 16 integer blocks A_a ∈ C^{20×2} (instance SHA-256 05289920…), take the other four parameters fixed at 0, single-copy POVMs, the matrix classical Fisher information, and the convention that outcomes with p_k = 0 contribute 0:

1. **S₊ = {0..11}.** At θ=0 there exists a finite POVM of 1764 rank-one regular elements whose 12×12 classical Fisher information equals the SLD quantum Fisher information. *Basis: exact-arithmetic certificate (ℚ and ℤ) and Theorem S₊. Status: CONDITIONAL (shared inputs not independently regenerated; elements not written out).*
2. **S₋ = {4..15}.** There are c, s₁ > 0 (not explicit) such that every finite POVM satisfies tr(F^Q(θ) − F_E(θ)) ≥ c for ∣θ∣ ≤ s₁, and Borel POVMs satisfy tr F^C_M ≤ tr F^Q − c. *Basis: internal proof (Theorem N, Cor. N₁, Prop. 7) plus a computer-assisted separator bound over a tiling of 3 955 841 cells. Status: CONDITIONAL.*
3. **Structure.** At θ=0 all 16 SLDs commute on the support (partial commutativity) and weakly commute, for both subsets. The ranks of the composite generators are 261 (S₊), 264 (S₋) and 399 (all 16). *Basis: executed. Status: VERIFIED.*
4. **Consequence.** The attainable/non-attainable contrast between S₊ and S₋ is not explained by partial commutativity or by asymptotic classicality, so it is a single-copy matrix-CFIM effect. *Status: CONDITIONAL.*

**What cannot be said:** that the S₋ quantum bound is unattainable in every sense (the directional quadratic form is saturable); that the result holds for general C¹ families (the limit forms N₁ and Prop 8 are refuted there); that the subset dependence is new; that the contrast is new relative to Nurdin's corrected conditions (unread); that any result has been externally reviewed.

## 7. Open evidence obligations

| ID | Obligation | Blocks | Class |
|---|---|---|---|
| OB-1 | Obtain the source register and diff it against `FULL_RESULTS_REGISTER_VERIFIED.md`; give each of its items a verdict | the audit's completeness | process |
| OB-2 | Read the IEEE CSL correction (DOI 10.1109/LCSYS.2024.3451468) in full | F6, F7, D4, letter wording | literature |
| OB-3 | Test S₊ and S₋ against Nurdin's corrected conditions (1) and (2′) | novelty of the contrast | math |
| OB-4 | Independent re-derivation of the Theorem N chain (Riesz bound, Łojasiewicz step, Lemma 6, Prop 7) by a mathematician or a different tool | C1–C3, C9–C11 | math |
| OB-5 | Independent second implementation or recomputation of the separator (different arithmetic, or an exact rational check of a sample of leaves) | E7 | computation |
| OB-6 | Independent regeneration of the S₊ bases and y (second path from the instance to the bases) | B5 | computation |
| OB-7 | Check the YPZJ theorem used in B6 against its primary proof; check their convention for p_k = 0 (D1 versus D2) | B6, F10 | literature |
| OB-8 | Check applicability of Suzuki Lemma 4.4 and of D-invariance to a rank-deficient state | D6 | math |
| OB-9 | Explicit exact POVM for S₊ (optional; existence does not need it) | B7 | computation |
| OB-10 | Driver-side enforcement of input hashes (C-O3-3) | E14 | code |
| OB-11 | External expert review | all | review |
| OB-12 | A systematic literature search for prior examples of the S₊/S₋ type | F9 | literature |
| OB-13 | Off-machine backup; `.gitattributes` decision; hang of Chernoff tests; move of the hook patch upstream | preservation | process |
| OB-14 | Commit the corrections made after `7711489` (novelty matrix, consistency note, these two files) — requires the owner's decision | records | process |

## 8. State of the working tree

Edited in the working tree since commit `7711489`, **not committed** (the contract forbids commits): `NOVELTY_MATRIX.md`, `FINAL_CONSISTENCY_2026-11-01.md`. New and untracked: `FULL_RESULTS_REGISTER_VERIFIED.md`, `FULL_RESULTS_AUDIT.md`, `novelty_checks/composite_rank_check.py/.out`. The draft replies are untracked drafts (v2 marked superseded, v3 corrected). No push, no external sending.

## 9. Coverage of the definition of done

| # | Requirement | Status |
|---|---|---|
| 1 | Each item of the source register has a verdict | **BLOCKED** (source missing) |
| 2 | Significant results absent from the source added | done for what the project contains: D1–D7, E1–E2, F5, G3 are new relative to the earlier ledger |
| 3 | Errors, overstatements, wrong numbers and unjustified novelty claims corrected | done for project documents (findings 1–3, 9, 10 fixed; 4–8 flagged); the external draft's claims are flagged, not edited |
| 4 | Audit and corrected register with change history | done (this file and the register) |
| 5 | Open obligations table and a consistent thesis | done (§6, §7) |

## 10. Remaining risks for publication

1. The Theorem N chain is an internal proof that nobody outside the project has read; its constants are not explicit.
2. The separator rests on one implementation in one arithmetic library with no independent recomputation.
3. Novelty of the contrast is unresolved until the corrected Nurdin conditions are applied to S₊ and S₋.
4. The S₊ certificate depends on inputs that were not regenerated independently.
5. Scope wording: the matrix-versus-directional distinction and the D1 convention must appear in any abstract or letter.

## Addendum (2026-11-01): OB-1 closed

The original ChatGPT register was supplied and compared item by item: `OB1_REGISTER_DIFF_2026-11-01.md`. Section 1 of this file ("Blocker: the source register is missing") and the "BLOCKED" rows of section 9 describe the state before that and are kept as history.

Result: 44 source items = 28 VERIFIED, 12 CONDITIONAL, 3 CORRECTED (P20 and U07: restoration test is complete; N05: 480 and 264 are row counts, ranks are 399/264/261), 1 UNKNOWN (N06, the corrigendum text), 0 REFUTED. Where the source is firmer than the evidence: P02, P03, P09, P16, N01–N04. One correction flows back into project documents: U03, the claim "both subsets are asymptotically classical" is not established (only eq. 104 as an equation; OB-8 open); `NOVELTY_MATRIX.md` row 3 corrected.

Reading of the six REFUTED items of the independent register: C6, C14, C15 refute over-wide mathematical generalizations (D2 limit along arbitrary curves; the limit form N₁ and Proposition 8 for general C¹ families, shown on a synthetic 5×3 toy); E12, E13 refute wording in `STAGE_C_FINAL_PROOF.md`; F8 refutes a novelty claim. None of them refutes the S₊/S₋ contrast or the O3 v3 certificate.

Open obligations after this step: OB-1 closed; OB-8 widened to include D-invariance of S₊ and S₋; all others unchanged.
