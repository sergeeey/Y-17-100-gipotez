import numpy as np
from solver_mask import *
from run_serial import MASKS
mask=MASKS['z3'](); idx=np.flatnonzero(mask.reshape(-1))
for seed in (5000,5001,5002):
    rng=np.random.default_rng(seed); R,w=random_masked_start(mask,rng,'gauss')
    out=[]
    for k in range(10):
        R,f,it,why=lm_mask(R,w,idx,maxit=150,abort=False)
        out.append('%.1e'%f)
        if why in('ok','stall'): break
    print(seed,why,out, 'detR=%.2e maxR=%.2e'%(abs(np.linalg.det(R)),np.abs(R).max()),flush=True)
