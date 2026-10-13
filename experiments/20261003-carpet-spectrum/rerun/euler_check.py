"""Independent structural check of the carpet vertex graph: Euler characteristic V - E + F = 1 - holes, F = 8^n cells, holes = (8^n-1)/7."""
from lib import carpet_graph
for n in range(1, 6):
    A, xy = carpet_graph(n)
    V = A.shape[0]; E = A.nnz // 2; F = 8**n; h = (8**n - 1) // 7
    print(f"n={n} V={V} E={E} F={F} chi=V-E+F={V-E+F} expected 1-holes={1-h} OK={V-E+F==1-h}", flush=True)
