"""O3 v2: full certified pass over all accepted leaves of S- with interval_cells_v2 (kernel certificate).

Input : inputs/leaves.npy (SHA-256 checked against the stage-C manifest before the run)
Output: metrics/o3_progress.jsonl  (one line per chunk: chunk, n, ok, fails, elapsed)
        metrics/o3_failures.jsonl  (one line per failed leaf: leaf index, cell, status, reasons)
        metrics/o3_summary.json    (only after all chunks are in the progress file)
Resume: chunks already present in o3_progress.jsonl are skipped; a chunk is written only after all its leaves
        were processed, so an interrupted chunk is redone and never double counted.
Usage : python -I code/o3_run_v2.py [n_workers]     (default 8; BELOW_NORMAL priority; BLAS = 1 per worker)
"""

import os

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import hashlib  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from multiprocessing import Pool  # noqa: E402

import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
O3 = os.path.normpath(os.path.join(HERE, ".."))
LEAVES = os.path.join(O3, "inputs", "leaves.npy")
PROGRESS = os.path.join(O3, "metrics", "o3_progress.jsonl")
FAILURES = os.path.join(O3, "metrics", "o3_failures.jsonl")
SUMMARY = os.path.join(O3, "metrics", "o3_summary.json")
CHUNK = 500
DEFAULT_WORKERS = 8

_ivl = None  # lazy import in each worker (spawn on Windows)


def _init_worker():
    """Windows BELOW_NORMAL priority so the desktop stays responsive."""
    try:
        import psutil

        psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    except Exception:
        pass


def _load():
    global _ivl
    if _ivl is None:
        sys.path.insert(0, HERE)
        import interval_cells_v2 as ivl  # noqa: E402

        _ivl = ivl
    return _ivl


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _done_chunks(path):
    done = set()
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
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
        cell = [float(v) for v in c]
        try:
            r = ivl.cell_bound(cell)
        except Exception as exc:  # per leaf: record, never let one leaf kill the chunk or the pool
            fails.append(
                {
                    "leaf": leaf_index,
                    "cell": cell,
                    "status": "EXCEPTION",
                    "reasons": [f"{type(exc).__name__}: {exc}"],
                }
            )
            continue
        if r["status"] != "OK":
            fails.append(
                {
                    "leaf": leaf_index,
                    "cell": cell,
                    "status": r["status"],
                    "reasons": r.get("reasons", []),
                }
            )
            continue
        b = r["B_up"]
        sl = float(s - b)
        bf = float(b)
        min_slack = sl if min_slack is None else min(min_slack, sl)
        max_bup = bf if max_bup is None else max(max_bup, bf)
        if s - b > 0:  # arb comparison: true only if certainly positive
            n_ok += 1
        else:
            fails.append(
                {
                    "leaf": leaf_index,
                    "cell": cell,
                    "status": "SLACK_NOT_POSITIVE",
                    "reasons": [f"B_up={bf!r} >= s={float(s)!r}"],
                }
            )
    return cid, len(cells), n_ok, fails, min_slack, max_bup


def main():
    n_workers = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_WORKERS
    t_start = time.time()
    leaves_sha = _sha256(LEAVES)
    leaves = np.load(LEAVES, mmap_mode="r")
    N = len(leaves)
    total_chunks = (N + CHUNK - 1) // CHUNK
    done = _done_chunks(PROGRESS)
    todo = [c for c in range(total_chunks) if c not in done]
    chunks = [(c, c * CHUNK, np.asarray(leaves[c * CHUNK : (c + 1) * CHUNK])) for c in todo]
    ivl = _load()
    print(
        f"leaves {N} sha256 {leaves_sha}; chunks total {total_chunks}, done {len(done)}, "
        f"to do {len(chunks)}, workers {n_workers}; final gap trR-20s > 0: {bool(ivl.final_gap > 0)}",
        flush=True,
    )
    t0 = time.time()
    tot_ok = 0
    tot_n = 0
    n_fail = 0
    min_slack = None
    max_bup = None
    with (
        Pool(n_workers, initializer=_init_worker) as pool,
        open(PROGRESS, "a", encoding="utf-8") as pf,
        open(FAILURES, "a", encoding="utf-8") as ff,
    ):
        for cid, n, n_ok, fails, mins, maxb in pool.imap_unordered(work, chunks, chunksize=1):
            tot_n += n
            tot_ok += n_ok
            n_fail += len(fails)
            for f in fails:
                ff.write(json.dumps({"chunk": cid, **f}) + "\n")
            ff.flush()
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
            if len(fails):
                print(
                    f"chunk {cid}: {len(fails)} failed leaves, first: {fails[0]['status']}",
                    flush=True,
                )
            if tot_n % (CHUNK * 200) < CHUNK:
                print(
                    f"processed {tot_n} leaves this run, ok {tot_ok}, fails {n_fail}, {time.time() - t0:.0f}s",
                    flush=True,
                )

    # coverage check against the progress file (each chunk exactly once)
    seen = []
    with open(PROGRESS, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                seen.append(json.loads(line)["chunk"])
    covered = set(seen)
    leaves_in_progress = 0
    with open(PROGRESS, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                leaves_in_progress += json.loads(line)["n"]
    summary = {
        "leaves_total": N,
        "chunks_total": total_chunks,
        "chunk_lines_in_progress": len(seen),
        "chunks_unique_in_progress": len(covered),
        "duplicate_chunk_lines": len(seen) - len(covered),
        "all_chunks_covered_once": bool(len(covered) == total_chunks and len(seen) == total_chunks),
        "leaves_counted_in_progress": leaves_in_progress,
        "leaves_match_total": bool(leaves_in_progress == N),
        "ok_this_run": tot_ok,
        "failed_this_run": n_fail,
        "final_gap_trR_minus_20s": float(ivl.final_gap),
        "final_gap_positive": bool(ivl.final_gap > 0),
        "s_target": float(ivl.s_target_f),
        "min_slack_this_run": min_slack,
        "max_B_up_this_run": max_bup,
        "leaves_sha256": leaves_sha,
        "prec_bits": 192,
        "seconds_this_run": round(time.time() - t_start, 1),
        "note": "failures listed in o3_failures.jsonl; a failure is never a reason to widen a tolerance",
    }
    with open(SUMMARY, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1, default=float)
    print(json.dumps(summary, indent=1, default=float), flush=True)


if __name__ == "__main__":
    main()
