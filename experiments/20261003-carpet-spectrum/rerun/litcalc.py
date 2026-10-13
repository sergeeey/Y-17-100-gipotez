import numpy as np
rho=1.251487
print("d_w=ln(8rho)/ln3 =", np.log(8*rho)/np.log(3), " d_s=2ln8/ln(8rho)=", 2*np.log(8)/np.log(8*rho), " 8rho=", 8*rho)
print("gasket d_w=ln5/ln2=",np.log(5)/np.log(2)," d_s=2ln3/ln5=",2*np.log(3)/np.log(5))
# measured: lowest-eigenvalue ratio r -> rho_est = r/8
for name,r in (("L1 4->5",9.9476),("L2 4->5",10.0321),("L2 3->4",10.0356)):
    print(name,"r",r,"rho_est",r/8,"d_w",np.log(r)/np.log(3),"rel diff to 8rho",(r-8*rho)/(8*rho))
