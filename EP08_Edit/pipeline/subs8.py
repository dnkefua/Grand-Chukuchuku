import json, subprocess
E=json.load(open('/tmp/e8/ed/edl8.json'))
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
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
cues=[]
for it in E:
    for lid,off in it['lines']:
        s=it['start']+off+0.05; d=dur(f'/tmp/e8/v3/{lid}.wav')-0.1; cues.append((lid,s,s+d))
def ts(t,ass=False):
    h=int(t//3600); m=int(t%3600//60); s=t%60
    return f'{h}:{m:02d}:{s:05.2f}' if ass else f'{h:02d}:{m:02d}:{int(s):02d},{int(round((s-int(s))*1000)):03d}'
out={}
for lang in T:
    rows=[]
    for lid,s,e in cues:
        parts=T[lang][lid]
        if len(parts)==1: rows.append((s,e,parts[0]))
        else:
            m=s+(e-s)*SPLIT[lid]; rows.append((s,m-0.04,parts[0])); rows.append((m,e,parts[1]))
    out[lang]=rows
    srt='\n'.join(f'{i+1}\n{ts(a)} --> {ts(b)}\n{t}\n' for i,(a,b,t) in enumerate(rows))
    open(f'/tmp/e8/ed/ep08.{lang}.srt','w',encoding='utf-8').write(srt)
TOT=E[-1]['start']+E[-1]['dur']; endst=E[-1]['start']
ass=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,DejaVu Sans,54,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,80,150,520,1
Style: Title,DejaVu Sans,78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,4,3,8,60,60,330,1
Style: Ep,DejaVu Sans,44,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,3,2,8,60,60,445,1
Style: End,DejaVu Sans,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,{ts(0.4,1)},{ts(4.2,1)},Title,,0,0,0,,{{\\fad(400,500)}}GRAND\\NCHUCKUCHUCKU
Dialogue: 0,{ts(0.6,1)},{ts(4.2,1)},Ep,,0,0,0,,{{\\fad(400,500)}}Episode 8 · The Message
Dialogue: 0,{ts(endst+0.2,1)},{ts(TOT,1)},End,,0,0,0,,{{\\fad(500,0)}}EPISODE 09\\N{{\\c&H00D6FF&}}LUC'S ONE MINUTE
"""
for a,b,t in out['en']: ass+=f"Dialogue: 0,{ts(a,1)},{ts(b,1)},Sub,,0,0,0,,{t}\n"
open('/tmp/e8/ed/ep08_vert.ass','w',encoding='utf-8').write(ass); print(len(out['en']),'cues; total',TOT)
