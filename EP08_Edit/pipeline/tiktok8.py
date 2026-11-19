import json, subprocess, os
E=json.load(open('/tmp/e8/ed/edl8.json')); FPS=24; OUT='/tmp/e8/ed/tt'; os.makedirs(OUT,exist_ok=True)
C={'01_est':(0.22,0.72),'AV_E1':(0.62,0.62),'AV_E2':(0.36,0.36),'04_story':(0.37,0.62),'AV_E4':(0.64,0.64),'AV_E5':(0.64,0.64),
   'AV_E6':(0.67,0.67),'08_bell':(0.45,0.45),'09_leave':(0.45,0.45),'AV_E7':(0.48,0.48),'AV_E8':(0.55,0.55),'12_hook':(0.25,0.5),'99_end':'black'}
def run(c): subprocess.run(c,check=True)
# 01 without title
it=E[0]; nf=round(it['dur']*FPS); z0,z1=it['kb']
run(['ffmpeg','-loglevel','error','-y','-loop','1','-t',f"{it['dur']:.3f}",'-i',it['src'],'-vf',f"scale=3840:-2,zoompan=z='{z0}+({z1}-{z0})*on/{nf}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={nf}:s=1920x1080:fps={FPS},setsar=1,format=yuv420p",'-frames:v',str(nf),'-an','-c:v','libx264','-preset','veryfast','-crf','18',f'{OUT}/src01.mp4'])
lst=[]
for n,it in enumerate(E):
    o=f'{OUT}/{n:03d}.mp4'; lst.append(o); nf=round(it['dur']*FPS); c=C[it['k']]
    if c=='black':
        run(['ffmpeg','-loglevel','error','-y','-f','lavfi','-i',f'color=black:s=1080x1920:r={FPS}','-frames:v',str(nf),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',o]); continue
    src=f'{OUT}/src01.mp4' if n==0 else f'/tmp/e8/ed/seg/{n:03d}_{it["k"]}.mp4'
    x0=c[0]*1920-304; x1=c[1]*1920-304; x0=max(0,min(1312,x0)); x1=max(0,min(1312,x1))
    xe=f"{x0:.1f}+({x1-x0:.1f})*n/{max(nf-1,1)}"
    run(['ffmpeg','-loglevel','error','-y','-i',src,'-vf',f"crop=608:1080:'{xe}':0,scale=1080:1920:flags=lanczos,setsar=1,format=yuv420p",'-frames:v',str(nf),'-an','-c:v','libx264','-preset','veryfast','-crf','18','-r',str(FPS),o])
open(f'{OUT}/list.txt','w').write(''.join(f"file '{x}'\n" for x in lst))
run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',f'{OUT}/list.txt','-c','copy',f'{OUT}/pic.mp4'])
run(['ffmpeg','-loglevel','error','-y','-i',f'{OUT}/pic.mp4','-i','/tmp/e8/ed/mix8.wav','-vf','ass=/tmp/e8/ed/ep08_vert.ass','-map','0:v','-map','1:a','-c:v','libx264','-preset','medium','-crf','20','-c:a','aac','-b:a','192k','-shortest','/tmp/e8/ed/GC_EP08_v1_tiktok.mp4'])
print('ok')
