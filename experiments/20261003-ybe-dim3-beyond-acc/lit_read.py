import json,sys
F="C:/Users/serge/.claude/projects/E-------------------------------------------------Y-17-100-gipotez/9e146a80-48ac-4700-aadb-0cf8d72b4b4e/tool-results/mcp-firecrawl-firecrawl_scrape-1791059204280.txt"
t=json.load(open(F,encoding='utf8'))['markdown']
open('lit_2310.03816.md','w',encoding='utf8').write(t)
i=t.find('Introduction')
print(t[i:i+4500])
