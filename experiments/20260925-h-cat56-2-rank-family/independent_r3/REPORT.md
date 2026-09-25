# Independent-code check of the r = 3 certificate (d = 23, s = 12): report and verdict

Verdict against `PREREG.md` (criteria fixed before the implementer started): **PASS**.
Evidence label: `[VERIFIED-independent-implementation, same-briefing-author]`, at most Medium on the independence ladder. Not U3.

## Who did what
- Implementer: a fresh `general-purpose` (Sonnet) agent, briefed only with the definitions and acceptance criteria, blind to the expected value (22), to `fp_certify.py` and its
  relatives, to any `metrics/` folder and to the r = 2 numbers. Its code: `cx_modp.py` (exact library, complex numbers as (re, im) residue pairs, no sqrt(-1) assumed),
  `run_exact.py`, `run_float.py`. The agent could not write this file (a tool policy for subagents) and returned the report as text; this file was written by me from
  that text after I re-checked it (below).
- Re-check by me (the audit rule: an agent's "verified" is my "inferred" until re-run): I re-ran both scripts. `exact_results.json` came out **byte-identical**, both logs identical
  apart from timing lines. A grep of its code for `20260919`, `20260920`, `fp_certify`, `exact_certify`, `h2_core`, `pcc_core`, `metrics`, `outreach` found nothing.
  Only a comment line (`# ruff: noqa ...`) was added to its three scripts afterwards; a re-run after that gave identical output.

## Results (d = 23, r = 3, k = 20, s = 12)
| check | independent code | my saved `fp_certify` value | agree |
|---|---|---|---|
| exact, p = 998244353, seeds 1, 2 | rank 507, dim V-perp 22 (both) | 22 | yes |
| exact, p = 1000000007, seeds 1, 2 | rank 507, dim V-perp 22 (both) | 22 | yes |
| float complex128 SVD, two seeds | dim V-perp 22; gap ratio 7.9e12 and 1.7e11, unique | 22 | yes |
| stage solution-space dims, j = 1..12 | 120, 111, 102, ..., 21 (= 120 - 9(j-1)) | identical list | yes |
| SLD equation, PCC on full 23 x 23 commutators, det QFIM != 0 | all hold, all four runs | all hold | yes |
| form of the SLD block | A_i = -2i B_i (found by solving, not assumed) | same | yes |
| negative controls | N1 corrupted entry: PCC fails on exactly the 11 pairs containing block 5; N2 duplicate block: det QFIM = 0; N3 s = 13: det QFIM = 0, dim V-perp stays 22 | (see claim.md addenda) | consistent |
| blind positive control d = 8, r = 2, s = 5 | dim V-perp 10 (rank 54), three exact runs and float | 10 (rank 54) | yes |

N3 is an independent confirmation of what the claim.md addenda say about s > s*: the implementer, who was not told about the kernel-dimension argument, reports a stage-13
solution space of dimension 12 (< 13), a singular QFIM, and observes on its own that B_13 must lie in the span of the earlier blocks.

## What this does and does not show
- Shows: a from-scratch implementation reproduces the same integers (dim V-perp = 22 on two primes and in float, plus the blind d = 8 control), so the value 22 for r = 3 is not
  an artefact of `fp_certify.py`'s particular code.
- Does NOT show: (1) independence of the DEFINITIONS (sigma, M, W, V and the tower), which both sides took from my write-up of arXiv:2601.21801; if that write-up mis-states the
  paper, both agree wrongly (for r = 2 the same definitions were cross-checked against the paper's own operators earlier, for r = 3 there is no additional check);
  (2) author independence: the implementer is a different model instance briefed by me; (3) an explicit Q(i) instance: the runs are generic random points mod p, so the passage to
  characteristic 0 still goes through the lifting lemma, which nobody has reviewed; (4) novelty; (5) anything for r = 4, 5.
- Small honest gap: exact V-rank is over F_p of the real coordinates. For p = 1000000007 (F_p[i] is a field) the implementer also computed the rank over F_{p^2} of the flattened
  complex stack and got the same numbers (507 and 54).
