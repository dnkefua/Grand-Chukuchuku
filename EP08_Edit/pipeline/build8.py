import json, subprocess
FL='/mnt/user-data/uploads/Grand-Chukuchuku/EP08_Board/flow_src'; AV='/mnt/user-data/uploads/Grand-Chukuchuku/EP08_Board/av'
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
E=[]; t=0.0
def add(k,src,d,ss=0.0,lines=(),cues=(),still=False,kb=None,title=False):
    global t; E.append(dict(k=k,src=src,dur=round(d,3),ss=ss,start=round(t,3),lines=list(lines),cues=list(cues),still=still,kb=kb,title=title)); t+=d
def av(k,pre=0.25,post=0.45):
    f=f'{AV}/AV_{k}.mp4'; d=min(dur(f'/tmp/e8/v3/{k}.wav'),dur(f)); add('AV_'+k,f,d+post,lines=[(k,0.0)]); return d
# 1 establishing still (push-in) + title
add('01_est',f'{FL}/EP08_F1_establishing.png',5.0,still=True,kb=(1.0,1.12),title=True)
av('E1',post=0.5)                       # Gideon: Wah big Zino...
av('E2',post=0.5)                       # Zino: Na so...
add('04_story',f'{FL}/EP08_V_zino_story.mp4',7.6,lines=[('E3',0.8)],cues=[('LAUGH',4.7,0.22)])
av('E4',post=0.6)                       # Gideon: I di tok na wetty...
av('E5',post=0.5)                       # Gideon: You see how the third bottle fall?
av('E6',post=0.6)                       # Girl: I see am...
add('08_bell',f'{FL}/EP08_V_bell.mp4',5.2,ss=0.4,cues=[('bell_rim',0.15,0)])
add('09_leave',f'{FL}/EP08_V_girl_leaves.mp4',7.2,ss=0.3,cues=[('steps_arey',0.5,-10)])
av('E7',post=0.4)                       # Gideon: Next time, no talk plenty
av('E8',post=0.8)                       # Zino: Next time, use your own mouth first
add('12_hook',f'{FL}/EP08_V_luc_hook.mp4',7.9)
add('99_end','/tmp/e8/gfx/endcard.png',4.0,still=True)
json.dump(E,open('/tmp/e8/ed/edl8.json','w'),indent=0); print('total',round(t,2)); [print(e['k'],e['start'],e['dur']) for e in E]
