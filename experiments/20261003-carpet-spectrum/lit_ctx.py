import json,sys
p=r"C:\Users\serge\.claude\projects\E-------------------------------------------------Y-17-100-gipotez\9e146a80-48ac-4700-aadb-0cf8d72b4b4e\tool-results\mcp-firecrawl-firecrawl_scrape-1791039573080.txt"
t=json.load(open(p,encoding='utf-8'))["markdown"]
i=t.find("We do not see evidence of the spectral decimation")
print(t[i-2500:i+300])
for k in ("walk dimension","2.09","spectral dimension"):
    j=t.find(k); print("---",k,j); 
    if j>0: print(t[max(0,j-200):j+300])
