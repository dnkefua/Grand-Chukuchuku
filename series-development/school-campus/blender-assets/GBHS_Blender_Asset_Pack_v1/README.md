# GBHS Kumba — reusable Blender campus and classrooms

Created locally for **Grand Chukuchuku**, 13 November 2026. This is an editable 3D environment reconstruction for review. The user's latest direction is the first days at GBHS after the pilot, including classroom sets for Episodes 2 and 3. Older episode numbering does not govern this asset pack.

## Open in Blender

- `models/GBHS_Campus_Classrooms_v1.blend`: the full campus and two furnished classrooms in their actual building locations. Includes named cameras and rigid door/shutter/gate controls.
- `models/GBHS_Classroom_A_First_Day.blend`: standalone complete first-day classroom, with its walls, roof, veranda, furniture, light and camera.
- `models/GBHS_Classroom_B_Lessons.blend`: standalone complete classroom for first lessons and later reuse.
- `models/GBHS_Campus_Classrooms_v1.glb`: portable geometry/material-color backup. The richer procedural Blender materials and editable hinge animation remain in the `.blend` source.

The installed application used is the Blender 5.0.1 executable in `D:\upbge-0.50-windows-x64\upbge-0.50-windows-x64`. It is a UPBGE distribution of Blender. The files use standard meshes, materials, cameras and object transforms, not game logic.

## Campus included

Forms One–Two, two-storey Form Three, two-storey Forms Four–Five, Lower/Upper Sixth, the Main Office opposite Form Five, science labs, open-sided cafeteria and Food and Nutrition building. The football field is between the junior and Form Three zones. Basketball begins beside Form Three; basketball, handball and long jump share one straight alignment. The sandpit is beside the cafeteria.

A rectangular concrete-block boundary surrounds the site. Houses are outside the north and east sides; vegetation is concentrated outside the other sides. An unpaved vehicle road leads from the gate nearest Sixth Form to the cafeteria. The 10-metre Form Three / Four–Five gap and the previous plan's two 500-metre zone separations are retained.

GBHS is a separate location from the Professional School opposite the residential compound. This asset pack does not merge those two schools.

## Classroom assets

Two 30-seat rooms, each with 15 two-pupil desks and benches, teacher desk and chair, board, exercise books, pencils, noticeboard, register, window openings, security bars, shutters and a door. A is dressed for a first-day welcome. B contains editable, generic arithmetic lesson text. Furniture, class size, exact classroom dimensions and lesson wording are proposed staging details; they are not represented as the author's confirmed memories.

The named camera objects include classroom back-to-board, teacher reverse, doorway, lesson view, veranda, Form Three passage, full-campus aerial, plan, sporting facilities, cafeteria and gate coverage. The same model supplies every view.

Select an object ending in `HINGE` and rotate its local Z axis to operate a rigid door, shutter or gate. Avoid scaling these controls. The main scene's frames 1–96 contain a four-second Classroom A door-opening action and two camera moves at 24 fps. The standalone sets preserve usable hinge hierarchy but do not contain the full campus timeline.

No named character model or crowd is included. Empty seat markers assist staging without introducing inconsistent versions of Zino, Luc or Gideon. The empty preview folders are reserved for subsequent rendered animations; this delivery is the editable environment and its still-camera references.

## Using the pack in OpenArt

Destination project: **Grand Chukuchuku — GBHS 3D Campus & Classrooms** (`GmI2LrpbkV2dW1JLV2zp`). Check `openart_upload_receipts.json` for the actual accepted uploads; a local file is not proof that an upload succeeded.

The OpenArt connector accepts image/video/audio references; direct `.blend` or GLB import is not established by its supported tool schema. This workflow uploads camera renders, while keeping the actual editable 3D models locally. OpenArt's published Worlds workflow takes image references and exports Gaussian Splats; that is not evidence of a Blender-mesh importer.

For geometry and background continuity, render camera changes and environment animation in Blender. Use those renders as video/reference plates or as starting frames in OpenArt. Keep the source model unchanged between shots. AI generation can still alter a reference, so it must be reviewed against the rendered source. No claim is made that an uploaded still locks geometry inside an AI video model.

Local Blender rendering uses no OpenArt generation credits. This can reduce the need to regenerate environments and camera changes, but does not waive OpenArt charges for generation or guarantee a fixed percentage saving. This pack was created without submitting a paid OpenArt generation.

## Reference prompts

**Campus:** Use this exact GBHS Kumba Blender render as the fixed environment reference. Preserve every building footprint, floor count, court location, fence, gate, road and camera perspective. Keep the road brown earth. Maintain the same daylight and materials. Place approved characters only where their feet contact the ground; do not add buildings or move sports facilities.

**Classroom:** Use this exact classroom camera render. Preserve the board, fifteen paired desks, bench positions, walkways, windows and teacher area. Use the separately approved teenage character references and short-sleeved three-pocket GBHS jackets with the circular badge on the wearer's left chest pocket. Only the specified character moves or speaks. Doors and shutters rotate about the visible hinge and retain rigid geometry. No floating books, morphing benches or changing class layout.

For cross-angle scenes, supply a Blender render from each actual camera at the same action time. Use a controlled Blender scene for exact continuity rather than asking a generator to invent a reverse view from one picture.

## Provenance and limits

Based on the saved campus specification, creator corrections v2/v3, and the existing visual references. Footprints, finish, roof detail, furniture, trees and nominal orientation are design proposals, not a measured campus survey. The old 500-metre descriptions retain their previous proposed edge-to-edge interpretation. Confirming the physical layout remains a creator review step.

This is a reusable environment base with simple stylized materials, not a finished character-animated episode or photoreal final film. Production lighting, detailed wear and character integration can be refined in the same files.

Build sources are under `source`. No downloaded textures or paid generation are required. The source Blender file contains a `READ_ME_GBHS_ASSET_PACK` text block. The model and scene locations are recorded in `asset_manifest.json`.

Official references: [OpenArt Worlds](https://openart.ai/feature/openart-worlds), [Blender command-line rendering](https://docs.blender.org/manual/en/latest/advanced/command_line/render.html).
