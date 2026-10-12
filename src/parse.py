import re,json,sys,statistics as st,collections
rows=[]
pat=re.compile(r'^\s*(\d+)\.\s+(\d+)\s+(.*?)\s{2,}(.*?)\s{2,}(\S.*?)\s+(\d+)\.\s+(\d+)\.\s+(\d:\d\d:\d\d,\d)\s+(\d:\d\d:\d\d,\d)\s+(\d:\d\d:\d\d,\d)\s*$')
def sec(s):h,m,x=s.split(':');return int(h)*3600+int(m)*60+float(x.replace(',','.'))
bad=[]
for line in open(sys.argv[1]):
    m=pat.match(line)
    if m:
        g=m.groups();rows.append(dict(rank=int(g[0]),bib=g[1],name=g[2],club=g[3].strip(),ak=g[4].strip(),akp=int(g[5]),mwp=int(g[6]),r1=sec(g[7]),r2=sec(g[8]),t=sec(g[9])))
    elif re.match(r'^\s*\d+\.\s+\d+',line): bad.append(line)
print(len(rows),len(bad));print(bad[:5])
json.dump(rows,open(sys.argv[2],'w'),ensure_ascii=False)
