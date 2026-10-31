# GBHS Kumba — campus visual pack

Six **generated photorealistic reconstructions** for the animated series, based on the author's account. These are location/design references, not real school photographs or a measured campus survey.

[Open the 11-page visual pack](GBHS_Kumba_Campus_Visual_Pack.pdf) · [Download images, plans and sources](../Grand-Chukuchuku_GBHS_Kumba_Campus_Package_v1.zip)

| View | Image |
| --- | --- |
| A01 — whole-campus oblique aerial | [PNG](images/01_Aerial_Oblique.png) |
| A02 — higher-angle aerial | [PNG](images/02_Aerial_High_Angle.png) |
| S01 — main classroom blocks, side-oblique | [PNG](images/03_Main_Blocks_Side.png) |
| S02 — Lower/Upper Sixth, side-oblique | [PNG](images/04_Sixth_Form_Side.png) |
| E01 — Form Three passage, student-eye view | [PNG](images/05_Form_Three_Gap_Eye_Level.png) |
| E02 — administration court toward labs/canteen | [PNG](images/06_Admin_Labs_Canteen_Eye_Level.png) |

[Overall plan](references/GBHS_Overall_Campus_Plan.pdf) · [Main cluster plan](references/GBHS_Main_Cluster_Plan.pdf) · [Badge construction reference](references/GBHS_Badge_Construction.pdf)

## Confirmed and proposed

**Author-supplied:** Government Bilingual High School Kumba, reported 10.7 km from Zino's compound; Forms One–Two one storey; Form Three, Forms Four–Five and Lower/Upper Sixth two storeys. Reported separations are 500 m / 10 m / 500 m. Administration is opposite Form Five; the Physics/Biology/Chemistry labs are adjacent; the canteen with food merchants is next to the labs.

**Proposed:** orientation, footprints, combined-block layouts, court size, paths, paint/roof materials, vegetation and terrain. The drawing's edge-to-edge interpretation of the distances is provisional. The second 500 m span locally includes labs/canteen; the proposed open ground after the canteen is 376 m. The real distance endpoints, travel route/time and site boundary remain open. Perspective images do not establish exact dimensions or consistent room/window counts across views.

The GBHS Sixth Form buildings do not move Zino's separate boarding-school years to GBHS. Professional School remains the distinct vocational/night-study location. Aerial A02 is a higher-angle perspective, not a vertical satellite view. A rejected nadir trial added roofs and is excluded.

## Uniform badge

The pocket is on the **wearer's left chest**. The circular badge carries **GBHS**, **Government Bilingual High School Kumba**, and a lit candle. Its supplied content is preserved in the vector construction reference. Navy/cream/sky-blue/gold colours, typeface and candle artwork are proposals pending an original crest reference. Tiny embroidery in images is approximate. No school uniforms or badges are used for Professional School night revision.

Mirabel, Lizzy and the core daytime friend portrait have been updated without changing their established faces or body designs. Earlier unbadged copies are archived. [Current uniform sheets](../character-bible/turnarounds/school-uniforms/README.md).

## Sources and rebuild

[Structured specification](campus_spec.json) · [Camera brief](GBHS_Kumba_Campus_Brief.md) · [Actual-asset review](../writers-room/GBHS_KUMBA_CAMPUS_REVIEW_2026-10-31.md) · [Native-image provenance](native_image_provenance.json).

Run `python3 series-development/school-campus/build_campus_package.py` to rebuild diagrams/PDF/ZIP from the existing native images. `--references` rebuilds only deterministic diagrams. The builder fits complete images without retouching/cropping them; it does not regenerate artwork.
