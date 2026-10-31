"""Full rigorous interval pass over ALL accepted leaves of the S- certificate (threshold s = 0.9 trR/20).

Input : metrics/c3h_S-_f090_all_accepted_leaves.npy  (N x 4: th_lo, th_hi, ph_lo, ph_hi), written by c3h_dump_all_leaves.py.
Work  : each leaf -> interval_cells.cell_bound (python-flint arb, 192 bit): rigorous upper bound B_up of the cell bound,
        accepted iff s_target - B_up > 0 with certainty (arb comparison).
Output: metrics/interval_full_summary.json (verdict, counts, min slack, max B_up) and
        metrics/interval_full_progress.jsonl (one line per chunk, so an interrupted run can be resumed by reading it).
Environment: BLAS threads forced to 1 per worker (24 workers on a 24-core machine).

Usage: python -I code/interval_full_parallel.py [n_workers]
"""

import os

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import json  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from multiprocessing import Pool  # noqa: E402

import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PHASE4 = os.path.normpath(os.path.join(HERE, ".."))
LEAVES = os.path.join(PHASE4, "metrics", "c3h_S-_f090_all_accepted_leaves.npy")
SUMMARY = os.path.join(PHASE4, "metrics", "interval_full_summary.json")
PROGRESS = os.path.join(PHASE4, "metrics", "interval_full_progress.jsonl")
CHUNK = 500

_ivl = None  # lazy import in each worker (spawn on Windows)
DEFAULT_WORKERS = (
    12  # WHY: 24 workers loaded the PC until it disconnected; half the cores keeps it responsive
)


def _init_worker():
    """Lower the priority of each worker so the desktop stays responsive (Windows BELOW_NORMAL class)."""
    try:
        import psutil

        psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    except Exception:
        pass


def _load():
    global _ivl
    if _ivl is None:
        sys.path.insert(0, HERE)
        import interval_cells as ivl  # noqa: E402

        _ivl = ivl
    return _ivl


def work(args):
    cid, cells = args
    ivl = _load()
    s = ivl.s_target
    n_ok = 0
    fails = []
    min_slack = None
    max_bup = None
    for c in cells:
        r = ivl.cell_bound(c.tolist())
        if r is None:
            fails.append({"cell": c.tolist(), "reason": "kappa>=1"})
            continue
        b = r["B_up"]
        slack_ok = bool(s - b > 0)
        sl = float(s - b)
        bf = float(b)
        min_slack = sl if min_slack is None else min(min_slack, sl)
        max_bup = bf if max_bup is None else max(max_bup, bf)
        if slack_ok:
            n_ok += 1
        else:
            fails.append({"cell": c.tolist(), "reason": "B_up>=s", "B_up": bf})
    return cid, len(cells), n_ok, fails, min_slack, max_bup


def main():
    n_workers = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_WORKERS
    leaves = np.load(LEAVES)
    N = len(leaves)
    chunks = [(i, leaves[k : k + CHUNK]) for i, k in enumerate(range(0, N, CHUNK))]
    ivl = _load()
    gap_pos = bool(ivl.final_gap > 0)
    print(
        f"leaves {N}, chunks {len(chunks)}, workers {n_workers}, final gap trR-20s > 0: {gap_pos}",
        flush=True,
    )
    t0 = time.time()
    tot_ok = 0
    tot_n = 0
    all_fails = []
    min_slack = None
    max_bup = None
    with (
        Pool(n_workers, initializer=_init_worker) as pool,
        open(PROGRESS, "w", encoding="utf-8") as pf,
    ):
        for cid, n, n_ok, fails, mins, maxb in pool.imap_unordered(work, chunks, chunksize=1):
            tot_n += n
            tot_ok += n_ok
            all_fails += fails
            if mins is not None:
                min_slack = mins if min_slack is None else min(min_slack, mins)
            if maxb is not None:
                max_bup = maxb if max_bup is None else max(max_bup, maxb)
            pf.write(
                json.dumps(
                    {
                        "chunk": cid,
                        "n": n,
                        "ok": n_ok,
                        "fails": len(fails),
                        "elapsed_s": round(time.time() - t0, 1),
                    }
                )
                + "\n"
            )
            pf.flush()
            if tot_n % (CHUNK * 200) < CHUNK:
                print(
                    f"{tot_n}/{N} done, ok {tot_ok}, fails {len(all_fails)}, {time.time() - t0:.0f}s",
                    flush=True,
                )
    verdict = (
        "CERTIFIED_all_leaves_rigorous" if (tot_ok == N and gap_pos) else "NOT_CERTIFIED_rigorous"
    )
    summary = {
        "verdict": verdict,
        "leaves": N,
        "rigorous_ok": tot_ok,
        "rigorous_fail": len(all_fails),
        "final_gap_trR_minus_20s": float(ivl.final_gap),
        "s_target": float(ivl.s_target_f),
        "min_slack_abs": min_slack,
        "max_B_up": max_bup,
        "prec_bits": 192,
        "seconds": round(time.time() - t0, 1),
        "fails_sample": all_fails[:50],
        "note": "rigorous per-leaf check of the leaves produced by c3h (float); the leaf tiling/coverage is argued in LEMMA_CELL_AUDIT.md",
    }
    with open(SUMMARY, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1)
    print(
        json.dumps({k: v for k, v in summary.items() if k != "fails_sample"}, indent=1), flush=True
    )


if __name__ == "__main__":
    main()
