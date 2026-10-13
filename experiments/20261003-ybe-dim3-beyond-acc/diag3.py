import numpy as np
from ybe import *
from solver import lm_solve
rng=np.random.default_rng(11)
R=fam_generic(0.3+0.2j,0.7-0.4j,1.1+0.3j,0)
R=R/abs(np.linalg.det(R))**(1/9)
print('cond',np.linalg.cond(R),'max',abs(R).max())
for noise in (1e-3,0.02,0.2):
    for t in range(2):
        R0=R+noise*(rng.normal(size=(9,9))+1j*rng.normal(size=(9,9)))/np.sqrt(2)
        w=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9)); R0=R0/np.sum(w*R0)
        Rf,f,it=lm_solve(R0,3,w,maxit=600)
        print(noise,t,'f=%.2e its=%d'%(f,it), 'rel',rel_res(Rf,3))
