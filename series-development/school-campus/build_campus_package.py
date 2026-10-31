#!/usr/bin/env python3
"""Build exact reference diagrams and package native-generated campus views."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import shutil
import zipfile

import fitz
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parent
SERIES = ROOT.parent
OUT = SERIES.parent.parent / "output" / "grand-chukuchuku"
REF = ROOT / "references"
ART = ROOT / "images"
PDF = ROOT / "GBHS_Kumba_Campus_Visual_Pack.pdf"
PACKAGE = SERIES / "Grand-Chukuchuku_GBHS_Kumba_Campus_Package_v1.zip"
REVIEW = SERIES / "writers-room" / "GBHS_KUMBA_CAMPUS_REVIEW_2026-10-31.md"
NAVY = colors.HexColor("#19384F")
TEAL = colors.HexColor("#307C79")
GOLD = colors.HexColor("#CDA54F")
PAPER = colors.HexColor("#FAF8F2")
MUTED = colors.HexColor("#52656B")
LINE = colors.HexColor("#C6D1CF")
W, H = landscape(A4)

VIEWS = [
    ("01_Aerial_Oblique.png", "A01 / Whole-campus oblique aerial", "Three zones and two broad reported 500 m separations. Proposed orientation, footprints, terrain and building materials."),
    ("02_Aerial_High_Angle.png", "A02 / High-angle aerial", "A second, higher aerial of the same three zones. The labelled overhead plan governs distances; this perspective is not a survey."),
    ("03_Main_Blocks_Side.png", "S01 / Forms Three–Five side view", "Two-storey classroom blocks with the reported 10 m separation; lower lab and canteen volumes are proposed."),
    ("04_Sixth_Form_Side.png", "S02 / Lower and Upper Sixth side view", "The GBHS Sixth Form building is two storeys. Its presence does not change Zino's separate boarding-school chapter."),
    ("05_Form_Three_Gap_Eye_Level.png", "E01 / The 10 m passage at eye level", "A proposed camera position between the separate two-storey Form Three and Forms Four–Five blocks."),
    ("06_Admin_Labs_Canteen_Eye_Level.png", "E02 / Administration, Form Five, labs and canteen", "Administration opposite Form Five; the Physics/Biology/Chemistry laboratory block adjacent; food merchants next to the labs."),
]


def fonts() -> None:
    p = Path("/usr/share/fonts/truetype/dejavu")
    for name, file in [("Campus", "DejaVuSans.ttf"), ("CampusBold", "DejaVuSans-Bold.ttf")]:
        pdfmetrics.registerFont(TTFont(name, str(p / file)))
    pdfmetrics.registerFontFamily("Campus", normal="Campus", bold="CampusBold")


def para(c, text, x, top, width, size=9, colour=MUTED):
    p = Paragraph(text, ParagraphStyle("campus", fontName="Campus", fontSize=size, leading=size * 1.4, textColor=colour))
    _, h = p.wrap(width, H)
    p.drawOn(c, x, top - h)
    return top - h


def chrome(c, title, page):
    c.setFillColor(PAPER); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(NAVY); c.setFont("CampusBold", 18); c.drawString(36, H - 38, title)
    c.setStrokeColor(LINE); c.line(36, 28, W - 36, 28)
    c.setFillColor(MUTED); c.setFont("Campus", 7)
    c.drawString(36, 16, "GBHS KUMBA / GENERATED RECONSTRUCTION / 31 OCTOBER 2026")
    c.drawRightString(W - 36, 16, str(page))


def render_first(source: Path, target: Path, scale=2):
    with fitz.open(source) as doc:
        doc[0].get_pixmap(matrix=fitz.Matrix(scale, scale)).save(target)


def badge_reference():
    """A precise text/placement construction reference, not an official crest."""
    path = REF / "GBHS_Badge_Construction.pdf"
    c = canvas.Canvas(str(path), pagesize=(800, 800), pageCompression=1)
    c.setTitle("GBHS Kumba | badge construction from the author's description")
    cx = cy = 400
    c.setFillColor(PAPER); c.rect(0, 0, 800, 800, fill=1, stroke=0)
    c.setFillColor(NAVY); c.circle(cx, cy, 345, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#F3E8C9")); c.circle(cx, cy, 331, fill=1, stroke=0)
    c.setStrokeColor(NAVY); c.setLineWidth(4); c.circle(cx, cy, 248, fill=0, stroke=1)
    c.setFillColor(colors.HexColor("#CBE2EF")); c.circle(cx, cy, 240, fill=1, stroke=0)
    def arc_text(text, start, end, radius, size, lower=False):
        for i, ch in enumerate(text):
            angle = start + (end - start) * i / max(1, len(text) - 1)
            rad = math.radians(angle)
            c.saveState(); c.translate(cx + radius * math.cos(rad), cy + radius * math.sin(rad))
            c.rotate(angle + 90 if lower else angle - 90)
            c.setFillColor(NAVY); c.setFont("CampusBold", size); c.drawCentredString(0, -size * .32, ch)
            c.restoreState()
    arc_text("GOVERNMENT BILINGUAL HIGH SCHOOL", 160, 20, 287, 20)
    arc_text("KUMBA", 252, 288, 287, 25, lower=True)
    c.setFillColor(NAVY); c.setFont("CampusBold", 60); c.drawCentredString(cx, 500, "GBHS")
    c.setFillColor(colors.HexColor("#FFF8E7")); c.setStrokeColor(NAVY); c.setLineWidth(4)
    c.roundRect(369, 215, 62, 185, 8, fill=1, stroke=1)
    c.setStrokeColor(NAVY); c.setLineWidth(5); c.line(400, 395, 400, 420)
    p = c.beginPath(); p.moveTo(400, 475); p.curveTo(357, 431, 362, 409, 400, 405); p.curveTo(438, 409, 443, 431, 400, 475)
    c.setFillColor(GOLD); c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#FFF3B5")); c.ellipse(388, 410, 412, 445, fill=1, stroke=0)
    c.setStrokeColor(NAVY); c.setLineWidth(10); c.line(320, 205, 480, 205); c.line(350, 190, 450, 190)
    c.save()
    render_first(path, REF / "GBHS_Badge_Construction.png", 1.5)


def plan_reference(spec, zoom=False):
    name = "GBHS_Main_Cluster_Plan" if zoom else "GBHS_Overall_Campus_Plan"
    path = REF / (name + ".pdf")
    pw, ph = 1600, 740
    c = canvas.Canvas(str(path), pagesize=(pw, ph), pageCompression=1)
    c.setTitle("GBHS Kumba | proposed " + ("main cluster" if zoom else "whole-campus") + " plan")
    c.setFillColor(PAPER); c.rect(0, 0, pw, ph, fill=1, stroke=0)
    c.setFillColor(NAVY); c.setFont("CampusBold", 27)
    c.drawString(45, ph - 50, "GBHS KUMBA / " + ("MAIN CLUSTER" if zoom else "OVERALL CAMPUS"))
    para(c, "Reconstruction from the author's account. Building footprints, orientation and gap endpoints are proposed; this is not an official site survey.", 45, ph - 68, pw - 90, 12)
    if zoom:
        xmin, xmax, ymin, ymax = 555, 860, -25, 125
    else:
        xmin, xmax, ymin, ymax = -40, 1330, -130, 170
    scale = min((pw - 150) / (xmax - xmin), 420 / (ymax - ymin))
    ox = (pw - (xmax - xmin) * scale) / 2
    oy = 180
    def xy(x, y): return ox + (x - xmin) * scale, oy + (y - ymin) * scale
    c.setFillColor(colors.HexColor("#E9EFE1")); c.rect(ox, oy, (xmax-xmin)*scale, (ymax-ymin)*scale, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor("#BBA27A")); c.setLineWidth(7 if zoom else 4)
    x0, y0 = xy(xmin, 35); x1, y1 = xy(xmax, 35); c.line(x0, y0, x1, y1)
    for b in spec["buildings"]:
        r = b["rect"]
        if r["x_max"] < xmin or r["x_min"] > xmax: continue
        x, y = xy(r["x_min"], r["y_min"])
        bw, bh = (r["x_max"] - r["x_min"]) * scale, (r["y_max"] - r["y_min"]) * scale
        c.setFillColor(NAVY if b["storeys"] == 2 else GOLD); c.setStrokeColor(colors.white); c.setLineWidth(1)
        c.rect(x, y, bw, bh, fill=1, stroke=1)
        if zoom:
            label = {"form_3":"FORM 3 / 2 STOREYS", "forms_4_5":"FORMS 4–5 / 2 STOREYS", "administration":"ADMINISTRATION", "laboratories":"PHYSICS / BIOLOGY / CHEMISTRY", "canteen":"CANTEEN"}.get(b["id"],b["label"])
            c.setFillColor(NAVY); c.setFont("CampusBold", 11)
            c.drawCentredString(x + bw / 2, y + bh + 13, label)
            if b["id"] == "forms_4_5":
                c.setStrokeColor(colors.white); c.line(x+bw/2,y,x+bw/2,y+bh)
                c.setFillColor(colors.white); c.setFont("CampusBold", 10)
                c.drawCentredString(x+bw*.25,y+bh*.45,"FORM 4"); c.drawCentredString(x+bw*.75,y+bh*.45,"FORM 5")
    def dimension(a, b, y, label):
        xa, yy = xy(a, y); xb, _ = xy(b, y)
        c.setStrokeColor(TEAL); c.setLineWidth(2); c.line(xa, yy, xb, yy)
        c.line(xa,yy-7,xa,yy+7); c.line(xb,yy-7,xb,yy+7)
        c.setFillColor(TEAL); c.setFont("CampusBold", 12 if zoom else 15)
        c.drawCentredString((xa+xb)/2,yy-22,label)
    if zoom:
        dimension(620, 630, -9, "10 m")
        ax, ay = xy(687.5, 75); bx, by = xy(690, 16)
        c.setStrokeColor(TEAL); c.setDash(6,4); c.line(ax,ay,bx,by); c.setDash()
        c.setFillColor(TEAL); c.setFont("CampusBold", 12); c.drawString(ax+12,(ay+by)/2,"OPPOSITE FORM 5")
    else:
        dimension(80,580,-50,"500 m reported")
        dimension(710,1210,-50,"500 m reported")
        for x,text in [(40,"FORMS 1–2 / ONE STOREY"),(700,"FORMS 3–5 / ADMIN / LABS / CANTEEN"),(1250,"LOWER + UPPER SIXTH / TWO STOREYS")]:
            xx,yy=xy(x,115);c.setFillColor(NAVY);c.setFont("CampusBold",12);c.drawCentredString(xx,yy,text)
        c.setFillColor(TEAL); c.setFont("CampusBold", 12); xx,yy=xy(625,-2);c.drawString(xx,yy-15,"10 m: see cluster zoom")
    para(c, "Blue = two-storey classroom blocks. Gold = one-storey blocks; admin/lab/canteen heights are proposed. The two 500 m values and 10 m separation come from the author; edge-to-edge placement is one proposed interpretation.",45,130,pw-90,12)
    para(c, "School is reported 10.7 km from Zino's compound. Road/footpath/straight-line basis and travel time remain open. Display orientation does not assert true compass bearings. GBHS Sixth Form facilities do not alter Zino's separate boarding-school chapter.",45,85,pw-90,11)
    c.save()
    render_first(path, REF / (name + ".png"), 1.2)


def references():
    fonts(); REF.mkdir(parents=True, exist_ok=True); ART.mkdir(parents=True, exist_ok=True)
    spec = json.loads((ROOT / "campus_spec.json").read_text())
    badge_reference(); plan_reference(spec); plan_reference(spec, zoom=True)
    return spec


def fitted(c, path, x, y, width, height):
    """Fit complete native image; never crop or retouch delivered artwork."""
    with Image.open(path) as im:
        iw, ih = im.size
    factor = min(width / iw, height / ih)
    dw, dh = iw * factor, ih * factor
    c.drawImage(str(path), x + (width - dw) / 2, y + (height - dh) / 2,
                dw, dh, preserveAspectRatio=True, mask="auto")


def visual_pack():
    for name, _, _ in VIEWS:
        if not (ART / name).is_file():
            raise FileNotFoundError(ART / name)
    c = canvas.Canvas(str(PDF), pagesize=(W, H), pageCompression=1)
    c.setTitle("Grand-Chukuchuku | GBHS Kumba campus visual pack")
    c.setAuthor("Nkeh Nkengzincho / Grand-Chukuchuku development")
    chrome(c, "Grand-Chukuchuku / GBHS Kumba", 1)
    para(c, "GOVERNMENT BILINGUAL HIGH SCHOOL KUMBA", 36, H - 65, W - 72, 14, TEAL)
    fitted(c, ART / VIEWS[0][0], 36, 170, W - 72, 305)
    para(c, "Six generated location references: two aerials, two side views and two student-eye views. An overall plan, a main-cluster plan and a badge construction reference accompany them.", 36, 146, W - 72, 11)
    para(c, "Based on the author's recollections. Architecture, materials, terrain, footprints and camera positions are proposals for the animated series; these are not photographs of the real campus. Confirmed relationships and unresolved measurements are distinguished in the source notes.", 36, 96, W - 72, 9)
    c.showPage()
    for page, (stem, title) in enumerate([
        ("GBHS_Overall_Campus_Plan", "Overall campus / reported distances"),
        ("GBHS_Main_Cluster_Plan", "Main academic cluster / relationships"),
    ], 2):
        chrome(c, title, page)
        fitted(c, REF / (stem + ".png"), 25, 82, W - 50, H - 140)
        note = "The second 500 m span includes the labs and canteen near Form Five. In this proposed geometry, open ground beyond the canteen is 376 m. Exact measurement endpoints remain open." if page == 2 else "Form Three is confirmed as two storeys. Administration is opposite Form Five; labs are adjacent; the canteen is next to the labs. Footprints, court size and lab/admin/canteen heights are proposed."
        para(c, note, 36, 76, W - 72, 9)
        c.showPage()
    for page, (name, title, caption) in enumerate(VIEWS, 4):
        chrome(c, title, page)
        fitted(c, ART / name, 25, 120, W - 50, H - 184)
        para(c, caption, 36, 102, W - 72, 10)
        para(c, "Generated reference / proposed architecture and camera. Do not measure building lengths or walking distances from this image. Perspective and background details are not a production-locked 3D model.", 36, 67, W - 72, 8)
        c.showPage()
    chrome(c, "Daytime uniform / pocket and badge", 10)
    fitted(c, REF / "GBHS_Badge_Construction.png", 36, 85, 395, 430)
    y = H - 90
    for heading, content in [
        ("SUPPLIED CONTENT", "Circular badge: GBHS; Government Bilingual High School Kumba around the circle; lit candle in the centre."),
        ("PLACEMENT", "Pocket on the wearer's LEFT chest: viewer-right in a frontal image. Respect books/arms covering the pocket. No badge on shirt backs."),
        ("WARDROBE", "Sky-blue short-sleeved shirts; dark-blue trousers for boys and skirts for girls. Night revision at Professional School uses casual clothes, without school badges."),
        ("PROPOSED ARTWORK", "Colours, border, typeface and candle drawing are a construction proposal, not a verified reproduction of the official crest. The vector reference preserves exact wording; tiny generated embroidery is approximate."),
    ]:
        y = para(c, heading, 458, y, W - 494, 10, TEAL) - 8
        y = para(c, content, 458, y, W - 494, 9) - 23
    c.showPage()
    chrome(c, "Continuity / source limits", 11)
    y = H - 76
    for heading, content in [
        ("AUTHOR-CONFIRMED", "GBHS school name and reported 10.7 km compound distance. Forms One–Two: one storey. Form Three, Forms Four–Five and Lower/Upper Sixth: two storeys. Reported separations: 500 m, 10 m, 500 m. Administration opposite Form Five; Physics/Biology/Chemistry laboratories adjacent; canteen next to labs."),
        ("STORY BOUNDARY", "GBHS Sixth Form facilities belong in the campus design. Zino's own two high-school years remain at a separate remote boarding school. Professional School remains a separate vocational/night-revision location."),
        ("PROPOSED / STILL OPEN", "True bearings, gate and route, site boundary, footprints, classroom allocation, materials, topography and badge colours are not supplied. Distances are author-reported; measurement endpoints and the 10.7 km route basis/travel time remain open. Do not stage a short walk based only on the morning routine."),
        ("REVIEW AND NEXT USE", "The primary agent inspected the six delivered images and three revised badge-bearing character assets. A first compact aerial and a later overhead trial with extra roofs were excluded. The delivered second aerial is explicitly high-angle, not vertical. Review notes accompany this package; no independent final critic sign-off is claimed after worker usage limits. Use the plans for layout and the images as material/camera proposals."),
    ]:
        y = para(c, heading, 36, y, W - 72, 11, TEAL) - 8
        y = para(c, content, 36, y, W - 72, 10) - 24
    c.save()


def package():
    files = [PDF, ROOT / "README.md", ROOT / "campus_spec.json",
             ROOT / "GBHS_Kumba_Campus_Brief.md", ROOT / "build_campus_package.py",
             ROOT / "native_image_provenance.json", REVIEW]
    files += sorted(REF.glob("*.png")) + sorted(REF.glob("*.pdf"))
    files += [ART / name for name, _, _ in VIEWS]
    with zipfile.ZipFile(PACKAGE, "w", zipfile.ZIP_DEFLATED) as z:
        for file in files:
            arc = file.relative_to(ROOT) if file.is_relative_to(ROOT) else Path("review") / file.name
            z.write(file, str(arc))
    OUT.mkdir(parents=True, exist_ok=True)
    for file in (PDF, PACKAGE):
        shutil.copy2(file, OUT / file.name)
    print(f"Built {PDF.name} (11 pages) and {PACKAGE.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--references", action="store_true"); args = parser.parse_args()
    references()
    if not args.references:
        visual_pack()
        package()
