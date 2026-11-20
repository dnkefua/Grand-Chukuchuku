import cv2, numpy as np, json, sys
Y = "/mnt/user-data/uploads/Final cut/Youtube submission/Grand Chuckuchucku - Episode 7 - First Bottle.mp4"
cuts = [0.0] + [float(x) for x in open('/home/claude/e7tt/cuts.txt').read().split()]
cap = cv2.VideoCapture(Y); FPS = cap.get(cv2.CAP_PROP_FPS); N = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
TOT = N / FPS; cuts.append(TOT)
# downsampled gray frames for every frame (192 wide)
G = []
while True:
    ok, f = cap.read()
    if not ok: break
    G.append(cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (192, 108), interpolation=cv2.INTER_AREA).astype(np.float32))
G = np.array(G); print('frames', len(G), FPS)
np.save('/home/claude/e7tt/G.npy', G)
W = 608 / 1920 * 192  # crop width in small px (9:16 of 1080 height)
shots = []
for a, b in zip(cuts[:-1], cuts[1:]):
    fa, fb = int(round(a * FPS)), int(round(b * FPS))
    if fb - fa < 3: continue
    cx = []
    for k in range(fa + 1, fb):
        d = np.abs(G[k] - G[k - 1])
        d[d < 6] = 0
        col = d.sum(0)
        if col.sum() < 50: cx.append(np.nan); continue
        xs = np.arange(192)
        cx.append(float((col * xs).sum() / col.sum()))
    cx = np.array(cx)
    # whole-shot motion distribution
    tot = np.zeros(192)
    for k in range(fa + 1, fb):
        d = np.abs(G[k] - G[k - 1]); d[d < 6] = 0; tot += d.sum(0)
    shots.append(dict(a=a, b=b, fa=fa, fb=fb, cx=[None if np.isnan(v) else v for v in cx], tot=tot.tolist()))
json.dump(shots, open('/home/claude/e7tt/shots.json', 'w'))
print(len(shots), 'shots')
