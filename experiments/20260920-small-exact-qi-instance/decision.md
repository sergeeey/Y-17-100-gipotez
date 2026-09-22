# Small explicit Gaussian-integer instance: PASS-SMALL (2026-09-20)

Pre-registered in `claim.md` (`f8c365a`), `claim_addendum_A_prime.md` (`8aa060e`), `claim_addendum_A_double_prime.md` (`c4f347c`), all pushed before the run they govern.

## Result

An explicit instance exists: `instance_d22_r2_s16.jsonl` (seed 701082): 16 blocks B_1..B_16, each a 20 x 2 Gaussian-integer matrix, **all real and imaginary parts of absolute value at most 78**.
For the state rho = diag(1, 2, 0, ..., 0) with SLD blocks A_i = -2i B_i, in exact integer arithmetic:

| Check | Result | Method |
|---|---|---|
| PCC, B_i^dag B_j Hermitian, all 120 pairs | exact, holds | plain Python integers (`verify_instance.py`), and full 22 x 22 commutators (`verify_exact_Q.py`) |
| SLD/Lyapunov identity | exact, holds | `verify_instance.py` |
| det QFIM (16 x 16 integer matrix) | nonzero | Bareiss, and FLINT `fmpz_mat.det` |
| dim_R V | **463**, so dim V-perp = **21 < 22 = d** | (a) rank of the stack mod two primes p = 1 mod 4 (lower bound, `exact_certify` routines); (b) **exact integer rank over Q** of the 544 x 968 matrix [Re, Im] of the generators iW, iM (own code, no shared construction, gives both bounds), FLINT |

So the non-saturation obstruction of Observation 2 is realised by an object that anyone can verify in seconds (`python verify_exact_Q.py instance_d22_r2_s16.jsonl 701082`, needs numpy and python-flint). The lifting lemma is no longer needed for the existence of a Q(i) instance.

Also, the V-builder is now validated by a control that can fail: `experiments/20260920-h-cat56-2-verification-gates/gate4b_lmcc_in_vperp.py`. The eight projectors of the paper's own saturating measurement (End Matter, Eqs. 34-41) satisfy `<pi|G|pi>` about 1e-16 for all 12 generators of V, sum to identity (1e-16) and give F^C = F^Q to 1e-15, whereas a random vector violates the conditions by 0.4 to 0.7.

## How it was found (honest account, in order)

1. Approach A as frozen (one of the 3 shortest kernel vectors per stage): 200 tuples, entries in {-1,0,1}, exact PCC and nonsingular QFIM in every one, but exact stack rank 229 to about 310. FAIL by the criteria.
2. Exploratory grid (not pre-registered), then A' (registered, 252 runs): larger pool of short vectors combined per stage raises the rank; best 456 (exact rank 456 = float 456 on the best tuple), no tuple at 463. FAIL by A's criteria.
3. A'' (registered): resample the tail of the 5 best A' tuples. 390 builds finished before I stopped the run at the first verified PASS; 62 of them reached float dim V = 463 with entries of at most 11 bits. This high rate is expected, not suspicious: the greedy rule replaces the start tuple by any improvement, so later resamples start from tuples already at or near the maximum, and 463 is the generic value, so once reached the rate is high.
4. Two candidates (seeds 706923 max entry 130, and 701082 max entry 78) verified exactly; 701082 saved as the instance.

Stated priors were 5 percent (A), 15 percent (A'), 30 percent (A''); the last one hit.

## What this does and does not show

- Removes: the dependence on the lifting lemma and on same-author F_p reasoning for existence over Q(i). Adds: a concrete file for the authors and for any independent reader.
- Does NOT remove: dependence on Observation 2 and on the Hollowization Theorem (proof reading recorded in `20260920-h-cat56-2-verification-gates/proof_and_scope.md`; the null-outcome condition depends on Ref. [29]); does not settle novelty; all code is still one author's, though verification uses two unrelated exact methods and a control on the paper's own example.
- Not a claim that this instance is typical: it was selected by search. For existence that is irrelevant.
- The selection rule (maximise float dim V, then verify exactly) means no statistical statement about how common such tuples are.

## Status delta

H-CAT56-2: explicit exact instance now exists (previously "exact Q(i) certificate absent"). Label stays `INTERNALLY VERIFIED / NOVELTY UNRESOLVED`; verification_strength stays `medium` until an independent party reproduces it.
The email draft and the lemma packet remain valid; the package for the authors can now include this instance (new version, recorded separately).
