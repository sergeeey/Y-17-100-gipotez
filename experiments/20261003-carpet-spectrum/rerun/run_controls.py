import numpy as np, json, time, sys
from lib import *
from search import search_all


def dist(ev):
    return cluster(ev, 1e-9)[0]


out = {}
rng = np.random.default_rng(12345)


def run(name, fine, coarse, dmax=6):
    t = time.time()
    res = search_all(dist(fine), dist(coarse), dmax)
    out[name] = res
    print(
        f"== {name}  (fine distinct {len(dist(fine))}, coarse distinct {len(dist(coarse))}) {time.time() - t:.1f}s",
        flush=True,
    )
    for r in res:
        a = None if r["a"] is None else [float(f"{x:.6g}") for x in r["a"]]
        print(
            f"   d={r['d']} matched={r['matched']}/{r['n_fine']} frac={r['frac']:.3f} cov={r['coverage']:.3f} a={a}",
            flush=True,
        )


# POSITIVE 1: gasket 4*L2
G = {}
for n in range(1, 8):
    A, v = gasket_graph(n)
    G[n] = np.linalg.eigvalsh((4 * laplacian(A, "L2")).toarray())
np.savez("gasket_4L2_spectra.npz", **{f"L{n}": G[n] for n in G})
for n in (3, 5, 6):
    run(f"POS1_gasket_{n}to{n + 1}", G[n + 1], G[n])

# POSITIVE 2: path graph Neumann (D-A), N = 2^n vertices
P = {}
for n in range(2, 10):
    N = 2**n
    P[n] = np.linalg.eigvalsh(laplacian(path_graph(N), "L1").toarray())
for n in (5, 7, 8):
    run(f"POS2_path_{2**n}to{2 ** (n + 1)}", P[n + 1], P[n])

# NEGATIVE 1: 2D grid N x N Neumann (D-A)
Gr = {}
for N in (8, 16, 32):
    Gr[N] = np.linalg.eigvalsh(laplacian(grid_graph(N), "L1").toarray())
for N in (8, 16):
    run(f"NEG1_grid_{N}to{2 * N}", Gr[2 * N], Gr[N])

# NEGATIVE 2: jittered gasket
for n in (5, 6):
    jit = G[n + 1] * (1 + 1e-4 * rng.standard_normal(len(G[n + 1])))
    run(f"NEG2_jittered_gasket_{n}to{n + 1}", jit, G[n])

json.dump(out, open("controls_result.json", "w"), indent=1, default=float)
