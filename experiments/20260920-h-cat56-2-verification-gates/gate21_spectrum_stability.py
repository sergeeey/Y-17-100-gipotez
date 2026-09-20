"""Gate 21: numerical stability of dim V for the d=22 (r=2, s=16) counterexample across the
positive spectrum p = (1-p2, p2). This tests robustness INSIDE the rank-2 stratum only.
It says nothing about p2 -> 0 as a pure-state limit: at p2 = 0 the state rank drops from 2 to 1
and the support/kernel decomposition (hence the SLD geometry) changes discontinuously.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "20260919-pcc-generic-quasipure-cat56-2"))
import orchestrator_independent_check as oc  # noqa: E402
from gate4_source_example import analyse  # noqa: E402


def main() -> int:
    k, r, s = 20, 2, 16
    rng = np.random.default_rng(20260920)
    blocks = oc.draw_blocks(k, r, s, rng)  # ONE PCC tuple, reused for every spectrum
    out = []
    for p2 in (0.4, 0.1, 1e-3, 1e-6):
        p = np.array([1 - p2, p2])
        rho, drho = oc.build_state(blocks, p)
        res = analyse(rho, drho, r)
        res["p2"] = p2
        out.append(res)
        print(
            f"p2={p2:g}: dimV={res['dimV_tol1e-08']} dimVperp={res['dimVperp']} "
            f"tolsweep={[res[f'dimV_tol{t:g}'] for t in (1e-6, 1e-8, 1e-10, 1e-12)]} "
            f"pcc={res['pcc_residual']:.1e} qfim_min={res['qfim_eigs'][0]:.2e}",
            flush=True,
        )
    (HERE / "metrics" / "gate21_spectrum_stability.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
