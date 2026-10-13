"""Control systems for the round-2 counter.  Rational data copied from arXiv:2508.02321 (eqs. (2),(3),(4),(15))."""

from fractions import Fraction as Fr

import numpy as np

from lc2_core import canon_zones
from pwl_r1 import Zone, hy_zones


def zones_from_AB(AR, bR, AL, bL):
    f = lambda M: (
        np.array([[float(x) for x in r] for r in M])
        if hasattr(M[0], "__len__")
        else np.array([float(x) for x in M])
    )
    return Zone(f(AR), f(bR)), Zone(f(AL), f(bL))


# HY, paper eq (2): line x=0 in the paper's coordinates (system (1) with x1<=0 -> L)
HY2 = dict(
    AR=[[Fr(19, 500), Fr(-1, 10)], [Fr(1, 10), Fr(19, 500)]],
    AL=[[Fr(1), Fr(-5)], [Fr(377, 1000), Fr(-13, 10)]],
    bR=[Fr(19, 500), Fr(1, 10)],
    bL=[Fr(1), Fr(377, 1000)],
)
FPTT21 = dict(
    AL=[[Fr(-1, 4), Fr(-1)], [Fr(65, 64), Fr(0)]],
    AR=[[Fr(3276710, 13106841), Fr(-1)], [Fr(174473488105306, 171789280999281), Fr(0)]],
    bL=[Fr(260534, 1045519), Fr(-65, 64)],
    bR=[Fr(-260534, 1045519), Fr(-96440395023695996806, 95571015330487000887)],
)
GRS = dict(
    AL=[[Fr(-1, 5), Fr(1)], [Fr(-1), Fr(-1, 5)]],
    AR=[[Fr(3, 8), Fr(1)], [Fr(-1), Fr(3, 8)]],
    bL=[Fr(1, 250), Fr(-51, 50)],
    bR=[Fr(1159, 1000), Fr(-14333, 2000)],
)
# Lienard canonical data (paper (15),(17),(18))
HY_CANON = dict(
    TL=Fr(-3, 10),
    DL=Fr(117, 200),
    aL=Fr(-117, 200),
    TR=Fr(19, 250),
    DR=Fr(2861, 250000),
    aR=Fr(-2861, 5000),
    b=Fr(9, 10),
)
FPTT_CANON = dict(
    TL=Fr(-1, 4),
    DL=Fr(65, 64),
    aL=Fr(65, 64),
    TR=Fr(3276710, 13106841),
    DR=Fr(174473488105306, 171789280999281),
    aR=Fr(96440395023695996806, 95571015330487000887),
    b=Fr(-521068, 1045519),
)
GRS_CANON = dict(
    TL=Fr(-2, 5),
    DL=Fr(26, 25),
    aL=Fr(-637, 625),
    TR=Fr(3, 4),
    DR=Fr(73, 64),
    aR=Fr(-60809, 8000),
    b=Fr(231, 200),
)


def zones(d):
    return zones_from_AB(d["AR"], d["bR"], d["AL"], d["bL"])


def canon(d):
    return canon_zones(*[float(d[k]) for k in ("TL", "DL", "aL", "TR", "DR", "aR", "b")])


def all_controls():
    c = {}
    c["HY_original_shifted"] = hy_zones()
    c["HY_paper_eq2"] = zones(HY2)
    c["HY_canonical"] = canon(HY_CANON)
    c["FPTT21_paper_eq3"] = zones(FPTT21)
    c["FPTT21_canonical"] = canon(FPTT_CANON)
    c["GRS_paper_eq4"] = zones(GRS)
    c["GRS_canonical"] = canon(GRS_CANON)
    c["ONE_CYCLE_continuous_lienard"] = canon_zones(-2.0, 5.0, 0.5, 0.5, 1.0, 0.5, 0.0)
    c["NEG_global_stable_focus_linear"] = canon_zones(-0.4, 1.5, 0.5, -0.4, 1.5, 0.5, 0.0)
    c["EXTRA_both_traces_negative_with_jump_b"] = canon_zones(-0.5, 1.0, 0.7, -0.3, 2.0, -0.4, 0.3)
    c["NEG_stable_focus_b0"] = canon_zones(-0.5, 1.0, 0.7, -0.3, 2.0, 0.4, 0.0)
    c["DEGEN_center_both_G_identically_0"] = canon_zones(0.0, 1.0, 0.5, 0.0, 2.0, 0.5, 0.0)
    return c
