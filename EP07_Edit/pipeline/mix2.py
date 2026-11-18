import json, subprocess
T=json.load(open('/tmp/ed/timeline2.json'))
start,dur,place,full=T['start'],T['dur'],T['place'],T['full']
TOT=T['total']+T['endcard']
A='/mnt/user-data/uploads/Grand-Chukuchuku/Audio files'; S='/tmp/ed/sfxn'
SFXG=-6.0   # global one-shot trim (dB)
# (shot, sfx, clip_time, gain_dB)  clip_time is in the source clip; slowed shots are scaled
CUES=[('02','coins_tin',0.8,-10),('05','knuckles',0.3,-4),
('07','kick_hard',1.8,0),('07','whoosh_fast',1.85,-10),
('08','run_steps',0,-8),('08','dribble_taps',0.3,-6),('09','run_steps',0,-14),
('10','dribble_taps',0,-6),('10','kick_hard',0.9,-3),('10','ball_roll',1.0,-10),
('11','run_steps',0,-6),('11','kick_hard',1.0,-4),('12','run_steps',0,-4),('12','dribble_taps',0.2,-4),
('13','slowmo_swell',0,-4),('13','slide_gravel',1.5,-1),('13','body_fall',2.3,-3),
('15','run_steps',0.5,-16),
('16','slowmo_swell',0,-6),('16','kick_hard',0.0,-6),('16','bottle_hit',0.08,0),('16','bottle_fall',0.3,-1),('16','gasp_boys',0.8,-8),
('18','stick_scratch',0.3,-2),('19','dribble_taps',0,-4),
('20','slowmo_swell',0,-6),('20','dribble_taps',0,-4),('20','whoosh_fast',1.4,-10),('20','ball_bounce',1.5,-8),
('21','whoosh_fast',0.6,-8),('21','run_steps',0,-10),
('22','slowmo_swell',0.8,-6),('22','dribble_taps',0,-8),('22','kick_hard',1.9,-8),('22','whoosh_fast',2.0,-8),
('23','gasp_boys',0.5,-6),('24','run_steps',0,-6),('24','dribble_taps',0,-6),
('25','slowmo_swell',0,-4),('25','slide_gravel',1.2,0),('25','kick_body',1.9,-2),('25','gasp_boys',2.4,-6),
('26','body_fall',0,-6),('29','kick_hard',1.1,-3),('29','ball_roll',1.3,-8),
('30','slowmo_swell',0,-6),('30','ball_roll',0,-8),('30','bottle_hit',1.1,0),('30','bottle_fall',1.25,-4),('30','cheer_boys',2.0,-4),
('31','cheer_boys',0,-6),
('32','slowmo_swell',0,-8),('32','header',0.5,-2),('32','body_fall',2.4,-8),
('33','slide_gravel',0.1,-2),('33','body_fall',1.9,-3),('33','gasp_boys',2.1,-8),
('34','run_steps',0,-2),('34','dribble_taps',0.5,-10),('35','stick_scratch',0.3,-2),
('36','slowmo_swell',0,-4),('36','kick_hard',0.2,-2),('36','block_hit',1.0,-8),('36','ball_roll',1.2,-8),('36','bottle_hit',2.3,0),('36','bottle_fall',2.45,-1),
('37','cheer_boys',0.2,-6),
('42','slowmo_swell',0,-6),('42','whoosh_fast',0.9,-2),('42','gasp_boys',1.5,-10),
('45','slowmo_swell',0,-6),('45','whoosh_fast',0.9,-2),('45','whoosh_fast',1.6,-6),('45','block_hit',1.8,-2),
('46','whoosh_fast',0.4,-6),('46','block_hit',0.9,-6),('46','kick_body',1.6,-6),('46','block_hit',2.3,-6),
('47','whoosh_fast',0.9,-2),('47','block_hit',1.8,-2),
('48','whoosh_fast',0.7,-4),('48','block_hit',1.5,-4),('48','whoosh_fast',2.1,-8),
('49','whoosh_fast',0.2,-2),('49','block_hit',1.5,-2),
('50','cheer_boys',0,-4),
('51','slowmo_swell',0,-2),('51','whoosh_fast',0.5,-6),('51','slowmo_impact',3.3,0),
('52','land_back',0.05,0),('52','gasp_boys',0.4,-4),
('53','slowmo_impact',0,-6),
('57','coins_tin',1.5,-2),('59','coins_tin',2.0,-6),('60','cheer_boys',1.2,-4)]
inputs=[]; filt=[]
def add(path,loop=False):
    if loop: inputs.extend(['-stream_loop','-1'])
    inputs.extend(['-i',path]); return sum(1 for x in inputs if x=='-i')-1
# dialogue
dl=[]
for lid,spk,shot,st,en in place:
    i=add(f'/tmp/ed/vo/{lid}_t.wav'); ms=int(st*1000)
    filt.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=mono,adelay={ms}|{ms},apad=whole_dur={TOT:.3f}[d{i}]'); dl.append(f'[d{i}]')
filt.append(f"{''.join(dl)}amix=inputs={len(dl)}:normalize=0,atrim=0:{TOT:.3f},asplit=2[dlg][key]")
s=lambda k: start[k]; e=lambda k: start[k]+dur[k]
# music: short title sting, match montage, the fight, outro only - low level
secs=[('06 - Lucky.wav',10.0,0.0,e('02'),0.6,1.5,0.13),
      ('06 - Lucky.wav',60.0,s('32'),e('35'),0.8,1.0,0.11),
      ('10 - Own Way.wav',48.0,s('42'),e('52'),0.5,0.4,0.11),
      ('06 - Lucky.wav',156.0,s('60'),TOT,1.5,2.0,0.15)]
ml=[]
for n,(f,off,t0,t1,fi,fo,v) in enumerate(secs):
    i=add(f'{A}/{f}'); L=t1-t0; ms=int(t0*1000)
    filt.append(f'[{i}:a]atrim={off}:{off+L:.3f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d={fi},afade=t=out:st={L-fo:.3f}:d={fo},volume={v},adelay={ms}|{ms},apad=whole_dur={TOT:.3f}[m{n}]'); ml.append(f'[m{n}]')
filt.append(f"{''.join(ml)}amix=inputs={len(ml)}:normalize=0,atrim=0:{TOT:.3f}[mus]")
filt.append('[key]aformat=channel_layouts=stereo,asplit=2[k2][k3]')
filt.append('[mus][k2]sidechaincompress=threshold=0.02:ratio=8:attack=30:release=400:makeup=1[mduck]')
# ambience beds
i=add(f'{S}/amb_street.wav',loop=True)
filt.append(f'[{i}:a]atrim=0:{TOT:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=1.5,afade=t=out:st={TOT-2:.3f}:d=2,volume=1.0[amb1]')
t0,t1=s('07'),e('53'); i=add(f'{S}/amb_match.wav',loop=True)
filt.append(f'[{i}:a]atrim=0:{t1-t0:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=1.0,afade=t=out:st={t1-t0-1.5:.3f}:d=1.5,volume=1.3,adelay={int(t0*1000)}|{int(t0*1000)},apad=whole_dur={TOT:.3f}[amb2]')
filt.append('[amb1][amb2]amix=inputs=2:normalize=0[ambm]')
filt.append('[ambm][k3]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=500:makeup=1[amb]')
# one-shots
sl=[]
for n,(shot,k,ct,g) in enumerate(CUES):
    f=dur[shot]/full[shot] if dur[shot]>full[shot]+0.05 else 1.0
    t=start[shot]+ct*f
    i=add(f'{S}/{k}.wav'); ms=int(t*1000)
    filt.append(f'[{i}:a]volume={g+SFXG}dB,adelay={ms}|{ms},apad=whole_dur={TOT:.3f}[x{n}]'); sl.append(f'[x{n}]')
for n,(f,shot,off,v) in enumerate([('SFX_Laughter/LAUGH_STREET_KIDS.mp3','17',0.2,0.35),('SFX_Laughter/CROWD_OOH_GATE.mp3','52',0.1,0.45),('SFX_Laughter/LAUGH_STREET_KIDS.mp3','60',0.2,0.3)]):
    i=add(f'{A}/{f}'); ms=int((start[shot]+off)*1000)
    filt.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={v},adelay={ms}|{ms},apad=whole_dur={TOT:.3f}[y{n}]'); sl.append(f'[y{n}]')
filt.append(f"{''.join(sl)}amix=inputs={len(sl)}:normalize=0,atrim=0:{TOT:.3f}[fx]")
filt.append('[dlg]aformat=channel_layouts=stereo,volume=1.15[dst]')
import os
STEM=os.environ.get('STEM')
if STEM:
    others=[x for x in ['dst','mduck','amb','fx'] if x!=STEM]
    filt.append(f'[{STEM}]anull[out]'); [filt.append(f'[{o}]anullsink') for o in others]
else:
    filt.append('[dst][mduck][amb][fx]amix=inputs=4:normalize=0,alimiter=limit=0.95,loudnorm=I=-15:TP=-1.5:LRA=13,aresample=48000[out]')
open('/tmp/ed/mix2_filter.txt','w').write(';\n'.join(filt))
subprocess.run(['ffmpeg','-loglevel','error','-y']+inputs+['-filter_complex_script','/tmp/ed/mix2_filter.txt','-map','[out]','-c:a','pcm_s16le',(f'/tmp/ed/stem_{STEM}.wav' if STEM else '/tmp/ed/mix2.wav')],check=True)
print('mix2 done',round(TOT,2),'cues',len(CUES))
