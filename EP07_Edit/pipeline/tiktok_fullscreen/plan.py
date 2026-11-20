import json, numpy as np, cv2, sys
Y = "/mnt/user-data/uploads/Final cut/Youtube submission/Grand Chuckuchucku - Episode 7 - First Bottle.mp4"
S = json.load(open('/home/claude/e7tt/shots.json'))
OV = json.load(open('/home/claude/e7tt/overrides.json')) if len(sys.argv) > 1 else {}
W = 608 / 10  # small px (192 wide)
for i, s in enumerate(S):
    tot = np.array(s['tot']); tot = tot / (tot.sum() + 1e-9)
    # prefer center slightly
    best, bx = -1, 96
    for c in np.arange(W / 2, 192 - W / 2 + 0.01, 1):
        lo, hi = int(c - W / 2), int(c + W / 2)
        sc = tot[lo:hi].sum() - 0.0015 * abs(c - 96)
        if sc > best: best, bx = sc, c
    s['c'] = float(bx) / 192  # fraction of width for crop center
    if str(i) in OV:
        s['c'] = OV[str(i)] if not isinstance(OV[str(i)], list) else OV[str(i)]
json.dump(S, open('/home/claude/e7tt/plan.json', 'w'))
cap = cv2.VideoCapture(Y)
tiles = []
for i, s in enumerate(S):
    t = (s['a'] + s['b']) / 2
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, f = cap.read()
    f = cv2.resize(f, (320, 180))
    cs = s['c'] if not isinstance(s['c'], list) else s['c']
    cl = [p[1] for p in cs] if isinstance(cs, list) else [cs]
    for k, c in enumerate(cl):
        x0 = int(c * 320 - 50.7); col = (0, 255, 255) if k == 0 else (255, 0, 255)
        cv2.rectangle(f, (x0, 0), (x0 + 101, 179), col, 2)
    cv2.putText(f, f'{i} {s["a"]:.1f}', (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 3)
    cv2.putText(f, f'{i} {s["a"]:.1f}', (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    tiles.append(f)
while len(tiles) % 8: tiles.append(np.zeros_like(tiles[0]))
rows = [np.hstack(tiles[r:r + 8]) for r in range(0, len(tiles), 8)]
cv2.imwrite('/home/claude/e7tt/plan_a.jpg', np.vstack(rows[:5]), [cv2.IMWRITE_JPEG_QUALITY, 85])
cv2.imwrite('/home/claude/e7tt/plan_b.jpg', np.vstack(rows[5:]), [cv2.IMWRITE_JPEG_QUALITY, 85])
