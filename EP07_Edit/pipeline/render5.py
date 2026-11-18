import json, subprocess, os, sys
E=json.load(open('/tmp/ed/edl5.json')); FPS=24
OUT='/tmp/ed/seg5'; os.makedirs(OUT,exist_ok=True)
A='/mnt/user-data/uploads/Grand-Chukuchuku/Audio files'; S='/tmp/ed/sfxn'
only=set(sys.argv[2:]) if len(sys.argv)>2 else None
def run(c): subprocess.run(c,check=True)
if sys.argv[1] in ('pic','all'):
    lst=[]
    for n,it in enumerate(E):
        o=f'{OUT}/{n:03d}_{it["k"]}.mp4'; lst.append(o); nf=round(it['dur']*FPS)
        if only and it['k'] not in only and os.path.exists(o): continue
        sp=it['speed']
        cr=it.get('crop',0); pre=f'crop=iw*{cr}:ih*{cr}:iw*{(1-cr)/2}:0,' if cr else ''
        vf=pre+f'setpts=PTS/{sp},fps={FPS},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,format=yuv420p,tpad=stop_mode=clone:stop_duration=3,trim=end_frame={nf}'
        run(['ffmpeg','-loglevel','error','-y','-ss',str(it['ss']),'-i',it['src'],'-an','-vf',vf,'-c:v','libx264','-preset','veryfast','-crf','18','-r',str(FPS),o])
    open(f'{OUT}/list.txt','w').write(''.join(f"file '{x}'\n" for x in lst))
    run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',f'{OUT}/list.txt','-c','copy','/tmp/ed/picture5.mp4'])
if sys.argv[1] in ('mix','all'):
    TOT=E[-1]['start']+E[-1]['dur']; st={it['k']:it['start'] for it in E}; en={it['k']:it['start']+it['dur'] for it in E}
    inputs=[]; filt=[]
    def add(p,loop=False):
        if loop: inputs.extend(['-stream_loop','-1'])
        inputs.extend(['-i',p]); return sum(1 for x in inputs if x=='-i')-1
    dl=[]
    for it in E:
        for lid,off in it['lines']:
            i=add(f'/tmp/ed/vo/{lid}_t.wav'); ms=int((it['start']+off)*1000)
            filt.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=mono,adelay={ms}|{ms},apad=whole_dur={TOT:.3f}[d{i}]'); dl.append(f'[d{i}]')
    filt.append(f"{''.join(dl)}amix=inputs={len(dl)}:normalize=0,atrim=0:{TOT:.3f},asplit=2[dlg][key]")
    secs=[('06 - Lucky.wav',10.0,0.0,en['02'],0.6,1.5,0.13),('06 - Lucky.wav',60.0,st['32'],en['35'],0.8,1.0,0.11),
          ('10 - Own Way.wav',48.0,st['41'],en['52'],0.5,0.6,0.12),('06 - Lucky.wav',156.0,st['60'],TOT,1.5,2.0,0.15)]
    ml=[]
    for n,(f,off,t0,t1,fi,fo,v) in enumerate(secs):
        i=add(f'{A}/{f}'); L=t1-t0; ms=int(t0*1000)
        filt.append(f'[{i}:a]atrim={off}:{off+L:.3f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d={fi},afade=t=out:st={L-fo:.3f}:d={fo},volume={v},adelay={ms}|{ms},apad=whole_dur={TOT:.3f}[m{n}]'); ml.append(f'[m{n}]')
    filt.append(f"{''.join(ml)}amix=inputs={len(ml)}:normalize=0,atrim=0:{TOT:.3f}[mus]")
    filt.append('[key]aformat=channel_layouts=stereo,asplit=2[k2][k3]')
    filt.append('[mus][k2]sidechaincompress=threshold=0.02:ratio=8:attack=30:release=400:makeup=1[mduck]')
    i=add(f'{S}/amb_street.wav',loop=True)
    filt.append(f'[{i}:a]atrim=0:{TOT:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=1.5,afade=t=out:st={TOT-2:.3f}:d=2,volume=1.0[amb1]')
    t0,t1=st['07'],en['53']; i=add(f'{S}/amb_match.wav',loop=True)
    filt.append(f'[{i}:a]atrim=0:{t1-t0:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=1.0,afade=t=out:st={t1-t0-1.5:.3f}:d=1.5,volume=1.3,adelay={int(t0*1000)}|{int(t0*1000)},apad=whole_dur={TOT:.3f}[amb2]')
    filt.append('[amb1][amb2]amix=inputs=2:normalize=0[ambm]')
    filt.append('[ambm][k3]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=500:makeup=1[amb]')
    sl=[]; n=0
    for it in E:
        for k,t,g in it['cues']:
            i=add(f'{S}/{k}.wav'); ms=int((it['start']+t)*1000)
            filt.append(f'[{i}:a]volume={g-6}dB,adelay={ms}|{ms},apad=whole_dur={TOT:.3f}[x{n}]'); sl.append(f'[x{n}]'); n+=1
        for f,t,v in it['laughs']:
            i=add(f); ms=int((it['start']+t)*1000)
            filt.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={v},adelay={ms}|{ms},apad=whole_dur={TOT:.3f}[x{n}]'); sl.append(f'[x{n}]'); n+=1
    filt.append(f"{''.join(sl)}amix=inputs={len(sl)}:normalize=0,atrim=0:{TOT:.3f}[fx]")
    filt.append('[dlg]aformat=channel_layouts=stereo,volume=1.15[dst]')
    filt.append('[dst][mduck][amb][fx]amix=inputs=4:normalize=0,alimiter=limit=0.95,loudnorm=I=-15:TP=-1.5:LRA=11[out]')
    open('/tmp/ed/mix5_filter.txt','w').write(';\n'.join(filt))
    run(['ffmpeg','-loglevel','error','-y',*inputs,'-filter_complex_script','/tmp/ed/mix5_filter.txt','-map','[out]','-ar','48000','-ac','2','/tmp/ed/mix5.wav'])
if sys.argv[1] in ('mux','all'):
    run(['ffmpeg','-loglevel','error','-y','-i','/tmp/ed/picture5.mp4','-i','/tmp/ed/mix5.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','256k','-shortest','/tmp/ed/GC_EP07_v5.mp4'])
    run(['ffmpeg','-loglevel','error','-y','-i','/tmp/ed/GC_EP07_v5.mp4','-vf','scale=1280:720','-c:v','libx264','-preset','veryfast','-crf','24','-c:a','aac','-b:a','160k','/tmp/ed/GC_EP07_v5_720p.mp4'])
