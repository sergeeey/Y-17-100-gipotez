import re
t=open('paper_2604.26870.md',encoding='utf-8').read()
# strip markdown links to arxiv anchors
t=re.sub(r'\[([^\]]*)\]\(https://arxiv\.org/html/2604\.26870#[^)]*\)',r'\1',t)
t=re.sub(r'\\','',t)
open('paper_clean.md','w',encoding='utf-8').write(t)
print(len(t))
