import json, subprocess, os, sys, math
T=json.load(open('/tmp/ed/timeline2.json')); D2,FULL=T['dur'],T['full']
FX='/mnt/user-data/uploads/Grand-Chukuchuku/EP07_Board/v1/fix'
AV='/mnt/user-data/uploads/Grand-Chukuchuku/EP07_Board/v1/av'
A='/mnt/user-data/uploads/Grand-Chukuchuku/Audio files'; S='/tmp/ed/sfxn'
ALEN={l.split()[0]:float(l.split()[1]) for l in open('/tmp/ed/av_lines.txt')}
exec(open('/tmp/ed/cues_old.py').read())   # CUES (shot, sfx, clip_time, gain)
OLD={}
for sh,k,t,g in CUES: OLD.setdefault(sh,[]).append((k,t,g))
def f_of(s): return D2[s]/FULL[s] if D2[s]>FULL[s]+0.05 else 1.0
E=[]  # items: dict(k, src, ss, dur, speed, lines[(lid,off)], cues[(sfx,t,g)], laughs[(file,t,vol)])
def seg(s, dur=None, lines=(), cues=None, laughs=()):
    d=D2[s] if dur is None else min(dur,D2[s])
    c=[(k,t*f_of(s),g) for k,t,g in OLD.get(s,[])] if cues is None else cues
    E.append(dict(k=s,src=f'/tmp/ed/seg3/{s}.mp4',ss=0,dur=d,speed=1,lines=list(lines),cues=[x for x in c if x[1]<d+0.5],laughs=list(laughs)))
def clip(k,src,dur,ss=0,speed=1,lines=(),cues=(),laughs=(),crop=0):
    E.append(dict(k=k,src=src,ss=ss,dur=dur,speed=speed,lines=list(lines),cues=list(cues),laughs=list(laughs),crop=crop))
CROP={'L03':0.8,'L12':0.8,'L28':0.74,'L30':0.82,'L31':0.8,'L36':0.9,'L39':0.88}
def cu(l,laughs=(),cues=()):
    clip('CU_'+l,f'{AV}/AV_{l}.mp4',ALEN[l],lines=[(l,0.15)],laughs=laughs,cues=cues,crop=CROP.get(l,0))
LG=f'{FX}/LAUGH_GIDEON.mp3'; LK=f'{FX}/LAUGH_KIDS_BIG.mp3'; LGG=f'{FX}/LAUGH_KIDS_GIGGLE.mp3'; LC=f'{FX}/LAUGH_CHEER.mp3'
LS=f'{A}/SFX_Laughter/LAUGH_STREET_KIDS.mp3'; OOH=f'{A}/SFX_Laughter/CROWD_OOH_GATE.mp3'
seg('01'); seg('02')
cu('L01',laughs=[(LG,ALEN['L01']-0.4,0.5)])
clip('M04',f'{FX}/MOD_04.mp4',2.6); cu('L02')
seg('05',2.4); cu('L03',laughs=[(LGG,ALEN['L03']-0.3,0.45)])
cu('L04')
seg('07')
seg('08',2.4); cu('L05')
cu('L06')
seg('10',2.4); cu('L07')
seg('11')
seg('12',2.4); cu('L08')
seg('13'); seg('14',lines=[('L09',0.05)])
seg('15',2.4); cu('L10',laughs=[(LGG,1.4,0.5)])
clip('M16',f'{FX}/M_16.mp4',3.0,cues=[('slowmo_swell',0,-6),('kick_hard',0.0,-6),('bottle_hit',0.08,0),('bottle_fall',0.3,-1),('gasp_boys',0.8,-8)],laughs=[(LC,1.3,0.45)])
cu('L11')
cu('L12',laughs=[(LG,ALEN['L12']-0.3,0.55)])
seg('18')
clip('DRIB',f'{FX}/DRIBBLE_A.mp4',10.0,lines=[('L13',1.0)],cues=[('run_steps',0,-8),('dribble_taps',0,-4),('dribble_taps',3.0,-4),('whoosh_fast',4.6,-6),('gasp_boys',5.2,-8),('dribble_taps',6.2,-4),('run_steps',6.5,-8),('cheer_boys',8.6,-6)])
cu('L14'); cu('L15',laughs=[(LS,ALEN['L15']-0.2,0.35)])
seg('25'); seg('26')
clip('M27',f'{FX}/MOD_27.mp4',2.6,laughs=[(LGG,0.9,0.4)]); cu('L16')
seg('28',lines=[('L17',0.08)]); seg('29')
clip('M30',f'{FX}/M_30.mp4',3.0,cues=[('slowmo_swell',0,-6),('ball_roll',0,-8),('bottle_hit',1.1,0),('bottle_fall',1.25,-4),('cheer_boys',2.0,-4)],laughs=[(LC,1.9,0.45)])
cu('L18a')
seg('31',2.4); cu('L18b'); cu('L19',laughs=[(LC,0.2,0.35)])
seg('32'); seg('33'); seg('34'); cu('L20'); seg('35')
clip('M36',f'{FX}/M_36.mp4',4.0,cues=[('slowmo_swell',0,-4),('kick_hard',0.2,-2),('block_hit',1.0,-8),('ball_roll',1.2,-8),('bottle_hit',2.3,0),('bottle_fall',2.45,-1)],laughs=[(LC,2.6,0.5)])
cu('L21')
seg('37'); seg('38',lines=[('L22',0.08)])
cu('L23'); cu('L24')
seg('41',2.2); cu('L25')
clip('M42',f'{FX}/MOD_42.mp4',3.0,cues=[('slowmo_swell',0,-6),('whoosh_fast',0.6,0),('block_hit',1.0,0),('whoosh_fast',1.6,-2),('punch_impact',2.0,0),('gasp_boys',2.2,-8)]); cu('L26')
seg('43',lines=[('L27',0.08)])
clip('M44',f'{FX}/MOD_44.mp4',3.2,cues=[('whoosh_fast',0.6,-2),('whoosh_fast',1.2,-2),('block_hit',1.4,-2)]); cu('L28')
clip('M45',f'{FX}/MOD_45.mp4',3.0,cues=[('slowmo_swell',0,-6),('whoosh_fast',0.5,0),('kick_body',1.0,2),('whoosh_fast',1.6,-2),('block_hit',1.8,0),('punch_impact',2.4,0)])
seg('46',2.4,cues=[('whoosh_fast',0.3,0),('block_hit',0.8,0),('kick_body',1.4,2),('punch_impact',2.0,0)]); cu('L29')
seg('47',2.4,cues=[('whoosh_fast',0.9,0),('whoosh_fast',1.6,0),('kick_body',1.95,3),('gasp_boys',2.1,-8)]); cu('L30')
seg('48',cues=[('whoosh_fast',0.5,0),('block_hit',0.9,0),('whoosh_fast',1.5,0),('punch_impact',1.9,0)]); seg('49',cues=[('whoosh_fast',0.2,0),('whoosh_fast',1.2,-2),('kick_body',1.6,2),('block_hit',2.2,-2)])
clip('M50',f'{FX}/MOD_50.mp4',3.0,cues=[('cheer_boys',0,-4),('whoosh_fast',0.6,-2),('block_hit',1.0,-2),('whoosh_fast',1.9,0),('punch_impact',2.1,1)]); cu('L31',laughs=[(LG,ALEN['L31']-0.3,0.5)])
clip('MATRIX',f'{FX}/MATRIX.mp4',10.0,cues=[('whoosh_fast',0.4,0),('slowmo_swell',1.6,0),('whoosh_fast',2.4,-4),('whoosh_fast',4.0,-6),('block_hit',6.9,0),('whoosh_fast',7.2,0),('slowmo_impact',8.05,0),('body_fall',8.15,4),('land_back',8.15,2),('slide_gravel',8.3,-4),('cheer_boys',8.7,-4)],laughs=[(LK,9.0,0.5)])
seg('52',cues=[('gasp_boys',0.4,-6)],laughs=[(OOH,0.1,0.45),(LGG,1.3,0.4)])
seg('53',lines=[('L32',0.08),('L33',0.75)]); seg('54'); seg('55',lines=[('L34',0.08)]); seg('56',lines=[('L35',0.08)])
cu('L36'); clip('M57',f'{FX}/M_57.mp4',5.0,cues=[('coins_tin',1.5,-2)])
cu('L37'); seg('58',cues=[('steps_arey',0.2,0)])
clip('S59',f'{FX}/S59.mp4',5.0,cues=[('coins_tin',0.8,-6),('coins_tin',2.6,-6)]); cu('L38')
seg('60',laughs=[(LC,0.3,0.4),(LS,1.2,0.3)]); cu('L39',laughs=[(LG,ALEN['L39']-0.2,0.55)])
seg('61')
clip('END','/tmp/ed/seg3/zz_end.mp4',2.5)
t=0
for it in E: it['start']=t; t+=it['dur']
TOT=t
if __name__=='__main__':
    miss=[it['src'] for it in E if not os.path.exists(it['src'])]
    print('items',len(E),'total',round(TOT,2),'missing',len(miss)); [print(' ',m) for m in miss]
    json.dump(E,open('/tmp/ed/edl5.json','w'),indent=0)
