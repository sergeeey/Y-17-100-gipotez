"""Carpet graph spectra, levels 1..4 full dense, level 5 via x/y reflection sectors.
Usage: python carpet_spectra.py [maxlevel_full=4] [do_level5=0|1]"""

import sys, time
import numpy as np
from lib import *

maxfull = int(sys.argv[1]) if len(sys.argv) > 1 else 4
do5 = int(sys.argv[2]) if len(sys.argv) > 2 else 0


def sector_spectra(A, xy, M, kind):
    """eigenvalues of Laplacian on the 4 (x-flip, y-flip) parity sectors; concatenated sorted."""
    L = laplacian(A, kind).tocsr()
    N = A.shape[0]
    key = {(int(x), int(y)): i for i, (x, y) in enumerate(xy)}
    px = np.array([key[(M - int(x), int(y))] for x, y in xy])
    py = np.array([key[(int(x), M - int(y))] for x, y in xy])
    pxy = px[py]
    reps = np.nonzero((xy[:, 0] * 2 < M) & (xy[:, 1] * 2 < M))[0]
    assert 4 * len(reps) == N, (4 * len(reps), N)
    allev = []
    for sx in (1, -1):
        for sy in (1, -1):
            rows = np.concatenate([reps, px[reps], py[reps], pxy[reps]])
            cols = np.concatenate([np.arange(len(reps))] * 4)
            vals = (
                np.concatenate(
                    [
                        np.ones(len(reps)),
                        sx * np.ones(len(reps)),
                        sy * np.ones(len(reps)),
                        sx * sy * np.ones(len(reps)),
                    ]
                )
                / 2.0
            )
            B = sp.csr_matrix((vals, (rows, cols)), shape=(N, len(reps)))
            H = (B.T @ L @ B).toarray()
            H = (H + H.T) / 2
            t = time.time()
            ev = np.linalg.eigvalsh(H)
            print(
                f"   sector sx={sx} sy={sy} size {H.shape[0]} eig {time.time() - t:.0f}s",
                flush=True,
            )
            allev.append(ev)
    return np.sort(np.concatenate(allev))


kinds = sys.argv[3].split(",") if len(sys.argv) > 3 else ["L1", "L2"]
for kind in kinds:
    res = {}
    for n in range(1, maxfull + 1):
        t = time.time()
        A, xy = carpet_graph(n)
        ev = spectrum(laplacian(A, kind))
        res[f"n{n}"] = ev
        print(f"{kind} level {n} V={A.shape[0]} full dense {time.time() - t:.1f}s", flush=True)
        if n in (3, 4):  # validate the sector reduction against the full spectrum
            M = 3**n
            ev2 = sector_spectra(A, xy, M, kind)
            print(f"   sector-vs-full max abs diff = {np.max(np.abs(ev2 - ev)):.2e}", flush=True)
    if do5:
        A, xy = carpet_graph(5)
        t = time.time()
        res["n5"] = sector_spectra(A, xy, 3**5, kind)
        print(f"{kind} level 5 sectors done {time.time() - t:.0f}s", flush=True)
    np.savez(f"carpet_spectra_{kind}.npz" if maxfull > 0 else f"carpet_spectra_{kind}_n5.npz", **res)
