# ruff: noqa
"""EXPLORATORY (not pre-registered; recorded as such): trade-off between entry size and dim V.

Approach A of claim.md takes one of the 3 shortest kernel vectors per stage. Here the pick is a +-1 combination of
`c` vectors drawn from the `m` shortest independent kernel vectors, with m and c varied. For every finished tuple
the float dim V (SVD, relative tolerance 1e-8) and the max entry bit length are recorded. Any tuple that reaches
dim V >= 463 is written out for the separate exact verifier; nothing here counts as a PASS by itself.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "20260920-h-cat56-2-verification-gates"))
sys.path.insert(0, str(HERE.parent / "20260919-pcc-generic-quasipure-cat56-2"))
import orchestrator_independent_check as oc  # noqa: E402
import search_a as sa  # noqa: E402
from gate4_source_example import analyse  # noqa: E402


def build(seed: int, m: int, c: int, maxbits: int) -> tuple[list[list[int]] | None, list[int]]:
    rng = np.random.default_rng(seed)
    blocks = [[int(x) for x in rng.integers(-1, 2, size=sa.N)]]
    curve = [sa.bits(blocks[0])]
    for _ in range(1, sa.S):
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
        if curve[-1] > maxbits:
            return None, curve
    return blocks, curve


def float_dimv(blocks: list[list[int]]) -> int:
    kr = sa.K * sa.R
    bl = []
    for x in blocks:
        re = np.array([[x[c * sa.R + a] for a in range(sa.R)] for c in range(sa.K)], dtype=float)
        im = np.array(
            [[x[kr + c * sa.R + a] for a in range(sa.R)] for c in range(sa.K)], dtype=float
        )
        bl.append(re + 1j * im)
    scale = max(np.abs(b).max() for b in bl)
    bl = [b / scale for b in bl]
    rho, drho = oc.build_state(bl, np.array([1 / 3, 2 / 3]))
    return analyse(rho, drho, sa.R)["dimV_tol1e-08"]


def main() -> int:
    maxbits = 400
    out = HERE / "metrics" / "explore_a2.jsonl"
    t0 = time.time()
    for m, c in [(3, 1), (6, 2), (12, 3), (25, 4), (40, 6)]:
        for seed in range(1000 * m, 1000 * m + 8):
            blocks, curve = build(seed, m, c, maxbits)
            row = {"m": m, "c": c, "seed": seed, "bit_curve": curve, "built": blocks is not None}
            if blocks is not None:
                row["dimV_float"] = float_dimv(blocks)
                row["max_bits"] = max(curve)
                if row["dimV_float"] >= 463:
                    row["blocks"] = blocks
            with out.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(row) + "\n")
            print(
                m,
                c,
                seed,
                row.get("built"),
                row.get("dimV_float"),
                row.get("max_bits"),
                f"{time.time() - t0:.0f}s",
                flush=True,
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
