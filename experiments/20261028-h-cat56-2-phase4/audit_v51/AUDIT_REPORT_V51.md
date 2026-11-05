# Independent audit of package V5.1 (2026-11-03) - record

Verdict: VERIFIED-CONDITIONAL. Not human-refereed. Scope: finite POVM, D1, theta=0, one copy. Nothing here changes the status of any registry node.

Contents of this folder: this report, my own scans (`m1_scan.py`, `m2_subsets.py`; run `python -I <script> <unpacked V5.1 package dir>`), and the two quick-check logs of the authors pipeline rerun from a clean extraction (`qc_c1.log`, `qc_c2.log`, both end in `QUICK_CHECK: ALL_PASS`). The extracted package copy and the original zip are not stored here (local audit folder outside the repo).

Open follow-ups named by the audit: (1) human referee for lemma A1 (`A1_CHECK.md` in the package) and PROOF_MAP rows 3-4; (2) D is rebuilt on every run from float `eigh` with `default_rng(0)` and rounded to 1e-6 (three copies of the recipe: `g1_data.py`, `g1_exact_chain.py`, `g1_rederive_indep.py`) - not frozen as a file, cross-environment rerun not done; (3) negative controls on chart 1, the 12 eleven-subset certificates (`search64/verify_found11.py`), full Y_q recomputation and the Dockerfile were not run; (4) novelty unknown.

---

# Audit report V5.1 (2026-11-03) — H-CAT56-2, S- = {4..15}, finite POVM, D1, theta=0, one copy

Verdict: VERIFIED-CONDITIONAL (math chain consistent, no gap found; NOT human-refereed; shared inputs not re-derived).
Nothing committed/sent/published; originals, GitHub, registry untouched. Work copy: D:\audit_v51_2026-11-03\x (extracted from the zip, sha 22957b8f...6b7ce).

| # | Claim | Status | Basis |
|---|---|---|---|
| 1 | Package integrity: archive SHA, 318 manifest entries, no mismatch/extra | CONFIRMED | own hash script |
| 2 | D1 definitions, integer blocks, Areal rank 40, H' Hermitian, Tr H' = -330941/1000000 | CONFIRMED | mine/m1_scan.py |
| 3 | Lemma A1 (Cauchy-Schwarz, real lambda, p_k=0 under D1, I20 = sum y y^H) | CONFIRMED by independent hand derivation; no human referee | read, step by step |
| 4 | Charts cover CP^1 (phase+scale, |x1|>=|x2|); SOS identity => y^H H' y >= t|y|^2 on fibre | CONFIRMED on paper (B^ mu = 0 kills B^T N terms) | not machine-checked |
| 5 | Chart 1 and chart 2: exact left null space, X*Op_N=0, X*Op_G==R_int, ranks, ball PD of Y_q-eps I, residual, correction bound < eps, 1170-equation residual | CONFIRMED (author pipeline rerun from clean extraction, ALL_PASS both charts) | qc_c1.log, qc_c2.log; same environment as authors (numpy 2.3.4, flint 0.9.0) |
| 6 | Negative controls | CONFIRMED chart 2 (4/4 rejected); chart 1 not run -> INCONCLUSIVE | qc_c2.log |
| 7 | Numeric scan of final inequality (own code) | corroboration only: min lambda 0.0049 (chart 1), 0.0072 (chart 2), fibre dim 4 everywhere; sampled, not a global bound | m1_scan.py |
| 8 | Consistency with 11-subsets: H' negative on all 12 fibres (-0.28..-0.40) | CONFIRMED numerically | m2_subsets.py |
| 9 | 12 eleven-subset POVM certificates, full Y_q recomputation, Dockerfile, explicit rational y* | INCONCLUSIVE (not run) | |
| 10 | Shared inputs: blob, recipes for G, D (float-derived), rounding of H' | INCONCLUSIVE; D depends on float eigh/rng, other library versions untested | |
| 11 | Novelty | UNKNOWN_PRIOR_ART | |

Package defects: A2_STATUS.md is stale ("not complete"); quick-check steps 1-2 use unconditional print needles (covered by step 4); control threshold in rederive changed after first run (disclosed by authors).
Missing links for full VERIFIED: human referee for A1 and rows 4/2-3; cross-environment rerun.
Next step: external theorist, not V6.
