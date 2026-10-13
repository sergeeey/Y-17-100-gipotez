import numpy as np
from ybe import *
d=np.load('dim2_search2.npz')
np.set_printoptions(precision=4, suppress=True, linewidth=160)
n=0
for i,R in enumerate(d['R']):
    Rn=R/abs(np.linalg.det(R))**0.25
    ev=np.linalg.eigvals(Rn)
    td,s=tangent_dim(Rn,2)
    if td==1:
        print(d['mode'][i], 'res',rel_res(R,2))
        print(Rn)
        print('eig',ev)
        print('sv jac',s[:8], s[-4:])
        n+=1
        if n>=2: break
