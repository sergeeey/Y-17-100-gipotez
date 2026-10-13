import sympy as sp, time, sys, itertools
e = sp.Rational(sys.argv[1]) if len(sys.argv) > 1 else sp.Integer(5)
a = 1 - e
# index map: |ij> -> 3i+j ; W=[0,1,3,4]; S1 = [2 (02), 5 (12), 6 (20), 7 (21)]
x = sp.symbols('x1:10')
R = sp.zeros(9, 9)
R[0, 0] = 1; R[4, 4] = 1; R[8, 8] = 1
R[1, 3] = a      # |01> <- |10>   (index 1 <- 3)
R[3, 1] = 1      # |10> <- |01>
R[3, 3] = e
# B1: rows/cols (02=2, 12=5, 20=6, 21=7)
R[2, 2] = 1; R[6, 6] = 1
R[5, 2], R[5, 5], R[5, 6], R[5, 7] = x[0], x[1], x[2], x[3]
R[7, 2], R[7, 5], R[7, 6] = x[4], x[5], x[6]
# gauge: x1 (12<-02) nonzero -> set to 1 for the solve
sub = {x[0]: 1}
R = R.subs(sub)
vars_ = [v for v in x if v not in sub and R.has(v)]
print('unknowns', vars_, flush=True)
I3 = sp.eye(3)
A = sp.kronecker_product(R, I3); B = sp.kronecker_product(I3, R)
F = (A*B*A - B*A*B).applyfunc(sp.expand)
eqs = list({q for q in F if q != 0})
print('distinct nonzero eqs', len(eqs), flush=True)
t = time.time()
G = sp.groebner(eqs, *vars_, order='grevlex', domain=sp.QQ)
print('groebner time', time.time() - t, 'size', len(G.exprs), flush=True)
for g in G.exprs: print(sp.factor(g))
