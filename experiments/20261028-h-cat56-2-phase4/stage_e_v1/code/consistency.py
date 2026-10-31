# WHY: dependent rows must be exact combinations of an independent subset, and their RHS must match
# the same combinations.  Numerical test: least-squares coefficients C with A_E ~ C A_I, then residuals.
import numpy as np
Af = np.load("../logs/A_float.npy")
bf = np.load("../logs/rhs_float.npy")
I = np.load("../logs/indep_rows.npy")
E = np.setdiff1d(np.arange(Af.shape[0]), I)
AI, AE = Af[I], Af[E]
C, *_ = np.linalg.lstsq(AI.T, AE.T, rcond=None)   # AE ~ C^T AI  ->  AI^T X = AE^T
C = C.T
print("rows independent:", len(I), " dependent:", len(E))
print("max |AE - C AI| (row dependence residual):", np.abs(AE - C @ AI).max())
print("max |bE - C bI| (RHS consistency residual):", np.abs(bf[E] - C @ bf[I]).max())
print("max |b| :", np.abs(bf).max())
