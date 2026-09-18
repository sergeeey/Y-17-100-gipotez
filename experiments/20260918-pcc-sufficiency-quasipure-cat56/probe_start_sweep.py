"""Self-falsification check: is the d=8 probe failure just too few random starts?

This experiment claims that a search-based "not saturable" answer is unsound, and the
evidence is a 0/8 probe success rate at `d = 8` where Theorem 3 guarantees success. The
obvious objection is that 250 starts is simply too few. If the probe succeeds once the
start count is raised, the claim weakens from "searching is unsound here" to "this search
was under-resourced", and the decision record must say so.

So: sweep the start count over roughly two orders of magnitude at `d = 8` and report the
success rate and the LP slack at each. Whatever the answer is, it goes in decision.md.

Run:  python probe_start_sweep.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pcc_core as pc
import pcc_sat as ps

OUT = Path(__file__).parent / "metrics" / "probe_start_sweep.json"


def main() -> None:
    rng = np.random.default_rng(20260919)
    models = []
    while len(models) < 3:
        m = pc.sample_bipartite_quasipure(4, 2, 2, rng)  # d = 8, above the Eq. (15) threshold
        if m is not None:
            models.append(m)
    anas = [pc.analyse(m) for m in models]

    rows = []
    for starts in (250, 500, 1000, 2000, 4000):
        t0 = time.time()
        res = []
        for model, ana in zip(models, anas, strict=True):
            probe = ps.constructive_probe(ana, model, rng, n_starts=starts, max_rounds=4)
            res.append(
                {
                    "constructed": bool(probe["constructed"]),
                    "lp_slack": probe.get("lp_slack"),
                    "n_v_sampled": probe.get("n_v_sampled"),
                    "povm_size": probe.get("povm_size"),
                }
            )
        rows.append(
            {
                "n_starts": starts,
                "dim_V_perp": anas[0].dim_v_perp,
                "d": anas[0].d,
                "successes": sum(r["constructed"] for r in res),
                "trials": len(res),
                "lp_slacks": [r["lp_slack"] for r in res],
                "n_v_sampled": [r["n_v_sampled"] for r in res],
                "seconds": round(time.time() - t0, 1),
            }
        )
        print(
            f"  starts={starts:5d}  success {rows[-1]['successes']}/{rows[-1]['trials']}  "
            f"slacks={[None if x is None else round(x, 4) for x in rows[-1]['lp_slacks']]}  "
            f"v sampled={rows[-1]['n_v_sampled']}  ({rows[-1]['seconds']}s)"
        )

    any_success = any(r["successes"] for r in rows)
    payload = {
        "purpose": "self-falsification of the 'search-based verdict is unsound' claim",
        "configuration": "bipartite d_sys=4, r=2, s=2 (d=8), ABOVE the Eq. (15) threshold, "
        "so Theorem 3 guarantees a saturating projective measurement exists",
        "rows": rows,
        "probe_ever_succeeded": bool(any_success),
        "interpretation": (
            "If probe_ever_succeeded is true, the d=8 failure is an under-resourced search "
            "and the claim must be weakened to 'this search was too small'. If it stays "
            "false across a 16x range of start counts while the same code succeeds at "
            "d=4/d=6, the failure is a property of searching this variety, not of the "
            "budget."
        ),
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("probe_ever_succeeded:", any_success)


if __name__ == "__main__":
    main()
