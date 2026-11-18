import json, sys
sys.path.insert(0,'/tmp/ed'); from lines import LINES
D=json.load(open('/mnt/user-data/outputs/ep07/ep07_data.json'))
durs=json.load(open('/tmp/ed/vo/durs_t.json'))
shots=[s['id'] for s in D['shots']]
base={s['id']:s['dur'] for s in D['shots']}
bullet={s['id']:s['bullet'] for s in D['shots']}
CLIPLEN=json.load(open('/tmp/ed/cliplen.json')) if __import__('os').path.exists('/tmp/ed/cliplen.json') else {}
OVR={}  # manual base overrides
def plan(base_over={}):
    dur={k:base_over.get(k,v) for k,v in base.items()}
    host={}
    for L in LINES: host.setdefault(L[2],[]).append(L)
    # iterate until stable
    for it in range(5):
        start={}; t=0
        for s in shots: start[s]=t; t+=dur[s]
        place=[]; changed=False
        for i,s in enumerate(shots):
            cur=start[s]
            for L in host.get(s,[]):
                lid,spk,_,segs,off=L
                st = cur+0.25 if off=='after' else start[s]+(off if off>=0.5 else min(off,0.08))
                en = st+durs[lid]
                place.append((lid,spk,s,st,en)); cur=en
            if host.get(s):
                endneed=cur+0.1
                # spill allowed into following shots without lines
                j=i+1; avail=start[s]+dur[s]
                while endneed>avail and j<len(shots) and not host.get(shots[j]):
                    avail=start[shots[j]]+dur[shots[j]]; j+=1
                if endneed>avail:
                    dur[s]+=endneed-avail; changed=True
        if not changed: break
    start={}; t=0
    for s in shots: start[s]=t; t+=dur[s]
    return dur,start,place,t
if __name__=='__main__':
    dur,start,place,t=plan()
    print('total',round(t,1))
    for s in shots:
        ext = dur[s]-base[s]
        if ext>0.05: print(s, 'base',base[s],'->',round(dur[s],2))
