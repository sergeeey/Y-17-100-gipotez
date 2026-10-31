"""O3 v3 (strict) driver: per-leaf certified records, chunk journal, non-overlapping chunk ranges.

Usage (from phase4):  python -I o3_v3/code/o3_run_v3.py <run_name> <first_chunk> <last_chunk> [n_workers]
  - chunks are 500 leaves each, numbered from 0; the leaf range of chunk c is [500c, min(500(c+1), N)).
  - a run only processes chunks in [first_chunk, last_chunk]; runs must be given disjoint ranges.
  - a chunk is done when its line is in o3v3_progress.jsonl; the record file is written before the line, so an
    interrupted chunk is simply redone (no double count, no gap).

Outputs (o3_v3/):
  records/chunk_XXXXX.jsonl.gz   one line per leaf: leaf, ok, slack (arb enclosure string), bup (arb enclosure)
                                  or, for a failed leaf, status and reasons
  metrics/o3v3_progress.jsonl    one line per chunk: chunk, n, ok, fails, min_slack, max_bup, record_sha256, sec
  metrics/run_manifest_<run>.json  SHA-256 of every input and code file, library versions, the chunk range
  metrics/run_summary_<run>.json   counts and the minimum certified slack of the run
Decision per leaf: arb `s - B > 0` (certain). Anything else is a recorded failure. A failure is never widened.
"""

import gzip
import hashlib
import json
import os
import platform
import sys
import time
from multiprocessing import Pool

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
O3V3 = os.path.normpath(os.path.join(HERE, ".."))
LEAVES = os.path.join(O3V3, "inputs", "leaves.npy")
RECORDS = os.path.join(O3V3, "records")
PROGRESS = os.path.join(O3V3, "metrics", "o3v3_progress.jsonl")
CHUNK = 500
_ivl = None


def _load():
    global _ivl
    if _ivl is None:
        sys.path.insert(0, HERE)
        import interval_cells_v3 as ivl  # noqa: E402

        _ivl = ivl
    return _ivl


def _init_worker():
    try:
        import psutil

        psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    except Exception:
        pass


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _done_chunks():
    done = set()
    if os.path.exists(PROGRESS):
        with open(PROGRESS, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    done.add(json.loads(line)["chunk"])
    return done


def work(args):
    cid, base, cells = args
    ivl = _load()
    s = ivl.s_target
    t0 = time.time()
    n_ok = 0
    n_fail = 0
    min_sl = None
    max_b = None
    lines = []
    for k, c in enumerate(cells):
        leaf = base + k
        cell = [float(v) for v in c]
        try:
            r = ivl.cell_bound(cell)
        except Exception as exc:  # recorded per leaf; never kills the chunk
            r = {"status": "EXCEPTION", "reasons": [f"{type(exc).__name__}: {exc}"]}
        if r["status"] != "OK":
            n_fail += 1
            lines.append(
                json.dumps(
                    {
                        "leaf": leaf,
                        "ok": False,
                        "status": r["status"],
                        "reasons": r.get("reasons", []),
                    }
                )
            )
            continue
        b = r["B_up"]
        sl = s - b
        if bool(sl > 0):  # arb-certain positivity
            n_ok += 1
            min_sl = sl if min_sl is None else ivl.arb_min(min_sl, sl)
            max_b = b if max_b is None else ivl.arb_max(max_b, b)
            lines.append(json.dumps({"leaf": leaf, "ok": True, "slack": str(sl), "bup": str(b)}))
        else:
            n_fail += 1
            lines.append(
                json.dumps(
                    {
                        "leaf": leaf,
                        "ok": False,
                        "status": "SLACK_NOT_CERTAIN_POSITIVE",
                        "slack": str(sl),
                        "bup": str(b),
                    }
                )
            )
    os.makedirs(RECORDS, exist_ok=True)
    path = os.path.join(RECORDS, f"chunk_{cid:05d}.jsonl.gz")
    tmp = path + ".tmp"
    with gzip.open(tmp, "wt", encoding="utf-8") as gz:
        gz.write("\n".join(lines) + "\n")
    os.replace(tmp, path)
    return {
        "chunk": cid,
        "n": len(cells),
        "ok": n_ok,
        "fails": n_fail,
        "min_slack": None if min_sl is None else str(min_sl),
        "max_bup": None if max_b is None else str(max_b),
        "record_sha256": sha256_file(path),
        "sec": round(time.time() - t0, 1),
    }


def main():
    run = sys.argv[1]
    first, last = int(sys.argv[2]), int(sys.argv[3])
    n_workers = int(sys.argv[4]) if len(sys.argv) > 4 else 24
    ivl = _load()
    leaves = np.load(LEAVES, mmap_mode="r")
    N = len(leaves)
    total_chunks = (N + CHUNK - 1) // CHUNK
    assert 0 <= first <= last < total_chunks, "chunk range outside the leaf index"
    manifest = {
        "run": run,
        "first_chunk": first,
        "last_chunk": last,
        "workers": n_workers,
        "leaves_total": N,
        "chunks_total": total_chunks,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "flint_version": __import__("flint").__version__,
        "sha256": {
            "leaves.npy": sha256_file(LEAVES),
            "interval_cells_v3.py": sha256_file(os.path.join(HERE, "interval_cells_v3.py")),
            "o3_run_v3.py": sha256_file(os.path.join(HERE, "o3_run_v3.py")),
            "R_input.npz": sha256_file(ivl.RPATH),
            "instance.jsonl": sha256_file(ivl.INST),
            "s8_admissible_span.py": sha256_file(ivl.S8PATH),
        },
        "s_target_binary64": float(ivl.s_target_f),
        "final_gap_arb_positive": bool(ivl.final_gap > 0),
    }
    os.makedirs(os.path.join(O3V3, "metrics"), exist_ok=True)
    with open(
        os.path.join(O3V3, "metrics", f"run_manifest_{run}.json"), "w", encoding="utf-8"
    ) as fh:
        json.dump(manifest, fh, indent=1)
    assert bool(ivl.final_gap > 0), "final gap not certainly positive: refuse to run"

    done = _done_chunks()
    todo = [c for c in range(first, last + 1) if c not in done]
    print(
        f"run {run}: chunks {first}..{last}, to do {len(todo)}, done-before {len(done)}, workers {n_workers}",
        flush=True,
    )
    jobs = [(c, c * CHUNK, np.asarray(leaves[c * CHUNK : min((c + 1) * CHUNK, N)])) for c in todo]
    t0 = time.time()
    tot_n = tot_ok = tot_fail = 0
    with (
        Pool(n_workers, initializer=_init_worker) as pool,
        open(PROGRESS, "a", encoding="utf-8") as pf,
    ):
        for res in pool.imap_unordered(work, jobs, chunksize=1):
            pf.write(json.dumps(res) + "\n")
            pf.flush()
            tot_n += res["n"]
            tot_ok += res["ok"]
            tot_fail += res["fails"]
            print(
                f"chunk {res['chunk']}: ok {res['ok']}/{res['n']} fails {res['fails']} ({time.time() - t0:.0f}s)",
                flush=True,
            )
    summary = {
        "run": run,
        "chunks_processed": len(jobs),
        "leaves_processed": tot_n,
        "ok": tot_ok,
        "fails": tot_fail,
        "seconds": round(time.time() - t0, 1),
        "note": "per-chunk certified min-slack enclosures are in metrics/o3v3_progress.jsonl (arb strings); no float selection is made in the driver",
    }
    with open(
        os.path.join(O3V3, "metrics", f"run_summary_{run}.json"), "w", encoding="utf-8"
    ) as fh:
        json.dump(summary, fh, indent=1)
    print(json.dumps(summary, indent=1), flush=True)


if __name__ == "__main__":
    main()
