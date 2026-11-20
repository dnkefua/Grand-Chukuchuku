import json,cv2,numpy as np,sys
S=json.load(open('plan.json'))
cap=cv2.VideoCapture("/mnt/user-data/uploads/Final cut/Youtube submission/Grand Chuckuchucku - Episode 7 - First Bottle.mp4")
i=int(sys.argv[1]); step=float(sys.argv[2]); out=sys.argv[3]; W=int(sys.argv[4]) if len(sys.argv)>4 else 384
s=S[i]; tiles=[]; t=s['a']+0.04
while t<s['b']-0.02:
    cap.set(cv2.CAP_PROP_POS_MSEC,t*1000); ok,f=cap.read(); f=cv2.resize(f,(W,W*9//16))
    for g in range(1,10): cv2.line(f,(W*g//10,0),(W*g//10,W*9//16),(0,255,255),1)
    cv2.putText(f,f'{i} +{t-s["a"]:.1f} ({(t-s["a"])/(s["b"]-s["a"]):.2f})',(4,16),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),3)
    cv2.putText(f,f'{i} +{t-s["a"]:.1f} ({(t-s["a"])/(s["b"]-s["a"]):.2f})',(4,16),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
    tiles.append(f); t+=step
while len(tiles)%5: tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(out,np.vstack([np.hstack(tiles[r:r+5]) for r in range(0,len(tiles),5)]),[cv2.IMWRITE_JPEG_QUALITY,82])
