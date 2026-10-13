import time, numpy as np
from search import *
t=time.time(); 
for _ in range(5): c=evaluate(P0)
print(c,(time.time()-t)/5)
t=time.time()
for _ in range(5): c=evaluate(P0,n=800)
print(c,(time.time()-t)/5)
