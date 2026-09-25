# Independent-code check of the r = 4 certificate (d = 31, s = 13), pre-registered 2026-09-25 before any run

Question type (EstimandOps L0): descriptive / existence check of an implementation, no causal layer.

## What is run
The from-scratch implementation written by the blind implementer for the r = 3 check (`../independent_r3/cx_modp.py`, `run_float.py`), UNCHANGED, called for (d, r, s) = (31, 4, 13)
through a thin driver (`run_r4.py`). Fresh blindness does not exist here: I know the value my own `fp_certify.py` reported (30), and I am the driver's author. What keeps the check meaningful:
the library was written by someone who never saw my code and was already validated by a blind control (d = 8 -> 10) and a match at r = 3; the prediction is fixed HERE, before the run;
the driver only passes parameters and prints the library's own outputs.

## Registered prediction and criteria (fixed now)
- Prediction (from the closed form r^2 + s + 1 and from `fp_certify`): dim V-perp = **30** for (31, 4, 13). Both are mine; this is a test of the independent code, not of a new number.
- **PASS**: on p in {998244353, 1000000007} with seeds {1, 2} (four exact runs) SLD equation, PCC on the full 31 x 31 commutators and det QFIM != 0 hold, all four give the SAME dim V-perp, it equals 30, and
  the float run (complex128 SVD, reported gap, two seeds) gives 30; stage solution-space dims equal `fp_certify`'s list [216, 200, 184, ..., 24] (216 - 16(j-1)).
- **Negative controls** (must be detected): N1 corrupt one entry of B_5 -> PCC fails; N2 B_13 := B_12 -> det QFIM = 0; N3 s = 14 -> report what happens (my prediction: stage-14 dimension 13 < 14, QFIM singular, dim V-perp = 30).
- **Plumbing sanity**: the driver also runs (23, 3, 12, one prime, one seed) and must give 22 (already known from the r = 3 check); if not, the driver is wrong and nothing else is trusted.
- **DISCREPANCY**: any other integer, or runs disagreeing with each other. Then no status change and neither number is trusted until explained.
- Label of a PASS: `[VERIFIED-independent-implementation, same-briefing-author]`, at most Medium; not U3.

## What this does NOT show
Same limits as the r = 3 report: shared definitions (my write-up of arXiv:2601.21801), generic mod-p points (no explicit Q(i) instance, lifting lemma unreviewed), a different model instance briefed by me, no novelty statement.
