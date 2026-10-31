#!/usr/bin/env python3
"""Package native-generated character turnarounds without modifying the images."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import zipfile

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parent
SERIES = ROOT.parents[1]
OUTPUT = SERIES.parent.parent / "output" / "grand-chukuchuku"
PDF = ROOT / "Grand-Chukuchuku_Five_Character_Turnarounds_v1.pdf"
PACKAGE = SERIES / "Grand-Chukuchuku_Five_Character_Turnarounds_v1.zip"
REVIEW = SERIES / "writers-room" / "NIGHT_WARDROBE_AND_TURNAROUNDS_REVIEW_2026-10-30.md"
DISTANCE_REVIEW = SERIES / "writers-room" / "LIZZY_MIRABEL_DISTANCE_REVIEW_2026-10-30.md"
COMPARISON = ROOT / "Grand-Chukuchuku_Lizzy_Mirabel_Design_Comparison.pdf"
UNIFORM_ROOT = ROOT / "school-uniforms"
UNIFORM_PDF = UNIFORM_ROOT / "Grand-Chukuchuku_Mirabel_Lizzy_Uniform_Turnarounds.pdf"
UNIFORM_COMPARISON = UNIFORM_ROOT / "Grand-Chukuchuku_Uniform_Comparison.pdf"
UNIFORM_PACKAGE = SERIES / "Grand-Chukuchuku_School_Uniform_Characters_v1.zip"
UNIFORM_REVIEW = SERIES / "writers-room" / "COMPLEXION_AND_UNIFORM_REVIEW_2026-10-31.md"
GBHS_REVIEW = SERIES / "writers-room" / "GBHS_KUMBA_CAMPUS_REVIEW_2026-10-31.md"
GBHS_BADGE = SERIES / "school-campus" / "references" / "GBHS_Badge_Construction.pdf"
W, H = landscape(A4)
PAPER = colors.HexColor("#FAF8F2")
INK = colors.HexColor("#183C39")
MUTED = colors.HexColor("#586863")
LINE = colors.HexColor("#D2DAD2")

CAST = [
    {
        "name": "Zino", "filename": "01_Zino_Turnaround.png",
        "author_traits": "Handsome; clean fades. Gifted, witty and quick-footed.",
        "design": "Crisp low fade with a curly top; slim athletic teenage silhouette. Proposed night outfit: burgundy T-shirt, charcoal casual trousers and dark sneakers.",
    },
    {
        "name": "Luc", "filename": "02_Luc_Turnaround.png",
        "author_traits": "Muscular build, big hands, big ears and high flat-top. Homemade evening weights; small Bible.",
        "design": "Strong adolescent shoulders and larger hands/ears. Proposed night outfit: mustard T-shirt, loose navy casual trousers and dark sneakers. Training onset remains open.",
    },
    {
        "name": "Gideon / Giddy", "filename": "03_Gideon_Turnaround.png",
        "author_traits": "Large head and nose, small front-tooth gap, W-shaped hairline and fuller almost-afro hair.",
        "design": "The front view's small smile reveals the gap. Proposed night outfit: forest-green polo, dark-brown casual trousers and worn sneakers. Camera bag remains his scene prop.",
    },
    {
        "name": "Mirabel", "filename": "04_Mirabel_Turnaround.png",
        "author_traits": "Black Cameroonian girl; low-cut natural hair, slim build and darker complexion than Lizzy. Zino's maths friend from Form Three.",
        "design": "Proposed angular oval face, straight brows, precise low-crop texture, teal/cream top, charcoal straight trousers and dark flats. Slim vertical outline; not Elianne.",
    },
    {
        "name": "Lizzy", "filename": "05_Lizzy_Turnaround.png",
        "author_traits": "Black Cameroonian girl with low-cut natural hair, pretty face and lighter complexion than Mirabel; Zino's school girlfriend.",
        "design": "Proposed rounder face, arched brows, short natural crop, loose rose top, full mustard A-line skirt and cream flats. Rounded face and triangular garment outline; natural school-age proportions.",
    },
]


def text(c: canvas.Canvas, value: str, x: float, top: float, width: float, size: float = 8.5) -> float:
    p = Paragraph(value, ParagraphStyle("turnaround", fontName="TurnBody", fontSize=size, leading=size * 1.38, textColor=MUTED))
    _, height = p.wrap(width, H)
    p.drawOn(c, x, top - height)
    return top - height


def build() -> None:
    font_dir = Path("/usr/share/fonts/truetype/dejavu")
    pdfmetrics.registerFont(TTFont("TurnBody", str(font_dir / "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("TurnBold", str(font_dir / "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFontFamily("TurnBody", normal="TurnBody", bold="TurnBold")
    for item in CAST:
        path = ROOT / item["filename"]
        if not path.is_file() or path.stat().st_size < 1000:
            raise FileNotFoundError(path)
        with Image.open(path) as im:
            im.verify()
    c = canvas.Canvas(str(PDF), pagesize=(W, H), pageCompression=1)
    c.setTitle("Grand-Chukuchuku | Five Character Turnarounds v1")
    c.setAuthor("Based on the life and character recollections of Nkeh Nkengzincho")
    for index, item in enumerate(CAST, 1):
        c.setFillColor(PAPER)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("TurnBold", 8)
        c.drawString(36, H - 28, "GRAND-CHUKUCHUKU / CHARACTER TURNAROUNDS")
        c.setFont("TurnBold", 21)
        c.drawString(36, H - 60, item["name"])
        text(c, "FRONT / LEFT SIDE / BACK · Proposed later-secondary model, approximately 14–15 · Casual clothes", 36, H - 73, W - 72, 8.3)
        path = ROOT / item["filename"]
        with Image.open(path) as im:
            iw, ih = im.size
        max_w, max_h = W - 72, H - 188
        scale = min(max_w / iw, max_h / ih)
        dw, dh = iw * scale, ih * scale
        c.drawImage(str(path), (W - dw) / 2, 98 + (max_h - dh) / 2, width=dw, height=dh, mask="auto")
        y = text(c, "<b>Author-supplied:</b> " + item["author_traits"], 36, 88, W - 72)
        y = text(c, "<b>Design proposal:</b> " + item["design"], 36, y - 4, W - 72)
        if y < 34:
            raise ValueError(f"Character notes overflow: {item['name']}")
        c.setStrokeColor(LINE)
        c.line(36, 28, W - 36, 28)
        c.setFillColor(MUTED)
        c.setFont("TurnBody", 7)
        c.drawString(36, 16, "31 OCTOBER 2026 · Model proposals, not verified likenesses or age-ten/adult turnarounds")
        c.drawRightString(W - 36, 16, f"{index:02d} / {len(CAST):02d}")
        c.showPage()
    c.save()
    manifest = {
        "title": "Grand-Chukuchuku — five-character turnaround set v1",
        "date": "2026-10-31", "author": "Nkeh Nkengzincho (Zino)",
        "age_scope": "Proposed later-secondary models, approximately 14–15; exact ages and training onset open",
        "views": ["front", "left side", "back"],
        "source": "Author-supplied traits with proposed animation faces, clothes and age variants; native-generated images",
        "wardrobe_rule": "Daytime school uniform is sky-blue/navy. Professional School night readers wear house/casual clothes; some dress to impress. No students wear uniforms at night.",
        "spelling": {"Giddeon": "Gideon", "Mirable": "Mirabel"},
        "characters": CAST,
        "complexion_rule": "Mirabel is darker than Lizzy; exact illustrated shades are proposals. Preserve the contrast in casual and uniform models.",
        "uniform_models": ["school-uniforms/04_Mirabel_Uniform_Turnaround.png", "school-uniforms/05_Lizzy_Uniform_Turnaround.png"],
        "school_and_badge": "GBHS: Government Bilingual High School Kumba. Wearer's left-chest pocket, circular school-name/GBHS/lit-candle badge. Placement/content supplied; badge colours/typeface/art proposed. No back badge or badge on night casual clothes.",
        "body_revision_status": "Lizzy body-size edit was declined by image safety and was not retried. Her accepted casual PNG remains unchanged; uniform model changes clothes, retaining current proportions.",
    }
    for item in manifest["characters"]:
        with Image.open(ROOT / item["filename"]) as im:
            item["pixels"] = list(im.size)
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


def package() -> None:
    files = [PDF, ROOT / "manifest.json", ROOT / "README.md", Path(__file__)]
    files += [ROOT / item["filename"] for item in CAST]
    if not REVIEW.exists():
        raise FileNotFoundError(REVIEW)
    files += [REVIEW, DISTANCE_REVIEW, COMPARISON, UNIFORM_REVIEW, GBHS_REVIEW, GBHS_BADGE]
    files += sorted(p for p in UNIFORM_ROOT.iterdir() if p.suffix in {".png", ".pdf", ".md", ".json"})
    with zipfile.ZipFile(PACKAGE, "w", zipfile.ZIP_DEFLATED) as z:
        for path in files:
            arc = Path("school-uniforms") / path.name if path.parent == UNIFORM_ROOT else Path(path.name)
            z.write(path, arc)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for path in [PDF, PACKAGE]:
        shutil.copy2(path, OUTPUT / path.name)


def comparison(uniform: bool = False) -> None:
    """Show the native front views at two display sizes using PDF clipping only."""
    target = UNIFORM_COMPARISON if uniform else COMPARISON
    image_root = UNIFORM_ROOT if uniform else ROOT
    c = canvas.Canvas(str(target), pagesize=(W, H), pageCompression=1)
    c.setTitle("Grand-Chukuchuku | Mirabel and Lizzy — distance comparison")
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("TurnBold", 20)
    c.drawString(36, H - 35, "Mirabel and Lizzy: same school uniform" if uniform else "Mirabel and Lizzy: low-cut character designs")
    text(c, "Both have low-cut natural hair. Mirabel's darker complexion and angular face contrast with Lizzy's warmer, lighter complexion and rounder face." + (" The uniform colours match." if uniform else " The casual garments are different."), 36, H - 48, W - 72, 8.5)
    # Identical source windows preserve proportions and a common baseline.
    # Original PNG files are never cropped, retouched or resampled here.
    def front(filename: str, x: float, y: float, height: float) -> None:
        left, top, right, bottom = 145, 45, 535, 970
        scale = height / (bottom - top)
        width = (right - left) * scale
        with Image.open(image_root / filename) as im:
            iw, ih = im.size
        c.saveState()
        clip = c.beginPath()
        clip.rect(x, y, width, height)
        c.clipPath(clip, stroke=0, fill=0)
        c.drawImage(str(image_root / filename), x - left * scale, y - (ih - bottom) * scale, width=iw * scale, height=ih * scale)
        c.restoreState()
    names = ["04_Mirabel_Uniform_Turnaround.png", "05_Lizzy_Uniform_Turnaround.png"] if uniform else ["04_Mirabel_Turnaround.png", "05_Lizzy_Turnaround.png"]
    for x, name, filename in [(95, "MIRABEL", names[0]), (330, "LIZZY", names[1])]:
        c.setFillColor(INK)
        c.setFont("TurnBold", 10)
        c.drawString(x, H - 90, name)
        front(filename, x, 116, 380)
    x = 585
    c.setFont("TurnBold", 9)
    c.drawString(x, H - 90, "SMALL-SCREEN CHECK")
    front(names[0], x + 10, 325, 105)
    front(names[1], x + 92, 325, 105)
    notes = "<b>Mirabel</b><br/>Deeper dark-brown complexion; slim silhouette; longer angular oval face and straighter brows.<br/><br/><b>Lizzy</b><br/>Warmer, lighter brown complexion; rounder face and current broader overall silhouette. Body proportions were not newly enlarged."
    text(c, notes, x, 295, W - x - 36, 9)
    text(c, "Low-cut hair, relative complexion and the sky-blue shirt/dark-blue skirt are author-supplied. Exact shades, faces and garment fit are proposals. Both remain ordinary school-age models in neutral poses.", 36, 85, W - 72, 8.5)
    c.setStrokeColor(LINE)
    c.line(36, 28, W - 36, 28)
    c.setFillColor(MUTED)
    c.setFont("TurnBody", 7)
    c.drawString(36, 16, "31 OCTOBER 2026 · Two character models · Native sheets preserved in full")
    c.save()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(target, OUTPUT / target.name)


def uniform_models() -> None:
    """Export the two native three-view uniform sheets without pixel editing."""
    c = canvas.Canvas(str(UNIFORM_PDF), pagesize=(W, H), pageCompression=1)
    c.setTitle("Grand-Chukuchuku | Mirabel and Lizzy — school uniform turnarounds")
    for index, (name, filename, cue) in enumerate([
        ("Mirabel", "04_Mirabel_Uniform_Turnaround.png", "Darker complexion; slim silhouette and proposed angular oval face/straighter brows."),
        ("Lizzy", "05_Lizzy_Uniform_Turnaround.png", "Lighter warm-brown complexion; proposed rounder face/arched brows and current natural proportions."),
    ], 1):
        path = UNIFORM_ROOT / filename
        with Image.open(path) as im:
            iw, ih = im.size
        c.setFillColor(PAPER); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont("TurnBold", 21)
        c.drawString(36, H - 40, name + " — daytime school uniform")
        text(c, "FRONT / SIDE / BACK · GBHS Kumba · Low-cut hair · Sky-blue shirt / navy skirt · Left-chest pocket and badge", 36, H - 54, W - 72)
        scale = min((W - 72) / iw, (H - 160) / ih)
        dw, dh = iw * scale, ih * scale
        c.drawImage(str(path), (W - dw) / 2, 82 + ((H - 160) - dh) / 2, width=dw, height=dh, mask="auto")
        text(c, cue + " Badge content/left-pocket placement supplied; crest artwork/colours, exact shades, face, fit and shoes proposed.", 36, 72, W - 72)
        c.setFillColor(MUTED); c.setFont("TurnBody", 7)
        c.drawString(36, 16, "31 OCTOBER 2026 · Proposed later-secondary model, approximately 14–15 · Neutral pose")
        c.drawRightString(W - 36, 16, f"{index:02d} / 02")
        c.showPage()
    c.save()
    shutil.copy2(UNIFORM_PDF, OUTPUT / UNIFORM_PDF.name)


def uniform_package() -> None:
    files = sorted(p for p in UNIFORM_ROOT.iterdir() if p.suffix in {".png", ".pdf", ".md", ".json"}) + [UNIFORM_REVIEW, GBHS_REVIEW, GBHS_BADGE]
    with zipfile.ZipFile(UNIFORM_PACKAGE, "w", zipfile.ZIP_DEFLATED) as z:
        for path in files:
            z.write(path, path.name)
    shutil.copy2(UNIFORM_PACKAGE, OUTPUT / UNIFORM_PACKAGE.name)


if __name__ == "__main__":
    build()
    comparison()
    uniform_models()
    comparison(uniform=True)
    package()
    uniform_package()
    print(PDF)
    print(PACKAGE)
