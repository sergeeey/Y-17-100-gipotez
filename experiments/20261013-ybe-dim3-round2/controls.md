# controls.md -- 20261013-ybe-dim3-round2

| id | control | result | marker |
|---|---|---|---|
| P1 | shift family (witness (2,3,5,7,11) + 3 random rationals): vertex YBE exact residual 0 entries, and Rbraid = P*Rvertex exact braid residual 0 entries (s01_shift_vs_cand.py, sympy over Q) | PASS (0 nonzero entries in all 4) | [VERIFIED] |
| P2 | spectrum of cand88/cand101 unchanged under random (g(x)g) conjugation | PASS | [VERIFIED] |
| N1 | comparison can return both answers: Id -> (9), flip -> (6,3), shift witness -> (3,3,3); cand101 -> (7,2), cand88 -> (2,2,2,1,1,1) | PASS (invariant separates five different cases) | [VERIFIED] |
| N2 | closed-form family with ONE entry perturbed by 1%: braid residual 5e-4 (vs 1e-17) | PASS | [VERIFIED] |
| P3a | sampler (expm(X), tr X=0, holomorphic LM, generic Gaussian starts, scale 1.0, n=1500, dim 2): hits H3,1, H2,1, H2,2, the (2,2)+(2,2) class H1,1/H1,2/H0,2, Id, and the U(1)-free family H1,4 (dimL=1) 21 times | PASS for diagonalisable families incl. one U(1)-free family | [VERIFIED] (signature match, not an explicit conjugacy) |
| P3a' | same, Jordan-type H2,3 and H0,1 | FAIL: 0/1500 (known blind spot, as in round 1) | [VERIFIED] |
| P3b | sampler (dim 3, scale 0.7, n=150, 114 converged): rediscovers Id (32), generic Hecke (8,1) (67), SCC/ACC-type (7,2) dimL=3 (6), and 3 weak-charge (7,2) dimL=2 tangent-dim-11 solutions (the cand101 type) from UNMASKED starts | PASS for the weak-charge region | [VERIFIED] |
| P3c | same sampler, U(1)-free Gaussian G1/G2 (dimL=1, spectrum (3,6)) | FAIL: 0/114 converged (0/150 starts); rule-of-three 95% upper bound on the hit rate 2.6% per converged start | [VERIFIED] -> sampler NOT validated for the dim-3 U(1)-free region; no negative statement made about it |
