"""Resume the full rigorous interval pass for chunks missing from interval_full_progress.jsonl.

WHY: the first run (interval_full_parallel.py, 12 workers) stopped at ~3.595M of 3,955,841 leaves
with "FLINT exception: Unable to allocate memory" and wrote no summary. This driver processes only
the chunks absent from the first progress file, and catches the exception PER LEAF: a leaf that
raises is recorded as a failure with its index and cell, not silently dropped and not allowed to
kill the pool. Old metrics files are not modified; new results go to interval_resume_progress.jsonl.

Input : metrics/c3h_S-_f090_all_accepted_leaves.npy, metrics/interval_full_progress.jsonl
Output: metrics/interval_resume_progress.jsonl (one line per chunk),
        metrics/interval_resume_summary.json (only after all chunks are covered by the two progress files)
Usage : python -I code/interval_resume_parallel.py [n_workers]
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
PROGRESS_OLD = os.path.join(PHASE4, "metrics", "interval_full_progress.jsonl")
PROGRESS_NEW = os.path.join(PHASE4, "metrics", "interval_resume_progress.jsonl")
SUMMARY = os.path.join(PHASE4, "metrics", "interval_resume_summary.json")
CHUNK = 500
DEFAULT_WORKERS = (
    8  # WHY: 12 workers ran out of arb memory near 3.6M; fewer workers also loads the PC less
)

_ivl = None  # lazy import in each worker (spawn on Windows)


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


def _done_chunks(path):
    done = set()
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                done.add(json.loads(line)["chunk"])
    return done


def work(args):
    cid, base, cells = args
    ivl = _load()
    s = ivl.s_target
    n_ok = 0
    fails = []
    min_slack = None
    max_bup = None
    for k, c in enumerate(cells):
        leaf_index = base + k
        try:
            r = ivl.cell_bound(c.tolist())
        except Exception as exc:  # per-leaf: record, do not let one leaf kill the chunk or the pool
            fails.append(
                {
                    "leaf": leaf_index,
                    "cell": c.tolist(),
                    "reason": f"exception: {type(exc).__name__}: {exc}",
                }
            )
            continue
        if r is None:
            fails.append({"leaf": leaf_index, "cell": c.tolist(), "reason": "kappa>=1"})
            continue
        b = r["B_up"]
        sl = float(s - b)
        bf = float(b)
        min_slack = sl if min_slack is None else min(min_slack, sl)
        max_bup = bf if max_bup is None else max(max_bup, bf)
        if s - b > 0:
            n_ok += 1
        else:
            fails.append({"leaf": leaf_index, "cell": c.tolist(), "reason": "B_up>=s", "B_up": bf})
    return cid, len(cells), n_ok, fails, min_slack, max_bup


def main():
    n_workers = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_WORKERS
    leaves = np.load(LEAVES)
    N = len(leaves)
    total_chunks = (N + CHUNK - 1) // CHUNK
    done_old = _done_chunks(PROGRESS_OLD)
    done_new = _done_chunks(PROGRESS_NEW)
    todo = [c for c in range(total_chunks) if c not in done_old and c not in done_new]
    chunks = [(c, c * CHUNK, leaves[c * CHUNK : (c + 1) * CHUNK]) for c in todo]
    ivl = _load()
    gap_pos = bool(ivl.final_gap > 0)
    print(
        f"leaves {N}, chunks total {total_chunks}, to do {len(chunks)}, workers {n_workers}, "
        f"final gap trR-20s > 0: {gap_pos}",
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
        open(PROGRESS_NEW, "a", encoding="utf-8") as pf,
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
            if len(all_fails) and len(fails):
                print(
                    f"chunk {cid}: {len(fails)} leaf failures, first: {fails[0]['reason']}",
                    flush=True,
                )
            if tot_n % (CHUNK * 100) < CHUNK:
                print(
                    f"{tot_n}/{N - sum(len(leaves[c * CHUNK : (c + 1) * CHUNK]) for c in done_old | done_new if c < total_chunks)} remaining done, ok {tot_ok}, fails {len(all_fails)}, {time.time() - t0:.0f}s",
                    flush=True,
                )

    covered = done_old | done_new | {c for c, *_ in chunks}
    complete = len(covered) == total_chunks
    summary = {
        "chunks_processed_this_run": len(chunks),
        "chunks_total": total_chunks,
        "covered_by_both_progress_files": complete,
        "rigorous_ok_this_run": tot_ok,
        "rigorous_fail_this_run": len(all_fails),
        "final_gap_trR_minus_20s": float(ivl.final_gap),
        "s_target": float(ivl.s_target_f),
        "min_slack_abs_this_run": min_slack,
        "max_B_up_this_run": max_bup,
        "prec_bits": 192,
        "seconds": round(time.time() - t0, 1),
        "fails_sample": all_fails[:50],
        "note": "resume of chunks missing from interval_full_progress.jsonl; per-leaf exceptions recorded as failures",
    }
    with open(SUMMARY, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1, default=float)
    print(
        json.dumps({k: v for k, v in summary.items() if k != "fails_sample"}, indent=1), flush=True
    )


if __name__ == "__main__":
    main()
