# Episode 7 "First Bottle" edit pipeline (v5)

- `build5.py` builds the edit decision list (`edl5.json`): shot order, close-ups, dialogue placement, sound-effect and laughter cues.
- `render5.py pic|mix|mux|all` renders the picture, the mix (dialogue, De$ music sections with ducking, ambience, SFX, laughs, -15 LUFS) and the final mux.
- `subs7.py` writes the English and French subtitles from the EDL timings; `ep07_tt.ass` is the TikTok burn-in style.
- `cues_old.py`, `lines.py`, `plan.py`, `render2.py`, `mix2.py`, `timeline2.json` are the v2–v4 sources the EDL reuses.
- `av_lines.txt`: padded line audio lengths used for the Kling Avatar lip-sync close-ups.

Character locks used for every regenerated shot: `EP07_Board/v1/fix/MS_ZINO.png`, `MS_GIDEON.png`, `MS_LUC.png` (from the bible turnarounds).
