import time, numpy as np
from solver import *
rng=np.random.default_rng(0)
for N in (2,3):
    R0,w=random_start(N,rng,'gauss')
    S=np.linalg.inv(R0)
    t=time.time()
    for _ in range(20): J=jac(R0,S,N,w)
    t1=(time.time()-t)/20
    t=time.time()
    for _ in range(20): A=J.conj().T@J
    t2=(time.time()-t)/20
    t=time.time()
    for _ in range(20): np.linalg.solve(A+np.eye(A.shape[0]),np.ones(A.shape[0]))
    t3=(time.time()-t)/20
    print(N,'jac',t1,'JHJ',t2,'solve',t3,flush=True)
