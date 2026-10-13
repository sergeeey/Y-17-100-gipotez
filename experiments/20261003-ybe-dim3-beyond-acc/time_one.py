import time, numpy as np
from solver import one_start
for mode in ['gauss','near_id','real']:
    for seed in range(3):
        t=time.time(); o=one_start((3, 900000+seed, mode, 200)); print(mode, seed, o['ok'], '%.2e'%o['f'], o['it'], '%.1fs'%(time.time()-t), flush=True)
