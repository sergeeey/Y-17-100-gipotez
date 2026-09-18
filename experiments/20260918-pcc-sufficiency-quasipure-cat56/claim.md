# claim.md — H-CAT56-1 (PCC-SUFFICIENCY-QUASIPURE-v1)

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | Random quasi-pure states `ρ_Δ` (Eq. 16 of Yang, Imai & Pezzè, arXiv:2601.21801: `ρ_Δ = (U_Δ⊗I)ρ_0(U_Δ†⊗I) = Σ_a q_a\|φ_a,Δ⟩⟨φ_a,Δ\|⊗\|a⟩⟨a\|`), small Hilbert space dimension `d` and parameter count `s`, chosen strictly BELOW the dimension threshold of the paper's own inequality (15). |
| **Falsifiable predicate** | Does the Partial Commutativity Condition (PCC, Eq. 8: `⟨ψ_a,Δ\|[L_i,L_j]\|ψ_b,Δ⟩=0` for all `i≠j,a,b`, `L_i` = symmetric logarithmic derivatives) hold for a sampled quasi-pure state WHILE the paper's own Observation 2 exact impossibility criterion (`dim(V^⊥)<d`, `V^⊥` = orthogonal complement of the span of vectorized `W_ij,ab`/`M_i,ab` operators — a pure rank/SVD computation, NOT a constructive search) CERTIFIES that saturation is impossible — i.e. does a counterexample to "PCC is sufficient for QCRB saturation, restricted to quasi-pure states" exist below the threshold where the paper's own Theorem 3 guarantees sufficiency? |
| **Measurable outcome** | For each sampled quasi-pure state: compute SLDs numerically, check PCC (explicit residual, not a bare boolean), and separately compute `dim(V^⊥)` via SVD (explicit rank with a documented singular-value tolerance). PCC-holds-with-margin AND `dim(V^⊥)<d`-with-margin, confirmed at increased numerical precision and by a second, independent reconstruction of the same physical state (different basis/parametrization, not reusing the first pass's tolerances/objects) = a CERTIFIED counterexample. **This is a one-directional test: `dim(V^⊥)≥d` does NOT certify saturability exists — it only means this specific fast check did not find a violation.** Zero certified counterexamples across the pre-registered sample is reported ONLY as "no counterexample found via this exact test under this sampling distribution" — NOT as evidence toward sufficiency (a positive sufficiency claim would need Theorem 3-style construction, out of scope below threshold). |

> Gate rule satisfied: entity, predicate, outcome all concretely specified from a
> directly-read primary source (arXiv:2601.21801, HTML full text, Eq. 8/15/16, Theorem
> 1/2/3), not a catalog paraphrase.

---

## L0: Question Type

- [x] Descriptive — "does a counterexample exist within a specific, bounded search space?"
- [ ] Predictive
- [ ] Causal

Existence-of-counterexample questions are descriptive: either a specific object with the
stated properties is found in the sampled space, or it is not — no population-level
causal or predictive claim is being made.

---

## Natural Language Statement

> We estimate whether the Partial Commutativity Condition (PCC) is sufficient for QCRB
> saturation, specifically for the class of quasi-pure states (Eq. 16), at Hilbert space
> dimension `d` and parameter count `s` chosen below the paper's own Theorem 3 threshold
> (inequality 15) — by direct numerical search for a counterexample among randomly
> sampled quasi-pure states, checking PCC and the exact hollowization criterion (Theorem
> 1) computationally rather than analytically.

---

## Source Trace (mandatory, AI-generated claim per FL Steps -4/-3, verified via direct fetch)

**Primary source:** Yang, Imai & Pezzè, "A geometric criterion for optimal measurements
in multiparameter quantum metrology", arXiv:2601.21801 (2026), `[VERIFIED]` via two
direct fetches of the HTML full text (not abstract-only, not a search-engine paraphrase).

**What the paper establishes, quoted/paraphrased from direct reads:**
- **Theorem 1** (exact iff-criterion for QCRB saturation by a rank-one POVM): a rank-one
  operator `E_ω=|π_ω⟩⟨π_ω|` saturates QCRB iff `⟨π_ω|W_ij,ab|π_ω⟩=0` and
  `⟨π_ω|M_i,ab|π_ω⟩=0` for all `i≠j,a,b`, where `W_ij,ab=L_iP_abL_j-L_jP_abL_i`,
  `M_i,ab=[L_i,P_ab]`, `P_ab=|ψ_a⟩⟨ψ_b|`.
- **Eq. 8 (PCC):** `⟨ψ_a,Δ|[L_i,L_j]|ψ_b,Δ⟩=0` for all `i≠j,a,b`.
- **Observation 2 / its consequence:** PCC is proven NOT sufficient for QCRB saturation
  IN GENERAL (already closed, not the target of this experiment).
- **The genuinely open piece, quoted directly:** "for generic quasi-pure states, whether
  PCC is sufficient or not is still open, as conjectured in Ref. [38]." — a DIFFERENT,
  narrower question than the already-resolved general case.
- **Theorem 3** gives an explicit iterative construction proving sufficiency ONLY when
  inequality (15) holds: `n ≥ max_{μ∈[1,2..d-2]} 2μ(d+1/2-μ)+(d-2)`, where `n` relates to
  the dimension of the orthogonal-complement subspace `𝒱^⊥`. Below this threshold,
  Theorem 3 does not apply and the paper does not claim sufficiency either way.
- **The paper does NOT provide a small explicit worked example below this threshold** —
  confirmed via direct fetch; this experiment's own sampled cases below the threshold are
  therefore genuinely unexplored territory in the published literature, not a re-check of
  an existing example.

---

## Claim Entropy

| Component | Count |
|---|---|
| Unsupported HIGH claims | 0 |
| Hidden assumptions | 0 (see HD-MAVP below) |
| Missing negative controls | 0 (positive control defined in controls.md: reconstruct a case ABOVE the Eq. 15 threshold where Theorem 3 guarantees sufficiency, confirm the harness agrees) |
| Ambiguous definitions | 0 |
| Unresolved blockers | 1 |
| **Total claim_entropy** | 1 |

> Unresolved blocker: exact numerical procedure for computing SLDs `L_i` for a
> parametrized quasi-pure state (Eq. 16) has not yet been implemented or verified in
> this project — no prior quantum-metrology code exists here to reuse.

---

## Counterfactual Frame

| Question | Answer |
|---|---|
| What must change for H to be true (a counterexample exists)? | Nothing beyond what's already established — the paper's own text says this is genuinely unknown, not merely unproven; a counterexample or its absence in a bounded sample is a direct, small-scale numerical question, no new physics needed. |
| How many independent changes required? | 1 — direct numerical instantiation of already-published, exact criteria (Theorem 1, Eq. 8), no new theory. |
| Known system where these conditions already hold? | The paper's own Section VII (two-qubit + qubit ancilla) is a quasi-pure state example, but it sits at a specific point (`λ=0`) chosen for local optimality, not explicitly below the Eq. 15 threshold — not directly reusable as a below-threshold instance without checking its own `n` against the inequality first. |

**Verdict:** `within-framework`.

---

## Falsifiable Claim

**Claim:** Among randomly sampled quasi-pure states with `(d,s)` chosen below the Eq.
(15) threshold, PCC holds (with margin) while the paper's own exact Observation 2
impossibility criterion (`dim(V^⊥)<d`, a pure rank/SVD computation) certifies saturation
is impossible (with margin, robust to increased precision, independently reconstructed)
for at least one sampled instance — a genuine, certified counterexample to "PCC
sufficient for quasi-pure states."

**Check:** Numerically compute SLDs, PCC residual, and `dim(V^⊥)` via SVD for each
sampled instance; report the fraction where PCC holds with margin; among those, report
the fraction where `dim(V^⊥)<d` with margin. Any PCC-true/rank-deficient instance is a
CANDIDATE, promoted to a counterexample only after independent re-derivation (Step 6 in
the experiment's own protocol). A clean sample (no candidates) is reported as "no
counterexample found via this exact test" — explicitly not evidence for sufficiency,
since the rank test is one-directional (see Zero-Signal Gate above).

---

## HD-MAVP Decomposition

### Assumptions

| # | Assumption | Type | Role | Depends On | Evidence | Status |
|---|---|---|---|---|---|---|
| A1 | SLDs `L_i` for a quasi-pure `ρ_Δ` can be computed numerically by solving `(L_iρ+ρL_i)/2=∂_iρ` (a linear system in `L_i` for each parameter direction, standard in quantum metrology) | mathematical/tooling | core | — | standard technique, not yet implemented in this project | unknown |
| A2 | PCC (Eq. 8) and `dim(V^⊥)` (Observation 2's rank/SVD criterion, built from the vectorized `W_ij,ab`/`M_i,ab` objects) can both be evaluated as direct numerical checks on the computed `L_i`, `ψ_a`, `P_ab`, with a well-defined, PRE-REGISTERED numerical tolerance for "=0" and for rank-deficiency (singular-value threshold) | mathematical | core | A1 | direct consequence of the paper's own exact algebraic definitions; the rank test (not a constructive optimizer search) is the load-bearing choice here, per the correction below | alive |
| A3 | A random sampling scheme for quasi-pure states at small `(d,s)` below the Eq. 15 threshold can be constructed that is not pathologically degenerate (e.g. avoids exactly-repeated eigenvalues by construction, which would trivially satisfy or violate PCC for uninteresting reasons) | operational | belt | — | not yet designed | unknown |
| A4 | A negative finding (zero counterexamples in N samples) is informative, not merely "didn't search enough" — requires a pre-registered sample size and an honest LEAD (not CONFIRMED) framing per this project's own AOG discipline | operational | peripheral | — | matches this project's own established vocabulary for existence-search null results | alive |

**Principal Assumption (cut vertex):** A1 — if SLD computation cannot be implemented
correctly and verified (e.g. against a known closed-form case), nothing else in this
experiment can proceed.

### Constraints

- Constraint 1: Applies only to the quasi-pure state SUBCLASS (Eq. 16), not to general
  mixed states — the general case's insufficiency is already established and is not
  re-tested here.
- Constraint 2: A negative result (no counterexample found) is bounded by the sample size
  and the specific `(d,s)` pairs tested — does not extend to all `(d,s)` below threshold,
  let alone prove the conjecture for all quasi-pure states.

### Unknowns

- [U] Whether small `(d,s)` pairs below the Eq. 15 threshold are even numerically
  reachable with a well-conditioned SLD computation (small `d` may make some parameter
  directions ill-defined if `ρ_Δ` has degenerate eigenvalues at generic `Δ`).
- [U] Whether the paper's own Section VII example, if checked against Eq. 15 for its own
  `(d,s)`, happens to already sit below the threshold (would make it a reusable positive
  control rather than requiring a fresh above-threshold construction).

### Dependencies

- Dependency 1: catalog screening (2026-09-18) that surfaced #56, downgraded to
  `NEEDS-REATOMIZATION` pending a concrete unresolved subclaim — this experiment IS that
  reatomization, per the user's own explicit choice.
- Dependency 2: `ADR-123`'s two-part gate (source-traced to a specific real open
  question + open-access verified) — both legs satisfied via direct HTML fetch above.

---

## Pearl Card

**Prediction:** if a counterexample is found, it should appear at the SMALLEST tested
`(d,s)` below threshold, not require pushing close to the Eq. 15 boundary — insufficiency
(if real) is more likely a small-dimension phenomenon, matching how PCC's general
insufficiency (Observation 2) was itself demonstrated on a small case.

**Falsification:** this experiment's own "no counterexample found" report (if that is the
outcome) is wrong if a counterexample is later found at ANY `(d,s)` below threshold not
covered by this experiment's own sample — the search is inherently incomplete, and (per
the correction above) even a fully clean sample is NOT a LEAD toward sufficiency, only an
absence of this specific type of certified violation.

---

## What This Does NOT Mean

1. Does NOT resolve the conjecture for ALL quasi-pure states, all `(d,s)` — only the
   specific, pre-registered sample tested here.
2. Does NOT touch the ALREADY-CLOSED general (non-quasi-pure) insufficiency result
   (Observation 2) — that is settled, not re-tested.
3. A negative result (no counterexample found via the exact rank test) does NOT prove
   PCC is sufficient for quasi-pure states, and is explicitly NOT reported as LEAD-level
   evidence toward sufficiency — the rank test (`dim(V^⊥)<d` ⟹ impossible) is
   ONE-DIRECTIONAL per the paper's own Observation 2; `dim(V^⊥)≥d` never certifies that a
   saturating measurement exists, only that this specific fast check found no violation.
   A genuine positive-sufficiency claim would require Theorem 3-style construction, which
   is out of scope for this experiment below the Eq. 15 threshold.
4. Does NOT require or attempt to reproduce Theorem 3's own constructive algorithm above
   threshold — that is already proven; this experiment only searches BELOW it.
5. Does NOT treat an optimizer's failure to construct a saturating measurement as
   evidence of impossibility, anywhere in this experiment — impossibility is established
   ONLY via the exact `dim(V^⊥)<d` rank/SVD certificate (Observation 2), independently
   reconstructed, never via a non-convex search's non-convergence.

## MCID

MCID: a single CERTIFIED counterexample (PCC-true-with-margin AND `dim(V^⊥)<d`-with-
margin, robust to increased precision, independently reconstructed by a second pass not
reusing the first's basis/tolerances) is sufficient to answer the question in the
negative — no further confirmation needed once certified. A "candidate" that fails
independent reconstruction is NOT reported as a counterexample and does not count toward
the pre-registered sample. For the "no counterexample found" outcome, MCID is the
pre-registered sample size (`N=200`, set in controls.md before running) — and the report
language itself (not a threshold) is what prevents overclaiming: "not found" is stated
as exactly that, never as evidence of sufficiency.
