# Small explicit Gaussian-integer instance of the H-CAT56-2 counterexample: pre-registration

Frozen BEFORE any search code is run. Not edited afterwards; any change is a new version.

## L0 (EstimandOps) and Zero-Signal gate

- **Question type: descriptive / constructive.** "Does an explicit object with a stated property exist and can be found within a budget?" It is not a claim about the physical world and not causal.
- Entity: 16 Gaussian-integer 20 x 2 matrices B_1..B_16 (d = 22, r = 2, s = 16). Predicate: exact PCC (B_i^dag B_j Hermitian for all pairs), QFIM nonsingular, real dimension of V at least 463. Measurable outcome: exact-arithmetic verification, described below. All three present, so the gate passes.
- What this result would NOT mean: it would not prove novelty, would not remove the need to check Observation 2, and a failed search would NOT show that no small instance exists.

## Why this is worth trying and what to expect (honest prior)

Explicit instance = anyone can verify in seconds, and it removes the dependence on the lifting lemma (`experiments/20260920-h-cat56-2-verification-gates/lifting_lemma.md`).
Prior of PASS-SMALL I state now: about 5 percent. Reason: the sequential construction has bit growth 221, 1241, 15541, 76707 (d = 8, 10, 12, 14); a heuristic count for the last stage (60 linear conditions, 80 unknowns, quadratic coefficient growth) says small entries are not expected in generic position; and the counterexample must attain the lower bound `dim V-perp = 21` exactly, which structured (symmetric) instances tend not to. A global point count (1280 unknowns, 480 quadrics) suggests small points exist, but that is a heuristic that needs Birch-type conditions I have not checked. So this is a bounded attempt, not an expectation.

## Outcomes (fixed now)

- **PASS-SMALL:** a tuple with every real and imaginary part of every entry of |value| <= 2^31, passing all verification checks below.
- **PASS-LARGE:** a tuple with entries of at most 20000 bits, passing all checks, verifiable in under 5 minutes with FLINT.
- **FAIL:** neither within the budget. FAIL does not say no small instance exists. It changes nothing about the status of H-CAT56-2; the lifting lemma remains the route.
- **INCONCLUSIVE:** a search run that dies for a resource reason (crash, out of memory). It is re-run once, then counted as FAIL.

## Verification checks (all exact integer arithmetic, no floating point; PASS requires all)

1. PCC: for all 120 pairs i < j, the 4 real equations of "B_i^dag B_j Hermitian" evaluate to exactly 0.
2. SLD/Lyapunov identity for the state rho = diag(1, 2, 0...0) with A_i = -2i B_i holds exactly.
3. QFIM matrix (16 x 16 integers) has determinant nonzero exactly.
4. The stack of iW, iM vectors built from the full 22 x 22 definitions has rank at least 463 modulo two distinct primes p = 1 mod 4 (a valid lower bound over Q(i)). The float SVD gap ratio is also reported.
5. The verifier is a script separate from the search script (`verify_instance.py`), run on the saved file only.

## Approaches, budget, stop rules

Total wall-clock budget for the whole experiment: **90 minutes**. Resources: at most 3 processes, cores 16-23, below-normal priority (the project's standing limit).

- **A. Shortest-vector sequential construction** (FLINT nullspace + LLL): at each stage take a single short vector (one of the 3 shortest) of the kernel lattice instead of a random combination of the whole basis. Randomised restarts, at most 200. Abort a run when any block entry exceeds 20000 bits. Records the bit-length curve per stage.
- **B. Small-alphabet local search:** entries in {-1, 0, 1} + i{-1, 0, 1}, objective = number of violated exact equations; simulated annealing, at most 30 minutes in total. Any zero-violation tuple goes to the verifier.
- **C. Rounded-float correction:** take a float solution, scale and round, then try to repair exactly with integer kernel lattices block by block (closest vector in the kernel lattice). At most 30 minutes.

Stop rules: stop when a PASS is verified; stop at the time budget; do not start another approach after the budget expires; do not extend the budget without a new pre-registration.
Order: A, then B, then C. A only writes bit-length curves; B and C only produce an instance if their tuple passes the separate verifier.

## Not part of this experiment

An independent second implementation of the whole pipeline (item 2 of the plan) is not started until this experiment has a result.
