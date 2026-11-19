# Episode 8 "The Message" edit pipeline

Mirrors the EP7 layout. Source video and lip-sync live on the author upload disk, not in git.

## Paths (local machine)

| Path | Contents |
| --- | --- |
| `…/EP08_Board/flow_src/` | Flow exports: `EP08_F1_establishing.png`, `EP08_V_*.mp4`, … |
| `…/EP08_Board/av/` | Kling Avatar lip-sync: `AV_E1.mp4` … `AV_E8.mp4` |
| `/tmp/e8/` | Render scratch: `ed/edl8.json`, mux outputs |

Default base in `build8.py`: `/mnt/user-data/uploads/Grand-Chukuchuku/EP08_Board/`.

## Scripts

| File | Role |
| --- | --- |
| `build8.py` | Builds `edl8.json` shot list and timings |
| `render8.py` | Picture / mix / mux |
| `subs8.py` | English and French SRT from EDL |
| `tiktok8.py` | Vertical full-screen TikTok master |
| `ep08_vert.ass` | TikTok burn-in style |

## Platform links

See [`series-development/PRODUCTION_HUB.md`](../../series-development/PRODUCTION_HUB.md) for Google Flow and OpenArt Seedance project URLs.

## Publish

Metadata and subtitles: `../pkg/YouTube/` and `../pkg/TikTok/`.