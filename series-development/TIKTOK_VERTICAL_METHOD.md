# TikTok vertical method: full-screen 9:16 cut

This is the house standard for every TikTok version of the series from **Episode 7** onward. Episode 7 "First Bottle" (TikTok v2, 20 Nov 2026) is the approved reference cut.

**Tool:** [`tools/tiktok_vertical/`](../tools/tiktok_vertical/README.md).
**Worked example:** [`EP07_Edit/pipeline/tiktok_fullscreen/`](../EP07_Edit/pipeline/tiktok_fullscreen/).

---

## 1. Rules (every episode)

1. **Full screen.**
   - 1080x1920, filled edge to edge.
   - No letterbox, no blurred bars, no picture-in-picture.
2. **Built from the finished YouTube master.**
   - The picture is reframed, never retimed: output frame *n* comes from master frame *n*.
   - The master's audio is copied untouched, so the mix and the lip-sync stay exactly as approved.
   - The frame count must equal the master's.
3. **Every spoken line shows its speaker.**
   - The speaker's face, mouth included, stays in frame for the whole line.
   - This holds for lip-sync shots and for calls made on the run, e.g. "Pass it! There's space at the back post!"
4. **Every action beat shows both sides.**
   - Who does it and who it's done to: kicker and ball, slider and the player tackled, attacker and victim.
   - If they don't fit in one 9:16 frame at the key moment, use a moving crop or a split screen (section 3).
5. **The payoff is in frame.**
   - The ball hitting the bottle.
   - The victim on the ground with his head in frame, not only his legs.
   - The coins changing hands.
6. **Energy.**
   - Every impact gets a short punch-in (+9%) and a short shake.
   - Every slow-motion moment gets a slow push-in (+10% over 2.2 s).
   - Both are placed automatically from the edit's own sound-effect cues, so they land on the sound.
7. **Text.**
   - English subtitles are burned in: DejaVu Sans Bold 54, white with a black outline, 520 px above the bottom so they sit clear of TikTok's caption area.
   - Show title "GRAND CHUCKUCHUCKU", with "Episode N · Title" under it, at the top over the opening.
   - French subtitles go on YouTube, which accepts subtitle files.
8. **No cropped burned-in text.**
   - If the master has a burned-in title, the opening shot is replaced by a title-free still with a slow push-in.
   - Use frame 0 of an earlier cut, or the clean source clip.
   - Never use a delogo smear.
9. **Same length as the YouTube episode.**

## 2. Workflow

| Step | Command (from repo root) | Check |
|---|---|---|
| 0. Stage | Copy the YouTube master from `Desktop\Grand Chuckuchuku\Final cut\Youtube submission\` into the workspace. Write `EPxx_Edit/pipeline/tiktok_fullscreen/epxx_tiktok.json` (copy the Ep 7 one). | The master is the final picture with final sound. |
| 1. Analyse | `python3 tools/tiktok_vertical/tt_analyze.py <cfg>` | Shot count looks right; no missed cuts. |
| 2. Plan sheets | `python3 tools/tiktok_vertical/tt_review.py <cfg> plan` | **Every shot**: 5 frames across the shot, with the 9:16 window as a yellow box. Fix each one in `camera.json`. |
| 3. Dialogue sheet | `... tt_review.py <cfg> dialogue` | **Every line**: the speaker is inside the box at mid-line. |
| 4. Action strips | `... tt_review.py <cfg> strip <shot> 0.5` | A 10% grid every 0.5 s. Read positions off the grid and write keyframes / split screens. |
| 5. Preview | `... tt_render.py <cfg> --range <frameA> <frameB>` | Action sequences, split screens, whip pans (renders in about 10 s). |
| 6. Render | `... tt_render.py <cfg>` | About 6 min for a 4:30 episode. The frame count equals the master's. |
| 7. Output sheet | `... tt_review.py <cfg> output` | Start, middle and end of every shot in the actual render. |
| 8. Deliver | — | See below. |

**Delivery:**
- Save to `Final cut\Tiktok submission`, named `Grand Chuckuchucku - Episode N - Title - TikTok.mp4`.
- Rename the old file "(previous …)".
- Update the post details file (it should say "full-screen vertical").
- Copy to `EPxx_Edit\pkg\TikTok`.
- Commit the config and `camera.json`.

## 3. Choosing the camera for a shot

| Shot | Camera | `camera.json` |
|---|---|---|
| Close-up or single speaker | Fixed, on the face | `"12": 0.47` |
| Two-shot, one speaker | Fixed, on that line's speaker (not the listener) | `"9": 0.52` |
| Two speakers in one shot | Pan at the line change (0.3–0.4 s) | `[[0,0.3],[0.48,0.3],[0.6,0.65],[1,0.65]]` |
| Camera moves or pushes in | Keyframes that follow the subject (read off the strip) | `"26": [[0,0.44],[0.4,0.46],[1,0.5]]` |
| Short exchange (≤1.5 s): punch, then reaction | Whip pan from actor to reactor | `"62": [[0,0.3],[0.35,0.3],[0.6,0.62],[1,0.62]]` |
| Two subjects more than about 0.3 of frame width apart at the key beat | **Split screen**: top = cause/attacker, bottom = target/effect. Return to a single frame when they meet. | see Ep 7 shot 64 |
| Zoom on a detail | Add a zoom value: `[frac, cx, cy, zoom]` | `[[0,0.5,0.6,1.0],[1,0.5,0.6,1.15]]` |
| Wide establishing shot or aerial | On the action / the street | `"78": 0.45` |
| End card | Centre | `"79": 0.5` |

`frac` runs from 0 to 1 through the shot. `cx` and `cy` are the window centre as fractions of frame width and height. Between keyframes the movement eases with a smoothstep.

**Split-screen spec** (Ep 7 shot 64, the slow-motion Matrix kick):
```json
{"single": [[0,0.5],[0.69,0.5],[0.8,0.48],[0.84,0.43],[1,0.44]],
 "split": {"range": [0.0, 0.69],
           "top": [[0,0.62,0.33],[0.25,0.62,0.35],[0.35,0.68,0.3],[0.6,0.7,0.3],[0.69,0.62,0.35]],
           "bot": [[0,0.37,0.55],[0.25,0.38,0.6],[0.35,0.47,0.72],[0.6,0.49,0.72],[0.69,0.48,0.7]]},
 "zoom_end": [[0.84,1.0],[1,1.03]]}
```
- **Top panel:** Arey's flying kick.
- **Bottom panel:** Zino bending back under it.
- **At frac 0.69:** it cuts to one frame of Zino standing over Arey on the ground.
- **Panel size:** each panel shows a 600 px-high window of the master (aspect 1080:957), and the panels are split by a 6 px light divider.

## 4. Lessons from Episode 7 (don't repeat these)

- **Auto-centre is only a first guess.**
  - It follows motion, so it fails when the camera moves (all of the frame moves) and when a speaker barely moves.
  - On Ep 7 it put the "Pass it!" caller out of frame, cut off the slider in both tackles, and ended the Matrix kick on dust.
- **One middle frame per shot is not a review.**
  - Subjects enter, leave and fall during a shot.
  - Review 5 frames across every shot, then the dialogue sheet, then strips of every action shot.
- **Check the victim's head end.** A lying body is wide; frame the head and the attacker, not the legs.
- **Never rebuild the timeline with ffmpeg `concat`/`trim`.**
  - Swapping in the opening that way added 71 frames, which pushed the picture 2.96 s out of sync with the sound.
  - The renderer builds frame *n* from master frame *n* instead.
  - Always compare frame counts with the master.
- **Impacts never carry across a cut.** The renderer ignores cues from before the shot's first frame.
- **Watch the action at full size.** Contact sheets hide a cropped head or a missing ball.

## 5. Inputs per episode

| Input | Where |
|---|---|
| YouTube master (final picture and mix) | `Final cut\Youtube submission\Grand Chuckuchucku - Episode N - Title.mp4` |
| Sound-effect cue times (for punch-ins) | The episode EDL with `cues` (e.g. `EP07_Edit/pipeline/edl5.json`), or a flat `[[t, "name"], ...]` list |
| English subtitles | The episode `.en.srt` or `.ass` |
| Title-free opening still (only if the master has a burned-in title) | Frame 0 of an earlier cut, or the clean source clip |

Cue names that trigger effects:
- **Strong impacts:** `punch_impact`, `kick_body`, `slowmo_impact`, `bottle_hit`, `body_fall`.
- **Light impacts:** `kick_hard`, `block_hit`, `header`, `land_back`.
- **Push-in:** `slowmo_swell`.

From Episode 9, the edit should log these cues in its EDL as it is cut, so the TikTok pass gets them for free.

## 6. Status by episode (21 Nov 2026)

| Episode | TikTok version | Through this method |
|---|---|---|
| 7 First Bottle | v2, full-screen, split-screen Matrix kick | **Yes**: the reference |
| 8 The Message | Full-screen, fixed per-shot speaker crops, made at the final cut | Partly; impacts and the full review still to do |
| Pilot, 2–6 | Full-screen versions from 17 Nov | Not yet; can be redone with this tool |
| 9 onward | — | Use this method |
