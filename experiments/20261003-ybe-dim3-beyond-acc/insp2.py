import numpy as np
from ybe import *
from analyze import sig_of
np.set_printoptions(precision=4, suppress=True, linewidth=170)
d=np.load('dim2_search2.npz')
P=flip(2)
cnt=0
for i,R in enumerate(d['R']):
    s,iv=sig_of(R,2)
    if s[1]==4 and s[0]==((3,3),(1,1)):
        Rn=R/abs(np.linalg.det(R))**0.25
        # fit R = a I + b P
        B=np.array([np.eye(4).ravel(),P.ravel()]).T
        c,*_=np.linalg.lstsq(B,Rn.ravel(),rcond=None)
        print('flip-like: a,b=',c,' fit err',np.linalg.norm(B@c-Rn.ravel()),' tangent',iv['tangent'], 'mode',d['mode'][i]); cnt+=1
        if cnt>=4: break
# tangent of exact P and of nearby 'a I + bP' using tolerance sweep
for tol in (1e-4,1e-7,1e-10):
    print('tol',tol,'tangent at P',tangent_dim(P.astype(complex),2,tol)[0], ' at 1.0*P+0.0', )
td,s=tangent_dim(P.astype(complex),2); print('sv at P',s)
