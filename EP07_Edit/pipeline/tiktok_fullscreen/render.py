import json, subprocess, re
Y = "/mnt/user-data/uploads/Final cut/Youtube submission/Grand Chuckuchucku - Episode 7 - First Bottle.mp4"
W = '/home/claude/e7tt'
S = json.load(open(f'{W}/plan.json'))
FPS = 24
# 1) clean opening: slow push-in on the title-free first frame of the v1 cut, same length as shot 0
f0 = S[1]['fa']
subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-y','-loop','1','-i',f'{W}/aer0.png','-vf',
  f"scale=3840:-2,zoompan=z='1.0+0.06*on/{f0}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={f0}:s=1920x1080:fps={FPS},setsar=1,format=yuv420p",
  '-frames:v',str(f0),'-c:v','libx264','-preset','veryfast','-crf','16',f'{W}/open.mp4'],check=True)
# 2) crop x per shot, switching on frame number
CW = 608
def xof(c): return max(0, min(1920 - CW, c * 1920 - CW / 2))
parts = []
for s in S:
    fa, fb = s['fa'], s['fb']
    c = s['c']
    if not isinstance(c, list):
        e = str(int(round(xof(c))))
    else:
        L = fb - fa; e = str(int(round(xof(c[-1][1]))))
        for (f0, c0), (f1, c1) in reversed(list(zip(c[:-1], c[1:]))):
            n1 = fa + f1 * L; x0 = xof(c0); x1 = xof(c1); n0 = fa + f0 * L
            e = f"if(lt(n,{n1:.1f}),{x0:.1f}+({x1 - x0:.1f})*(n-{n0:.1f})/{max(1, n1 - n0):.1f},{e})"
    parts.append((fa, fb, e))
expr = parts[-1][2]
for fa, fb, e in reversed(parts[:-1]):
    expr = f"if(lt(n,{fb}),{e},{expr})"
open(f'{W}/cropx.txt','w').write(expr)
# 3) subtitles: reuse the Ep 7 TikTok lines, restyled for full screen
src = open('/mnt/user-data/uploads/Grand-Chukuchuku/EP07_Edit/pipeline/ep07_tt.ass', encoding='utf-8').read()
dl = [l for l in src.splitlines() if l.startswith('Dialogue:')]
hdr = """[Script Info]
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
Dialogue: 0,0:00:00.30,0:00:02.90,Title,,0,0,0,,{\\fad(400,400)}GRAND CHUCKUCHUCKU
Dialogue: 0,0:00:00.50,0:00:02.90,Ep,,0,0,0,,{\\fad(400,400)}Episode 7 · First Bottle
"""
open(f'{W}/ep07_full.ass','w',encoding='utf-8').write(hdr + '\n'.join(dl) + '\n')
# 4) render: clean opening + rest of the YouTube master, reframed per shot
fc = (f"[1:v][0:v]overlay=0:0:eof_action=pass,"
      f"crop={CW}:1080:'{expr}':0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.5,setsar=1,ass={W}/ep07_full.ass,format=yuv420p[v]")
open(f'{W}/fc.txt','w').write(fc)
out = f'{W}/Grand Chuckuchucku - Episode 7 - First Bottle - TikTok.mp4'
subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-y','-i',f'{W}/open.mp4','-i',Y,'-filter_complex_script',f'{W}/fc.txt',
  '-map','[v]','-map','1:a','-c:v','libx264','-preset','medium','-crf','19','-r',str(FPS),'-c:a','copy','-movflags','+faststart',out],check=True)
print('done')
