import json, re, math
from collections import defaultdict, Counter
pairs=json.load(open('pairs.json'))
STOP=set()
def etok(s):
    s=s.lower().replace("'s"," 's")
    return [w for w in re.findall(r"[a-z]+", s)]
def stok(t):
    toks=[]
    for w in t.split():
        w=''.join(ch for ch in w if 0xE000<=ord(ch)<=0xF8FF)
        if not w: continue
        w=w.replace('','')
        if not w: continue
        toks.append(w)
    return toks
data=[(stok(t), etok(e)) for k,t,e in pairs]
data=[(s,e) for s,e in data if s and e]
print('verse pairs', len(data))
svocab=Counter(w for s,_ in data for w in s); evocab=Counter(w for _,e in data for w in e)
print('SUN word types', len(svocab), 'English types', len(evocab))
# IBM Model 1: P(e|s) with NULL
def model1(src, tgt, iters=8):
    t=defaultdict(lambda:1.0)
    for it in range(iters):
        count=defaultdict(float); total=defaultdict(float)
        for S,E in zip(src,tgt):
            S2=['NULL']+S
            for e in E:
                z=sum(t[(e,s)] for s in S2)
                for s in S2:
                    c=t[(e,s)]/z; count[(e,s)]+=c; total[s]+=c
        t=defaultdict(lambda:1e-9, {k:v/total[k[1]] for k,v in count.items()})
    return t
src=[s for s,e in data]; tgt=[e for s,e in data]
t_es=model1(src,tgt)          # P(english | sun)
t_se=model1(tgt,src)          # P(sun | english)
# co-occurrence
co=defaultdict(Counter); ecount=Counter(); scount=Counter()
for S,E in data:
    Sset=set(S); Eset=set(E)
    for s in Sset:
        scount[s]+=1
        for e in Eset: co[s][e]+=1
    for e in Eset: ecount[e]+=1
N=len(data)
def dice(s,e): return 2*co[s][e]/(scount[s]+ecount[e])
rows=[]
for s,n in svocab.most_common():
    cands={}
    for e in co[s]:
        if co[s][e]<2: continue
        score = 0.5*t_es[(e,s)]+0.5*t_se[(s,e)] + 0.3*dice(s,e)
        cands[e]=score
    top=sorted(cands.items(), key=lambda kv:-kv[1])[:5]
    cp='+'.join(f'U+{ord(ch):04X}' for ch in s)
    rows.append({'sun':cp,'count':n,'verses':scount[s],'top':[(e,round(sc,3),co[s][e]) for e,sc in top]})
json.dump(rows, open('alignment.json','w'), ensure_ascii=False, indent=0)
for r in rows[:60]:
    print(r['sun'], r['count'], r['top'][:3])
