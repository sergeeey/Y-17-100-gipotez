# Technical memo: zero-probability outcomes, CFIM conventions and the geometry of saturating POVMs (H-CAT56-2)

Status: internal research record. Not a submission. No author contact, no push, no publication. Corrections after referee review (2026-10-21): see `decision.md` (A1 rank hypothesis; A5 withdrawn sentence in §7).
Evidence markers: [PROVED] argument in this memo; [VERIFIED-exact] Fraction or sympy; [VERIFIED-mp] mpmath 40-50 digits;
[VERIFIED-float] float64 check; [TEXT] statement read from a source (location given); [REFEREE] pending independent review.
L0 class: Descriptive. FL tier: Full. Pre-registered claims: `claim.md`.

## 0. Notation and the three local notions

rho on C^d, P_+ the support projector (rank r), P_0 = 1 - P_+. Outcomes E_k are fixed (theta-independent).
Regular outcome: p_k(theta0) > 0. Null outcome: p_k(theta0) = 0, equivalently E_k rho = 0.
N_E,ab = Re tr(E L_a rho L_b) is the whole QFI contribution of E. F^Q_ab = Re tr(rho L_a L_b).
For a regular outcome, D_k = N_k - dp dp^T / p is positive semidefinite (Cauchy-Schwarz; [PROVED]).

Three local notions at theta0:
- (P) point CFIM: F_pos = sum over regular outcomes of dp dp^T / p (null outcomes contribute 0).
- (L) direction-wise limit: F_L(h) = lim_{t->0} CFIM(theta0 + t h), null outcomes included at their own probabilities.
- (H) Hellinger quadratic form: H_quad(h) = lim_{t->0} t^-2 sum_k (sqrt p_k(theta0 + t h) - sqrt p_k(theta0))^2.

## 1. Decisive check: Nurdin Example 2 (arXiv:2405.01471 v1, p. 11), numbers

Model: D = 1/2, c = (1, 7/10), theta0 = (3/10, 3/5). The specified POVM is the canonical form of Theorem 2 (regular
projectors on the support eigenbasis, null projector on the kernel), reconstructed from the printed Theorem 2 and
the printed Section 4 of v5; the printed paper does not write the POVM elements of Example 2 [TEXT, explorer A].

| quantity | value | evidence |
| --- | --- | --- |
| F^Q(theta0) | [[5.2869047619, 0.3675],[0.3675, 0.25725]] | [VERIFIED-mp] |
| F_pos (point CFIM) | diag(4.7619047619, 0) | [VERIFIED-mp] |
| F^Q - F_pos | N = [[21/40, 147/400],[147/400, 1029/4000]] = 0.525 [[1, 0.7],[0.7, 0.49]], rank one | [VERIFIED-exact] |
| p_null(theta) | 2 (1 - theta_1) g^2 (1 - cos(c.(theta - theta0))), g^2 = 3/16 | [VERIFIED-exact] (symbolic), error 5e-52 [VERIFIED-mp] |
| Hess p_null(theta0) | N/2 | [VERIFIED-exact] |
| lim_{t->0} CFIM(theta0 + t h) (regular plus null) | equals F^Q for h = (1,0), (0,1), (1,1), (1,-2), all with c·h ≠ 0; for c·h = 0 the limit is F_pos (decision.md A7); error linear in t | [VERIFIED-mp] |
| lim_{t->0} H_quad(h) vs F^Q(h,h)/4 | agree to O(t), e.g. 1.32172606772 vs 1.32172619048 at t = 1e-7 | [VERIFIED-mp] |

Reading. The null outcome has zero probability at theta0, but its probability grows quadratically, and its classical
contribution along h is (d_h p)^2/p -> h^T N h. So the point CFIM misses N, while the limit CFIM (L) and the Hellinger
form (H) recover N. Consequently the specified POVM is point-suboptimal and limit-optimal.

## 2. Source conventions (what the papers actually define)

Verified quotes (explorer reports, checked by search where marked):
- arXiv:2405.01471 v1, p. 4: F_{theta,c} is written as E[d ln p d ln p] = sum_k p_k (d ln p_k)^2, i.e. the expectation
  form, with k running over all outcomes (null included). No convention for p_k = 0 is stated [TEXT].
- arXiv:2405.01471 v1, p. 7: "a null component is given by Re tr(rho L_l E^n_k L_m). As shown in [11], saturation of the QCRB is
  equivalent to each regular and null POVM operators separately saturating their corresponding regular and null components
  of the QFIM elements." [11] = Ref. [29] (below). [TEXT]
- arXiv:2402.11567 v5, Sec. 2 and Sec. 6: the same expectation form; the null part is again taken from the saturation theorem. [TEXT]
- arXiv:1806.07337 v3 (Yang, Pang, Zhou, Jordan, PRA 100, 032104 (2019)) [search-verified]: "null operator will make the CFIM
  elements ill-defined and therefore some regularization is required when calculating their contributions to the CFIM."
  Their regularization is the limit F^k_ij = lim g^k_ij / h^k along approaches to the point (their Eq. (23)); their
  expansion (Eq. (32)) is direction-dependent; their Theorem 2 null condition (Eq. (44)) requires real proportionality
  independent of the eigenstate index, which is the direction-independence needed for the limit to be a single matrix [TEXT, explorer B].
- arXiv:2601.21801 v1 (Yang, Imai, Pezzè): Eq. (1) is written for all omega without a case distinction; Eqs. (2)-(3)
  reproduce the conditions of [29] with xi and eta; no own convention for p = 0 [TEXT, explorer B].

Consequence. The source's CFIM is written pointwise (expectation form, zero contribution from p_k = 0), while its null-outcome
saturation theorem is taken from a limit convention. These two are inconsistent unless null contributions are read as limits.
The limit reading makes the printed null conditions correct; the pointwise reading makes them incorrect (section 4).

## 3. Dichotomy identities ([PROVED] and checked)

Let theta0 be interior, the family smooth, rank rho_theta constant near theta0 (added 2026-10-21 after referee review: without it D1-D3 fail, see decision.md A1), and E a null outcome.

D1 (Hessian): Hess_ab p_E(theta0) = N_E,ab / 2.
Proof: differentiate dRho_a = (rho L_a + L_a rho)/2 in direction b and sandwich with E; terms with E rho or rho E vanish;
tr(E d_b d_a rho) = (1/4)[tr(E L_b rho L_a) + tr(E L_a rho L_b)] = (1/2) Re tr(E L_a rho L_b). [VERIFIED-mp] six random models,
relative error <= 1e-41; symbolic for Example 2.

D2 (direction-wise limit): for h^T N_E h > 0,
lim_{t->0} (grad p_E)(grad p_E)^T / p_E at theta0 + t h = (N_E h)(N_E h)^T / (h^T N_E h).
Proof: p_E(theta0 + t h) = (t^2/2) h^T H h + o(t^2), grad p_E = t H h + o(t), H = N_E/2. [VERIFIED-mp] (<= 1e-22).
Note: the matrix limit depends on the approach direction h unless N_E is rank one, but its quadratic form does not.

D3 (Hellinger): lim_{t->0} t^-2 sum_k (sqrt p_k(theta0 + t h) - sqrt p_k(theta0))^2 = (1/4) h^T (F_pos + sum_null N_E) h.
[VERIFIED-mp] (<= 1e-23).

D4 (QFI decomposition): F^Q = F_pos + sum_null N_E + sum_reg D_k for any POVM with sum E_k = I. [PROVED] and
[VERIFIED-float] (error 1e-14).

Consequence: the point CFIM is lower semicontinuous at theta0 and jumps at that point: nearby CFIM values include the null terms.

## 4. Saturation criteria per notion, and what the printed conditions correspond to

- Regular outcomes (all notions): D_k = 0 iff E(L_a - c_a) P_+ = 0 for real c_a, with c = 0 allowed. This is Theorem A and equals
  [29] Thm 1, Eq. (39): Pi_k L_i |psi_n> = xi^k_i Pi_k |psi_n>, xi real (the xi sits on the L side and may vanish).
  The printed Eq. (2) of arXiv:2601.21801 v1 places xi on the other side, which divides by <pi|L|psi> and therefore excludes xi = 0.
  This is a transcription difference from its source, not a different criterion [VERIFIED-exact; the Example 2 projector
  |psi><psi| has c_2 = 0 and saturates].
- Null outcomes, point notion (P): N_E = 0, i.e. E L_a rho = 0 for all a (strict condition).
- Null outcomes, limit notion (L) of [29]: N_E must have rank at most one, so that the direction-wise limit is a single matrix
  (Eq. (44)). Lemma 4.1: N_E has rank at most one iff the kernel-support rows r_a are real multiples of one common vector,
  i.e. pairwise one-sided proportionality E B_l = c E B_m or E B_m = c' E B_l with real c, c' [PROVED; VERIFIED-mp, Z8: 6/6 models].
- Null outcomes, Hellinger notion (H): unconstrained.
- Printed null conditions: Nurdin v1 Thm 1(2) Eq. (9), [29] Eq. (44), arXiv:2601.21801 v1 Eq. (3), and corrigendum v5 Condition 2' (its
  null part, Eq. (18)) are all written for ALL ordered pairs with FINITE real constants. This literal form excludes the one-sided case
  (a kernel vector coupled to one parameter only) and is therefore too strong for (L). Their proofs carry the case
  "both columns zero" but not "exactly one column zero" (Nurdin v1 p. 10 [TEXT]).
  Verified on control point D (section 7): the literal form fails for 18/22 outcomes of the projective ONB and for 32/36 outcomes
  of the 36-outcome POVM; the one-sided form holds for every unordered pair in both POVMs (0 failures) [VERIFIED-exact].
- Hellinger triviality for quasi-pure models ([PROVED] and [VERIFIED-float]): if L^{++}_a = 0 for all a, the block POVM
  (support projectors plus an orthonormal kernel basis) has F_pos = 0 and sum over kernel basis vectors of N_k = F^Q,
  hence H_quad = F^Q/4. The Hellinger notion is therefore satisfied by a block POVM for every quasi-pure family with constant rank near theta0 (referee C6; A1) and cannot
  discriminate measurements. The limit notion (L) is not trivial, because each kernel vector needs a rank-one N_k.

Summary table (what is required for saturation):
| notion | regular outcomes | null outcomes |
| --- | --- | --- |
| (P) point CFIM (standard CRB at theta0) | Theorem A, c in R with 0 allowed | N_E = 0, i.e. E L_a rho = 0 |
| (L) multivariate limit of [29] | Theorem A | rank N_E <= 1 (one-sided proportionality) |
| (H) Hellinger form | Theorem A | none (block POVM always saturates for quasi-pure families) |

## 5. Geometric characterization (point notion, G1-G3) [PROVED] and [VERIFIED-float]

W(c) = {v : P_+(L_a - c_a) v = 0 for all a}; U = union over c of W(c).
G1: A POVM saturates (P) iff for every outcome k there is c^k with range(E_k) in W(c^k).
G2: v in U iff for each a, P_+ L_a v is a real multiple of P_+ v (zero if P_+ v = 0).
G3: a projective (P)-saturating POVM is an orthonormal basis inside U. The (L) version adds the rank-one condition for
kernel vectors; the (H) version drops it.
Checks (rank-one elements, decision.md L7): regular G1 positive 40/40 and negative 40/40, null negative 40/40 for each p; null G1 positive 30/30 and negative 30/30 for each p; G2 members, non-members, zero-branch members and non-members 25/25 each for each p (the earlier G2 200/200 check was vacuous, decision.md); identity
F^Q = F_pos + sum N_null + sum D_reg with worst error ≤ 3.6e-15 (random basis) and ≤ 3.6e-15 (block basis, null outcomes included) [VERIFIED-float, geometric_criterion_check.py].
Relation to the literature: G1 for regular and null outcomes is the element-wise content of [29] Theorems 1-2, and for
rank-one POVMs it is equivalent in content to the hollowization criterion of arXiv:2601.21801 v1 (Theorem 1, title "A geometric
criterion ..."). G1-G3 are therefore NOT new as equivalences; the new content is the explicit union U, the real-collinearity
form of G2, and the separation of notions in section 4. Formal equivalence with 2601.21801 Eqs. (4)-(5) is [PENDING].

## 6. Lemma 2 and projective measurements

Control point D (quasi-pure, K = 20): the 22-outcome projective ONB (H_9 blocks plus four kernel rows) attains F^C = F^Q
exactly [VERIFIED-exact, `point_D_projective_onb_check.py` in the projective-criterion folder]. Its regular outcomes have
kernel components, so block diagonality (Nurdin Lemma 2, v1 p. 7-8) fails already for projective point-saturating measurements.
Lemma 2 is refuted in the point and limit notions. Nurdin's Lemma 2 text is quoted in [TEXT, explorer A].

## 7. Proposition 6: readings at control point D

Printed Condition 2' (arXiv:2402.11567 v5, Sec. 6, Eq. (18)): E_k00 Y^dagger(d_l V~ - c^k_{lm} d_m V~) = 0 for l, m = 1..p,
for some POVM {E_k00} on the kernel with sum = I_{r0} and real constants c^k_{lm}. [TEXT, explorer A]. The constants are
"real" with no statement on zero or infinite values. Reduction: Y^dagger V = 0 and Y^dagger d_l V = B_l/2, so the kernel
condition is E_k00 (B_l - c^k_{lm} B_m) = 0 for every ordered pair (l, m).

Exact results ([VERIFIED-exact], `prop6_readings_check.py`):
- Literal (finite real c for every ordered pair): fails at D for 18/22 outcomes of the projective ONB (1152 failing ordered pairs)
  and for 32/36 outcomes of the 36-outcome POVM (480 failing ordered pairs).
- One-sided (for each unordered pair, E B_l = c E B_m or E B_m = c' E B_l): holds for all pairs in both POVMs (0 failures of 2640 and 4320).
- D saturates the point notion exactly (section 6).

Verdicts.
- P1: the printed literal Condition 2' is NOT necessary for pointwise saturation: D saturates and violates it. This refutes the
  printed claim that Conditions 1 and 2' are necessary and sufficient (part i of the corrected theorem) [VERIFIED-exact].
- P2: the one-sided reading is satisfied at D [VERIFIED-exact]. The necessity of the one-sided condition for quasi-pure
  saturating POVMs follows from Theorem A for regular outcomes and the rank-one null condition for null outcomes
  [PROVED; C8 of claim.md under [REFEREE] review].
- Correction (2026-10-21; referee C7; consistent with the H-CAT56-2 manuscript's Proposition 6): the literal necessity claim FAILS at D, because D saturates and violates the literal condition. The earlier sentence "Proposition 6, as printed (literal), holds" is withdrawn. The one-sided condition is not refuted by D. The literal Condition 2' is unsatisfiable at D for every kernel POVM with sum I (referee C7).

## 8. Novelty and priority (status)

- Element-wise criteria (Theorem A, regular and null): present in [29] Thms 1-2 (2019) and in arXiv:2601.21801 v1 Eqs. (2)-(3)
  (with the transcription and convention issues above). Not new.
- Direction-wise limit identity N = 2 Hess and the direction-dependent formula (D1, D2): present in [29] Eq. (32). Not new.
- Printed null conditions correspond to the limit convention (L) and are too strong in the literal form: the one-sided
  correction is a consequence of the rank-one characterisation (Lemma 4.1). Priority to be checked against 2601.21801 and 2602.12097.
- Hellinger triviality for quasi-pure block POVMs (section 4): verified; priority not checked.
- Lemma 2 refutation at control point D for projective measurements: verified; 2601.21801 contains no block-diagonality
  statement (search "block" returned 0 passages), but a full priority check against the literature is [PENDING].
- Prop 6 (literal): verified against the printed text; corrected reading not refuted.

## 9. Open items and limitations

- A0 and A0+ (dimension obstruction of the earlier record): notion-dependence not tested here. Under the limit notion the
  question becomes whether a kernel frame with the one-sided property exists; not computed.
- One-sided necessity (C8) is a proof sketch here and awaits the referee.
- Infinite outcome sets: not treated; the local limits assume finitely many outcomes.
- Operational meaning: (P) is the standard single-copy variance bound at theta0; (L)/(H) are Poisson-type local information
  from rare null events. The asymptotic interpretation is an analysis, not a theorem here.
- Numerical checks use one seed per configuration; exact checks cover Example 2 and control point D.

## 10. Evidence ledger (scripts and outputs in this folder)

- `example2_zero_probability_limits.py` -> `metrics/example2_zero_prob_limits_2026-10-21.json` (mp, Z1-Z4)
- `example2_limit_symbolic.py` (sympy exact: closed forms, limit, Hessian)
- `zero_prob_identities_random.py` -> `metrics/zero_prob_identities_2026-10-21.json` (mp, Z5-Z8, six models)
- `geometric_criterion_check.py` -> `metrics/geometric_criterion_check_2026-10-21.json` (float, G1-G2, identity)
- `prop6_readings_check.py` (Fraction, P1-P2 at control point D)
- `hellinger_block_triviality.py` -> `metrics/hellinger_block_triviality_2026-10-21.json` (float, section 4)
- `tests/test_h_cat56_cfim_convention.py` (6 tests, passing; round-1 fixes, decision.md section 9)
- [REFEREE] adversarial review received 2026-10-21 (agent a5542126409fd702e); verdicts in decision.md, sections 2 and 9.
