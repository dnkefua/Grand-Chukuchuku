"""RULE from Episode 9: the YouTube version has French subtitles burned in.
English stays as an uploaded subtitle file (.en.srt); the .fr.srt is still uploaded too.

usage: python3 tools/subtitles/burn_french_youtube.py <clean master .mp4> <episode .fr.srt> <output .mp4>

House YouTube style: DejaVu Sans Bold 50 on 1920x1080, yellow (same yellow as the French line on TikTok),
black outline, 60 px above the bottom. The master's audio is copied untouched.
"""
import sys, os, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tiktok_vertical'))
from tt_common import srt_to_events, ass_time

HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: FR,DejaVu Sans,50,&H003FD2FF,&H003FD2FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,160,160,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def main(master, fr_srt, out):
    ass = os.path.splitext(out)[0] + '.fr_burn.ass'
    body = ''.join(f"Dialogue: 0,{ass_time(a)},{ass_time(b)},FR,,0,0,0,,{t}\n" for a, b, t in srt_to_events(fr_srt))
    open(ass, 'w', encoding='utf-8').write(HEADER + body)
    esc = ass.replace('\\', '/').replace(':', '\\:').replace("'", "\\'")
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', master, '-vf', f"ass='{esc}',format=yuv420p",
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-c:a', 'copy', '-movflags', '+faststart', out], check=True)
    print('wrote', out)

if __name__ == '__main__':
    main(*sys.argv[1:4])
