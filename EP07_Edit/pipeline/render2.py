import sys, json, os, subprocess
sys.path.insert(0,'/tmp/ed')
import plan
CL='/mnt/user-data/uploads/Grand-Chukuchuku/EP07_Board/v1/clips'
M=json.load(open('/tmp/ed/motion.json'))
def clip(s):
    if s=='36' and not os.path.exists(f'{CL}/EP07_36.mp4'): return '/tmp/ed/EP07_36_standin.mp4'
    return f'{CL}/EP07_{s}.mp4'
def length(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
FPS=24; ENDCARD=2.5
# v4 rule: every shot plays its whole clip (moves finish); talking shots grow to fit their lines
full={s:round(length(clip(s))-0.08,3) for s in plan.shots}
dur,start,place,total=plan.plan(full)
json.dump({'dur':dur,'start':start,'place':place,'total':total,'endcard':ENDCARD,'full':full},open('/tmp/ed/timeline2.json','w'),indent=0)
print('picture total',round(total,2),'+ end card',ENDCARD,'=',round(total+ENDCARD,2))
if '--plan' in sys.argv: sys.exit()
lst=[]
for s in plan.shots:
    f=clip(s); c=length(f)-0.05; d=dur[s]; nf=round(d*FPS)
    speed = 1.0 if c>=d else max(c/d,1/1.4)
    vf=f"setpts=(PTS-STARTPTS)/{speed:.4f},fps={FPS},scale=1920:1080:flags=lanczos,setsar=1,tpad=stop_mode=clone:stop_duration=6,trim=end_frame={nf},format=yuv420p"
    out=f'/tmp/ed/seg2/{s}.mp4'
    if s=='01':
        fc=f"[0:v]{vf}[b];[1:v]format=rgba,fade=t=in:st=0.2:d=0.5:alpha=1,fade=t=out:st={d-0.7:.2f}:d=0.6:alpha=1[t];[b][t]overlay=0:0:shortest=1,format=yuv420p[o]"
        subprocess.run(['ffmpeg','-loglevel','error','-y','-i',f,'-loop','1','-t',f'{d:.3f}','-i','/tmp/ed/gfx/title.png','-filter_complex',fc,'-map','[o]','-an','-c:v','libx264','-preset','veryfast','-crf','16','-r',str(FPS),out],check=True)
    else:
        subprocess.run(['ffmpeg','-loglevel','error','-y','-i',f,'-vf',vf,'-an','-c:v','libx264','-preset','veryfast','-crf','16','-r',str(FPS),out],check=True)
    lst.append(out)
subprocess.run(['ffmpeg','-loglevel','error','-y','-loop','1','-i','/tmp/ed/gfx/endcard.png','-t',str(ENDCARD),'-vf','fade=t=in:st=0:d=0.4,format=yuv420p','-r',str(FPS),'-c:v','libx264','-preset','veryfast','-crf','16','/tmp/ed/seg2/zz_end.mp4'],check=True)
lst.append('/tmp/ed/seg2/zz_end.mp4')
open('/tmp/ed/seg2/list.txt','w').write(''.join(f"file '{p}'\n" for p in lst))
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i','/tmp/ed/seg2/list.txt','-c','copy','/tmp/ed/picture2.mp4'],check=True)
print('picture2', length('/tmp/ed/picture2.mp4'))
