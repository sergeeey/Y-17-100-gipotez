"""H-CAT31-4 -- prime-n sweep of Var(log(theta(G)/sqrt(n))), random dense circulant graphs, p=1/2.

Design is locked in claim.md / controls.md (written before this file was executed). The LP and the
sampler are reused unchanged from H-CAT31-1. Per-instance theta values are appended to
metrics/thetas_<block>.jsonl so an interrupted run resumes without recomputation.

Usage:
    python run.py gate            # substrate gate + negative control only
    python run.py sweep           # main prime sweep (block "main")
    python run.py sweep2          # independent seed block for n in {509, 1021, 2053} (control 7)
"""

from __future__ import annotations

import importlib.util
import json
import multiprocessing as mp
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"
H_CAT31_1 = HERE.parent / "20260909-lovasz-theta-random-circulant-graphs" / "run.py"

SEED_BASE = 330000
SEED_OFFSET_BLOCK2 = 5_000_000
N_WORKERS = 4
FIRST_CORE = 8
CORES_PER_WORKER = 2

PRIME_REPS = [
    (67, 300),
    (127, 300),
    (251, 300),
    (509, 250),
    (1021, 200),
    (2053, 200),
    (3001, 200),
    (4093, 100),
]
BLOCK2_REPS = [(509, 200), (1021, 200), (2053, 200)]


def _load_base():
    spec = importlib.util.spec_from_file_location("h_cat31_1_base", H_CAT31_1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _init_worker(counter, first_core: int, cores_per_worker: int) -> None:
    """Pin this worker to its own small core block and lower its priority.

    Operational change made after the first launch (12 unpinned workers, each a 3.6 GB / 16-thread
    HiGHS solve at n=4093) overloaded the machine and it rebooted. The statistical design in
    claim.md is unchanged.
    """
    import psutil

    with counter.get_lock():
        idx = counter.value
        counter.value += 1
    cores = [first_core + idx * cores_per_worker + j for j in range(cores_per_worker)]
    proc = psutil.Process()
    proc.cpu_affinity(cores)
    proc.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)


def solve_one(n: int, seed: int) -> dict:
    base = _load_base()
    c = base.sample_circulant_neighbors(n, 0.5, seed)
    t0 = time.time()
    theta = float(base.theta_via_lp(c))
    return {"n": n, "seed": seed, "theta": theta, "seconds": time.time() - t0}


def substrate_gate() -> dict:
    base = _load_base()
    c5 = np.zeros(5)
    c5[1] = 1.0
    c5[4] = 1.0
    theta_c5 = float(base.theta_via_lp(c5))
    n = 67
    c = base.sample_circulant_neighbors(n, 0.5, 770)
    cbar = np.zeros(n)
    for k in range(1, (n - 1) // 2 + 1):
        cbar[k] = 1.0 - c[k]
        cbar[n - k] = 1.0 - c[n - k]
    prod = float(base.theta_via_lp(c) * base.theta_via_lp(cbar))
    neg_vals = [float(base.theta_via_lp(np.zeros(n))) for _ in range(5)]
    x = np.log(np.array(neg_vals) / np.sqrt(n))
    out = {
        "theta_c5": theta_c5,
        "c5_ok": bool(abs(theta_c5 - np.sqrt(5)) < 1e-6),
        "prime_n": n,
        "theta_g_times_gbar": prod,
        "identity_ok": bool(abs(prod - n) < 1e-4),
        "negative_control_var": float(np.var(x, ddof=1)),
        "negative_control_ok": float(np.var(x, ddof=1)) < 1e-10,
    }
    out["substrate_ready"] = bool(
        out["c5_ok"] and out["identity_ok"] and out["negative_control_ok"]
    )
    return out


def load_done(path: Path) -> dict[tuple[int, int], dict]:
    done: dict[tuple[int, int], dict] = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue  # a line truncated by a crash is simply recomputed
                done[(rec["n"], rec["seed"])] = rec
    return done


def run_block(block: str, reps_table: list[tuple[int, int]], seed_offset: int) -> None:
    METRICS.mkdir(exist_ok=True)
    path = METRICS / f"thetas_{block}.jsonl"
    done = load_done(path)
    tasks = []
    for n, reps in reps_table:
        for i in range(reps):
            seed = SEED_BASE + n * 1000 + i + seed_offset
            if (n, seed) not in done:
                tasks.append((n, seed))
    tasks.sort(key=lambda t: t[0])  # smallest first: partial results accumulate, big solves last
    print(f"block={block} tasks_to_run={len(tasks)} already_done={len(done)}", flush=True)
    t_start = time.time()
    finished = 0
    counter = mp.Value("i", 0)
    with (
        ProcessPoolExecutor(
            max_workers=N_WORKERS,
            initializer=_init_worker,
            initargs=(counter, FIRST_CORE, CORES_PER_WORKER),
        ) as pool,
        path.open("a", encoding="utf-8") as fh,
    ):
        futs = {pool.submit(solve_one, n, s): (n, s) for n, s in tasks}
        for fut in as_completed(futs):
            rec = fut.result()
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
            finished += 1
            if finished % 20 == 0 or rec["n"] >= 3001:
                print(
                    f"[{time.time() - t_start:8.0f}s] {finished}/{len(tasks)} last n={rec['n']}"
                    f" theta={rec['theta']:.5f} ({rec['seconds']:.1f}s)",
                    flush=True,
                )


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "gate"
    if cmd == "gate":
        gate = substrate_gate()
        METRICS.mkdir(exist_ok=True)
        (METRICS / "substrate_gate.json").write_text(json.dumps(gate, indent=2), encoding="utf-8")
        print(json.dumps(gate, indent=2))
    elif cmd == "sweep":
        gate_path = METRICS / "substrate_gate.json"
        if not gate_path.exists() or not json.loads(gate_path.read_text())["substrate_ready"]:
            raise SystemExit("substrate gate not READY; refusing to run the sweep")
        run_block("main", PRIME_REPS, 0)
    elif cmd == "sweep2":
        run_block("block2", BLOCK2_REPS, SEED_OFFSET_BLOCK2)
    else:
        raise SystemExit(f"unknown command {cmd}")


if __name__ == "__main__":
    main()
