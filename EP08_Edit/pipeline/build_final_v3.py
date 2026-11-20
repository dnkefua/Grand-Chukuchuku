import subprocess, json, os
W = '/home/claude/e8/final'; os.makedirs(W, exist_ok=True)
OA = '/home/claude/e8/oa'; FL = '/home/claude/e8/flow'; SFX = '/home/claude/e8/sfx'
V = '/home/claude/vox/out2'
A = '/mnt/user-data/uploads/Grand-Chukuchuku/Audio files'
LAU = f'{A}/SFX_Laughter'
EP6 = '/mnt/user-data/uploads/Grand-Chukuchuku/EP06_Edit/GC_EP06_Lunch_Money_v2.mp4'
FPS = 24
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
L = {k: dur(f'{V}/{k}.wav') for k in ['E1','E2','E3','E4','E5','E6','E7','E8']}
PAD = 0.35
# id, source, in-point, seconds (None = line length + pad), line, sfx [(file, t, gain)]
SH = [
 ('A01', f'{FL}/EP08_A01.mp4', 0.0, 3.0, None, [(f'{SFX}/BREEZE_LEAVES.mp3',0.0,0.6)]),
 ('X11', f'{FL}/EP08_B11.mp4', 4.0, 1.5, None, [(f'{SFX}/TENSION_STING.mp3',0.0,0.55)]),
 ('R01', f'{OA}/R01.mp4', 0.0, 2.5, None, [(f'{SFX}/LIZARD_SCUTTLE.mp3',0.5,0.5)]),
 ('R02', f'{OA}/R02.mp4', 0.0, 2.0, None, [(f'{SFX}/BREEZE_LEAVES.mp3',0.0,0.5)]),
 ('A02', f'{FL}/EP08_A02.mp4', 0.0, 5.0, None, [(f'{SFX}/CRUTCH_CONCRETE.mp3',0.4,4.0)]),
 ('A03', f'{FL}/EP08_A03.mp4', 0.0, 5.0, None, [(f'{SFX}/BODY_THUD.mp3',0.4,0.45),(f'{LAU}/LAUGH_CLASS_SHORT.mp3',0.7,0.9)]),
 ('A04', f'{FL}/EP08_A04.mp4', 0.0, 6.0, None, [(f'{SFX}/HEARTBEAT.mp3',1.5,0.35)]),
 ('A05', f'{OA}/A05.mp4', 0.0, None, 'E1', []),
 ('A06', f'{OA}/A06.mp4', 0.0, None, 'E2', []),
 ('B01', f'{OA}/B01.mp4', 0.0, 4.0, None, [(f'{SFX}/CRUTCH_DIRT.mp3',0.0,3.5)]),
 ('B02', f'{OA}/B02.mp4', 0.0, 3.0, None, [(f'{SFX}/GIRLS_OOH.mp3',0.3,0.6)]),
 ('B03', f'{OA}/B03.mp4', 0.0, None, 'E3', []),
 ('B04', f'{OA}/B04.mp4', 0.0, 2.6, None, [(f'{LAU}/LAUGH_CLASS.mp3',0.0,0.8)]),
 ('B05', '/home/claude/e8/print/B05_test.mp4', 0.0, None, 'E4', []),
 ('B06', f'{OA}/B06.mp4', 0.0, 3.0, None, [(f'{SFX}/MISCHIEF_PLUCK.mp3',0.2,0.4)]),
 ('B07', f'{OA}/B07.mp4', 0.0, None, 'E5', []),
 ('B08', f'{OA}/B08.mp4', 0.0, None, 'E6', []),
 ('B09', EP6, 13.2, 3.0, None, [(f'{SFX}/HAND_BELL.mp3',0.0,0.7)]),
 ('B10', f'{OA}/B10.mp4', 0.0, 5.0, None, [(f'{SFX}/SHIMMER.mp3',0.6,0.6)]),
 ('B11', f'{FL}/EP08_B11.mp4', 0.0, 4.0, None, [(f'{SFX}/TENSION_STING.mp3',0.1,0.4)]),
 ('C01', f'{OA}/C01.mp4', 0.0, None, 'E7', []),
 ('C02', f'{OA}/C02.mp4', 0.0, None, 'E8', []),
 ('C03', f'{OA}/C03.mp4', 0.0, 3.0, None, []),
 ('D01', f'{OA}/D01.mp4', 0.0, 6.0, None, [(f'{SFX}/BREEZE_LEAVES.mp3',0.0,0.4)]),
 ('TAG', 'TAG', 0.0, 3.0, None, [(f'{SFX}/HEARTBEAT.mp3',0.0,0.7)]),
 ('BLK', 'BLK', 0.0, 1.0, None, []),
]
t = 0.0; EDL = []
for sid, src, inp, d, line, sfx in SH:
    if d is None: d = round(L[line] + PAD, 3)
    EDL.append(dict(id=sid, src=src, inp=inp, dur=d, start=round(t,3), line=line, sfx=sfx)); t += d
TOT = round(t, 3)
json.dump(EDL, open(f'{W}/edl.json','w'), indent=1)
print('total', TOT)
assert TOT <= 120.0
st = {e['id']: e['start'] for e in EDL}; en = {e['id']: e['start']+e['dur'] for e in EDL}

# ---------- picture ----------
segs = []
for n, e in enumerate(EDL):
    o = f'{W}/seg{n:02d}.mp4'; nf = round(e['dur']*FPS)
    base = f'fps={FPS},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,format=yuv420p,tpad=stop_mode=clone:stop_duration=2,trim=end_frame={nf}'
    if e['src'] == 'BLK':
        cmd = ['ffmpeg','-nostdin','-loglevel','error','-y','-f','lavfi','-i',f'color=black:s=1920x1080:r={FPS}','-frames:v',str(nf)]
    elif e['src'] == 'TAG':
        cmd = ['ffmpeg','-nostdin','-loglevel','error','-y','-f','lavfi','-i',f'color=0x0b0d14:s=1920x1080:r={FPS}','-frames:v',str(nf)]
    else:
        cmd = ['ffmpeg','-nostdin','-loglevel','error','-y','-ss',str(e['inp']),'-i',e['src'],'-an','-vf',base,'-frames:v',str(nf)]
    cmd += ['-c:v','libx264','-preset','veryfast','-crf','18','-r',str(FPS),'-pix_fmt','yuv420p',o]
    subprocess.run(cmd, check=True); segs.append(o)
open(f'{W}/list.txt','w').write(''.join(f"file '{s}'\n" for s in segs))
subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-y','-f','concat','-safe','0','-i',f'{W}/list.txt','-c','copy',f'{W}/pic.mp4'],check=True)

# ---------- audio ----------
ins=[]; flt=[]
def add(p, loop=False):
    if loop: ins.extend(['-stream_loop','-1'])
    ins.extend(['-i',p]); return sum(1 for x in ins if x=='-i')-1
mix=[]
for e in EDL:
    if e['line']:
        i=add(f"{V}/{e['line']}.wav"); ms=int(e['start']*1000)
        flt.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms},apad=whole_dur={TOT}[d{i}]'); mix.append(f'[d{i}]')
flt.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0,atrim=0:{TOT},asplit=2[dlg][key]")
# music (De$): Lucky for the open, Own Way for the bell->stare and the ending
mus=[('06 - Lucky.wav',10.0,0.0,en['A04'],1.0,2.5,0.20),
     ('10 - Own Way.wav',30.0,st['B09'],en['B11'],0.8,1.5,0.16),
     ('10 - Own Way.wav',48.0,st['D01'],st['BLK']+0.9,1.0,1.8,0.20)]
ml=[]
for n,(f,o,a,b,fi,fo,v) in enumerate(mus):
    i=add(f'{A}/{f}'); Ln=b-a; ms=int(a*1000)
    flt.append(f'[{i}:a]atrim={o}:{o+Ln:.3f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d={fi},afade=t=out:st={Ln-fo:.3f}:d={fo},volume={v},adelay={ms}|{ms},apad=whole_dur={TOT}[m{n}]'); ml.append(f'[m{n}]')
flt.append(f"{''.join(ml)}amix=inputs={len(ml)}:normalize=0,atrim=0:{TOT}[mus]")
flt.append('[mus][key]sidechaincompress=threshold=0.02:ratio=8:attack=30:release=400[md]')
# school ambience bed from R01 to end of C03, ducked under dialogue too
sl=[]
i=add(f'{SFX}/AMB_SCHOOL_BREAK.mp3', loop=True); a=st['R01']; b=en['C03']; ms=int(a*1000)
flt.append(f'[{i}:a]atrim=0:{b-a:.3f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=1.0,afade=t=out:st={b-a-1.5:.3f}:d=1.5,volume=0.35,adelay={ms}|{ms},apad=whole_dur={TOT}[amb]')
for e in EDL:
    for f,tt,g in e['sfx']:
        i=add(f); ms=int((e['start']+tt)*1000)
        flt.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g},adelay={ms}|{ms},apad=whole_dur={TOT}[x{i}]'); sl.append(f'[x{i}]')
flt.append(f"[amb]{''.join(sl)}amix=inputs={len(sl)+1}:normalize=0,atrim=0:{TOT}[fx0]")
flt.append('[key]asplit=1[key2]')
flt.append('[dlg]volume=1.2[dd];[dd][md][fx0]amix=inputs=3:normalize=0,alimiter=limit=0.95,loudnorm=I=-16:TP=-1.5:LRA=11,atrim=0:'+f'{TOT}'+'[out]')
# key used once by sidechain; drop unused split
flt.remove('[key]asplit=1[key2]')
open(f'{W}/mix.txt','w').write(';\n'.join(flt))
subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-y',*ins,'-filter_complex_script',f'{W}/mix.txt','-map','[out]','-ar','48000','-ac','2',f'{W}/mix.wav'],check=True)

# ---------- subtitles ----------
T={'en':{'E1':["Wow, big Zino! Tai Chi Jet Li Zino!","Grand Chuckuchucku Zino! Please, talk to that girl for me."],
 'E2':["Oh, really? The other day you were Fon Echikie and Jean Lambert on commentary.","All that mouth!"],
 'E3':["If it's match commentary, Gideon turns into Martin Tyler."],'E4':["I only say what I see, oh."],
 'E5':["Did you see how the third bottle fell?"],'E6':["I saw it. Zino almost broke that bottle."],
 'E7':["Next time, don't talk so much."],'E8':["Next time, use your own mouth first."]},
 'fr':{'E1':["Waouh, grand Zino ! Zino, le Jet Li du tai-chi !","Zino de Grand Chuckuchucku ! S'il te plaît, parle à cette fille pour moi."],
 'E2':["Ah bon ? L'autre jour, tu faisais Fon Echikie et Jean Lambert aux commentaires.","Que de paroles !"],
 'E3':["Pour commenter un match, Gideon devient Martin Tyler."],'E4':["Je dis seulement ce que je vois, hein."],
 'E5':["Tu as vu comment la troisième bouteille est tombée ?"],'E6':["Je l'ai vu. Zino a presque cassé cette bouteille."],
 'E7':["La prochaine fois, ne parle pas trop."],'E8':["La prochaine fois, sers-toi d'abord de ta propre bouche."]}}
SPLIT={'E1':0.42,'E2':0.78}
def ts(x,ass=False):
    h=int(x//3600); m=int(x%3600//60); s=x%60
    if ass: return f'{h}:{m:02d}:{s:05.2f}'
    ms=int(round((s-int(s))*1000)); return f'{h:02d}:{m:02d}:{int(s):02d},{ms:03d}'
cues=[(e['line'], e['start']+0.05, e['start']+L[e['line']]-0.05) for e in EDL if e['line']]
rows={}
for lang in T:
    r=[]
    for lid,s,e in cues:
        p=T[lang][lid]
        if len(p)==1: r.append((s,e,p[0]))
        else:
            m=s+(e-s)*SPLIT[lid]; r.append((s,m-0.04,p[0])); r.append((m,e,p[1]))
    rows[lang]=r
    open(f'{W}/ep08.{lang}.srt','w',encoding='utf-8').write('\n'.join(f'{i+1}\n{ts(a)} --> {ts(b)}\n{t}\n' for i,(a,b,t) in enumerate(r)))
ttl0=st['R01']; ttl1=en['R02']; tg=st['TAG']; tg1=en['TAG']
def ass(resx,resy,sub_fs,sub_mv,ttl_fs,ep_fs,ttl_mv,ep_mv,end_fs):
    s=f"""[Script Info]
ScriptType: v4.00+
PlayResX: {resx}
PlayResY: {resy}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,DejaVu Sans,{sub_fs},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,80,80,{sub_mv},1
Style: Title,DejaVu Sans,{ttl_fs},&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,4,3,8,60,60,{ttl_mv},1
Style: Ep,DejaVu Sans,{ep_fs},&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,3,2,8,60,60,{ep_mv},1
Style: End,DejaVu Sans,{end_fs},&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,{ts(ttl0+0.2,1)},{ts(ttl1,1)},Title,,0,0,0,,{{\\fad(400,500)}}GRAND CHUCKUCHUCKU
Dialogue: 0,{ts(ttl0+0.4,1)},{ts(ttl1,1)},Ep,,0,0,0,,{{\\fad(400,500)}}Episode 8 · The Message
Dialogue: 0,{ts(tg+0.2,1)},{ts(tg1,1)},End,,0,0,0,,{{\\fad(400,300)}}{{\\fs{int(end_fs*0.55)}}}TOMORROW\\N{{\\fs{end_fs}}}EPISODE 9\\N{{\\c&H00D6FF&}}THE DECIDING PASS
"""
    return s
open(f'{W}/ep08_h.ass','w',encoding='utf-8').write(ass(1920,1080,46,60,72,38,120,215,72))
v=ass(1080,1920,54,520,78,44,330,445,80)
for a,b,t in rows['en']: v+=f"Dialogue: 0,{ts(a,1)},{ts(b,1)},Sub,,0,0,0,,{t}\n"
open(f'{W}/ep08_v.ass','w',encoding='utf-8').write(v)
print('built pic+mix+subs', TOT)
