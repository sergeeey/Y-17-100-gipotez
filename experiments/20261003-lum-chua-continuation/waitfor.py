import sys,time
f,pat,to=sys.argv[1],sys.argv[2],float(sys.argv[3])
t=time.time()
while time.time()-t<to:
    try:
        s=open(f,encoding="utf8",errors="ignore").read()
        if pat in s: break
    except Exception: pass
    time.sleep(3)
print(open(f,encoding="utf8",errors="ignore").read()[-1500:])
