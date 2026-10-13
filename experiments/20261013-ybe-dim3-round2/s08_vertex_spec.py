import sympy as sp, numpy as np
e, u, v, x = sp.symbols('e u v x')
def fam(e, u, v):
    R = sp.zeros(9, 9)
    R[0, 0] = R[4, 4] = R[8, 8] = 1
    R[1, 3] = 1 - e; R[3, 1] = 1; R[3, 3] = e
    R[2, 2] = 1; R[6, 6] = 1
    R[5, 2] = 1; R[5, 5] = e; R[5, 6] = (e-1)*v/u; R[5, 7] = -(e-1)/u
    R[7, 2] = u/(e-1); R[7, 5] = u; R[7, 6] = v
    return R
Pq = sp.Matrix(9, 9, lambda a, b: 1 if (a == 3*(b % 3) + b//3) else 0)
Rb = fam(e, u, v)
Rv = Pq * Rb
print('vertex-form charpoly:', sp.factor(Rv.charpoly(x).as_expr()))
# nonzero pattern of vertex form
print(Rv)
# is Rv diagonalizable generically? rank of (Rv - 1)
print('rank(Rv-1) at e=5,u=2,v=3:', (Rv - sp.eye(9)).subs({e: 5, u: 2, v: 3}).rank())
