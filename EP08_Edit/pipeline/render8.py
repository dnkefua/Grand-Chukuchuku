import json, subprocess, os, sys
E=json.load(open('/tmp/e8/ed/edl8.json')); FPS=24
OUT='/tmp/e8/ed/seg'; os.makedirs(OUT,exist_ok=True)
A='/mnt/user-data/uploads/Grand-Chukuchuku/Audio files'; S='/tmp/ed/sfxn'
SFX={'bell_rim':'/tmp/e8/sfx/bell_rim.wav','LAUGH':f'{A}/SFX_Laughter/LAUGH_STREET_KIDS.mp3'}
def run(c): subprocess.run(c,check=True)
TOT=E[-1]['start']+E[-1]['dur']
if sys.argv[1] in ('pic','all'):
    lst=[]
    for n,it in enumerate(E):
        o=f'{OUT}/{n:03d}_{it["k"]}.mp4'; lst.append(o); nf=round(it['dur']*FPS)
        if it['still']:
            z0,z1=it['kb'] if it['kb'] else (1.0,1.0)
            zexpr=f"{z0}+({z1}-{z0})*on/{nf}"
            vf=f"scale=3840:-2,zoompan=z='{zexpr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={nf}:s=1920x1080:fps={FPS},setsar=1,format=yuv420p"
            if it['k']=='99_end': vf=f"scale=1920:1080,fade=t=in:st=0:d=0.5,setsar=1,format=yuv420p"
            cmd=['ffmpeg','-loglevel','error','-y','-loop','1','-t',f"{it['dur']:.3f}",'-i',it['src']]
            if it['title']:
                fc=f"[0:v]{vf}[b];[1:v]format=rgba,fade=t=in:st=0.4:d=0.5:alpha=1,fade=t=out:st=3.6:d=0.6:alpha=1[t];[b][t]overlay=0:0,format=yuv420p[o]"
                cmd+=['-loop','1','-t',f"{it['dur']:.3f}",'-i','/tmp/e8/gfx/title.png','-filter_complex',fc,'-map','[o]']
            else: cmd+=['-vf',vf]
            run(cmd+['-frames:v',str(nf),'-an','-c:v','libx264','-preset','veryfast','-crf','18','-r',str(FPS),o])
        else:
            vf=f"fps={FPS},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,format=yuv420p,tpad=stop_mode=clone:stop_duration=3,trim=end_frame={nf}"
            run(['ffmpeg','-loglevel','error','-y','-ss',str(it['ss']),'-i',it['src'],'-an','-vf',vf,'-c:v','libx264','-preset','veryfast','-crf','18','-r',str(FPS),o])
    open(f'{OUT}/list.txt','w').write(''.join(f"file '{x}'\n" for x in lst))
    run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',f'{OUT}/list.txt','-c','copy','/tmp/e8/ed/picture8.mp4'])
if sys.argv[1] in ('mix','all'):
    st={it['k']:it['start'] for it in E}; en={it['k']:it['start']+it['dur'] for it in E}
    inputs=[]; filt=[]
    def add(p,loop=False):
        if loop: inputs.extend(['-stream_loop','-1'])
        inputs.extend(['-i',p]); return sum(1 for x in inputs if x=='-i')-1
    dl=[]
    for it in E:
        for lid,off in it['lines']:
            i=add(f'/tmp/e8/v3/{lid}.wav'); ms=int((it['start']+off)*1000)
            filt.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=mono,adelay={ms}|{ms},apad=whole_dur={TOT:.3f}[d{i}]'); dl.append(f'[d{i}]')
    filt.append(f"{''.join(dl)}amix=inputs={len(dl)}:normalize=0,atrim=0:{TOT:.3f},asplit=2[dlg][key]")
    secs=[('06 - Lucky.wav',10.0,0.0,en['01_est']+1.5,0.8,2.0,0.16),('10 - Own Way.wav',30.0,st['08_bell']+1.0,en['09_leave'],1.0,1.5,0.12),
          ('10 - Own Way.wav',48.0,st['12_hook'],TOT,1.0,2.5,0.17)]
    ml=[]
    for n,(f,off,t0,t1,fi,fo,v) in enumerate(secs):
        i=add(f'{A}/{f}'); L=t1-t0; ms=int(t0*1000)
        filt.append(f'[{i}:a]atrim={off}:{off+L:.3f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d={fi},afade=t=out:st={L-fo:.3f}:d={fo},volume={v},adelay={ms}|{ms},apad=whole_dur={TOT:.3f}[m{n}]'); ml.append(f'[m{n}]')
    filt.append(f"{''.join(ml)}amix=inputs={len(ml)}:normalize=0,atrim=0:{TOT:.3f}[mus]")
    filt.append('[key]aformat=channel_layouts=stereo,asplit=2[k2][k3]')
    filt.append('[mus][k2]sidechaincompress=threshold=0.02:ratio=8:attack=30:release=400:makeup=1[mduck]')
    i=add(f'{S}/amb_street.wav',loop=True); te=st['99_end']
    filt.append(f'[{i}:a]atrim=0:{te:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=1.5,afade=t=out:st={te-1.5:.3f}:d=1.5,volume=0.55,apad=whole_dur={TOT:.3f}[ambm]')
    filt.append('[ambm][k3]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=500:makeup=1[amb]')
    sl=[]; n=0
    for it in E:
        for k,t,g in it['cues']:
            p=SFX.get(k,f'{S}/{k}.wav'); i=add(p); ms=int((it['start']+t)*1000)
            vol=f'volume={g}' if k=='LAUGH' else f'volume={g-6}dB'
            filt.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,{vol},adelay={ms}|{ms},apad=whole_dur={TOT:.3f}[x{n}]'); sl.append(f'[x{n}]'); n+=1
    filt.append(f"{''.join(sl)}amix=inputs={len(sl)}:normalize=0,atrim=0:{TOT:.3f}[fx]")
    filt.append('[dlg]aformat=channel_layouts=stereo,volume=1.15[dst]')
    filt.append('[dst][mduck][amb][fx]amix=inputs=4:normalize=0,alimiter=limit=0.95,loudnorm=I=-15:TP=-1.5:LRA=11[out]')
    open('/tmp/e8/ed/mix8_filter.txt','w').write(';\n'.join(filt))
    run(['ffmpeg','-loglevel','error','-y',*inputs,'-filter_complex_script','/tmp/e8/ed/mix8_filter.txt','-map','[out]','-ar','48000','-ac','2','/tmp/e8/ed/mix8.wav'])
if sys.argv[1] in ('mux','all'):
    run(['ffmpeg','-loglevel','error','-y','-i','/tmp/e8/ed/picture8.mp4','-i','/tmp/e8/ed/mix8.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','256k','-shortest','/tmp/e8/ed/GC_EP08_v1.mp4'])
