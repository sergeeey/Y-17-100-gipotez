"""Graph builders and spectra for the carpet-spectrum experiment. Pure numpy/scipy."""

import numpy as np
import scipy.sparse as sp


# ----------------------------------------------------------------- gasket
def gasket_edges(n):
    """Edges of Sierpinski gasket graph level n on integer triangular lattice side 2^n."""
    E = {((0, 0), (1, 0)), ((0, 0), (0, 1)), ((1, 0), (0, 1))}
    side = 1
    for _ in range(n):
        new = set()
        for dx, dy in [(0, 0), (side, 0), (0, side)]:
            for p, q in E:
                a = (p[0] + dx, p[1] + dy)
                b = (q[0] + dx, q[1] + dy)
                new.add((a, b) if a < b else (b, a))
        E = new
        side *= 2
    return E


def adjacency_from_edges(E):
    verts = sorted({v for e in E for v in e})
    idx = {v: i for i, v in enumerate(verts)}
    rows, cols = [], []
    for a, b in E:
        i, j = idx[a], idx[b]
        rows += [i, j]
        cols += [j, i]
    N = len(verts)
    A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(N, N))
    return A, verts


def gasket_graph(n):
    A, verts = adjacency_from_edges(gasket_edges(n))
    return A, verts


# ----------------------------------------------------------------- carpet
def carpet_cells(n):
    """Boolean array (3^n x 3^n) of retained unit cells of the level-n carpet."""
    c = np.ones((1, 1), dtype=bool)
    for _ in range(n):
        s = c.shape[0]
        new = np.zeros((3 * s, 3 * s), dtype=bool)
        for i in range(3):
            for j in range(3):
                if (i, j) != (1, 1):
                    new[i * s : (i + 1) * s, j * s : (j + 1) * s] = c
        # NOTE: this builds F_{n+1} as 8 copies of F_n (copy structure), same set as
        # replacing every retained cell by a level-1 carpet.
        c = new
    return c


def carpet_graph(n):
    """Vertex graph of the level-n carpet: lattice points of retained closed cells, edges = cell sides.
    Returns (A, coords) with coords an (N,2) int array (x=column index, y=row index)."""
    cells = carpet_cells(n)
    M = cells.shape[0]  # 3^n cells per side, lattice has M+1 points per side
    # a lattice edge is horizontal between (x,y)-(x+1,y); it is a side of cell (row y-1 or y, col x)
    pad = np.zeros((M + 2, M + 2), dtype=bool)
    pad[1 : M + 1, 1 : M + 1] = cells  # pad[r+1,c+1] = cells[r,c]
    # horizontal edge at lattice row y (0..M), column x (0..M-1): cells rows y-1 and y, col x
    H = pad[0 : M + 1, 1 : M + 1] | pad[1 : M + 2, 1 : M + 1]  # shape (M+1, M)
    # vertical edge at lattice row y (0..M-1), column x (0..M): cells row y, cols x-1 and x
    V = pad[1 : M + 1, 0 : M + 1] | pad[1 : M + 1, 1 : M + 2]  # shape (M, M+1)
    present = np.zeros((M + 1, M + 1), dtype=bool)
    present[:, :-1] |= H
    present[:, 1:] |= H
    present[:-1, :] |= V
    present[1:, :] |= V
    ids = -np.ones((M + 1, M + 1), dtype=np.int64)
    ys, xs = np.nonzero(present)
    ids[ys, xs] = np.arange(len(ys))
    N = len(ys)
    ey, ex = np.nonzero(H)
    a1 = ids[ey, ex]
    b1 = ids[ey, ex + 1]
    ey2, ex2 = np.nonzero(V)
    a2 = ids[ey2, ex2]
    b2 = ids[ey2 + 1, ex2]
    a = np.concatenate([a1, a2])
    b = np.concatenate([b1, b2])
    assert (a >= 0).all() and (b >= 0).all()
    A = sp.csr_matrix(
        (np.ones(2 * len(a)), (np.concatenate([a, b]), np.concatenate([b, a]))), shape=(N, N)
    )
    coords = np.stack([xs, ys], axis=1)
    return A, coords


# ----------------------------------------------------------------- misc graphs (controls)
def path_graph(N):
    A = sp.diags([np.ones(N - 1), np.ones(N - 1)], [-1, 1], format="csr")
    return A


def grid_graph(N):
    P = path_graph(N)
    I = sp.identity(N, format="csr")
    return (sp.kron(P, I) + sp.kron(I, P)).tocsr()


# ----------------------------------------------------------------- Laplacians / spectra
def laplacian(A, kind="L1"):
    d = np.asarray(A.sum(axis=1)).ravel()
    if kind == "L1":
        return sp.diags(d) - A
    if (
        kind == "L2"
    ):  # random-walk generator I - D^{-1}A, symmetrised similar matrix I - D^{-1/2} A D^{-1/2}
        Dm = sp.diags(1.0 / np.sqrt(d))
        return sp.identity(A.shape[0]) - Dm @ A @ Dm
    raise ValueError(kind)


def spectrum(M):
    M = M.toarray() if sp.issparse(M) else M
    return np.linalg.eigvalsh(M)


def cluster(ev, tol=1e-9):
    """Return (distinct values, multiplicities) clustering sorted eigenvalues at tolerance tol."""
    ev = np.sort(np.asarray(ev))
    vals, mult = [], []
    start = 0
    for i in range(1, len(ev) + 1):
        if i == len(ev) or ev[i] - ev[i - 1] > tol:
            seg = ev[start:i]
            vals.append(seg.mean())
            mult.append(len(seg))
            start = i
    return np.array(vals), np.array(mult)
