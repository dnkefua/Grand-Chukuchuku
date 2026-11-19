# Grand Chukuchuku — production hub

Single place for **live tool links**, **folder naming rules**, and **repo vs platform status**. Update this file when you add a Flow collection or OpenArt folder.

Recorded **19 November 2026** (Asia/Dubai). Platform inventory below is from the Cloud Agent browser pass **without your login** — content lists must be refreshed after you sign in.

---

## Canonical platform links (authoritative)

| Platform | Role | Link |
| --- | --- | --- |
| **Google Flow** | Keyframes, Omni/Veo clips, pilot scene assembly, episode storyboard tiles | [Project home](https://flow.google.com/project/f0228615-cbd8-4825-bdf5-797f61bdc9ff) |
| **OpenArt — Seedance 2.5** | Series episode video generation (image/video → clip) | [Director project `TSqslj00fmlacTjsUsxf`](https://openart.ai/suite/create-video/byte-plus-seedance-2-5?projectId=TSqslj00fmlacTjsUsxf) |
| **OpenArt — Lip-sync** | Avatar lip-sync dialogue lines (EP7–8 pipeline) | [Lip-sync suite](https://openart.ai/suite/lip-sync/openart-lipsync) |
| **OpenArt — GBHS campus** | Environment reference uploads only (not daily episodes) | [Project `GmI2LrpbkV2dW1JLV2zp`](https://openart.ai/project/GmI2LrpbkV2dW1JLV2zp) |

### Google Flow — deep links (pilot)

| Asset | Link |
| --- | --- |
| Collection `01 Pilot — Characters and Compound` | [Open collection](https://flow.google.com/project/f0228615-cbd8-4825-bdf5-797f61bdc9ff/collection/1c1fecfa-5ee2-4a1e-aca1-9d683a087018) |
| Scene `Grand Chukuchuku — Pilot Draft` (26 clips) | [Open scene](https://flow.google.com/project/f0228615-cbd8-4825-bdf5-797f61bdc9ff/scene/36ae1ae5-db2d-482c-96f5-134e40d0f039) |

Shot-level pilot status: [`pilot-chapter-one/Grand_Chukuchuku_Flow_Remaining_Shots_Manifest.md`](pilot-chapter-one/Grand_Chukuchuku_Flow_Remaining_Shots_Manifest.md).

---

## How to keep Flow tidy

Use **one Flow project** (`f0228615-…`) and separate work by **collection**:

| Collection name | Holds |
| --- | --- |
| `01 Pilot — Characters and Compound` | Pilot only (`A01`–`C23`). Do not add daily episodes here. |
| `EP07 — First Bottle` | Flow tiles + keyframes for episode 7 |
| `EP08 — The Message` | Flow tiles + keyframes for episode 8 |
| `EP09 — Luc's One Minute` | Next episode (create when boarding starts) |

**Tile / clip naming**

- Pilot: keep manifest IDs (`A01`, `B09`, …).
- Episodes: `EP08_F1_establishing`, `EP08_V_zino_story`, `EP08_V_bell`, … matching files under local `EP08_Board/flow_src/`.
- Voice ingredients: `Zino — Cameroon draft`, `Gideon — Cameroon draft`, `Luc — Cameroon draft` (same names as pilot).

**Do not delete** ambiguous tiles until the matching file is in the edit pipeline (`EP0x_Edit/pipeline/edl*.json`).

**Settings reminders:** Pilot manifest used **Omni 1.1 Flash**, **16:9**, **720p**. Episode YouTube masters target **1080p** — label exports clearly (`720p-draft` vs `1080p-master`).

---

## How to keep OpenArt (Seedance) tidy

In director project **`TSqslj00fmlacTjsUsxf`**:

| Folder / label (create in OpenArt) | Holds |
| --- | --- |
| `Voices — Zino/Gideon/Luc` | Voice clones used for dialogue |
| `EP07 — First Bottle` | Seedance / video gens for ep 7 |
| `EP08 — The Message` | Seedance / video gens for ep 8 |
| `Lip-sync — dialogue` | Kling Avatar outputs (`AV_E1`, …) |

Keep **GBHS campus** uploads in project **`GmI2LrpbkV2dW1JLV2zp`** only — do not mix campus stills into the Seedance episode project.

Default generation for new episode boards: **16:9**, **480p/720p** for iteration; only promote finals used in `render*.py`.

---

## Where we are (repo = source of truth)

| Episode | Title | Script | Flow (git) | OpenArt (git) | Edit pipeline | Publish kit |
| ---: | --- | :---: | :---: | :---: | :---: | :---: |
| Pilot | The Man Who Never Ran | Storyboard v2 | Manifest `A01–C23` **completed** in docs | Plan doc only | Not in repo | — |
| **7** | First Bottle | v2 script + dialogue txt | Locks in `EP07_Board/v1/fix/` | Not linked yet | `EP07_Edit/pipeline` **v5** | YouTube + TikTok copy |
| **8** | The Message | `EP08_…_EDITABLE.txt` | Paths in `build8.py` (local upload disk) | Commit notes; **no project URL until this hub** | `EP08_Edit/pipeline` | EN/FR SRT + upload copy |
| **9** | Luc's One Minute | Development beats only | — | — | — | — |

**Local media (not on GitHub):** `*.mp4`, `*.wav`, etc. are gitignored. EP08 pipeline expects assets under:

`/mnt/user-data/uploads/Grand-Chukuchuku/EP08_Board/flow_src` and `…/av`

Those folders exist on your **machine with uploads**, not this Cloud Agent VM.

**Git:** `main` includes EP08 pipeline commit **19 Nov 2026 ~10:41 Dubai**.

---

## Platform access (agent, 19 Nov 2026)

| Platform | Agent could enter? | Note |
| --- | :---: | --- |
| Google Flow | No | Google sign-in required on project URL |
| OpenArt Seedance project | No | Login modal; project content not visible anonymously |

**To let the agent tidy inside the tools:** stay signed in on the Cloud Agent desktop browser (same Google / OpenArt account), then ask for a **follow-up pass** — rename only, no deletes.

---

## After you log in — 10-minute tidy checklist

### Flow

1. Open [project home](https://flow.google.com/project/f0228615-cbd8-4825-bdf5-797f61bdc9ff).
2. Confirm pilot clips live only under `01 Pilot — Characters and Compound`.
3. Create collections `EP07 — First Bottle`, `EP08 — The Message` if missing; move stray episode tiles out of the pilot collection.
4. Paste collection URLs into the table below and commit.

### OpenArt

1. Open [Seedance project](https://openart.ai/suite/create-video/byte-plus-seedance-2-5?projectId=TSqslj00fmlacTjsUsxf).
2. Create folders `EP07`, `EP08`, `Voices`, `Lip-sync`.
3. Move orphan gens into the right episode folder.
4. Note credit balance and refill date here:

| Field | Value (fill in) |
| --- | --- |
| OpenArt credits remaining | |
| Flow credits remaining | |
| EP07 Flow collection URL | |
| EP08 Flow collection URL | |

---

## Related docs

- Script source of truth: [`scripts/SCRIPT_SOURCE.md`](scripts/SCRIPT_SOURCE.md)
- EP7 edit: [`../../EP07_Edit/pipeline/README.md`](../../EP07_Edit/pipeline/README.md)
- EP8 edit: [`../../EP08_Edit/pipeline/README.md`](../../EP08_Edit/pipeline/README.md)
- Continuity: [`CONTINUITY_LOG.md`](CONTINUITY_LOG.md)