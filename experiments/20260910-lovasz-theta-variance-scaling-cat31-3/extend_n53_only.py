"""Extends the density-vs-shape decomposition (check_density_vs_shape_decomposition.py) to
n=53 WITHOUT recomputing n=11..47, which are already verified and stored in
metrics/density_vs_shape_decomposition.json from the prior run. Reuses run_one_n() from that
module UNCHANGED (same code path, same theta_via_lp_robust / orbit-reduction machinery,
already cross-validated to 8.88e-14 against exhaustive n=23) -- this is not a new
implementation, only avoiding redundant recomputation of already-verified values for n<53.

n=53 (m=26) is the most expensive point run so far: 2^26 ~= 67M subsets in the delta-loop,
~2.6M necklace orbits before complement-pairing halves the LP-solve count to ~1.3M.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"
JSON_PATH = METRICS / "density_vs_shape_decomposition.json"

spec = importlib.util.spec_from_file_location(
    "density_shape_mod", HERE / "check_density_vs_shape_decomposition.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

if __name__ == "__main__":
    with open(JSON_PATH, encoding="utf-8") as f:
        existing = json.load(f)
    existing_ns = {row["n"] for row in existing["rows"]}
    if 53 in existing_ns:
        print("n=53 already present, nothing to do.")
    else:
        row53 = mod.run_one_n(53)
        existing["rows"].append(row53)
        existing["rows"].sort(key=lambda r: r["n"])
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)
        print("\n--- updated summary: n^2*density_part vs n^2*shape_part across prime n ---")
        for r in existing["rows"]:
            print(
                f"  n={r['n']:3d}  n^2*density={r['n2_times_density_part']:.4f}  "
                f"n^2*shape={r['n2_times_shape_part']:.4f}  "
                f"shape_frac={r['shape_fraction_of_Edelta2']:.4f}"
            )
