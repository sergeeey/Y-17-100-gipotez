import numpy as np
from ybe import *
from solver import lm_solve
rng=np.random.default_rng(5)
H=hiet_families(rng)['H2,3']
H=H/abs(np.linalg.det(H))**0.25
R0=H+0.3*(rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)))/np.sqrt(2)
w=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
R0=R0/np.sum(w*R0)
for maxit in (300,3000):
    R,f,it=lm_solve(R0,2,w,maxit=maxit)
    print(maxit,'final f',f,'iters',it,'rel_res',rel_res(R,2))
