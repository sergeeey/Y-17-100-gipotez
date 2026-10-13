"""Power test for the U1-free (non-Lie-charge-conserving) region in dim 3: start lm_det from noisy copies of the two Gaussian (Weyl-Heisenberg) solutions
of the controls; count convergence and the L-class of the limit.  If recovery is poor at the noise scale of the random-start search, a
null result for U1-free components from that search is uninformative."""
import numpy as np, collections
from ybe import *
from solver_mask import lm_det
from classify3 import analyse, clean
w = np.exp(2j*np.pi/3); Xm = np.roll(np.eye(3),1,axis=0); Zm = np.diag([w**j for j in range(3)]); PS = np.kron(Xm,Zm)
G1 = (np.eye(9)+w*(PS+PS@PS))/np.sqrt(3)
eta = np.exp(1j*np.pi/6); x=-eta/np.sqrt(3); y=1+x; G2 = x*np.eye(9)+y*PS+y*PS@PS
idx = np.arange(81)
for nm,G in (('G1',G1),('G2',G2)):
    G = clean(G); a0 = analyse(G); print(nm,'res0=%.1e'%a0['res'],a0['label'],'dimL',a0['dimL'],'mults',a0['mults'])
    for noise in (0.02,0.05,0.1,0.2,0.4,0.8):
        c = collections.Counter()
        for t in range(25):
            rng=np.random.default_rng(31*t+7)
            R0 = G + noise*(rng.normal(size=(9,9))+1j*rng.normal(size=(9,9)))/np.sqrt(2)
            R0 = R0*np.linalg.det(R0)**(-1/9)
            Rf,f,it,why = lm_det(R0, idx, maxit=200, abort=False)
            if why!='ok': c['nc-'+why]+=1; continue
            a = analyse(Rf); c['ok-'+a['label']+'-dimL%d'%a['dimL']]+=1
        print('  noise %.2f'%noise, dict(c), flush=True)
