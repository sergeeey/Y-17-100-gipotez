import json,sys
d=json.load(open(r"C:/Users/serge/.claude/projects/E-------------------------------------------------Y-17-100-gipotez/9e146a80-48ac-4700-aadb-0cf8d72b4b4e/tool-results/mcp-firecrawl-firecrawl_scrape-1791017586438.txt",encoding='utf-8'))
md=d['markdown']
open('paper_2604.26870.md','w',encoding='utf-8').write(md)
print(len(md), d['metadata'].get('title'))
