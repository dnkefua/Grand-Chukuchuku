import json,cv2,numpy as np,sys
S=json.load(open('plan.json'))
def cat(s,fr):
    c=s['c']
    if not isinstance(c,list): return c
    for (f0,c0),(f1,c1) in zip(c[:-1],c[1:]):
        if fr<=f1: return c0+(c1-c0)*(fr-f0)/max(1e-6,f1-f0)
    return c[-1][1]
cap=cv2.VideoCapture("/mnt/user-data/uploads/Final cut/Youtube submission/Grand Chuckuchucku - Episode 7 - First Bottle.mp4")
ids=[int(x) for x in sys.argv[2].split(',')] if len(sys.argv)>2 else range(len(S))
rows=[];cur=[]
for i in ids:
    s=S[i]; g=[]
    for k in range(5):
        fr=k/4; t=s['a']+0.08+(s['b']-s['a']-0.16)*fr
        cap.set(cv2.CAP_PROP_POS_MSEC,t*1000); ok,f=cap.read(); f=cv2.resize(f,(256,144))
        x0=int(cat(s,fr)*256-40.5); cv2.rectangle(f,(x0,0),(x0+81,143),(0,255,255),2)
        if k==0: cv2.putText(f,f'{i}',(4,18),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),4);cv2.putText(f,f'{i}',(4,18),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
        g.append(f)
    g=np.hstack(g); cv2.rectangle(g,(0,0),(1279,143),(255,255,255),1); cur.append(g)
    if len(cur)==2: rows.append(np.hstack(cur)); cur=[]
if cur: rows.append(np.hstack(cur+[np.zeros_like(cur[0])]))
for n in range(0,len(rows),10):
    cv2.imwrite(f'{sys.argv[1]}_{n//10}.jpg',np.vstack(rows[n:n+10]),[cv2.IMWRITE_JPEG_QUALITY,80])
