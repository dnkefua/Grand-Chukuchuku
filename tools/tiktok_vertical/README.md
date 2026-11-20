# tiktok_vertical: full-screen 9:16 TikTok cuts from the YouTube master

The method, rules and camera guide are in [series-development/TIKTOK_VERTICAL_METHOD.md](../../series-development/TIKTOK_VERTICAL_METHOD.md). Read it first.

**Needs:**
- Python 3 with `opencv-python` and `numpy`.
- `ffmpeg` and `ffprobe` with libass, for the burned-in subtitles.

```bash
CFG=EP07_Edit/pipeline/tiktok_fullscreen/ep07_tiktok.json   # one config per episode
python3 tools/tiktok_vertical/tt_analyze.py $CFG            # cuts + auto crop centre -> <work>/shots.json
python3 tools/tiktok_vertical/tt_review.py  $CFG plan       # every shot, 5 frames, 9:16 box
python3 tools/tiktok_vertical/tt_review.py  $CFG dialogue   # every line: is the speaker in the box?
python3 tools/tiktok_vertical/tt_review.py  $CFG strip 64 0.5   # gridded strip for writing keyframes
#   ... edit the episode's camera.json ...
python3 tools/tiktok_vertical/tt_render.py  $CFG --range 4740 5160   # quick preview of a sequence
python3 tools/tiktok_vertical/tt_render.py  $CFG                     # full render (master audio copied)
python3 tools/tiktok_vertical/tt_review.py  $CFG output     # QC sheet of the render
```

## Episode config

```json
{
  "episode": "Episode 7 - First Bottle",
  "master": "<staged YouTube master .mp4>",
  "work": "<scratch folder>",
  "camera": "ep07_camera.json",
  "cues": "../edl5.json",
  "subtitles": {"ass": "../ep07_tt.ass"},
  "title": {"line1": "GRAND CHUCKUCHUCKU", "line2": "Episode 7 · First Bottle", "start": 0.3, "end": 2.9},
  "clean_opening": {"image": "ep07_opening_clean.jpg", "until_shot": 1, "cx": 0.45, "push": 0.06},
  "output": "<.../Grand Chuckuchucku - Episode 7 - First Bottle - TikTok.mp4>"
}
```

- Relative paths are read from the config's own folder.
- `subtitles` takes either `srt` or `ass` (only the Dialogue lines are used; the house vertical style is applied).
- Leave out `clean_opening` when the master has no burned-in title.
- `camera.json` keys are shot numbers from `shots.json`. Shots you don't list keep the auto centre.

## Files

| File | Purpose |
|---|---|
| `tt_common.py` | Config, shot and cue loading; keyframe easing; vertical subtitle style |
| `tt_analyze.py` | Cut detection (ffmpeg scene > 0.3) and a motion-weighted auto crop centre per shot |
| `tt_review.py` | Plan, dialogue, strip and output review sheets |
| `tt_render.py` | Frame-exact renderer: fixed or moving crops, split screen, impact punch-ins and shake, slow-motion push-ins, title-free opening |
