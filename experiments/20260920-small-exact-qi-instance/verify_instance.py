# ruff: noqa
"""Separate verifier (claim.md check 5): runs the exact checks of exact_certify.certify on a SAVED tuple only.

Usage: python verify_instance.py <jsonl file> <seed>
It reuses exact_certify.certify (already reviewed: exact PCC on full matrices, exact Lyapunov, exact QFIM
determinant by Bareiss, F_p rank of the stack of iW/iM from the FULL 22 x 22 definitions at two primes) by
replacing only its block-construction step with the saved blocks. It also reports plain-integer PCC as a
cross-check that does not use exact_certify's matrix helpers.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.set_int_max_str_digits(0)
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "20260919-pcc-generic-quasipure-cat56-2"))
import exact_certify as ec  # noqa: E402

K, R, S = 20, 2, 16


def plain_pcc(blocks: list[list[int]]) -> bool:
    kr = K * R
    for i in range(S):
        for j in range(i + 1, S):
            for a in range(R):
                for b in range(R):
                    # (B_i^dag B_j)_{ab} = sum_c conj(B_i[c,a]) B_j[c,b]
                    def n(a_: int, b_: int) -> tuple[int, int]:
                        re = im = 0
                        for c in range(K):
                            xr, xi = blocks[i][c * R + a_], blocks[i][kr + c * R + a_]
                            yr, yi = blocks[j][c * R + b_], blocks[j][kr + c * R + b_]
                            re += xr * yr + xi * yi
                            im += xr * yi - xi * yr
                        return re, im

                    r1, i1 = n(a, b)
                    r2, i2 = n(b, a)
                    if r1 != r2 or i1 != -i2:
                        return False
    return True


def main() -> int:
    path, seed = Path(sys.argv[1]), int(sys.argv[2])
    rec = None
    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row["seed"] == seed and row["blocks"]:
            rec = row
    if rec is None:
        print("no built tuple for that seed")
        return 2
    blocks = [[int(v) for v in x] for x in rec["blocks"]]
    max_abs = max(abs(v) for x in blocks for v in x)
    cross = plain_pcc(blocks)
    ec.build_blocks = lambda k, r, s, seed_, lll: (blocks, [0] * s)
    res = ec.certify(K, R, S, seed, True)
    res["plain_integer_pcc"] = cross
    res["max_abs_entry"] = max_abs
    out = HERE / "metrics" / f"verify_{path.stem}_seed{seed}.json"
    out.write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    keep = (
        "max_abs_entry",
        "plain_integer_pcc",
        "lyapunov_exact_zero",
        "pcc_exact_zero",
        "qfim_det_nonzero",
        "rank_mod_p",
        "need_dimV_ge",
        "exact_certified_dimVperp_lt_d",
        "seconds_total",
    )
    print({k: res[k] for k in keep})
    return 0


if __name__ == "__main__":
    sys.exit(main())
