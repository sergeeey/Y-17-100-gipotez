import time, sys
import numpy as np
from exact3 import *
from cox import gram_from_L, L_from_edges
from cox2 import geom_validate

def star_edges(arms):
    e = {}; idx = 1
    for a in arms:
        prev = 0
        for _ in range(a):
            e[(prev, idx)] = 3; prev = idx; idx += 1
    return e, idx

def run(name, edges, n, expect):
    t = time.time()
    v = validate(n, edges)
    ve = vinberg_exact(n, edges)
    L = np.zeros((n, n), dtype=int)
    for (i, j), m in edges.items(): L[i, j] = L[j, i] = m
    g = geom_validate(gram_from_L(L))
    ok = v['ok'] and ve['finite']
    print("%-34s exact3.ok=%s vinberg_exact=%s | cox2.ok=%s | expect %s | %s | %.1fs" % (
        name, v['ok'], ve['finite'], g['ok_polytope'], expect,
        "PASS" if (ok == expect and (g['ok_polytope'] == expect)) else "*** MISMATCH ***", time.time() - t), flush=True)
    if v['ok']:
        print("      d=%d n_rays=%d ideal=%d nonsimple=%d fvec=%s euler=%d disjoint=%d" % (v['d'], v['n_rays'], v['n_ideal'], v['nonsimple_vertices'], v['fvec'], v['euler'], len(v['disjoint_pairs'])), flush=True)
    else:
        print("      reason:", v['reason'], flush=True)

which = sys.argv[1] if len(sys.argv) > 1 else "small"
if which == "small":
    # simplex positives (d=3..9): E10 = T(2,3,7)  (quasi-Lanner, d=9);  [3,3,6],[6,3,6] d=3 ; [4,4,4]; negatives: E11 = T(2,3,8) (sig (10,2)); chain [3,4,4,3]? 
    for nm, arms in (("E10 T(2,3,7)", (1, 2, 6)), ("E11 T(2,3,8) NEG", (1, 2, 7)), ("E9~ affine T(2,3,6) NEG", (1, 2, 5))):
        e, n = star_edges(arms)
        run(nm, e, n, nm.find("NEG") < 0)
    for nm, labs, exp in (("[3,3,6]", [3, 3, 6], True), ("[6,3,6]", [6, 3, 6], True), ("[4,4,4]", [4, 4, 4], True), ("[3,6,3]", [3, 6, 3], True),
                          ("[4,3,6]", [4,3,6], True), ("[6,3,3,3] NEG? (sig check)", [6,3,3,3], None)):
        e = {(i, i + 1): m for i, m in enumerate(labs)}
        if exp is None: continue
        run(nm, e, len(labs) + 1, exp)
    # d=4 negative: cycle of 5 with labels 3 (affine A4~) not hyperbolic
    e = {(i, (i + 1) % 5): 3 for i in range(5)}
    run("A4~ affine NEG", e, 5, False)
    # decomposable NEG
    run("two disjoint [3,3,6] NEG", {(0,1):3,(1,2):3,(2,3):6,(4,5):3,(5,6):3,(6,7):6}, 8, False)
elif which == "dim11":
    s = "0-1:inf 1-13:3 2-3:inf 3-13:3 4-5:3 4-6:3 4-8:3 6-7:3 8-9:3 9-10:3 10-11:3 11-12:3 12-13:3"
    e = parse_edges(s)
    run("dim11 E8~+A1~+A1~ pyramid (n=14)", e, 14, True)
    # negative: one label changed 12-13: 3 -> 4  (breaks the E10-type quasi-Lanner link) and expect not a polytope
    e2 = dict(e); e2[(12, 13)] = 4
    run("dim11 with 12-13:4  NEG", e2, 14, False)
    e3 = dict(e); e3[(1, 13)] = 6
    run("dim11 with 1-13:6 NEG", e3, 14, False)
