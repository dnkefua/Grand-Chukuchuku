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
        "author_traits": "Beautiful, slim build; friendship with Zino begins through maths in Form Three.",
        "design": "Proposed oval face, low braided bun, loose teal knee-length dress and flat shoes. Her face and hair are a new animation proposal; she is not Elianne.",
    },
    {
        "name": "Lizzy", "filename": "05_Lizzy_Turnaround.png",
        "author_traits": "Pretty face; Form One crush, girlfriend from Form Two, breakup in Form Three.",
        "design": "Natural school-age proportions and neutral stance. Proposed cornrows into a low puff, loose dusty-rose blouse, relaxed navy knee-length skirt and flat shoes. Distinct from Mirabel and Elianne.",
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
        c.drawString(36, 16, "30 OCTOBER 2026 · Model proposals, not verified likenesses or age-ten/adult turnarounds")
        c.drawRightString(W - 36, 16, f"{index:02d} / {len(CAST):02d}")
        c.showPage()
    c.save()
    manifest = {
        "title": "Grand-Chukuchuku — five-character turnaround set v1",
        "date": "2026-10-30", "author": "Nkeh Nkengzincho (Zino)",
        "age_scope": "Proposed later-secondary models, approximately 14–15; exact ages and training onset open",
        "views": ["front", "left side", "back"],
        "source": "Author-supplied traits with proposed animation faces, clothes and age variants; native-generated images",
        "wardrobe_rule": "Daytime school uniform is sky-blue/navy. Professional School night readers wear house/casual clothes; some dress to impress. No students wear uniforms at night.",
        "spelling": {"Giddeon": "Gideon", "Mirable": "Mirabel"},
        "characters": CAST,
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
    files += [REVIEW]
    with zipfile.ZipFile(PACKAGE, "w", zipfile.ZIP_DEFLATED) as z:
        for path in files:
            z.write(path, path.name)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for path in [PDF, PACKAGE]:
        shutil.copy2(path, OUTPUT / path.name)


if __name__ == "__main__":
    build()
    package()
    print(PDF)
    print(PACKAGE)
