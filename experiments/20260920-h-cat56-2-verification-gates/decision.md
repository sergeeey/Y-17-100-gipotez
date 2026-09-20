# H-CAT56-2 verification gates (2026-09-20)

Not a new hypothesis: post-hoc gates on the H-CAT56-2 counterexample (`experiments/20260919-pcc-generic-quasipure-cat56-2`),
triggered by the goal-expansion report and an external write-up of "what I ran". Same claim, more scrutiny.
Evidence markers as in `proof_and_scope.md`. Author of every script here: the orchestrator (same model family as
the original agent), so none of this is external verification.

## Results

| Gate | What | Result | Marker |
|---|---|---|---|
| 4 | Published End Matter example of arXiv:2601.21801 (two qubits + ancilla), same generic pipeline. Scope of this control: it checks the SLD/QFIM code (eigenvalue set) and PCC/quasi-pure residuals only. It does NOT test the V-builder (52 >= 8 cannot fail, and there is no gap evidence at 12 rows). A control that could fail on V would check that the paper's saturating LMCC projectors lie in V-perp (not done) | QFIM eigenvalues match the published `diag(4, 4q+4(1-q)sin^2 t)` to 1e-14 at 3 parameter points; PCC and quasi-pure residuals < 5e-15. `dim V = 12`, `dim V-perp = 52 >= d = 8` (saturation not excluded, consistent with the paper's LMCC measurement). The paper prints no `dim V`, so 12/52 is a derived number, not a reproduced one | `[VERIFIED]` (QFIM), derived (dim V) |
| 21 | Same PCC tuple, spectrum p2 = 0.4, 0.1, 1e-3, 1e-6, d=22, r=2, s=16 | `dim V = 463`, `dim V-perp = 21` at every p2 and every tolerance 1e-6..1e-12. Says only that ranks are stable inside the rank-2 stratum; p2 = 0 is a different stratum (rank 1) and this is NOT a pure-state limit statement | `[VERIFIED]` |
| 13 | First size where the proven bound stops forbidding `dim V-perp < d`, r = 2..12 | d* = 22, 23, 31, 41, 54, 69, 85, 104, 125, 148, 173. Hand asymptotic `k > (r^2-r+1)(r^2+1)/(r-1)^2` is a lower estimate, ratio to the true k* falls from 1.33 (r=2) to 1.01 (r=12). No closed form for the exact d* claimed | `[VERIFIED]` (arithmetic on a proven bound), asymptotic `[INFERRED]` |
| 1 | Explicit Q(i) instance with exact rank | **Not produced.** FLINT nullspace+LLL removes the sympy failure at d <= 14 (not tried beyond) but not the growth: max bit-length of block entries is 221 (d=8,s=5), 1241 (d=10,s=6), 15541 (d=12,s=8), 76707 (d=14,s=9), wall time 0.04 s, 0.1 s, 1.3 s, 20 s. Extrapolation to d=22, s=16 is my judgement (the four points have different s and are non-firing configs, not a fitted curve); a d=22 run was started and stopped by me after ~20 min with no output, and no log of it was kept | `[VERIFIED]` (measurement) |
| 1' | Existence of a Q(i) point, by lifting the F_p certificate | Rigorous on paper (below), not machine-checked | `[PROOF]` |
| 3 / 8 | Proof of the non-saturation test and scope | see `proof_and_scope.md`. Null outcomes CHECKED against the source PDF (main text Eq.(3) + Supplemental S1.A/S1.B): null operators satisfy the M-condition automatically and the W-condition is equivalent to Eq.(3), so they lie in V-perp too. Remaining dependence: the iff between saturation and Eq.(3) is taken from Ref. [29] (PRA 100, 032104), not read | `[PROOF]` + `[DOCS, read]` |
| 10 | Regression tests | `tests/test_h_cat56_2_gates.py`, 5 passed in 0.9 s | `[VERIFIED]` |

## Lifting lemma (gate 1')

`fp_certify.py` (H-CAT56-2) builds the tower B_1..B_16 over F_p with the integer real/imag coordinates of each block as
unknowns. Stage j imposes `r^2 = 4` integer-linear rows per earlier block, so `C_j` has `4(j-1)` rows on `n = 80`
unknowns. The recorded F_p kernel dimensions are `80, 76, ..., 20 = n - 4(j-1)` for both primes (`fp_certify_d22_r2_s16.json`),
i.e. `C_j` has **full row rank mod p at every stage**.

1. Full row rank mod p gives a nonzero `4(j-1)`-minor `m_j`, a nonzero polynomial over Z in the earlier free coordinates.
2. On `{m_j != 0}` the kernel is parametrised rationally (Cramer) with denominator `m_j`; over Q the rank is at most the
   number of rows and at least the rank mod p, so it equals `4(j-1)` and the same parametrisation is valid in characteristic 0.
   This is the step the earlier docstring only checked against float kernel dimensions; here it follows from the row count.
3. All B_j are rational functions of the free coordinates t. `T(t) = det(QFIM) * (chosen 463-minor of the iW/iM stack)`
   is a rational function with denominators products of the `m_j`; its numerator N(t) reduces mod p (with `i -> sqrt(-1)`)
   to a nonzero value at the found F_p point, so N is not the zero polynomial.
4. Hence an integer t exists with `N(t) != 0` and all `m_j(t) != 0`. That is a Gaussian-rational state, PCC exact by
   construction, QFIM nonsingular, and stack rank over Q(i) at least 463. Real-independent Hermitian matrices are
   complex-independent, so `dim_R V >= 463`, `dim V-perp <= 21 < 22`.

So for the theorem only the lower bound is used; the exact value 463 (upper bound `dim V-perp >= 21`) is not needed.
Residual risk of the lemma: steps 1-4 are my derivation and have not been machine-checked or reviewed by anyone else.

## Assessment of the external write-up

Checked against my own runs:
- QFIM formula, `dim V = 12 / 52`, thresholds 22/23/31/41: reproduced. **Correct.**
- "Ranks and upper bound needed for an exact certificate": **overstated**, see above; only a lower bound is needed.
- "Reduction to a linearly independent POVM" in the proof: unnecessary (a basis among the vectors suffices).
- "Hollowization gives every rank-one outcome in V-perp": true, and now confirmed for null outcomes too from the PDF (S1.A/S1.B). At the time of the write-up neither it nor my own derivation had covered null outcomes; that gap is now closed down to a dependence on Ref. [29]. Also checked: the V-generators involve only L_i|psi_a> and <psi_b|L_j (sigma is supported on the support), so the arbitrary kernel-kernel block of the SLD does not matter.
- "Novelty: strongly plausible": my check is weaker. Semantic Scholar lists 4 citers of 2601.21801 (2602.12097, 2608.10490,
  2609.18558, 2504.06812); I read 2602.12097 (no `quasi-pure`) and the 2608.10490 abstract (single-parameter Heisenberg
  scaling, no counterexample); the other two are about semiclassical geometric tensors and were not read. Semantic Scholar
  returned zero citers for 2405.00405 (suspect, likely an indexing gap) and my INSPIRE query returned garbage.
  Conclusion unchanged: no prior counterexample found, `[WEAK]`, not certified.
- The external run could not test the H-CAT56-2 instance; here it is tested (gates 1, 21).

## Not done

- Machine-checked lifting proof or explicit Q(i) instance (gate 1 as originally worded).
- Independent implementation in another system (no Sage/Julia here; all code is still from one author).
- Adversarial search against the bound (gate 27), Lean (2, 25), reading Ref. [29] for the null-outcome convention.
- Ask the authors. Needs a fresh go for anything that leaves this machine.

## Status delta for the registry

H-CAT56-2 stays `INTERNALLY VERIFIED / NOVELTY UNRESOLVED`. What changed: existence over Q(i) is now argued by an explicit lifting
lemma (still same-author, unchecked), the published example reproduces the QFIM through the same pipeline, and the one proof gap
(null outcomes) was named and then closed against the source PDF, down to a dependence on Ref. [29].
