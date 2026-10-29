#!/usr/bin/env python3
"""Build the Artlist-ready music and sound storyboard for the Chapter One pilot."""

from __future__ import annotations

from pathlib import Path
import shutil
import zipfile

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle


ROOT = Path(__file__).resolve().parent
PILOT = ROOT.parent
SERIES = PILOT.parent
PROJECT = SERIES.parent
PDF = ROOT / "Grand-Chukuchuku_Chapter_01_Pilot_Artlist_Audio_Storyboard_v1.pdf"
PACKAGE = SERIES / "Grand-Chukuchuku_Chapter_01_Pilot_Artlist_Audio_Storyboard_v1.zip"
OUTPUT = PROJECT.parent / "output" / "grand-chukuchuku"
W, H = A4
M = 42
INK = colors.HexColor("#183C39")
MUTED = colors.HexColor("#586863")
GOLD = colors.HexColor("#BD8D42")
PAPER = colors.HexColor("#FAF8F2")
PALE = colors.HexColor("#E8EEE7")
LINE = colors.HexColor("#D2DAD2")
NAVY = colors.HexColor("#152E5B")
RUST = colors.HexColor("#B96037")
TEAL = colors.HexColor("#356F70")
SILENCE = colors.HexColor("#797671")


def fonts() -> None:
    root = Path("/usr/share/fonts/truetype/dejavu")
    for name, filename in [
        ("AudioSans", "DejaVuSans.ttf"),
        ("AudioSansB", "DejaVuSans-Bold.ttf"),
        ("AudioSerif", "DejaVuSerif.ttf"),
        ("AudioSerifB", "DejaVuSerif-Bold.ttf"),
    ]:
        pdfmetrics.registerFont(TTFont(name, str(root / filename)))
    pdfmetrics.registerFontFamily("AudioSans", normal="AudioSans", bold="AudioSansB")


STYLES = {
    "title": ParagraphStyle("a-title", fontName="AudioSerifB", fontSize=25, leading=30, textColor=INK),
    "h1": ParagraphStyle("a-h1", fontName="AudioSerifB", fontSize=19, leading=23, textColor=INK),
    "h2": ParagraphStyle("a-h2", fontName="AudioSansB", fontSize=10.2, leading=13.3, textColor=INK),
    "body": ParagraphStyle("a-body", fontName="AudioSans", fontSize=8.5, leading=11.7, textColor=INK),
    "small": ParagraphStyle("a-small", fontName="AudioSans", fontSize=7.7, leading=10.25, textColor=MUTED),
    "white": ParagraphStyle("a-white", fontName="AudioSans", fontSize=8.5, leading=11.7, textColor=colors.white),
    "quote": ParagraphStyle("a-quote", fontName="AudioSerif", fontSize=12.7, leading=17, textColor=INK),
}


CUES = [
    ("A", "Fiango bed", "instrumental afro fusion warm playful guitar hand percussion", "Warm compound pulse; 92–102 BPM feel, no lead vocal, dialogue-safe.", RUST),
    ("B", "Grand motif", "instrumental uplifting afro soul plucked guitar subtle chime cinematic", "Dignified gold lift; one short rising phrase, never heroic-action music.", GOLD),
    ("C", "Bottle stakes", "instrumental rhythmic afrobeat tension hand percussion minimal bass", "Dry rhythm and one build; must cut cleanly on a bottle hit.", NAVY),
    ("D", "Pressure / school", "instrumental minimal african ambient tense piano percussion", "Sparse and unresolved; supports chalk, paper and money pressure without horror.", TEAL),
    ("E", "End tag", "instrumental hopeful unresolved guitar marimba sparse", "A short tail in the Grand colour family; no musical resolution at 5:00.", SILENCE),
]

BOARDS = [
    ("01", "0:00–0:08", "THE BALL", "A1", "1.5 seconds naked compound ambience, then hand percussion under the ball thump.", "First kick is downbeat."),
    ("02", "0:08–0:21", "THE COMPOUND", "A1", "A1 low under dialogue; bucket rope and distant radio establish home.", "Keep Gideon/Luc clear."),
    ("03", "0:21–0:40", "THE MISS", "A1 → SFX", "Thin to one guitar pulse; kill music at basin impact and hold real sound.", "Basin splash transition."),
    ("04", "0:40–0:58", "THE FIRST LEGEND", "B1", "Grand’s gold lift plus one restrained chime as the ball bends.", "Hard cut into water."),
    ("05", "0:58–1:18", "BACK TO EARTH", "A2", "Soft guitar and rope rhythm return; Mother’s first line remains dry.", "Lower on correction."),
    ("06", "1:18–1:38", "WELL WATER", "A2", "Hand rhythm follows rope pull; avoid scoring the joke too broadly.", "Bucket fill completes bar."),
    ("07", "1:38–1:58", "THE PRICE", "D1", "Remove warmth. Room tone and a nearly inaudible pulse arrive after the notebook.", "No invented debt emphasis."),
    ("08", "1:58–2:16", "A SMALL PLAN", "D1", "Muted guitar harmonic; bottles sit far away in the sound field.", "Coin → school desk."),
    ("09", "2:16–2:38", "SCHOOL MORNING", "D2", "Chalk, bench scrape and two or three soft ticks only.", "Dialogue leads."),
    ("10", "2:38–3:00", "THE ANSWER", "D2", "Stop score for the correct answer; falling paper becomes rhythmic pickup.", "Paper → cloth."),
    ("11", "3:00–3:18", "THE OFFER", "C1", "Dry handclap/foot pattern starts with the target-bottle close-up.", "Ball rolls on beat one."),
    ("12", "3:18–3:37", "FIRST HIT", "C1", "Build modestly; cut one beat before glass clink. Crowd remains diegetic.", "Bottle fall is accent."),
    ("13", "3:37–3:58", "THE TEST", "C1 + B1", "Strip C1 to low pulse and feet. A near-inaudible Grand harmonic touches the gold edge.", "No fantasy rescue."),
    ("14", "3:58–4:16", "THE MISS / CALL", "SFX", "Stop C1 at the miss. Mother’s call travels through empty space.", "Call bridges home."),
    ("15", "4:16–4:34", "THE NOTICE", "SFX", "Run, ball, door, papers, radio from a neighbour. No score.", "Doorway absorbs street."),
    ("16", "4:34–4:48", "THE QUESTION", "SFX", "Breath, paper edge and bucket fill only. No sad cue.", "Silence starts early."),
    ("17", "4:48–5:00", "COINS / TITLE", "E1 + B2", "E1 begins on open palm; one Grand fragment rises and stays unresolved.", "Hard cut at 5:00."),
]


def page(c: canvas.Canvas, number: int, total: int, label: str) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(LINE)
    c.line(M, H - 39, W - M, H - 39)
    c.line(M, 42, W - M, 42)
    c.setFillColor(MUTED)
    c.setFont("AudioSansB", 7.3)
    c.drawString(M, H - 29, "GRAND-CHUKUCHUKU")
    c.setFont("AudioSans", 7.1)
    c.drawRightString(W - M, H - 29, label.upper())
    c.drawString(M, 29, "ARTLIST SEARCH + EDIT HANDOFF · 29 OCTOBER 2026")
    c.setFont("AudioSansB", 7.5)
    c.drawRightString(W - M, 29, f"{number:02d} / {total:02d}")


def para(c: canvas.Canvas, text: str, style: str, x: float, top: float, width: float) -> float:
    item = Paragraph(text, STYLES[style])
    _, height = item.wrap(width, H)
    item.drawOn(c, x, top-height)
    return top-height


def label(c: canvas.Canvas, text: str, x: float, top: float, colour=GOLD) -> float:
    c.setFillColor(colour)
    c.setFont("AudioSansB", 7.5)
    c.drawString(x, top, text.upper())
    return top - 16


def fit_image(c: canvas.Canvas, image: Path, x: float, y: float, width: float, height: float) -> None:
    with PILImage.open(image) as img:
        iw, ih = img.size
    scale = min(width / iw, height / ih)
    dw, dh = iw * scale, ih * scale
    c.setFillColor(colors.white)
    c.roundRect(x, y, width, height, 8, fill=1, stroke=0)
    c.drawImage(str(image), x+(width-dw)/2, y+(height-dh)/2, width=dw, height=dh, mask="auto")
    c.setStrokeColor(LINE)
    c.roundRect(x, y, width, height, 8, fill=0, stroke=1)


def cover(c: canvas.Canvas) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    fit_image(c, PILOT / "images" / "01_Grand_Bends_the_Ball.png", 94, 131, W-188, H-220)
    c.setFillColor(colors.Color(.05, .11, .11, alpha=.78))
    c.roundRect(50, 52, W-100, 190, 10, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#F9F2E4"))
    c.setFont("AudioSansB", 8.7)
    c.drawString(72, 211, "5-MINUTE PILOT · MUSIC & SOUND STORYBOARD")
    c.setFont("AudioSerifB", 26)
    c.drawString(72, 166, "THE COURTYARD")
    c.drawString(72, 129, "KEEPS SCORE")
    c.setFont("AudioSans", 10)
    c.drawString(72, 97, "Artlist search briefs, cue map and edit handoff")
    c.setFillColor(GOLD)
    c.rect(72, 222, 76, 4, fill=1, stroke=0)
    c.showPage()


def music_identity(c: canvas.Canvas) -> None:
    page(c, 2, 7, "Music identity")
    y = H - 75
    y = para(c, "The sound of Fiango", "h1", M, y, W-2*M) - 8
    y = para(c, "Start with life before score: well rope, a radio through compound walls, football on packed earth, cooking and evening insects. Music is Zino’s emotional storytelling, not a generic background label.", "body", M, y, W-2*M) - 17
    y = label(c, "MUSIC GRAMMAR", M, y)
    blocks = [
        ("FIANGO BED", "Warm, percussive, guitar-led instrumental Afro-fusion/highlife-leaning groove. It leaves space for Pidgin and English dialogue."),
        ("GRAND MOTIF", "Muted plucked guitar or clean strings, one small bell/chime and a controlled upward phrase. Elegant, human and brief."),
        ("MONEY PRESSURE", "Remove melody and low end. Let notebook paper, rope, radio distance and silence do the work."),
        ("NACKING BOTTLE", "Dry foot percussion, handclaps and one low pulse. The glass strike is the story accent."),
        ("FEE NOTICE", "No music under Mother’s last lines. The unresolved motif returns only after coins open in Zino’s palm."),
    ]
    for title, body in blocks:
        c.setFillColor(PALE)
        c.roundRect(M, y-56, W-2*M, 48, 6, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.setFont("AudioSansB", 8)
        c.drawString(M+12, y-22, title)
        para(c, body, "small", M+12, y-28, W-2*M-24)
        y -= 63
    y -= 5
    y = label(c, "CONNECTION STATUS", M, y)
    para(c, "Your Artlist account may be connected in ChatGPT, but no callable Artlist connector or account-authentication route is exposed to this workspace. Use this as a ready-to-audition handoff when the account is open; do not call a track licensed until the account holder confirms its record and intended social usage.", "quote", M, y, W-2*M)
    c.showPage()


def master_map(c: canvas.Canvas) -> None:
    page(c, 3, 7, "Master cue map")
    y = H - 75
    y = para(c, "Five minutes, one musical arc", "h1", M, y, W-2*M) - 9
    y = para(c, "The score moves from Fiango warmth to private calculation, then stops so Mother’s words can land. Grand’s motif is a promise, never a solution.", "subtitle" if "subtitle" in STYLES else "body", M, y, W-2*M) - 16
    segments = [
        (0, 40, RUST, "A1 · COMPOUND"), (40, 58, GOLD, "B1 · GRAND"), (58, 98, RUST, "A2 · HOME"),
        (98, 180, TEAL, "D1/D2 · PRESSURE"), (180, 256, NAVY, "C1 · BOTTLE"), (256, 288, SILENCE, "SFX ONLY"), (288, 300, GOLD, "E1/B2 · TAG"),
    ]
    x0, bar_y, bar_w, bar_h = M, y-38, W-2*M, 46
    for start, end, colour, title in segments:
        x = x0 + bar_w*start/300
        width = bar_w*(end-start)/300
        c.setFillColor(colour)
        c.roundRect(x, bar_y, width, bar_h, 5, fill=1, stroke=0)
        if width > 55:
            c.setFillColor(colors.white)
            c.setFont("AudioSansB", 6.4)
            c.drawCentredString(x+width/2, bar_y+19, title)
    c.setFillColor(MUTED)
    c.setFont("AudioSans", 7)
    for second, text in [(0,"0:00"),(60,"1:00"),(120,"2:00"),(180,"3:00"),(240,"4:00"),(300,"5:00")]:
        x = x0 + bar_w*second/300
        c.drawCentredString(x, bar_y-13, text)
    y = bar_y - 41
    rows = [
        ["TIME", "CUE", "STORY FUNCTION", "EDIT ACTION"],
        ["0:00–0:40", "A1", "Fiango, friendship and Zino’s humour", "Start under real sound; silence at basin."],
        ["0:40–0:58", "B1", "Grand-Chukuchuku arrives", "One gold-lift phrase; hard cut to water."],
        ["0:58–1:38", "A2", "Home, work and friendship", "Rope rhythm folds into groove."],
        ["1:38–3:00", "D1/D2", "Rent, lunch money, hunger and school", "Sparse texture; dialogue leads."],
        ["3:00–4:16", "C1", "Nacking Bottle stakes", "Build to hit; stop at Zino’s miss."],
        ["4:16–4:48", "SFX", "School-fee notice", "No score: door, paper, breath, water."],
        ["4:48–5:00", "E1/B2", "Coins become the question", "Return fragment; cut before resolution."],
    ]
    parsed = [[Paragraph(cell, STYLES["small"] if r else STYLES["h2"]) for cell in row] for r,row in enumerate(rows)]
    table = Table(parsed, colWidths=[72,50,164,185])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PALE), ("GRID", (0,0), (-1,-1), .35, LINE),
        ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    _, height = table.wrap(W-2*M, 500)
    table.drawOn(c, M, y-height)
    c.showPage()


def board_page(c: canvas.Canvas, number: int, rows) -> None:
    page(c, number, 7, "17-board audio timeline")
    y = H - 75
    y = para(c, "Board-by-board sound edit", "h1", M, y, W-2*M) - 8
    y = para(c, "The visual pilot board remains the framing authority. These instructions tell the editor where music must yield to football, dialogue, silence and Mother’s final question.", "body", M, y, W-2*M) - 13
    for board, timing, beat, cue, instruction, cut in rows:
        h = 91
        c.setFillColor(colors.white)
        c.roundRect(M, y-h, W-2*M, h, 7, fill=1, stroke=0)
        c.setStrokeColor(LINE)
        c.roundRect(M, y-h, W-2*M, h, 7, fill=0, stroke=1)
        c.setFillColor(GOLD if cue not in {"SFX"} else SILENCE)
        c.roundRect(M+11, y-h+12, 52, h-24, 5, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("AudioSansB", 8)
        c.drawCentredString(M+37, y-h+50, f"{board}")
        c.setFont("AudioSans", 6.6)
        c.drawCentredString(M+37, y-h+38, timing)
        x = M+78
        c.setFillColor(INK)
        c.setFont("AudioSansB", 9.4)
        c.drawString(x, y-22, beat)
        c.setFillColor(MUTED)
        c.setFont("AudioSansB", 7)
        c.drawString(x, y-37, f"CUE  {cue}")
        para(c, instruction, "small", x+70, y-30, W-M-(x+70)-10)
        c.setFillColor(GOLD)
        c.setFont("AudioSansB", 7)
        c.drawString(x, y-66, "EDIT POINT")
        para(c, cut, "small", x+70, y-59, W-M-(x+70)-10)
        y -= 102
    c.showPage()


def artlist_search(c: canvas.Canvas) -> None:
    page(c, 7, 7, "Artlist search handoff")
    y = H - 75
    y = para(c, "Artlist audition plan", "h1", M, y, W-2*M) - 8
    y = para(c, "Search three candidates for each cue. Pick a coherent sound family instead of five unrelated songs. The queries below are editable language, not track titles or catalog claims.", "body", M, y, W-2*M) - 15
    for key, name, query, test, colour in CUES:
        c.setFillColor(PALE)
        c.roundRect(M, y-78, W-2*M, 69, 7, fill=1, stroke=0)
        c.setFillColor(colour)
        c.roundRect(M+12, y-61, 32, 32, 6, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("AudioSansB", 13)
        c.drawCentredString(M+28, y-50, key)
        c.setFillColor(INK)
        c.setFont("AudioSansB", 9)
        c.drawString(M+58, y-27, name.upper())
        para(c, "<b>SEARCH:</b> " + query, "small", M+58, y-33, W-2*M-70)
        para(c, test, "small", M+58, y-54, W-2*M-70)
        y -= 87
    y -= 3
    y = label(c, "DELIVERY CHECKLIST", M, y)
    checklist = [
        "Download full mix; choose a loopable section or short cut only where the catalog offers one.",
        "Where available, keep percussion and bass stems for dialogue-safe editorial control.",
        "Record exact track title, artist, version, licence date and intended social use beside the final master.",
        "Record dialogue first. Build cue lengths around performance; never force Pidgin cadence to a chosen song.",
        "Export a 5:00 master and 15-second / 60-second cutdowns that preserve the B1/E1 motif.",
    ]
    for item in checklist:
        y = para(c, "• " + item, "body", M, y, W-2*M) - 5
    c.showPage()


def build_pdf() -> None:
    fonts()
    c = canvas.Canvas(str(PDF), pagesize=A4, pageCompression=1)
    c.setTitle("Grand-Chukuchuku | Pilot Artlist Audio Storyboard")
    c.setAuthor("Based on the life of Nkeh Nkengzincho (Zino)")
    cover(c)
    music_identity(c)
    master_map(c)
    board_page(c, 4, BOARDS[:6])
    board_page(c, 5, BOARDS[6:12])
    board_page(c, 6, BOARDS[12:])
    artlist_search(c)
    c.save()


def package() -> None:
    files = [PDF, ROOT / "Grand-Chukuchuku_Chapter_01_Pilot_Artlist_Audio_Storyboard_v1.md", ROOT / "README.md", ROOT / "build_artlist_audio_storyboard.py"]
    with zipfile.ZipFile(PACKAGE, "w", zipfile.ZIP_DEFLATED) as z:
        for file in files:
            z.write(file, file.name)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PDF, OUTPUT / PDF.name)
    shutil.copy2(PACKAGE, OUTPUT / PACKAGE.name)


def main() -> None:
    build_pdf()
    package()
    print(PDF)
    print(PACKAGE)


if __name__ == "__main__":
    main()
