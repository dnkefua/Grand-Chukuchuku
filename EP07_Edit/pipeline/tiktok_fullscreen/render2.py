"""Ep 7 full-screen TikTok, v2: per-shot camera (pans, zooms, split-screen) + impact punches/shake.
Frame-exact with the YouTube master, so lip-sync and the mix are untouched."""
import json, subprocess, sys, math
import cv2, numpy as np
W = '/home/claude/e7tt'
Y = "/mnt/user-data/uploads/Final cut/Youtube submission/Grand Chuckuchucku - Episode 7 - First Bottle.mp4"
EDL = '/mnt/user-data/uploads/Grand-Chukuchuku/EP07_Edit/pipeline/edl5.json'
S = json.load(open(f'{W}/plan.json'))
OV = json.load(open(f'{W}/overrides.json'))
FPS = 24.0; OW, OH = 1080, 1920
for i, s in enumerate(S):
    if str(i) in OV: s['spec'] = OV[str(i)]
    else: s['spec'] = s['c']
# impact moments from the edit's own SFX cues
IMP = ('kick_hard', 'bottle_hit', 'kick_body', 'punch_impact', 'block_hit', 'body_fall', 'header', 'slowmo_impact', 'land_back')
imps, swells = [], []
for e in json.load(open(EDL)):
    for c in e.get('cues', []):
        t = e['start'] + c[1]
        if c[0] in IMP: imps.append((t, 1.0 if c[0] in ('punch_impact', 'kick_body', 'slowmo_impact', 'bottle_hit', 'body_fall') else 0.6))
        if c[0] == 'slowmo_swell': swells.append(t)
imps.sort(); swells.sort()
shot_of = np.zeros(int(S[-1]['fb']) + 2, int)
for i, s in enumerate(S): shot_of[s['fa']:s['fb']] = i
def ss(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def interp(kf, fr):
    """kf: list of [frac, v1, v2, ...] -> values at fr with smoothstep easing"""
    if fr <= kf[0][0]: return kf[0][1:]
    for a, b in zip(kf[:-1], kf[1:]):
        if fr <= b[0]:
            u = ss((fr - a[0]) / max(1e-6, b[0] - a[0]))
            return [x + (y - x) * u for x, y in zip(a[1:], b[1:])]
    return kf[-1][1:]
def fx(t, i):
    """punch-in zoom multiplier and shake offset (source px) at time t, within shot i"""
    a, b = S[i]['a'], S[i]['b']; z = 1.0; dx = dy = 0.0
    for T, k in imps:
        if T > t: break
        if T < a - 0.01 or t - T > 0.6: continue
        d = t - T
        z *= 1 + 0.09 * k * math.exp(-d / 0.16)
        amp = 9 * k * math.exp(-d / 0.10)
        dx += amp * math.sin(d * 95); dy += amp * 0.7 * math.cos(d * 80)
    for T in swells:
        if a - 0.05 <= T < b: z *= 1 + 0.10 * ss((t - T) / 2.2) if t >= T else 1
    return z, dx, dy
def win(img, cx, cy, z, ar_w, ar_h, base_h, dx=0, dy=0):
    H, Wd = img.shape[:2]
    h = base_h / z; w = h * ar_w / ar_h
    x0 = cx * Wd - w / 2 + dx; y0 = cy * H - h / 2 + dy
    x0 = min(max(0, x0), Wd - w); y0 = min(max(0, y0), H - h)
    M = np.float32([[ar_w / w, 0, -x0 * ar_w / w], [0, ar_h / h, -y0 * ar_h / h]])
    return cv2.warpAffine(img, M, (ar_w, ar_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
def render_frame(img, n):
    i = shot_of[n]; s = S[i]; t = n / FPS
    fr = (n - s['fa']) / max(1, s['fb'] - s['fa'] - 1)
    z, dx, dy = fx(t, i)
    sp = s['spec']
    if isinstance(sp, dict):
        sr = sp.get('split')
        if sr and sr['range'][0] <= fr < sr['range'][1]:
            PH = (OH - 6) // 2
            tx, ty = interp(sr['top'], fr); bx, by = interp(sr['bot'], fr)
            top = win(img, tx, ty, z, OW, PH, 600, dx, dy)
            bot = win(img, bx, by, z, OW, OH - 6 - PH, 600, -dx, dy)
            div = np.full((6, OW, 3), 235, np.uint8)
            return np.vstack([top, div, bot])
        cx = interp(sp['single'], fr)[0]
        if 'zoom_end' in sp: z *= interp(sp['zoom_end'], fr)[0]
        cy = 0.5
    elif isinstance(sp, list):
        v = interp(sp, fr); cx = v[0]; cy = v[1] if len(v) > 1 else 0.5
        if len(v) > 2: z *= v[2]
    else:
        cx, cy = sp, 0.5
    return win(img, cx, cy, z, OW, OH, 1080, dx, dy)
def main(limit=None, only=None):
    aer = cv2.imread(f'{W}/aer0.png')
    f0 = S[1]['fa']
    cap = cv2.VideoCapture(Y)
    out = f'{W}/ep07_tt_v2.mp4' if not only else f'{W}/preview.mp4'
    cmd = ['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{OW}x{OH}', '-r', '24', '-i', '-',
           '-i', Y, '-map', '0:v', '-map', '1:a', '-vf', f'unsharp=5:5:0.4,ass={W}/ep07_full.ass,format=yuv420p',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', out]
    if only:
        a, b = only; cap.set(cv2.CAP_PROP_POS_FRAMES, a)
        cmd = ['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{OW}x{OH}', '-r', '24', '-i', '-',
               '-ss', str(a / FPS), '-t', str((b - a) / FPS), '-i', Y, '-map', '0:v', '-map', '1:a', '-vf', 'format=yuv420p',
               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', '-c:a', 'aac', '-shortest', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = only[0] if only else 0; end = only[1] if only else len(shot_of) - 2
    while n < end:
        ok, img = cap.read()
        if not ok: break
        if n < f0:  # clean opening aerial (title-free frame from v1), slow push-in
            k = n / f0; z = 1.0 + 0.06 * k
            img = cv2.resize(aer, (1920, 1080)); frame = win(img, 0.45, 0.5, z, OW, OH, 1080)
        else:
            frame = render_frame(img, n)
        p.stdin.write(frame.tobytes()); n += 1
    p.stdin.close(); p.wait(); print('wrote', out, n)
if __name__ == '__main__':
    if len(sys.argv) > 2: main(only=(int(sys.argv[1]), int(sys.argv[2])))
    else: main()
