"""Step 3: render the full-screen 9:16 TikTok version.

usage:
  python3 tt_render.py <config>                    # full episode -> cfg['output']
  python3 tt_render.py <config> --range 4740 5160  # quick preview of frames [a, b) -> <work>/preview.mp4

Every output frame n is built from master frame n, so picture, mix and lip-sync stay frame-exact
(the master's audio is copied untouched). Camera per shot comes from camera.json (see METHOD doc):
  number                -> fixed crop centre x (0..1 of frame width)
  [[frac, cx(, cy, zoom)], ...]  -> moving crop, smoothstep between keys (frac = 0..1 through the shot)
  {"single": [...], "split": {"range": [f0, f1], "top": [[frac, cx, cy], ...], "bot": [...]},
   "zoom_end": [[frac, z], ...]}   -> split screen inside [f0, f1): two stacked panels (e.g. attacker / victim)
Automatic energy, from the edit's SFX cues: punch-in (+9%) and a short shake on every impact,
slow push-in (+10% over 2.2 s) on every slow-motion swell.
"""
import sys, os, json, math, subprocess, argparse
import cv2, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tt_common import load_config, load_shots, load_cues, interp, smooth, build_vertical_ass, OW, OH

PUNCH, PUNCH_DECAY = 0.09, 0.16      # impact zoom amount and decay (s)
SHAKE, SHAKE_DECAY = 9.0, 0.10       # impact shake (source px) and decay (s)
SWELL_ZOOM, SWELL_TIME = 0.10, 2.2   # slow-motion push-in
DIV = 6                              # split-screen divider height (px)


def window(img, cx, cy, z, ow, oh, base_h, dx=0.0, dy=0.0):
    H, W = img.shape[:2]; h = base_h / z; w = h * ow / oh
    x0 = min(max(0.0, cx * W - w / 2 + dx), W - w); y0 = min(max(0.0, cy * H - h / 2 + dy), H - h)
    M = np.float32([[ow / w, 0, -x0 * ow / w], [0, oh / h, -y0 * oh / h]])
    return cv2.warpAffine(img, M, (ow, oh), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)


class Camera:
    def __init__(self, cfg, S, fps):
        self.S, self.fps = S, fps
        self.imps, self.swells = load_cues(cfg)
        self.shot_of = np.zeros(S[-1]['fb'] + 2, int)
        for i, s in enumerate(S): self.shot_of[s['fa']:s['fb']] = i

    def energy(self, t, i):
        a, b = self.S[i]['a'], self.S[i]['b']; z, dx, dy = 1.0, 0.0, 0.0
        for T, k in self.imps:
            if T > t: break
            if T < a - 0.01 or t - T > 0.6: continue      # never carry an impact across a cut
            d = t - T; z *= 1 + PUNCH * k * math.exp(-d / PUNCH_DECAY)
            amp = SHAKE * k * math.exp(-d / SHAKE_DECAY); dx += amp * math.sin(d * 95); dy += amp * 0.7 * math.cos(d * 80)
        for T in self.swells:
            if a - 0.05 <= T < b and t >= T: z *= 1 + SWELL_ZOOM * smooth((t - T) / SWELL_TIME)
        return z, dx, dy

    def frame(self, img, n):
        i = self.shot_of[n]; s = self.S[i]; t = n / self.fps
        fr = (n - s['fa']) / max(1, s['fb'] - s['fa'] - 1)
        z, dx, dy = self.energy(t, i); sp = s['spec']
        if isinstance(sp, dict):
            sr = sp.get('split')
            if sr and sr['range'][0] <= fr < sr['range'][1]:
                ph = (OH - DIV) // 2
                tx, ty = interp(sr['top'], fr)[:2]; bx, by = interp(sr['bot'], fr)[:2]
                top = window(img, tx, ty, z, OW, ph, 600, dx, dy)
                bot = window(img, bx, by, z, OW, OH - DIV - ph, 600, -dx, dy)
                return np.vstack([top, np.full((DIV, OW, 3), 235, np.uint8), bot])
            cx, cy = interp(sp['single'], fr)[0], 0.5
            if 'zoom_end' in sp: z *= interp(sp['zoom_end'], fr)[0]
        elif isinstance(sp, list):
            v = interp(sp, fr); cx = v[0]; cy = v[1] if len(v) > 1 else 0.5
            if len(v) > 2: z *= v[2]
        else:
            cx, cy = float(sp), 0.5
        return window(img, cx, cy, z, OW, OH, 1080, dx, dy)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('config'); ap.add_argument('--range', nargs=2, type=int)
    a = ap.parse_args(); cfg = load_config(a.config); S = load_shots(cfg)
    cap = cv2.VideoCapture(cfg['master']); fps = cap.get(cv2.CAP_PROP_FPS); cam = Camera(cfg, S, fps)
    ass = build_vertical_ass(cfg, os.path.join(cfg['work'], 'vertical.ass'))
    op = cfg.get('clean_opening'); aer = cv2.resize(cv2.imread(op['image']), (1920, 1080)) if op else None
    op_end = S[op.get('until_shot', 1)]['fa'] if op else 0
    raw = ['-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{OW}x{OH}', '-r', f'{fps:.6f}', '-i', '-']
    if a.range:
        n0, n1 = a.range; out = os.path.join(cfg['work'], 'preview.mp4'); cap.set(cv2.CAP_PROP_POS_FRAMES, n0)
        cmd = ['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', *raw, '-ss', f'{n0 / fps:.4f}', '-t', f'{(n1 - n0) / fps:.4f}', '-i', cfg['master'],
               '-map', '0:v', '-map', '1:a', '-vf', 'format=yuv420p', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', '-c:a', 'aac', '-shortest', out]
    else:
        n0, n1 = 0, S[-1]['fb']; out = cfg['output']
        cmd = ['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', *raw, '-i', cfg['master'], '-map', '0:v', '-map', '1:a',
               '-vf', f'unsharp=5:5:0.4,ass={ass},format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19',
               '-c:a', 'copy', '-shortest', '-movflags', '+faststart', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); n = n0
    while n < n1:
        ok, img = cap.read()
        if not ok: break
        if n < op_end:   # title-free opening still with a slow push-in (masters carry a burned-in title)
            frame = window(aer, op.get('cx', 0.5), 0.5, 1 + op.get('push', 0.06) * n / op_end, OW, OH, 1080)
        else:
            frame = cam.frame(img, n)
        p.stdin.write(frame.tobytes()); n += 1
    p.stdin.close(); p.wait(); print('wrote', out, n - n0, 'frames')


if __name__ == '__main__':
    main()
