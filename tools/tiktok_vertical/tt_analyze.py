"""Step 1: find every cut in the master and propose a crop centre for each shot.

usage: python3 tt_analyze.py <episode_config.json> [--scene 0.3]
writes <work>/shots.json : [{a, b, fa, fb, c}]  (times in s, frames, auto crop centre 0..1)

The auto centre is the 9:16 window that holds the most frame-to-frame motion in the shot
(talking mouths, kicks, running), with a slight pull to the middle. It is only a first guess:
every shot is checked on the review sheets and corrected in camera.json.
"""
import sys, json, os, subprocess, argparse
import cv2, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tt_common import load_config, CROP_FRAC


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('config'); ap.add_argument('--scene', type=float, default=0.3)
    a = ap.parse_args(); cfg = load_config(a.config)
    # 1) cuts
    r = subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-i', cfg['master'], '-vf',
                        f"select='gt(scene,{a.scene})',showinfo", '-f', 'null', '-'], capture_output=True, text=True)
    cuts = [float(x.split(':')[1]) for x in r.stderr.split() if x.startswith('pts_time:')]
    cap = cv2.VideoCapture(cfg['master']); fps = cap.get(cv2.CAP_PROP_FPS)
    # 2) small grey frames
    G = []
    while True:
        ok, f = cap.read()
        if not ok: break
        G.append(cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (192, 108), interpolation=cv2.INTER_AREA).astype(np.float32))
    G = np.array(G); N = len(G)
    bounds = [0] + [int(round(c * fps)) for c in cuts] + [N]
    W = CROP_FRAC * 192
    shots = []
    for fa, fb in zip(bounds[:-1], bounds[1:]):
        if fb - fa < 3:   # flash frames: merge into the previous shot
            if shots: shots[-1]['fb'] = fb; shots[-1]['b'] = round(fb / fps, 3)
            continue
        tot = np.zeros(192)
        for k in range(fa + 1, fb):
            d = np.abs(G[k] - G[k - 1]); d[d < 6] = 0; tot += d.sum(0)
        tot /= tot.sum() + 1e-9
        best, bx = -1, 96
        for c in np.arange(W / 2, 192 - W / 2 + 0.01, 1):
            sc = tot[int(c - W / 2):int(c + W / 2)].sum() - 0.0015 * abs(c - 96)
            if sc > best: best, bx = sc, c
        shots.append(dict(a=round(fa / fps, 3), b=round(fb / fps, 3), fa=fa, fb=fb, c=round(float(bx) / 192, 3)))
    json.dump(shots, open(os.path.join(cfg['work'], 'shots.json'), 'w'), indent=0)
    print(f'{len(shots)} shots, {N} frames @ {fps:.3f} fps -> {cfg["work"]}/shots.json')


if __name__ == '__main__':
    main()
