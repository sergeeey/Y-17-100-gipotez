import glob, json, re, sys
for f in sorted(glob.glob("results/c*.txt"), key=lambda s:(s.split('_')[0], int(re.search(r'd(\d+)',s).group(1)))):
    L=open(f,encoding='utf8',errors='replace').read().splitlines()
    if not L or not L[0].startswith('{'): print(f, "NO-STATS yet", len(L)); continue
    s=json.loads(L[0]); 
    print(f.split('/')[-1], "d=%d n=%d found=%d leaves=%d secs=%s"%(s['d'],s['n'],s['found'],s['leaves'],s['secs']), "TRUNC" if s.get('truncated') else "")
