# ruff: noqa
"""A'' search frozen in claim_addendum_A_double_prime.md: prefix resampling around the best A' tuples."""
import json, sys, time, glob
from pathlib import Path
import numpy as np
import explore_a2 as e
import search_a as sa

HERE = Path(__file__).parent
MAXBITS = 400


def build_from_prefix(prefix, seed, m, c):
    rng = np.random.default_rng(seed)
    blocks = [list(b) for b in prefix]
    curve = [sa.bits(b) for b in blocks]
    for _ in range(len(blocks), sa.S):
        rows = sa.ec.constraint_rows(sa.blocks_as_prev(blocks), sa.K, sa.R)
        vecs = sa.kernel_short(rows)
        pool = []
        for v in vecs:
            if sa.independent(blocks + pool, v):
                pool.append(v)
            if len(pool) >= m:
                break
        if not pool:
            return None, curve
        take = rng.choice(len(pool), size=min(c, len(pool)), replace=False)
        vec = [0] * sa.N
        for t in take:
            sgn = int(rng.choice([-1, 1]))
            vec = [a + sgn * b for a, b in zip(vec, pool[t], strict=True)]
        if not any(vec) or not sa.independent(blocks, vec):
            vec = pool[0]
        blocks.append(vec)
        curve.append(sa.bits(vec))
        if curve[-1] > MAXBITS:
            return None, curve
    return blocks, curve


def main():
    part = int(sys.argv[1])
    rows = [json.loads(l) for f in glob.glob(str(HERE / "metrics" / "aprime_part*.jsonl")) for l in open(f, encoding="utf-8")]
    top = sorted((r for r in rows if r["built"]), key=lambda r: -r["dimV_float"])[:5]
    starts = []
    for r in top:
        blocks, _ = e.build(r["seed"], r["m"], r["c"], MAXBITS)
        starts.append((r, blocks, r["dimV_float"]))
    out = HERE / "metrics" / f"aprime2_part{part}.jsonl"
    t0 = time.time()
    for si, (r, blocks, best) in enumerate(starts):
        if si % 3 != part:
            continue
        cur, cur_dim = blocks, best
        for t in (6, 8, 10, 12, 14):
            for m in (8, 10, 12):
                for c in (2, 3):
                    for k in range(12):
                        seed = 700000 + si * 10000 + t * 100 + m * 10 + c + k * 1000
                        nb, curve = build_from_prefix(cur[:t], seed, m, c)
                        row = {"start": si, "t": t, "m": m, "c": c, "seed": seed, "built": nb is not None}
                        if nb is not None:
                            row["dimV_float"] = e.float_dimv(nb)
                            row["max_bits"] = max(curve)
                            if row["dimV_float"] > cur_dim:
                                cur, cur_dim = nb, row["dimV_float"]
                                row["improved"] = True
                            if row["dimV_float"] >= 463:
                                row["blocks"] = nb
                        with out.open("a", encoding="utf-8") as fh:
                            fh.write(json.dumps(row) + "\n")
                        if row.get("dimV_float", 0) >= 463:
                            print("CANDIDATE", seed, flush=True)
                        if time.time() - t0 > 1700:
                            print("budget", flush=True)
                            return 0
        print("start", si, "final", cur_dim, f"{time.time()-t0:.0f}s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
