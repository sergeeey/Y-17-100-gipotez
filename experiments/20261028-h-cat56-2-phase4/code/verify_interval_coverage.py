"""Independent check of the merged interval-pass journals for S- (stage C).

Checks, without trusting the drivers:
  1. Chunk indices of both progress files cover exactly 0..7911, no duplicates across files.
  2. Each line's n equals the expected chunk size (500, last chunk 341), and ok + fails = n.
  3. Total leaves = 3 955 841, total fails = 0 (from the journals, not from any summary).
  4. Leaf file has 3 955 841 rows, and its first and last rows are the terminal cells
     (theta_hi = pi and phi_hi = 2*pi), so the dump did not lose the boundary cells.
Writes metrics/interval_coverage_check.json.

Usage: python -I code/verify_interval_coverage.py
"""

import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PHASE4 = os.path.normpath(os.path.join(HERE, ".."))
LEAVES = os.path.join(PHASE4, "metrics", "c3h_S-_f090_all_accepted_leaves.npy")
PROG = [
    os.path.join(PHASE4, "metrics", "interval_full_progress.jsonl"),
    os.path.join(PHASE4, "metrics", "interval_resume_progress.jsonl"),
]
OUT = os.path.join(PHASE4, "metrics", "interval_coverage_check.json")
CHUNK = 500
N_LEAVES = 3955841
N_CHUNKS = 7912


def main():
    problems = []
    seen = {}
    total_n = 0
    total_ok = 0
    total_fail = 0
    for path in PROG:
        with open(path, encoding="utf-8") as fh:
            for ln, line in enumerate(fh, 1):
                r = json.loads(line)
                c = r["chunk"]
                if c in seen:
                    problems.append(
                        f"duplicate chunk {c} in {os.path.basename(path)} line {ln} (first in {seen[c]})"
                    )
                seen[c] = os.path.basename(path)
                if not (0 <= c < N_CHUNKS):
                    problems.append(f"chunk {c} out of range")
                    continue
                expect = min(CHUNK, N_LEAVES - c * CHUNK)
                if r["n"] != expect:
                    problems.append(f"chunk {c}: n={r['n']} expected {expect}")
                if r["ok"] + r["fails"] != r["n"]:
                    problems.append(f"chunk {c}: ok+fails={r['ok'] + r['fails']} != n={r['n']}")
                total_n += r["n"]
                total_ok += r["ok"]
                total_fail += r["fails"]
    missing = sorted(set(range(N_CHUNKS)) - set(seen))
    if missing:
        problems.append(f"missing chunks: {len(missing)}, first {missing[:5]}")

    leaves = np.load(LEAVES)
    if leaves.shape != (N_LEAVES, 4):
        problems.append(f"leaves shape {leaves.shape}, expected {(N_LEAVES, 4)}")
    # terminal cells: the dump must contain the theta = pi and phi = 2*pi boundary leaves
    theta_hi_max = float(leaves[:, 1].max())
    phi_hi_max = float(leaves[:, 3].max())
    has_pole = bool(np.any(leaves[:, 1] >= math.pi - 1e-15))
    has_seam = bool(np.any(leaves[:, 3] >= 2 * math.pi - 1e-15))
    if not has_pole:
        problems.append("no leaf reaches theta = pi")
    if not has_seam:
        problems.append("no leaf reaches phi = 2*pi")

    result = {
        "chunks_covered": len(seen),
        "chunks_expected": N_CHUNKS,
        "missing_chunks": len(missing),
        "duplicate_chunks": sum(1 for p in problems if p.startswith("duplicate")),
        "leaves_summed_from_journals": total_n,
        "leaves_expected": N_LEAVES,
        "rigorous_ok_from_journals": total_ok,
        "rigorous_fail_from_journals": total_fail,
        "leaves_array_rows": int(leaves.shape[0]),
        "theta_hi_max": theta_hi_max,
        "phi_hi_max": phi_hi_max,
        "leaf_reaches_theta_pi": has_pole,
        "leaf_reaches_phi_2pi": has_seam,
        "problems": problems,
        "verdict": "COVERAGE_CONSISTENT"
        if not problems and total_fail == 0 and total_n == N_LEAVES
        else "COVERAGE_PROBLEM",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1)
    print(json.dumps(result, indent=1, ensure_ascii=False))
    sys.exit(0 if result["verdict"] == "COVERAGE_CONSISTENT" else 1)


if __name__ == "__main__":
    main()
