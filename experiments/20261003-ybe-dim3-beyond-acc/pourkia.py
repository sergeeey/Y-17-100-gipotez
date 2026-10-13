"""Pourkia arXiv:1806.08400 n=3 family R_9 (as printed in the paper): braid-form solution with 7 free params."""
import numpy as np
from ybe import *
def R9(a1,b1,x1,y1,a2,b2,x):
    M=np.array([
     [a1,0,x1,0,0,0,y1,0,b1],
     [0,0,0,a2,0,b2,0,0,0],
     [y1,0,b1,0,0,0,a1,0,x1],
     [0,a2,0,0,0,0,0,b2,0],
     [0,0,0,0,x,0,0,0,0],
     [0,b2,0,0,0,0,0,a2,0],
     [x1,0,a1,0,0,0,b1,0,y1],
     [0,0,0,b2,0,a2,0,0,0],
     [b1,0,y1,0,0,0,x1,0,a1]],dtype=complex)
    return M
if __name__=='__main__':
    rng=np.random.default_rng(1)
    z=lambda: complex(rng.normal(),rng.normal())
    for t in range(4):
        R=R9(*[z() for _ in range(7)])
        R=R/abs(np.linalg.det(R))**(1/9)
        iv=invariants(R,3)
        print('res',rel_res(R,3),'det',abs(np.linalg.det(R)),'dimL',iv['dimL'],iv['cc'],'spec',iv['spec'],'tangent',iv['tangent'],'moduli',iv['moduli'],'rank',iv['rank'])
    # negative control: perturb
    R=R9(*[z() for _ in range(7)]); R[0,0]+=0.05
    print('perturbed res',rel_res(R,3))
