import numpy as np
from lib import *

for n in range(0, 6):
    A, xy = carpet_graph(n)
    N = A.shape[0]
    E = A.nnz // 2
    deg = np.asarray(A.sum(axis=1)).ravel()
    # connectivity
    ncomp = sp.csgraph.connected_components(A)[0]
    cells = int(carpet_cells(n).sum())
    print(
        f"n={n} V={N} E={E} cells={cells} (8^n={8**n}) comps={ncomp} degs={np.bincount(deg.astype(int))[2:]} lattice={3**n + 1}^2",
        flush=True,
    )
# hand check n=1: 16 vertices, 24 edges
A, xy = carpet_graph(1)
assert A.shape[0] == 16 and A.nnz // 2 == 24
# Euler check: V - E + F = 1 + (#holes) for planar cell complex; F=cells; connected, holes count (bounded faces not cells)
# n=2: V-E+cells = 1 - holes  => holes = 1 + ... (just print)
for n in range(1, 5):
    A, xy = carpet_graph(n)
    V = A.shape[0]
    E = A.nnz // 2
    F = int(carpet_cells(n).sum())
    print(
        f"Euler n={n}: V-E+F = {V - E + F}  (should be 1 - #holes where holes of the cell complex = (8^n-1)/7 ... )",
        "holes expected",
        (8**n - 1) // 7,
    )
