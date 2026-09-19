"""Prior Result Gate toy check for the H-CAT56-3 candidate (minimal POVM size), NOT an experiment.

Question: on states whose QCRB is saturable by an explicitly constructed POVM (LP completeness with
zero slack), is a d-element measurement (an orthonormal basis, which is the smallest possible size)
already found by direct search? A found solution is a certificate of existence; a failed search is
NOT a certificate of anything, which is why an Eq.(16) control class (theorem-guaranteed d-element
LMCC basis) is run first: if the search fails there, the tool is too weak to say anything.

Reuses H-CAT56-1's modules unchanged. One process, cores 16-23, below-normal priority.
"""

import importlib.util
import json
import os
import sys
import time
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import numpy as np  # noqa: E402  (thread env vars must be set before numpy loads)
import psutil  # noqa: E402

try:
    psutil.Process().cpu_affinity(list(range(16, 24)))
    psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
except (AttributeError, psutil.Error, OSError):
    pass

OLD = (
    Path(__file__).resolve().parents[1] / "experiments" / "20260918-pcc-sufficiency-quasipure-cat56"
)
sys.path.insert(0, str(OLD))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(f"h1_{name}", OLD / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod.__name__] = mod
    spec.loader.exec_module(mod)
    return mod


pc = _load("pcc_core")
ps = _load("pcc_sat")

N_STATES = 12
MAX_EXTRA = 3  # try n = d, d+1, ..., d+MAX_EXTRA


def min_size_found(model, ana, rng) -> dict:
    d = ana.d
    sols = ps.find_hollowizing_vectors(ana.v_basis, d, 400, rng)
    slack, alphas = ps.completeness_lp(sols, d)
    out = {"d": d, "dim_v_perp": ana.dim_v_perp, "lp_slack": float(slack)}
    if not (slack < 1e-7 and alphas is not None):
        out["saturable_by_lp_sample"] = False
        return out
    out["saturable_by_lp_sample"] = True
    out["lp_povm_size"] = int(np.sum(alphas > 1e-9))
    found = None
    for n in range(d, d + MAX_EXTRA + 1):
        povm = ps.direct_povm_search(ana.v_basis, d, n, rng, n_starts=12)
        if povm is not None:
            found = n
            break
    out["min_size_found"] = found
    return out


def run_class(label: str, sampler, n_states: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    rows = []
    t0 = time.time()
    tries = 0
    while len(rows) < n_states and tries < n_states * 20:
        tries += 1
        model = sampler(rng)
        if model is None:
            continue
        ana = pc.analyse(model)
        if not (ana.pcc_holds and ana.qfim_rank == ana.s):
            continue
        rows.append(min_size_found(model, ana, rng))
    sat = [r for r in rows if r["saturable_by_lp_sample"]]
    hit_d = [r for r in sat if r.get("min_size_found") == r["d"]]
    miss = [r for r in sat if r.get("min_size_found") is None]
    out = {
        "class": label,
        "n_states": len(rows),
        "n_saturable_by_lp": len(sat),
        "n_found_at_d": len(hit_d),
        "n_no_solution_up_to_d_plus_3": len(miss),
        "sizes_found": sorted({r.get("min_size_found") for r in sat}, key=lambda x: (x is None, x)),
        "dim_v_perp_values": sorted({r["dim_v_perp"] for r in rows}),
        "below_theorem3_threshold_note": "see decision text; d=4 needs dimVperp-1 >= 12",
        "seconds": time.time() - t0,
        "rows": rows,
    }
    return out


def main() -> None:
    results = []
    # control first: Eq.(16) class, an orthonormal LMCC basis of d elements exists by theorem
    results.append(
        run_class(
            "control Eq16 d_sys=2 r=2 s=2 (d=4)",
            lambda g: pc.sample_bipartite_quasipure(2, 2, 2, g),
            N_STATES,
            101,
        )
    )
    results.append(
        run_class(
            "control Eq16 d_sys=3 r=2 s=2 (d=6)",
            lambda g: pc.sample_bipartite_quasipure(3, 2, 2, g),
            N_STATES,
            102,
        )
    )
    results.append(
        run_class(
            "generic d=4 r=2 s=2", lambda g: pc.sample_generic_quasipure(4, 2, 2, g), N_STATES, 103
        )
    )
    results.append(
        run_class(
            "generic d=5 r=2 s=3", lambda g: pc.sample_generic_quasipure(5, 2, 3, g), N_STATES, 104
        )
    )
    results.append(
        run_class(
            "generic d=6 r=2 s=4", lambda g: pc.sample_generic_quasipure(6, 2, 4, g), N_STATES, 105
        )
    )
    out = Path(__file__).resolve().parents[1] / "reports" / "hcat56_3_gate_toy.json"
    out.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    for r in results:
        print(
            f"{r['class']}: states={r['n_states']} saturable_by_LP={r['n_saturable_by_lp']}"
            f" found_at_d={r['n_found_at_d']} none_up_to_d+3={r['n_no_solution_up_to_d_plus_3']}"
            f" sizes_found={r['sizes_found']} dimVperp={r['dim_v_perp_values']}"
            f" ({r['seconds']:.0f}s)",
            flush=True,
        )


if __name__ == "__main__":
    main()
