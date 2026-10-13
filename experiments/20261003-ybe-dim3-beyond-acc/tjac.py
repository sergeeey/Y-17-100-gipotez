import time, numpy as np
from ybe import *
rng=np.random.default_rng(1)
for N in (2,3):
    R=rng.normal(size=(N*N,N*N))+1j*rng.normal(size=(N*N,N*N))
    a=jac_F_ref(R,N); b=jac_F_fast(R,N)
    print(N,'diff',np.abs(a-b).max(), np.abs(a).max())
    t=time.time()
    for _ in range(10): jac_F_fast(R,N)
    print('time fast',(time.time()-t)/10)
