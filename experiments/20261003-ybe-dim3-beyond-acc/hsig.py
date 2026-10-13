import numpy as np
from ybe import *
from analyze import sig_of
rng=np.random.default_rng(7)
for name,R in hiet_families(rng).items():
    s,iv=sig_of(R,2)
    print(name, s)
