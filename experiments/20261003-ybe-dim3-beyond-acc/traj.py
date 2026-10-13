import numpy as np
from solver import random_start, lm_solve
import solver
for mode,seed in [('gauss',900000),('near_flip',900001),('gauss',900005)]:
    rng=np.random.default_rng(seed); R0,w=random_start(3,rng,mode)
    # record trajectory by running in chunks of 20 iters
    R=R0
    for k in range(10):
        R,f,it=lm_solve(R,3,w,maxit=30)
        print(mode,seed,'iter',30*(k+1),'f=%.2e'%f,flush=True)
        if f<1e-12 or R is None: break
