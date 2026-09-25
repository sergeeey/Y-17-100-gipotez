# ruff: noqa  (style lint waived: independent implementer code kept as written; only this comment line was added)
import json
import sys
import time

import numpy as np

from cx_modp import build_tower, pipeline


def show(label, out):
    print("  ", label)
    for k_, v in out.items():
        print("     %-38s %s" % (k_, v))


def main():
    results = {}
    t0 = time.time()
    # ---- Task 1 : four exact runs ----
    for p in (998244353, 1000000007):
        for seed in (1, 2):
            Bs, dims = build_tower(23, 3, 12, p, seed)
            print("=== EXACT d=23 r=3 s=12 p=%d seed=%d  (t=%.0fs)" % (p, seed, time.time() - t0))
            print("   stage solution-space dims (j=2..12):", dims)
            out = pipeline(23, 3, 12, p, Bs, field_check=(p % 4 == 3))
            show("pipeline", out)
            out["stage_dims"] = dims
            results["d23_p%d_seed%d" % (p, seed)] = out
            sys.stdout.flush()

    # ---- Negative controls on (p=998244353, seed=1) ----
    p, seed = 998244353, 1
    Bs, dims = build_tower(23, 3, 12, p, seed)
    # N1: corrupt one entry of B_5 (index 4) by +1 in the real part
    Bc = [B.copy() for B in Bs]
    Bc[4][0, 0, 0] = (Bc[4][0, 0, 0] + 1) % p
    print("=== N1 corrupt B_5[0,0].re += 1")
    out = pipeline(23, 3, 12, p, Bc, compute_V=False)
    show("N1", out)
    results["N1"] = out
    # N2: replace B_12 by copy of B_11
    Bd = [B.copy() for B in Bs]
    Bd[11] = Bd[10].copy()
    print("=== N2 B_12 := B_11")
    out = pipeline(23, 3, 12, p, Bd)
    show("N2", out)
    results["N2"] = out
    # N3: s = 13
    Bs13, dims13 = build_tower(23, 3, 13, p, seed)
    print("=== N3 d=23 r=3 s=13  stage dims:", dims13)
    out = pipeline(23, 3, 13, p, Bs13)
    show("N3", out)
    out["stage_dims"] = dims13
    results["N3"] = out
    # N3b: other prime, other seed, to see whether it is seed/prime dependent
    for pp, sd in ((1000000007, 2), (998244353, 2)):
        Bs13b, dims13b = build_tower(23, 3, 13, pp, sd)
        print("=== N3b d=23 r=3 s=13 p=%d seed=%d stage dims last:" % (pp, sd), dims13b[-3:])
        outb = pipeline(23, 3, 13, pp, Bs13b)
        show("N3b", outb)
        results["N3b_p%d_seed%d" % (pp, sd)] = outb

    # ---- Task 4: d=8, r=2, s=5 ----
    for pp, sd in ((998244353, 1), (998244353, 2), (1000000007, 1)):
        Bs8, dims8 = build_tower(8, 2, 5, pp, sd)
        print("=== POSCTRL d=8 r=2 s=5 p=%d seed=%d stage dims:" % (pp, sd), dims8)
        out = pipeline(8, 2, 5, pp, Bs8, field_check=(pp % 4 == 3))
        show("d8", out)
        out["stage_dims"] = dims8
        results["d8_p%d_seed%d" % (pp, sd)] = out

    with open("exact_results.json", "w") as f:
        json.dump(results, f, indent=1, default=str)
    print("done in %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
