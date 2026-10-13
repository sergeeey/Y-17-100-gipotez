"""Robustness variant (post-hoc, declared as such): CELL-adjacency graph of the level-n carpet (the object used in
the discrete-magic-carpet survey arXiv:1902.03408 is of this cell type [WEAK: only inferred from 'eight cells in MC_m']).
Vertices = retained unit cells (8^n); edges: (E4) share a side, (E8) share a side or a corner.
Operators L1 = D-A, L2 = I - D^-1/2 A D^-1/2. Same blind search (pre-registered family) on pairs 2->3, 3->4."""
import json, time
import numpy as np
import scipy.sparse as sp
from lib import cluster, laplacian
from search import search_all
from lib import carpet_cells

def cell_graph(n, eight):
    c = carpet_cells(n); M = c.shape[0]
    ids = -np.ones((M, M), dtype=np.int64)
    ys, xs = np.nonzero(c); ids[ys, xs] = np.arange(len(ys)); N = len(ys)
    r, q = [], []
    shifts = [(0, 1), (1, 0)] + ([(1, 1), (1, -1)] if eight else [])
    for dy, dx in shifts:
        for y, x in zip(ys, xs):
            y2, x2 = y + dy, x + dx
            if 0 <= y2 < M and 0 <= x2 < M and c[y2, x2]:
                r.append(ids[y, x]); q.append(ids[y2, x2])
    r = np.array(r); q = np.array(q)
    A = sp.csr_matrix((np.ones(2 * len(r)), (np.concatenate([r, q]), np.concatenate([q, r]))), shape=(N, N))
    return A

OUT = {}
for eight in (False, True):
    for kind in ("L1", "L2"):
        spec = {}
        for n in (1, 2, 3, 4):
            A = cell_graph(n, eight)
            deg = np.asarray(A.sum(axis=1)).ravel()
            assert deg.min() > 0
            spec[n] = np.linalg.eigvalsh(laplacian(A, kind).toarray())
        for n in (2, 3):
            fv = cluster(spec[n + 1], 1e-9)[0]; cv = cluster(spec[n], 1e-9)[0]
            t = time.time()
            res = search_all(fv, cv, 6)
            name = f"cell{'8' if eight else '4'}_{kind}_{n}to{n+1}"
            OUT[name] = [{k: v for k, v in r.items()} for r in res]
            best = max(r["frac"] for r in res)
            print(f"[{name}] distinct fine {len(fv)} coarse {len(cv)} best_frac={best:.3f} "
                  + " ".join(f"d{r['d']}:{r['matched']}" for r in res) + f" {time.time()-t:.0f}s", flush=True)
json.dump(OUT, open("cellgraph_result.json", "w"), indent=1, default=float)
