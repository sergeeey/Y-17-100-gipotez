# Independent-code check of the r = 5 certificate (d = 41, s = 14), pre-registered 2026-09-25 before any run

Question type (EstimandOps L0): descriptive / existence check of an implementation, no causal layer.

## What is run
The blind implementer's library from the r = 3 check (`../independent_r3/cx_modp.py`, `run_float.py`), UNCHANGED, for (d, r, s) = (41, 5, 14) through thin drivers
(`run_r5.py`, `run_float_r5.py`; parameters and printing only, copied from the r = 4 drivers). Same standing as the r = 4 check: no fresh blindness (I know my own value and wrote the
drivers); what keeps it meaningful is that the library was written by someone who never saw my code, was validated by a blind control (d = 8 -> 10) and matches at r = 3 and r = 4, and that
every prediction below is fixed HERE, before the run.

## Registered predictions and criteria (fixed now)
- Main: dim V-perp = **40** for (41, 5, 14) (closed form r^2 + s + 1 = 25 + 14 + 1; my `fp_certify` also gave 40). Mine, not new information about the world; a test of the independent code.
- **PASS**: on p in {998244353, 1000000007}, seeds {1, 2} (four exact runs) SLD, PCC on the full 41 x 41 commutators and det QFIM != 0 hold, all four give the same dim V-perp, equal to 40;
  float run (two seeds) gives 40 with a unique gap; stage solution-space dims (j = 2..14) equal 360 - 25(j-1) = 335, 310, ..., 35.
- Controls: N1 corrupt one entry of B_5 -> PCC fails, on exactly the pairs containing block 5 (13 of them, since s = 14: 4 earlier + 9 later). N2 B_14 := B_13 -> det QFIM = 0 and
  **dim V-perp = 61**, the value of my pre-registered below-crossing control (41, 5, 13) (a prediction: at r = 4 the analogous value matched by coincidence of construction, here it is registered in advance).
  N3 s = 15 -> stage-15 nullity 14 < 15, det QFIM = 0, dim V-perp 40 (exact and float).
- Plumbing sanity: (23, 3, 12) through the driver must give 22 first.
- **DISCREPANCY**: any other integer, or runs disagreeing; no status change, neither number trusted until explained. **INCONCLUSIVE** if a run does not finish or a rank gap is not unique.
- Label of a PASS: `[VERIFIED-independent-implementation, same-briefing-author]`, at most Medium; not U3.

## What this does NOT show
Same limits as r = 3 and r = 4: shared definitions (my write-up of arXiv:2601.21801), generic mod-p points (no explicit Q(i) instance, lifting lemma unreviewed), a different model instance briefed
by me, no novelty statement. r = 5 is the largest rank checked; nothing about r >= 6.
