"""Exact tiling check (stage C, item O2) for the accepted leaves of S-.

Method. The leaf dump refines the root grid (16 x 32 cells from np.linspace) by splitting each
failing cell at float midpoints tm = 0.5*(a+b), pm = 0.5*(c+d). Children share the same float
midpoint, so each split partitions its parent exactly in real arithmetic. The accepted leaves are
exactly the cells that were accepted during this refinement, so the leaf set must equal the leaves
of the reconstructed partition tree. This script rebuilds that tree level by level with the same
float operations and checks, with exact float-bit equality (no tolerance):

  1. every accepted leaf occurs in the tree exactly once (no duplicates, nothing outside the tree);
  2. every node of the tree is either an accepted leaf or is split; nothing is left uncovered
     at the stopping depth.

Hence the accepted leaves form an exact partition of the root rectangle [0, pi_f] x [0, 2 pi_f].
Matching is on the IEEE-754 bit patterns, so this is an exact equality test.

Writes metrics/tiling_exact_check.json.
Usage: python -I code/verify_tiling_exact.py
"""

import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PHASE4 = os.path.normpath(os.path.join(HERE, ".."))
LEAVES = os.path.join(PHASE4, "metrics", "c3h_S-_f090_all_accepted_leaves.npy")
OUT = os.path.join(PHASE4, "metrics", "tiling_exact_check.json")
N_TH0, N_PH0 = 16, 32  # root grid used by c3h_dump_all_leaves.py (arguments 4 and 5)
MAX_DEPTH = 14  # argument 6; the run stopped at depth 10 with no failed cells


def split(cells):
    """Same float operations as split() in c3h_dump_all_leaves.py."""
    tm = 0.5 * (cells[:, 0] + cells[:, 1])
    pm = 0.5 * (cells[:, 2] + cells[:, 3])
    z = cells[:, 0]
    return np.concatenate(
        [
            np.stack([z, tm, cells[:, 2], pm], axis=1),
            np.stack([z, tm, pm, cells[:, 3]], axis=1),
            np.stack([tm, cells[:, 1], cells[:, 2], pm], axis=1),
            np.stack([tm, cells[:, 1], pm, cells[:, 3]], axis=1),
        ]
    )


def as_keys(a):
    """Bit-exact row keys: each row of 4 float64 -> one 32-byte void value."""
    a = np.ascontiguousarray(a, dtype=np.float64)
    return a.view(np.dtype((np.void, 32))).ravel()


def main():
    leaves = np.load(LEAVES)
    n_leaves = len(leaves)
    lkeys = as_keys(leaves)
    n_distinct = len(np.unique(lkeys))

    th_edges = np.linspace(0, math.pi, N_TH0 + 1)
    ph_edges = np.linspace(0, 2 * math.pi, N_PH0 + 1)
    root = np.array(
        [
            [th_edges[i], th_edges[i + 1], ph_edges[j], ph_edges[j + 1]]
            for i in range(N_TH0)
            for j in range(N_PH0)
        ]
    )

    current = root
    matched_total = 0
    nodes_total = 0
    accepted_by_depth = []
    stop_depth = None
    for depth in range(MAX_DEPTH + 1):
        nodes_total += len(current)
        keys = as_keys(current)
        hit = np.isin(keys, lkeys)
        matched = int(hit.sum())
        matched_total += matched
        accepted_by_depth.append(matched)
        remaining = current[~hit]
        if len(remaining) == 0:
            stop_depth = depth
            break
        if depth == MAX_DEPTH:
            break
        current = split(remaining)

    uncovered = int(len(remaining)) if stop_depth is None else 0
    checks = {
        "leaves_in_file": n_leaves,
        "distinct_leaves": int(n_distinct),
        "tree_leaves_matched": matched_total,
        "tree_nodes_visited": nodes_total,
        "stop_depth": stop_depth,
        "uncovered_cells_at_max_depth": uncovered,
        "accepted_by_depth": accepted_by_depth,
    }
    ok = n_leaves == n_distinct == matched_total and stop_depth is not None and uncovered == 0
    result = dict(checks, verdict="TILING_EXACT" if ok else "TILING_PROBLEM")
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1)
    print(json.dumps(result, indent=1))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
