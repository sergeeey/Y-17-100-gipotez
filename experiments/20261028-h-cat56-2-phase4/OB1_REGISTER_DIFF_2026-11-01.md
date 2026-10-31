# OB-1: diff of the ChatGPT register against the independent register (2026-11-01)

**Source document.** `review_package/H-CAT56-2_FULL_RESULTS_REGISTER_2026-11-01.md`, copied from `C:\Users\serge\Downloads\` (SHA-256 `32650d10ddc513d15c8030618618e3445e517cf4e6319093300035432b9a760e`, identical to the original). 44 items: P01–P20 (positive), N01–N15 (negative and impossibility), U01–U09 (boundaries and unknowns). Section I states the setting, V lists evidence locations, VI lists priorities.
**Compared with.** `FULL_RESULTS_REGISTER_VERIFIED.md` (64 items, v1, unchanged) and the primary files named there.
**Source self-description.** Its header says it is built from Claude Code and Codex reports and the conversation, "not a new independent check". Its agreement with my register is therefore not independent evidence for either.
**Rule used.** A status is never raised because the source states a claim. Verdicts use the v1 vocabulary; **CORRECTED** is added for a claim that was true when made but is superseded or partly stale.
**New executions for this diff:** `novelty_checks/register_diff_checks.py` (+ `.out`), `novelty_checks/toy_povm8_rerun.out` (rerun of `toy_rank_jump/povm8_jump.py`, byte-identical to the recorded `.out`), `ruff --isolated --select F821,F811,F841` over the whole phase4 folder, and a read of `o3_v3/metrics/audit_run{A,B,C,D}.json`.

## Result

| Verdict | Count | Items |
|---|---|---|
| VERIFIED | 28 | P01, P04–P08, P10–P15, P18, P19; N07, N08, N10–N13, N15; U01–U05, U08, U09 |
| CONDITIONAL | 12 | P02, P03, P09, P16, P17; N01–N04, N09, N14; U06 |
| CORRECTED (partly stale or superseded) | 3 | P20, N05, U07 |
| UNKNOWN | 1 | N06 |
| REFUTED | 0 | none of the 44 is a false statement; several are stated more firmly than the evidence allows (see below) |
| Total | 44 | |

All 44 items have a counterpart or a stated gap. Items present in the source but not in v1: P07 pair (14,15) numbers, N08 kernel-outcome statement, N09 earlier-fault list, U06, U08. Items present in v1 and missing from the source are listed at the end.

## Item-by-item

| ID | Source claim (short) | v1 counterpart | Verdict | Note |
|---|---|---|---|---|
| P01 | Model, 16 SLDs `[[0,A†],[A,0]]`, F_U | A1, A2 | VERIFIED | L_kk = 0 is one admissible choice, not "the" SLD (A2: arbitrary). F^Q and the support-block commutators do not depend on it (checked: for a random Hermitian L_kk the kernel-outcome N differs from the L_kk = 0 value by exactly 0.0; this is also clear analytically because ρ₀ has a zero kernel block). "Constant rank" is correct for F_U only (spectrum fixed), not for general families (C14). |
| P02 | Two 12-subsets, different single-copy matrix attainability | B1, C1, D7 | CONDITIONAL | Rests on B1 (shared inputs, B5) and C1 (internal proof, C7/E7). Stated as an established result in the source. |
| P03 | S₊ attainable, exact certificate, θ=0 | B1–B3, B6, B7 | CONDITIONAL | Exact for the moments; explicit POVM not written (B7 UNKNOWN); θ=0 only; shared inputs. |
| P04 | 1764 outcomes, 280 blocks PD, 484/484 equations | B2, B3, B4 | VERIFIED | Output read, arithmetic re-done (182·7+98·5 = 1764); runs not repeated. |
| P05 | Two S₊ checkers not fully independent; shared bases, `exact_sdp2_M.pkl`, `indep_rows.npy` | B5 | VERIFIED | Files exist: `stage_e_v1/logs/exact_bases2.pkl`, `exact_sdp2_M.pkl`, `indep_rows.npy`. |
| P06 | Control deficit 2.43e-12, matrix error 1.47e-10 | B6 | VERIFIED | Same numbers as `control_differential.json` (2.4e-12, 1.5e-10). |
| P07 | Partial commutativity for 120/66/66 pairs; (14,15): A₁₄†A₁₅ = [[136,144i],[−144i,−132]] | D1 | VERIFIED | Pair numbers executed now: the matrix equals the claim exactly, Hermitian defect 0.0. |
| P08 | Weak commutativity for all pairs | D2 | VERIFIED | |
| P09 | S₋ no-go "checked" in finite and natural Borel classes | C1, C2, C7, E7 | CONDITIONAL | "Checked" overstates: internal proof not re-derived, certificate internal. |
| P10 | Certified object H = (R₀+R₀†)/2; defect 5.2e-17; tr H vs tr R₀ 2.3e-17 | E2 | VERIFIED | |
| P11 | s* sequential binary64 = 0x1.c057f53368882p−7, one ulp above the once-rounded exact value | E1 | VERIFIED | Once-rounded value …881; difference 1.73·10⁻¹⁸ = one ulp. |
| P12 | γ ≈ 0.030405245308261095 > 0; validity depends on interval lemmas and coverage | E1, E7 | VERIFIED (value) | The dependence clause is E7 (CONDITIONAL). |
| P13 | 7912 chunks, 3 955 841 leaves, all ok, four disjoint runs | E6, E10 | VERIFIED | |
| P14 | Per-run ranges, chunk counts, leaf counts, min slack, worst bound ≈ 8.3948e-9, all COMPLETE_STRICT | E6, E8 | VERIFIED | Read from `audit_run{A,B,C,D}.json`: min slack A 3.1338e-8, B 2.9217e-8, C 8.40e-9 (±5.16e-12), D 2.022e-8; chunk and leaf counts as stated; 8.40e-9 − 5.16e-12 = 8.3948e-9. |
| P15 | `phi_rows` encoding, phase reduction, path bound, sampled checks not a proof | A5, A6, E11 | VERIFIED | |
| P16 | Theorem N v8 corrected; conditional on O3; uniform trace deficit with non-explicit constant | C1, C9–C11 | CONDITIONAL | |
| P17 | Y_S equals the union of real lines; equivalent reformulation | C8 | CONDITIONAL | Converse direction not re-derived by me (ledger: "forward inclusion numerical; converse analytic"). |
| P18 | Codex audits localized faults; v3 PASS (internal); v2 conditional | I-class, E; `O3_V3_INDEPENDENT_AUDIT.md` | VERIFIED | As a description of the audits; not external review. |
| P19 | Commit f0c6df5, 306 files, "normal hooks", 258 tests, Chernoff incomplete, no push | G1 | VERIFIED | Two corrections: (a) a second commit `7711489` (5 files) exists; (b) "normal hooks" is inaccurate: the commit path needed an owner-approved patch of `~/.claude/hooks/lib/discovery.py` (`run_git` crashed on non-UTF-8 logs) and a scoped ruff exemption in `pyproject.toml`. The hook patch is not mentioned anywhere in the source. |
| P20 | Archive 1.79 GB, 7938 entries, hash; restoration test launched, no result; no remote copy | G2 | CORRECTED | Archive facts verified. The restoration claim is stale: the test was completed (`RESTORATION_TEST_2026-11-01.md`; archive 7938/7938; byte-exact text snapshot 305/305; D: copy 10/10) with the finding F2/G3 (git normalised CRLF in 135 files). No off-machine copy: true (D: is on the same machine). |
| N01 | S₋ has no POVM with matrix CFIM = QFIM at θ=0 | C1, C2 | CONDITIONAL | Follows from the trace gap at |θ| ≤ s₁ (includes 0), convention D1. "Under proved definitions" overstates: the proof is internal. |
| N02 | The no-go is about the matrix; the directional form can be saturated | C12 | CONDITIONAL | Precision: Proposition 8 is a limit statement hᵀF_E(th)h → hᵀF^Q(0)h for F_U, not saturation at a fixed θ; false for rank-jump families (C15). |
| N03 | No measurement removes the positive trace deficit near θ=0 inside the constant-rank orbit | C1, C2, C14 | CONDITIONAL | |
| N04 | Partial commutativity not sufficient for single-copy matrix attainability, though it holds for all 16 | D1, D4, D7 | CONDITIONAL | Not new as a general fact: the full model is already an example if D4 holds, and the vault note of 2026-10-20 records that arXiv:2601.21801 (Observation 2) states the insufficiency of PCC in general. That source was not re-read in this audit (vault record only). |
| N05 | Thresholds 399, "120·4 = 480", "66·4 = 264"; a count is not a rank; 12-subset not excluded | D3, D4, D5 | CORRECTED | The source's caveat is right and is exactly the error found in the letters. Computed ranks: 399 (all 16), 264 (S₋), 261 (S₊); the numbers 480 and 264 are row counts. |
| N06 | 2024 corrigendum restricts Nurdin's iff conditions to separated POVMs | F6 | UNKNOWN | Relayed. The corrigendum text is not in the project and was not accessible (IEEE paywall). The source says it was "provided in the conversation"; I have not seen it. OB-2 stays open. |
| N07 | Rank-jump counterexample; D2 along every curve fails; Theorem N revised to rays and limsup | C6, C14, C15 | VERIFIED | The toy script `povm8_jump.py` was rerun now: output byte-identical to `povm8_jump.out` (tr F^Q 65.5134 vs 61.5137; hF_Eh 16.3991 vs hF^Q(0)h 12.3991). The curve-limit part (C6) is relayed from PROOF_OBLIGATIONS B15. Toy is synthetic 5×3. |
| N08 | For `{I₂⊕0, 0⊕I₂₀}` all of N sits in the kernel outcome; ΣN = F^Q | A4 | VERIFIED | Executed now: N for `I₂⊕0` is exactly 0; N for `0⊕I₂₀` equals F^Q to 1.5·10⁻¹¹ (float residual) and is identical for random L_kk (difference 0.0); tr F^Q (16×16) = 60152. Caveat: F^Q is computed by the formula Re tr(Q A_aᴴ A_b), so the identity is partly definitional. |
| N09 | Earlier Theorem N v8 faults: ω through full N_v, explicit s₁ without L, blanket D2, Lemma 5 normalisation | C6, C9, C16 | CONDITIONAL | Corroborated: blanket D2 (C6); the "old ω formula … corrected after Codex 2026-10-31" is recorded in a project text quoted in `codex_logs/o3v3_codex_audit_2026-11-01.txt` (line 2179, garbled encoding). Not located: "explicit s₁ without L", "Lemma 5 normalisation" as earlier faults. I did not compare the earlier versions. |
| N10 | O3 v2 was not a full interval certificate; v3 replaced it; v2 stays as history | E-series; `O3_AUDIT_RECORD.md` §1–8 | VERIFIED | |
| N11 | Stored R₀ not exactly Hermitian; STAGE_C lines 71–73 contradict line 103; ERRATA | E2, E12 | VERIFIED | |
| N12 | The two S₊ checkers are not independent | B5 | VERIFIED | |
| N13 | Sampled bounds do not prove the interval formulas | E11 | VERIFIED | |
| N14 | The 16-parameter rank condition and counts do not transfer to S₋ | D5 | CONDITIONAL | Depends on the criterion text (D4). Ranks are 264 and 261, below 399. |
| N15 | Subset dependence is not known to be new; ours are known, not nuisance; applicability unchecked | F3, F8, OB-8 | VERIFIED | |
| U01 | No human referee checked the argument | G4 | VERIFIED | |
| U02 | Prior-art equivalence UNKNOWN; compare Nurdin, YPZJ, Suzuki, Nurdin projective | F1–F7, F9 | VERIFIED (as an open item) | The listed "Nurdin arXiv:2405.01471" is **withdrawn** (F5): its Corollaries 2, 3 and Theorem 3 are not usable. The claim that the corrigendum is available is UNKNOWN to me (N06). |
| U03 | D-invariance not checked; rank-deficiency may break Suzuki's assumptions; avoid "both asymptotically attain the same bound" | D6, D7, OB-8 | VERIFIED | **The source is stricter than my v1 on this point and correct.** My D6 checked only the weak-commutativity equation (Suzuki eq. 104). Lemma 4.4's applicability to the rank-deficient ρ₀ and D-invariance (eq. 102) were not checked. Adopted: `NOVELTY_MATRIX.md` row-3 check result corrected today; the Obsidian notes were corrected too. |
| U04 | Reproducibility needs binding to all inputs and code | E10, E14 | VERIFIED | |
| U05 | S₊ moment inputs not independently regenerated | B5 | VERIFIED | |
| U06 | No physical sensor or implementation demonstrated | — | CONDITIONAL | Scope statement about a theory project; accepted, not searched. |
| U07 | Local commit and archive on one machine; restoration test with no reported result | G2 | CORRECTED | Local-only: true. Restoration result: stale (see P20). |
| U08 | Ruff exemption covers phase4 scripts including possible F821 | P-class (pyproject) | VERIFIED | The exemption is `["E","F","I","UP","RUF"]`, so it hides F-rules. Checked now (`ruff --isolated --select F821,F811,F841`): 20 findings in phase4, none in the O3 v3 or S₊ certificate code. 14 × F821 are all in `toy_rank_jump/povm8_jump.py`, where the names are defined by `exec(src)`; the script runs and reproduces its recorded output (N07). 6 × F841 (unused locals) in `checks/fu_normalization_and_Y_2026-10-31.py:139,140,193`, `code/o1_check.py:59`, `stage_e_v1/code/control_differential.py:115`, `control_min_deficit.py:87`. Other exempted families (E, I, UP, RUF) are style rules; not examined for semantics. |
| U09 | Draft letter to Nurdin not sent | — | VERIFIED | Draft v3 is unsent; v2 is marked superseded. |

## Where the source is firmer than the evidence

P02, P03, P09, P16, N01–N03: stated as results; v1 holds them CONDITIONAL (internal proof, internal certificate, shared S₊ inputs). N04: presented as a finding; the insufficiency of partial commutativity is already in the literature (N04 note).

## What v1 has that the source lacks

A2–A6 (SLD form, F^Q formula, Φ_x), C4 (refinement monotonicity), C5, C9–C13, C16, D3 (computed ranks 261/264/399), D4/D5 (what the rank criterion does and does not decide), E3 (cell lemma), E4–E5, E7–E9 (decision logic, tiling), E14 (driver does not enforce hashes), F1–F5, F9, F10 (literature statuses, the withdrawal of 2405.01471, D1 vs D2 in YPZJ), G3 (CRLF finding), G4.

## Changes made in this step (historical documents are edited only where an error was found; the replaced text stays in git history)

1. New (all new files are untracked until committed): this file, `novelty_checks/register_diff_checks.py` and `.out`, `novelty_checks/toy_povm8_rerun.out`, and the copy of the source register in `review_package/`.
2. `NOVELTY_MATRIX.md` edited (historical file; the earlier edit that replaced the live citation of the withdrawn arXiv:2405.01471 [S5] in Rows 1–3 and the readiness section is also in this commit, together with `FINAL_CONSISTENCY_2026-11-01.md`). In this step: row 3 "CHECK RESULT", the CONFIDENCE bullet and the "What we cannot claim" list were narrowed so that Suzuki's Lemma 4.4, D-invariance and the unread correction [S4] are not asserted (U03, N06). The previous text is in git history (`7711489`).
3. Addenda appended at the end of `FULL_RESULTS_REGISTER_VERIFIED.md` and `FULL_RESULTS_AUDIT.md` (their original text untouched; both files are new in this commit).
4. `review_package/SHA256SUMS.txt` refreshed (95 entries); the previous version is kept as `SHA256SUMS.txt.bak-before-ob1` (untracked).

## Open after OB-1

OB-2 (corrigendum text; needed for N06, F6, F7), OB-3, OB-8 (now also covers D-invariance for S±), OB-4 to OB-7 and OB-9 to OB-14 unchanged. OB-1 is closed by this file.
