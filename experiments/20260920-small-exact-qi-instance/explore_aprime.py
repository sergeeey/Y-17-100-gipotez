# ruff: noqa
"""A' search frozen in claim_addendum_A_prime.md. Reuses build() and float_dimv() from explore_a2.py unchanged."""

import json
import sys
import time
from pathlib import Path

import explore_a2 as e

HERE = Path(__file__).parent
GRID_M = (8, 10, 12, 14, 16, 18, 20)
GRID_C = (2, 3, 4)
SEEDS = 12
MAXBITS = 400


def main() -> int:
    part = int(sys.argv[1])  # 0..2, splits the m-grid across up to 3 processes
    out = HERE / "metrics" / f"aprime_part{part}.jsonl"
    t0 = time.time()
    ms = [m for i, m in enumerate(GRID_M) if i % 3 == part]
    for m in ms:
        for c in GRID_C:
            for k in range(SEEDS):
                seed = 50000 + m * 100 + c * 10 + k
                blocks, curve = e.build(seed, m, c, MAXBITS)
                row = {"m": m, "c": c, "seed": seed, "built": blocks is not None,
                       "bit_curve": curve}
                if blocks is not None:
                    row["dimV_float"] = e.float_dimv(blocks)
                    row["max_bits"] = max(curve)
                    if row["dimV_float"] >= 463:
                        row["blocks"] = blocks
                with out.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(row) + "\n")
                print(m, c, seed, row["built"], row.get("dimV_float"), row.get("max_bits"),
                      f"{time.time() - t0:.0f}s", flush=True)
                if row.get("dimV_float", 0) >= 463:
                    print("CANDIDATE", seed, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
