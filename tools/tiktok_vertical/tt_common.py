"""Shared helpers for the Grand Chuckuchucku TikTok vertical reframe tool.

A vertical cut is the finished 16:9 YouTube master, reframed shot by shot into
1080x1920. The picture is never retimed, so the mix and lip-sync stay exact.
"""
import json, os, re, math, subprocess

OW, OH = 1080, 1920          # output size (9:16)
SRC_W, SRC_H = 1920, 1080    # master size (16:9)
CROP_FRAC = (SRC_H * OW / OH) / SRC_W   # 9:16 window width as a fraction of frame width at zoom 1 (~0.316)

# SFX cue names that count as impacts (get a punch-in + shake) and slow-motion swells (get a push-in)
IMPACT_STRONG = {'punch_impact', 'kick_body', 'slowmo_impact', 'bottle_hit', 'body_fall'}
IMPACT_LIGHT = {'kick_hard', 'block_hit', 'header', 'land_back'}
SWELL = {'slowmo_swell'}


def load_config(path):
    cfg = json.load(open(path))
    base = os.path.dirname(os.path.abspath(path))
    def fix(p):
        return p if (p is None or os.path.isabs(p)) else os.path.normpath(os.path.join(base, p))
    for k in ('master', 'work', 'camera', 'cues', 'output'):
        if k in cfg: cfg[k] = fix(cfg[k])
    if cfg.get('subtitles'):
        for k in ('ass', 'srt'):
            if k in cfg['subtitles']: cfg['subtitles'][k] = fix(cfg['subtitles'][k])
    if cfg.get('clean_opening') and cfg['clean_opening'].get('image'):
        cfg['clean_opening']['image'] = fix(cfg['clean_opening']['image'])
    os.makedirs(cfg['work'], exist_ok=True)
    return cfg


def probe_fps(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=r_frame_rate',
                          '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip()
    a, b = out.split('/')
    return float(a) / float(b)


def load_shots(cfg):
    """shots.json from tt_analyze.py, with the camera specs from camera.json applied."""
    shots = json.load(open(os.path.join(cfg['work'], 'shots.json')))
    cam = json.load(open(cfg['camera'])) if cfg.get('camera') and os.path.exists(cfg['camera']) else {}
    for i, s in enumerate(shots):
        s['spec'] = cam.get(str(i), s['c'])
    return shots


def load_cues(cfg):
    """Returns (impacts [(t, strength)], swells [t]).
    cues file: either an edit list [{start, cues:[[name, offset], ...]}, ...] (our pipeline EDL format)
    or a flat list [[t, name], ...]."""
    if not cfg.get('cues') or not os.path.exists(cfg['cues']):
        return [], []
    raw = json.load(open(cfg['cues'])); flat = []
    if raw and isinstance(raw[0], dict):
        for e in raw:
            for c in e.get('cues', []):
                flat.append((e['start'] + c[1], c[0]))
    else:
        flat = [(float(t), n) for t, n in raw]
    imps = sorted((t, 1.0 if n in IMPACT_STRONG else 0.6) for t, n in flat if n in IMPACT_STRONG | IMPACT_LIGHT)
    swells = sorted(t for t, n in flat if n in SWELL)
    return imps, swells


def smooth(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)


def interp(kf, fr):
    """kf: [[frac, v1, v2, ...], ...] -> [v1, v2, ...] at frac fr (smoothstep easing between keys)."""
    if fr <= kf[0][0]: return list(kf[0][1:])
    for a, b in zip(kf[:-1], kf[1:]):
        if fr <= b[0]:
            u = smooth((fr - a[0]) / max(1e-6, b[0] - a[0]))
            return [x + (y - x) * u for x, y in zip(a[1:], b[1:])]
    return list(kf[-1][1:])


def centre_at(spec, fr):
    """Single-frame crop centre x for drawing review boxes (split shots report the 'single' path)."""
    if isinstance(spec, dict): return interp(spec['single'], fr)[0]
    if isinstance(spec, list): return interp(spec, fr)[0]
    return float(spec)


def split_active(spec, fr):
    return isinstance(spec, dict) and spec.get('split') and spec['split']['range'][0] <= fr < spec['split']['range'][1]


def ass_time(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f'{h}:{m:02d}:{s:05.2f}'


def srt_to_events(path):
    txt = open(path, encoding='utf-8-sig').read().replace('\r', '')
    ev = []
    for blk in re.split(r'\n\s*\n', txt.strip()):
        lines = blk.split('\n')
        for k, l in enumerate(lines):
            m = re.match(r'(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)', l)
            if m:
                g = [int(v) for v in m.groups()]
                a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000; b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
                ev.append((a, b, '\\N'.join(lines[k + 1:]).strip())); break
    return ev


def subtitle_events(cfg):
    """[(start, end, text)] for every spoken line (used by the dialogue review sheet)."""
    sub = cfg.get('subtitles') or {}
    if sub.get('srt'): return srt_to_events(sub['srt'])
    if sub.get('ass'):
        ev = []
        for l in open(sub['ass'], encoding='utf-8'):
            if l.startswith('Dialogue:'):
                p = l.rstrip('\n').split(',', 9)
                def t(x): h, m, s = x.split(':'); return int(h) * 3600 + int(m) * 60 + float(s)
                ev.append((t(p[1]), t(p[2]), re.sub(r'\{[^}]*\}', '', p[9])))
        return ev
    return []


ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,DejaVu Sans,54,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,80,80,520,1
Style: Title,DejaVu Sans,78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,4,3,8,60,60,330,1
Style: Ep,DejaVu Sans,44,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,3,2,8,60,60,445,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def build_vertical_ass(cfg, out_path):
    """House vertical style: subtitles low on screen (bottom margin 520 px, above TikTok's caption area),
    show title + episode line top-centre over the opening."""
    body = ''
    t = cfg.get('title')
    if t:
        body += f"Dialogue: 0,{ass_time(t['start'])},{ass_time(t['end'])},Title,,0,0,0,,{{\\fad(400,400)}}{t['line1']}\n"
        body += f"Dialogue: 0,{ass_time(t['start'] + 0.2)},{ass_time(t['end'])},Ep,,0,0,0,,{{\\fad(400,400)}}{t['line2']}\n"
    for a, b, txt in subtitle_events(cfg):
        body += f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Sub,,0,0,0,,{txt}\n"
    open(out_path, 'w', encoding='utf-8').write(ASS_HEADER + body)
    return out_path
