# ruff: noqa
"""Approach A (pre-registered in claim.md): sequential PCC tower, one SHORT kernel vector per stage.

Kernel lattice of C_j (integer, exact, python-flint nullspace + LLL); pick one of the 3 shortest LLL vectors
that is not real-linearly dependent on the earlier blocks (the kernel always contains the earlier blocks
themselves, so a dependent pick would be a degenerate tuple). Abort a run when any entry exceeds MAXBITS.
Writes the per-stage bit-length curve; a tuple is only saved if all s = S blocks were built.
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import flint
import numpy as np
import psutil

sys.set_int_max_str_digits(0)
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "20260919-pcc-generic-quasipure-cat56-2"))
import exact_certify as ec  # noqa: E402

try:
    psutil.Process().cpu_affinity(list(range(16, 24)))
    psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
except (AttributeError, psutil.Error, OSError):
    pass

K, R, S = 20, 2, 16
N = 2 * K * R
MAXBITS = 20000


def blocks_as_prev(blocks: list[list[int]]) -> list[tuple]:
    kr = K * R
    prev = []
    for x in blocks:
        br = [[x[c * R + a] for a in range(R)] for c in range(K)]
        bi = [[x[kr + c * R + a] for a in range(R)] for c in range(K)]
        prev.append((br, bi))
    return prev


def kernel_short(rows: list[list[int]]) -> list[list[int]]:
    m = flint.fmpz_mat(rows)
    nul, nullity = m.nullspace()
    vecs = []
    for j in range(nullity):
        col = [int(nul[i, j]) for i in range(N)]
        g = math.gcd(*col)
        vecs.append([x // g for x in col] if g else col)
    red = flint.fmpz_mat(vecs).lll()
    out = [[int(red[i, j]) for j in range(N)] for i in range(red.nrows())]
    out = [v for v in out if any(v)]
    out.sort(key=lambda v: sum(x * x for x in v))
    return out


def independent(blocks: list[list[int]], v: list[int]) -> bool:
    mat = flint.fmpz_mat(blocks + [v])
    return mat.rank() == len(blocks) + 1


def bits(v: list[int]) -> int:
    return max(abs(x) for x in v).bit_length()


def run(seed: int, budget_s: float) -> dict:
    rng = np.random.default_rng(seed)
    t0 = time.time()
    first = [int(x) for x in rng.integers(-1, 2, size=N)]
    blocks = [first]
    curve = [bits(first)]
    status = "built"
    for j in range(1, S):
        if time.time() - t0 > budget_s:
            status = "timeout"
            break
        rows = ec.constraint_rows(blocks_as_prev(blocks), K, R)
        vecs = kernel_short(rows)
        pick = None
        order = list(rng.permutation(min(3, len(vecs)))) + list(range(3, len(vecs)))
        for idx in order:
            if independent(blocks, vecs[idx]):
                pick = vecs[idx]
                break
        if pick is None:
            status = "no_independent_vector"
            break
        blocks.append(pick)
        curve.append(bits(pick))
        if curve[-1] > MAXBITS:
            status = f"abort_bits>{MAXBITS}"
            break
    return {
        "seed": seed,
        "status": status,
        "stages_built": len(blocks),
        "bit_curve": curve,
        "seconds": time.time() - t0,
        "blocks": blocks if status == "built" else None,
    }


def main() -> int:
    seeds = [int(x) for x in sys.argv[1:-1]]
    budget = float(sys.argv[-1])
    out = HERE / "metrics" / f"search_a_{seeds[0]}_{seeds[-1]}.jsonl"
    with out.open("a", encoding="utf-8") as fh:
        for sd in seeds:
            res = run(sd, budget)
            fh.write(json.dumps(res) + "\n")
            fh.flush()
            print(
                sd,
                res["status"],
                res["stages_built"],
                res["bit_curve"],
                f"{res['seconds']:.0f}s",
                flush=True,
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
