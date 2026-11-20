"""Step 2: review sheets. Look at every one before rendering.

usage:
  python3 tt_review.py <config> plan                 # every shot: 5 frames across the shot, yellow box = 9:16 window
  python3 tt_review.py <config> plan 15,26,64        # only these shots
  python3 tt_review.py <config> dialogue             # every subtitle line: frame at mid-line + box -> is the SPEAKER inside?
  python3 tt_review.py <config> strip 64 0.5         # one shot every 0.5 s, 10% grid, for writing keyframes
  python3 tt_review.py <config> output [video]       # rendered vertical: start / middle / end of every shot
Sheets are written to <work>/review/.
"""
import sys, os, json
import cv2, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tt_common import load_config, load_shots, subtitle_events, centre_at, split_active, interp, CROP_FRAC


def label(img, txt, y=18, s=0.55):
    cv2.putText(img, txt, (4, y), cv2.FONT_HERSHEY_SIMPLEX, s, (0, 0, 0), 4)
    cv2.putText(img, txt, (4, y), cv2.FONT_HERSHEY_SIMPLEX, s, (255, 255, 255), 1)


def boxed(cap, s, fr, w=256):
    t = s['a'] + 0.06 + (s['b'] - s['a'] - 0.12) * fr
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, f = cap.read()
    h = w * 9 // 16; f = cv2.resize(f, (w, h)); bw = int(CROP_FRAC * w)
    if split_active(s['spec'], fr):   # split screen: magenta = top panel, cyan = bottom panel
        sp = s['spec']['split']
        for kf, col in ((sp['top'], (255, 0, 255)), (sp['bot'], (255, 255, 0))):
            cx, cy = interp(kf, fr)[:2]; ph = int(h * 600 / 1080); pw = int(ph * 1080 / 957)
            x0 = int(cx * w - pw / 2); y0 = int(cy * h - ph / 2)
            cv2.rectangle(f, (x0, y0), (x0 + pw, y0 + ph), col, 2)
    else:
        x0 = int(centre_at(s['spec'], fr) * w - bw / 2)
        cv2.rectangle(f, (x0, 0), (x0 + bw, h - 1), (0, 255, 255), 2)
    return f


def save_rows(rows, name, per=10):
    out = []
    for n in range(0, len(rows), per):
        p = os.path.join(REV, f'{name}_{n // per}.jpg'); cv2.imwrite(p, np.vstack(rows[n:n + per]), [cv2.IMWRITE_JPEG_QUALITY, 82]); out.append(p)
    print('\n'.join(out))


def plan(cfg, S, ids):
    cap = cv2.VideoCapture(cfg['master']); rows, cur = [], []
    for i in ids:
        g = [boxed(cap, S[i], k / 4) for k in range(5)]; label(g[0], str(i))
        g = np.hstack(g); cv2.rectangle(g, (0, 0), (g.shape[1] - 1, g.shape[0] - 1), (255, 255, 255), 1); cur.append(g)
        if len(cur) == 2: rows.append(np.hstack(cur)); cur = []
    if cur: rows.append(np.hstack(cur + [np.zeros_like(cur[0])]))
    save_rows(rows, 'plan')


def dialogue(cfg, S):
    cap = cv2.VideoCapture(cfg['master']); tiles = []
    for n, (a, b, txt) in enumerate(subtitle_events(cfg)):
        m = (a + b) / 2; i = next(k for k, s in enumerate(S) if s['a'] <= m < s['b'] or k == len(S) - 1)
        s = S[i]; fr = (m - s['a']) / max(1e-6, s['b'] - s['a'])
        cap.set(cv2.CAP_PROP_POS_MSEC, m * 1000); ok, f = cap.read(); f = cv2.resize(f, (480, 270))
        x0 = int(centre_at(s['spec'], fr) * 480 - CROP_FRAC * 240); cv2.rectangle(f, (x0, 0), (x0 + int(CROP_FRAC * 480), 269), (0, 255, 255), 2)
        label(f, f'L{n} sh{i} ' + txt.replace('\\N', ' ')[:40], 262, 0.45); tiles.append(f)
    while len(tiles) % 5: tiles.append(np.zeros_like(tiles[0]))
    save_rows([np.hstack(tiles[r:r + 5]) for r in range(0, len(tiles), 5)], 'dialogue', 4)


def strip(cfg, S, i, step):
    cap = cv2.VideoCapture(cfg['master']); s = S[i]; tiles = []; t = s['a'] + 0.04; W = 384
    while t < s['b'] - 0.02:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, f = cap.read(); f = cv2.resize(f, (W, W * 9 // 16))
        for g in range(1, 10): cv2.line(f, (W * g // 10, 0), (W * g // 10, W * 9 // 16), (0, 255, 255), 1)
        label(f, f'{i} +{t - s["a"]:.1f}s  frac {(t - s["a"]) / (s["b"] - s["a"]):.2f}', 16, 0.5); tiles.append(f); t += step
    while len(tiles) % 5: tiles.append(np.zeros_like(tiles[0]))
    save_rows([np.hstack(tiles[r:r + 5]) for r in range(0, len(tiles), 5)], f'strip_{i}', 8)


def output(cfg, S, video):
    cap = cv2.VideoCapture(video); tiles = []
    for i, s in enumerate(S):
        g = []
        for t in (s['a'] + 0.15, (s['a'] + s['b']) / 2, s['b'] - 0.15):
            cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, f = cap.read(); g.append(cv2.resize(f, (100, 178)))
        g = np.hstack(g); cv2.rectangle(g, (0, 0), (299, 177), (0, 255, 255), 1); label(g, str(i), 14, 0.45); tiles.append(g)
    while len(tiles) % 8: tiles.append(np.zeros_like(tiles[0]))
    save_rows([np.hstack(tiles[r:r + 8]) for r in range(0, len(tiles), 8)], 'output', 5)


if __name__ == '__main__':
    cfg = load_config(sys.argv[1]); S = load_shots(cfg); mode = sys.argv[2]
    REV = os.path.join(cfg['work'], 'review'); os.makedirs(REV, exist_ok=True)
    if mode == 'plan': plan(cfg, S, [int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else range(len(S)))
    elif mode == 'dialogue': dialogue(cfg, S)
    elif mode == 'strip': strip(cfg, S, int(sys.argv[3]), float(sys.argv[4]) if len(sys.argv) > 4 else 0.5)
    elif mode == 'output': output(cfg, S, sys.argv[3] if len(sys.argv) > 3 else cfg['output'])
