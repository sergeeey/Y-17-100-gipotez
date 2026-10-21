# decision.md — 20261021-h-cat56-2-cfim-zero-prob-convention

Scope: the pre-registered claims in `claim.md` (Z1–Z10, G1–G3, P1–P3) and the memo `MEMO_zero_prob_geometry.md`.

Evidence markers: `[VERIFIED-exact]` / `[VERIFIED-mp]` / `[VERIFIED-float]` are identity checks, not data validation. `[PROVED]` is an argument written here. `[REFEREE]` is the independent context-blind review (agent `a5542126409fd702e`, 2026-10-21). `[REVIEWER]` is the pre-commit logic review (rounds 1 and 2, 2026-10-21). `[TEXT]` is a statement read from a source. `[CONFLICT]` means the sources contradict each other.

## 1. Verdict

- [ ] PROMOTE
- [ ] REPEAT
- [x] **REJECT** for the pre-registered *general* forms: Z3 for directions with c·h = 0, Z5, Z6, Z7, and the limit/Hellinger clauses of Z9 (no rank hypothesis). Killed by counterexamples (section 4). Copied to `null_results/20261021-h-cat56-2-cfim-zero-prob-convention-general-identities.md`.
- [ ] ARCHIVE

The same decision **PROMOTES the amended forms**: the rank hypothesis (A1) and, for Z3, the restriction to c·h ≠ 0 (A7). The element-level G1 and G2 checks are PROMOTED for rank-one elements only (limitation L7). Per-claim status is in section 2, which is authoritative. Left open: P3 (Proposition 6 as printed), the Lemma 2 question, Z10 (`[CONFLICT]`), and G3 (partial).

## 2. Claim status

Referee numbering C1–C9 is mapped to claim IDs by content (my mapping, `[INFERRED]`): C1↔Z5, C2↔Z6, C3↔Z7, C4↔G1 with Theorem A, C5↔Z8, C6↔memo §4 Hellinger triviality, C7↔P1/P2, C8↔memo §7 one-sided necessity, C9↔memo §6 (D is not block-diagonal).

| id | claim (short) | status | evidence | referee / reviewer |
|---|---|---|---|---|
| Z1 | F_pos = diag(4.7619, 0); F^Q − F_pos = 0.525·[[1, 0.7], [0.7, 0.49]], rank one | CONFIRMED | `[VERIFIED-mp]` 50 digits; pytest asserts \|F^Q − F_pos − N\| < 1e-25 | — |
| Z2 | closed form of p_null along θ | CONFIRMED | max error 4.9e-52 `[VERIFIED-mp]`; sympy residual 0 | — |
| Z3 | direction-wise limit of CFIM = F^Q for every direction h | **REFUTED as stated** (directions with c·h = 0); CONFIRMED for c·h ≠ 0 (A1, A7) | Example 2, constant rank: residual 9.8e-3, 9.8e-5, 9.8e-7 at t = 1e-3, 1e-5, 1e-7 for h = (1, 0), (1, 1), (1, −2) (linear in t); 1.6e-16 at t = 1e-7 for h = (0, 1). For c·h = 0 (e.g. h = (0.7, −1)): p_null ≡ 0 along the line, F_lim = F_pos, deviation N `[PROVED]`, section 4 | C2 holds at constant rank; REVIEWER round 1 P1-3 |
| Z4 | H_quad(h) = hᵀF^Q h / 4 | CONFIRMED for Example 2 (A1) | H/t² at t = 1e-7 differs from F^Q/4 by ~1e-7 (relative); F_pos part tested here | C3 holds at constant rank |
| Z5 | Hess_E = N_E / 2 for every null E | **REFUTED as stated**; CONFIRMED with A1 | counterexample, section 4; constant-rank families: rel. error ≤ 1.3e-41 `[VERIFIED-mp]` | C1 |
| Z6 | limit of null CFIM = (Nh)(Nh)ᵀ / (hᵀNh) | **REFUTED as stated**; CONFIRMED with A1, A2 | constant-rank families: rel. error ≤ 1.1e-22 `[VERIFIED-mp]` | C2 |
| Z7 | Hellinger identity H_quad = hᵀ(F_pos + ΣN_E)h / 4 | **REFUTED as stated**; CONFIRMED with A1 | constant-rank families: rel. error ≤ 2.7e-23 `[VERIFIED-mp]`; the random family has F_pos ≡ 0, so its F_pos part is tested only by Z4 for Example 2 (limitation L2) | C3 |
| Z8 | N_E rank ≤ 1 ⇔ kernel-support rows real-proportional | CONFIRMED | 6/6 models (3 rank-two, 3 rank-one); Gram-matrix argument | C5 VERIFIED |
| Z9 | saturation classes per notion | point clause CONFIRMED; limit and Hellinger clauses CONFIRMED only with A1 | regular element criterion plus N_E = 0 for null outcomes | C4, C6 |
| Z10 | the disagreement with Nurdin Example 2 is definitional | **CONFLICT** (source-internal); POVM facts CONFIRMED for Example 2 | referee: the source uses the pointwise formula together with a limit-convention theorem, so it is not consistent. Elementary example: qubit cos θ\|0⟩ + sin θ\|1⟩, measured in {e₀, e₁}: point CFIM 0 at θ0 = 0, limit CFIM 4 = F^Q `[PROVED]` | consistency: NOT consistent |
| G1 | element-level criterion, rank-one elements | CONFIRMED for rank-one elements (regular and null, all classes counted) | regular: positive 40/40, negative 40/40; null negative 40/40 (p = 2 and p = 3, `[VERIFIED-float]`). Null positive: 30/30, negative 30/30 for each p, in a family where a kernel vector k0 satisfies P_+ L_a k0 = 0. Skipped 0. Referee C4: 300 random models ≤ 3e-14 | C4 VERIFIED; REVIEWER round 1 P1-2 fixed; round 2 F1 fixed; scope L7 |
| G2 | union U characterization, rank-one elements | CONFIRMED for rank-one elements (all four classes) | members 25/25, non-members 25/25, zero-branch members 25/25, zero-branch non-members 25/25, for each p `[VERIFIED-float]`. The earlier 200/200 check used generic vectors only and was vacuous (REVIEWER round 1 P1-1), withdrawn. The ⇒ direction is by construction (L8). POVM-level outcomes of rank ≥ 2 are not tested (L7) | round 1 P1-1 fixed; round 2 F1, F2 fixed; F3, F4 documented as L8, L7 |
| G3 | projective saturation iff an ONB lies in U | PARTIAL | D's 22-outcome ONB saturates exactly `[VERIFIED-exact]`; the "iff" was not tested | C9 facts |
| identity | Σ_E N_E = F^Q over all outcomes | CONFIRMED for both bases | worst error ≤ 3.6e-15 (random basis, regular outcomes only) and ≤ 3.6e-15 (block basis, 60 null outcomes) `[VERIFIED-float]`. F_pos cancels by construction (L1) | REVIEWER round 1 P2-4, partly fixed |
| P1 | literal Condition 2′ fails at D | CONFIRMED, strengthened | 18/22 outcomes (1152 ordered pairs); 32/36 outcomes (480 pairs) `[VERIFIED-exact]`. Referee C7: the literal form is unsatisfiable at D for **any** kernel POVM with ΣE = I₂₀ `[PROVED]` (pair (i, 8+j) forces E e_i = 0 for every outcome) | C7 VERIFIED |
| P2 | one-sided reading holds at D | CONFIRMED | 0 failures of 2640 and 4320 pairs `[VERIFIED-exact]`; referee C8: every saturating element has all E₀₀B_a on one real line `[PROVED]` | C7, C8 VERIFIED; evidence path corrected (A8) |
| P3 | Proposition 6 holds only for the literal reading | **NOT SUPPORTED as written; OPEN** | section 3 (A5, A6): the direction was reversed. Needs corrigendum v5 Section 6 | not checked against text |

Lemma 2 (block diagonality) is Lemma 2 of arXiv:2405.01471 v1 (p. 7). An earlier draft of this file cited arXiv:1806.07337 and arXiv:2402.11567 for it; that was wrong. The arXiv record (page read in this session) shows v2 of 2405.01471 (22 Dec 2024) as withdrawn "due to an irreparable error". The note places the error in Lemma 2 (Section 4) and says that Corollaries 2 and 3 and Theorem 3 of that section are affected. Only the key phrase is a quotation; the rest is a paraphrase by the reading model, so the Comments field should be checked directly. Our control point D (a projective ONB of 22 outcomes, exact) is consistent with this: D is not block-diagonal and saturates the point notion `[VERIFIED-exact]`. What replaced Lemma 2 in the published version (DOI 10.1109/LCSYS.2024.3451468) is NOT verified: the IEEE page returned no text. The verdict is unchanged; this is a citation and status correction.

## 3. Amendments (pre-registered text kept unchanged; these are proposed corrections)

- **A1 (rank hypothesis).** Z5, Z6, Z7, Z9 (limit and Hellinger clauses), memo §3 (D1–D3) and memo §4 (Hellinger triviality) hold only if rank ρ_θ is constant in a neighbourhood of θ0. Example 2 satisfies this. Its spectrum is {1−θ₁, θ₁, 0} for all θ: the 2×2 block has trace s and determinant s²(D²(1−D²) − g²) = 0, because g² = D²(1−D²) (`[PROVED]`). So rank = 2 for 0 < θ₁ < 1.
- **A2 (Z6).** State the condition as hᵀHh > 0, with H the Hessian of p_E (equal to N_E/2 under A1).
- **A3 (B_l).** Define B_l explicitly, as Y†∂_lV or with the factor stated. The referee notes that (L_l)_KS and Y†L_lV differ by a right factor ρ_S^½. This does not change proportionality, but it changes which matrix is called B_l.
- **A4 (literal Condition 2′).** Unsatisfiable at D for any kernel POVM with ΣE = I (C7). Keep the one-sided form as the candidate necessary condition. The C8 derivation: for a quasi-pure family, a saturating element gives E₀₀B_a = c_a E_KS with real c_a `[PROVED]`.
- **A5 (memo §7, last line).** The sentence "Therefore Proposition 6, as printed (literal), holds" is **withdrawn**. D saturates and violates the literal condition (P1), so the literal necessity claim fails at D. The H-CAT56-2 manuscript states the same, Proposition 6: "the necessity claim of arXiv:2402.11567 v5 fails at D" (`experiments/20260919-pcc-generic-quasipure-cat56-2/dmdp/MANUSCRIPT_DRAFT_EN_v3_snapshot_2026-10-21.md`).
- **A6 (P3).** Rewritten: if the corrected Condition 2′ is one-sided, D does not refute Proposition 6; if it is literal, D refutes it. Which reading the corrigendum uses is OPEN until its Section 6 is read. The earlier P3 wording had this direction reversed relative to A5.
- **A7 (Z3, direction restriction).** Z3 as stated ("for every direction h") is false for h with c·h = 0. There p_null(θ0 + t h) = 2(1 − θ₁′)G²(1 − cos(t·c·h)) ≡ 0, so the null outcome drops out of the CFIM, and the limit is F_pos ≠ F^Q (the null term N ≠ 0). Amended Z3: for every h with c·h ≠ 0 (equivalently hᵀNh > 0), F_lim(h) = F^Q. Check of the amended form: the four numerical directions all have c·h ≠ 0.
- **A8 (P2 evidence path and references).** The pre-registered P2 evidence `condition2_prime_readings.py` does not exist in this folder; the verification is `prop6_readings_check.py`. The model reference in the `example2_zero_probability_limits.py` docstring now points to `../20261021-h-cat56-2-projective-criterion/example2_check.py`, where that file lives.

## 4. Kill analysis (REJECT part)

**Killed** (as pre-registered, no rank hypothesis): Z5, Z6, Z7, the limit/Hellinger clauses of Z9, and Z3 for directions with c·h = 0 (A7).

Counterexample for Z5–Z7 `[PROVED]`: ρ_θ = diag(1 − θ², θ²) on C², θ0 = 0, E = |1⟩⟨1|. This E is null at θ0. p_E(θ) = θ², so Hess p_E = 2. ∂ρ(0) = 0, so the SLD vanishes at θ0 and N_E = 0. Hence Hess p_E ≠ N_E/2. The rank drops at θ0 (the eigenvalue θ² → 0), the SLD on the kernel block behaves like 1/θ, and the step "drop tr(Eρ∂L) because Eρ = 0" fails. Referee (numerically): Hess 2.000 with N_E = 0; a three-level example gives Hess 4.000 against N/2 = 1.

Counterexample for Z3 `[PROVED]`: in Example 2, h = (0.7, −1) has c·h = 0 exactly. Along θ0 + t h the closed form gives p_null ≡ 0, the null outcome is excluded from the CFIM, and the regular part converges to F_pos = diag(4.7619, 0), not to F^Q. The deviation is N, of size 0.525 in the (1,1) entry. Reviewer round 1 (P1-3) found this; my earlier "for every direction" statement was wrong.

**Not killed:** the same identities at constant rank (A1), and Z3 for c·h ≠ 0 (A7). Example 2 is constant-rank (section 3), so Z1, Z2, Z4 and Z3 for c·h ≠ 0 are not affected.

**Relaxation map** (one assumption at a time):

| assumption | action | result |
|---|---|---|
| constant rank of ρ_θ near θ0 | remove | killed (counterexample for Z5–Z7) |
| constant rank | restore (A1) | survives: numerically and algebraically |
| c·h ≠ 0 (Z3 direction class) | remove (allow c·h = 0) | killed (counterexample for Z3) |
| c·h ≠ 0 | restore (A7) | survives: numerically at four directions |
| interior θ0, smooth family | unchanged | — |

**Revival condition:** none for the general forms (theorem-level counterexamples). A1 and A7 are new variants, not revivals.

## 5. AOG check for the amended claims (A1, A7)

| check | result |
|---|---|
| AOG-1 pre-registration | partly. The constant-rank assumption was implicit in memo D1 ("family smooth") and in the random families (V P V† with V of full column rank, so rank 2 everywhere). The restriction c·h ≠ 0 was not stated at all; it comes from the counterexample above |
| AOG-2 specificity | yes: the amended claims are restrictions of the originals |
| AOG-3 novel prediction | yes: Hess p_E = N_E/2 + Hess tr(EΣ) ≥ N_E/2, with Σ the Schur complement (referee); for Z3, F_lim = F_pos on the line c·h = 0 |
| AOG-4 non-triviality | yes: rank-jump families falsify the rank-hypothesis form; the c·h = 0 line falsifies the restricted Z3 |
| AOG-5 independent motivation | yes: the rank condition makes the SLD well behaved, and the c·h condition is the degeneracy hᵀNh = 0, both from the derivation |

Result: 5/5 for both amendments. The amended claims may be promoted.

## 6. Retroscan (CLAUDE.md: invalidation → graph edges in the same session)

- `registry/graph.yaml`: no node or edge references this experiment or its claims. No graph status change is forced by an edge.
- **Related node H-CAT56-2** (status `confirmed`, PCC-generic quasi-pure states; experiment `experiments/20260919-pcc-generic-quasipure-cat56-2`). Its `dmdp/cycle.json` target T1p (stage PROOF_ATTEMPT) states that for instance T1 the single-copy matrix QCRB is not saturable, citing "Lemma 2 и Eq. (9) Ref. [29]".
- The same folder's `dmdp/controls/point_D_saturation_exact.py` is the control point D used here (our `prop6_readings_check.py` cites it). Its manuscript v3 snapshot, dated 2026-10-21, states Theorem 3 (exact saturation at D, same A-matrices, P = diag(2/3, 1/3)) and that D is not block-diagonal. This agrees with P1 and with the saturating POVMs here.
- **Tension** `[INFERRED, not verified here]`: if T1p's non-saturation proof uses Lemma 2 as block diagonality, that premise fails at D, which the manuscript itself records. The T1 conclusion would then need another route (for example its Proposition 2, the dimension obstruction) or an instance-specific check.
- **Timing:** the author U2 clock started 2026-09-23 (registry text), so it ends about 2026-10-23.
- **Action:** none applied to `graph.yaml`. Changing H-CAT56-2's status is a research decision for the project owner.

## 7. Open items

1. Read corrigendum v5 Section 6 (Condition 2′, Proposition 6). Settles P3 and A5/A6.
2. Establish what the published version (DOI 10.1109/LCSYS.2024.3451468) puts in place of Lemma 2 of arXiv:2405.01471 v1. The IEEE page must be read directly, or its abstract and statement supplied. This decides between scenarios A, B and C of the 2026-10-21 analysis.
3. Z10 `[CONFLICT]`: the source's CFIM convention against its limit-convention theorem. Needs the authors' answer (U2) or an explicit convention in our text.
4. H-CAT56-2 T1p premise (section 6). Decide before 2026-10-23.
5. Pre-commit status: the full `pytest tests/` run on the final code finished with 421 passed (exit code 0; the run took 1 h 37 min). Reviewer round 3 returned LGTM (section 9).

## 8. Evidence and reproducibility

- Scripts: `example2_zero_probability_limits.py`, `example2_limit_symbolic.py`, `zero_prob_identities_random.py`, `geometric_criterion_check.py`, `prop6_readings_check.py`, `hellinger_block_triviality.py`. The geometric metrics JSON was regenerated after the round-2 fixes; the other JSON files are unaffected by those fixes.
- `tests/test_h_cat56_cfim_convention.py`: 6 tests, all pass (targeted run on the current code). The Z1 test asserts the N-level identity at 50 digits. The geometric test asserts each class is non-empty and agrees with its truth value.
- Lint: ruff clean on the folder and test file; format check passes.
- Referee scratch scripts: session scratchpad only, nothing written into the repo.

## 9. Concerns and resolutions

**Referee (round 0, 2026-10-21)**

| concern | resolution |
|---|---|
| C1–C3 false without a rank hypothesis | accepted: A1 |
| C6 Hellinger clause fails at rank jumps | accepted: A1 |
| C7 literal Condition 2′ unsatisfiable at D | accepted: A4; P1 strengthened |
| memo §7 final line contradicts P1 | accepted: A5 (withdrawn) |
| B_l and "pointwise" undefined | accepted: A3, to define |
| C9 "refutes Lemma 2" | the statement is Lemma 2 of arXiv:2405.01471 v1; the arXiv record shows the author withdrew v2 for an irreparable error in Lemma 2; what replaced it in the published version is open (section 2) |
| source internally inconsistent | accepted as `[CONFLICT]` (Z10) |

**Reviewer round 1 (pre-commit, logic of the code and tests)**

| finding | resolution |
|---|---|
| P1-1: G2 check vacuous (random vectors only; both predicates identical) | accepted and fixed: members constructed in W(c) and non-members, each class asserted |
| P1-2: G1 null positive case never occurs for generic L_a; the dead branch was never executed | accepted and fixed: `g1_null_check` with a family in which a kernel vector k0 satisfies P_+ L_a k0 = 0 |
| P1-3: Z3 false for c·h = 0 | accepted: A7 and the counterexample in section 4 |
| P2-4: identity cancels F_pos; random basis never produces null outcomes | partly fixed: block basis exercises the null branch; the cancellation is documented (limitation L1) |
| P2-5: Z1 not asserted in pytest; symbolic Z3 test covers one direction | Z1 test added; the symbolic test's docstring now says h = (1, −2) |
| P2-6: random family in `zero_prob_identities_random.py` has F_pos ≡ 0 | not fixed; limitation L2 |
| P2-7: `hellinger_block_triviality.py` checks the algebra, not the Hellinger limit | not fixed; limitation L4 |
| P2-8: stale references (P2 evidence file; example2 docstring path) | fixed: A8 and the docstring |

**Reviewer round 2 (scope: the changed functions and tests)**

| finding | resolution |
|---|---|
| Round-1 P1-1, P1-2, P1-3 | confirmed fixed by round 2 |
| F1 (blocker): the regular positive class of G1 was not asserted; a `None` from `random_in_w` was skipped silently and the test passed; `tie_constants` hard-coded the affine coefficients | fixed: `g1_check` reports `regular_pos_tested` and `regular_neg_tested`, `skipped` is asserted zero, and `tie_constants` takes the coefficients from `setup` |
| F2 (blocker): the zero branch P_+ v = 0 of G2 was not exercised | fixed: four G2 classes, including zero-branch members and non-members in the modified family |
| F3 (documentation): the member construction and `in_union` express the same linear condition, so the ⇒ direction is tautological | accepted as limitation L8; G2 is claimed as implementation consistency, not as an independent proof of the characterization |
| F4 (documentation): the checks cover rank-one elements, not POVMs with outcomes of rank ≥ 2 | accepted as limitation L7; G1 and G2 are scoped to rank-one elements in claim.md |

**Reviewer round 3 (last allowed under the evaluator–optimizer cap): LGTM.** F1 and F2 are confirmed closed by reading the code: `skipped == 0` holds by construction (4 equations on 5 unknowns for p = 2; rank 4 for p = 3 after the affine tie), and the zero-branch mutations (`return True` / `return False`) would each be caught by a class assertion. The reviewer found no blocking error. One non-blocking gap (P2) is recorded as L9.

## 10. Limitations (stated, not fixed)

- **L1.** `identity_check` writes D_E + dp dpᵀ/p = N_E for regular E, so F_pos cancels by construction. The substantive content is Σ_E N_E = F^Q, which is checked against the trace formula.
- **L2.** The random family in `zero_prob_identities_random.py` has F_pos ≡ 0: p_e0 = P_0/denom(θ), and denom(θ) is quadratic in θ, so the first derivative vanishes. Z7's F_pos part is therefore tested only by Z4 for Example 2 (JSON, not asserted in pytest).
- **L3.** The Example 2 limit numbers for Z3 and Z4 are in the JSON only. pytest asserts Z1 and the symbolic Z3 at h = (1, −2).
- **L4.** `hellinger_block_triviality.py` checks F_pos = 0 and Σ N_k = F^Q at one point. It does not compute H_quad; the claim "H_quad = F^Q/4" for the block POVM rests on Z7 at constant rank.
- **L5.** The constants (`h9`, `a_vals`, `w_vals`) in `prop6_readings_check.py` are copied from `point_D_saturation_exact.py`; the copy was not compared line by line.
- **L6.** In `zero_prob_identities_random.py`, Z8 divides by r1[m]. If the kernel row of the second generator vanishes, the code divides by zero. Seeds 1–3 do not trigger this.
- **L7.** G1 and G2 are checked at element level (rank-one elements E = |v><v|). The POVM-level statement for outcomes of rank ≥ 2 (one constant c^k for the whole range of E_k) is not tested.
- **L9.** G2's "real multiple" qualifier is tested only through the members (real c) and the generic non-members. No class covers a complex multiplier, P_+ L_a v = i·c·P_+ v with c ≠ 0, which must be rejected. A mutation that replaces `c.real` by `c` and drops the imaginary check would not fail any test (reviewer round 3, P2). A non-member class with a complex multiplier is the natural fix; it was not added after the LGTM.
- **L8.** In G2, the member construction (vectors in W(c)) and the predicate `in_union` express the same linear condition P_+ L_a v = c_a P_+ v. The check therefore verifies the implementation of the characterization, and the ⇒ direction holds by construction. The independent content is the non-member and zero-branch classes.

## 11. Result of this decision in one line

REJECT the general forms (Z3 for c·h = 0, Z5–Z7, Z9 limit/Hellinger clauses); PROMOTE their amended forms (A1, A7), Z1, Z2, Z4, Z8, G1 and G2 for rank-one elements, P1, P2; Z10 CONFLICT; P3 and the Lemma 2 question OPEN.
