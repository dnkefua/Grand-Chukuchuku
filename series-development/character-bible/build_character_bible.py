#!/usr/bin/env python3
"""Build the Grand-Chukuchuku character bible and download package."""

from __future__ import annotations

from pathlib import Path
import shutil
import zipfile

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parent
SERIES = ROOT.parent
PROJECT = SERIES.parent
PDF = ROOT / "Grand-Chukuchuku_Character_Bible_v2.pdf"
PACKAGE = SERIES / "Grand-Chukuchuku_Character_Bible_v2.zip"
OUTPUT = PROJECT.parent / "output" / "grand-chukuchuku"
W, H = A4
M = 42
INK = colors.HexColor("#183C39")
MUTED = colors.HexColor("#586863")
GOLD = colors.HexColor("#BD8D42")
PAPER = colors.HexColor("#FAF8F2")
PALE = colors.HexColor("#E8EEE7")
LINE = colors.HexColor("#D2DAD2")


def fonts() -> None:
    root = Path("/usr/share/fonts/truetype/dejavu")
    for name, filename in [
        ("CastSans", "DejaVuSans.ttf"),
        ("CastSansB", "DejaVuSans-Bold.ttf"),
        ("CastSerif", "DejaVuSerif.ttf"),
        ("CastSerifB", "DejaVuSerif-Bold.ttf"),
    ]:
        pdfmetrics.registerFont(TTFont(name, str(root / filename)))
    pdfmetrics.registerFontFamily("CastSans", normal="CastSans", bold="CastSansB")


STYLES = {
    "title": ParagraphStyle("cast-title", fontName="CastSerifB", fontSize=25, leading=30, textColor=INK),
    "subtitle": ParagraphStyle("cast-subtitle", fontName="CastSans", fontSize=10.2, leading=14.5, textColor=MUTED),
    "h1": ParagraphStyle("cast-h1", fontName="CastSerifB", fontSize=19, leading=23, textColor=INK),
    "h2": ParagraphStyle("cast-h2", fontName="CastSansB", fontSize=10.4, leading=13.4, textColor=INK),
    "body": ParagraphStyle("cast-body", fontName="CastSans", fontSize=8.65, leading=12, textColor=INK),
    "small": ParagraphStyle("cast-small", fontName="CastSans", fontSize=7.8, leading=10.4, textColor=MUTED),
    "quote": ParagraphStyle("cast-quote", fontName="CastSerif", fontSize=12.5, leading=17, textColor=INK),
}


def image(key: str) -> Path:
    return ROOT / "images" / {
        "zino": "01_Zino_and_Grand.png",
        "friends": "02_Friends_and_Elianne.png",
        "family": "03_Family.png",
        "adults": "04_School_and_Compound_Adults.png",
    }[key]


def page(c: canvas.Canvas, number: int, total: int, label: str) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(LINE)
    c.line(M, H - 39, W - M, H - 39)
    c.line(M, 42, W - M, 42)
    c.setFillColor(MUTED)
    c.setFont("CastSansB", 7.3)
    c.drawString(M, H - 29, "GRAND-CHUKUCHUKU")
    c.setFont("CastSans", 7.1)
    c.drawRightString(W - M, H - 29, label.upper())
    c.drawString(M, 29, "AUTHOR-BASED CHARACTER DEVELOPMENT · UPDATED 31 OCTOBER 2026")
    c.setFont("CastSansB", 7.5)
    c.drawRightString(W - M, 29, f"CORE {number:02d} / {total:02d}")


def para(c: canvas.Canvas, text: str, style: str, x: float, top: float, width: float) -> float:
    obj = Paragraph(text, STYLES[style])
    _, height = obj.wrap(width, H)
    obj.drawOn(c, x, top - height)
    return top - height


def fit_image(c: canvas.Canvas, source: Path, x: float, y: float, width: float, height: float) -> None:
    with PILImage.open(source) as im:
        iw, ih = im.size
    scale = min(width / iw, height / ih)
    dw, dh = iw * scale, ih * scale
    c.setFillColor(colors.white)
    c.roundRect(x, y, width, height, 7, fill=1, stroke=0)
    c.drawImage(str(source), x + (width - dw) / 2, y + (height - dh) / 2, width=dw, height=dh, mask="auto")
    c.setStrokeColor(LINE)
    c.roundRect(x, y, width, height, 7, fill=0, stroke=1)


def label(c: canvas.Canvas, text: str, x: float, top: float) -> float:
    c.setFillColor(GOLD)
    c.setFont("CastSansB", 7.4)
    c.drawString(x, top, text.upper())
    return top - 17


def card(c: canvas.Canvas, x: float, top: float, width: float, heading: str, role: str, body: str, distinct: str, hold: str | None = None) -> float:
    y = top
    y = label(c, "CHARACTER", x, y)
    y = para(c, heading, "h2", x, y, width) - 4
    y = para(c, role, "small", x, y, width) - 8
    y = label(c, "ON SCREEN", x, y)
    y = para(c, body, "body", x, y, width) - 8
    y = label(c, "DISTINCT SIGNALS", x, y)
    y = para(c, distinct, "body", x, y, width) - 8
    if hold:
        y = label(c, "CONTINUITY HOLD", x, y)
        y = para(c, hold, "small", x, y, width) - 8
    return y


def cover(c: canvas.Canvas) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    fit_image(c, image("zino"), 59, 132, W - 118, H - 235)
    c.setFillColor(colors.Color(.05, .11, .11, alpha=.75))
    c.roundRect(50, 52, W - 100, 173, 10, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#F9F2E4"))
    c.setFont("CastSansB", 8.8)
    c.drawString(72, 196, "AN AUTOBIOGRAPHICAL ANIMATED THRILLER")
    c.setFont("CastSerifB", 30)
    c.drawString(72, 151, "CHARACTER BIBLE")
    c.setFont("CastSans", 10)
    c.drawString(72, 119, "Fiango core cast and protected future-cast guide")
    c.setFillColor(GOLD)
    c.rect(72, 207, 74, 4, fill=1, stroke=0)
    c.showPage()


def cast_system(c: canvas.Canvas) -> None:
    page(c, 2, 8, "Cast system")
    y = H - 75
    y = para(c, "Character system", "h1", M, y, W - 2*M) - 8
    y = para(c, "Every visual difference must reveal how a person acts under pressure. These images are character-development composites, not literal portraits.", "subtitle", M, y, W - 2*M) - 15
    items = [
        ("ZINO", "Handsome, clean fade and quick movement; turns loss into a story."),
        ("GRAND", "Stillness, clean navy and gold; the imagined answer to every impossible problem."),
        ("GIDEON", "Big head/nose, small tooth gap, W hairline and camera bag; always finding a gig."),
        ("LUC", "High flat-top, big ears/hands, trained shoulders and Bible; evening weights, public faith."),
        ("MOTHER", "Teacher’s papers, practical shoes and upright control; care expressed through action."),
        ("UNCLE", "Lawyer-era suits, faith and bulk cocoa trade; family pride with unresolved limits."),
        ("MISS MUKETE", "Glass, chalk and blue/white precision; academic attention with standards."),
        ("LANDLORD", "Keys and ledger; money pressure present without turning him into a villain."),
    ]
    col_x = [M, M + 253]
    top = y
    for index, (name, text) in enumerate(items):
        x = col_x[index % 2]
        if index and index % 2 == 0:
            top -= 69
        c.setFillColor(PALE)
        c.roundRect(x, top - 53, 237, 53, 6, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.setFont("CastSansB", 8)
        c.drawString(x + 11, top - 15, name)
        para(c, text, "small", x + 11, top - 22, 215)
    y = top - 84
    y = label(c, "NON-NEGOTIABLE FACT BOUNDARIES", M, y)
    boundaries = [
        "Zino’s father is family testimony and must remain outside Zino’s firsthand point of view.",
        "Elianne’s timing and story are unconfirmed; she receives agency before romance.",
        "The unnamed aunt, U.S. girlfriend, crypto circle and boarding cast are protected placeholders until Zino supplies the detail needed to distinguish them truthfully.",
        "Author-supplied traits govern the animation proposals below; faces, clothes and age variants remain proposals where no real reference is supplied.",
    ]
    for line in boundaries:
        y = para(c, "• " + line, "body", M, y, W - 2*M) - 6
    c.showPage()


def zino_page(c: canvas.Canvas) -> None:
    page(c, 3, 8, "Zino / Grand")
    c.setFillColor(INK)
    c.setFont("CastSerifB", 19)
    c.drawString(M, H - 78, "Nkeh “Zino” Nkengzincho")
    c.setFillColor(MUTED)
    c.setFont("CastSans", 9.2)
    c.drawString(M, H - 96, "The real boy at the centre of the story")
    fit_image(c, image("zino"), M, 195, 246, 437)
    card(c, 312, H - 122, 240, "ZINO", "Gifted footballer, storyteller and future-builder.",
         "Ten at the opening; born 1990. Bright, witty, kind and just. Maths feels like a puzzle; science comes readily. A Catholic and former primary-school altar server. He wants to build his mother a house.",
         "Handsome, clean fade, curly top and slim quick-footed silhouette. Age-ten street wear: white vest and worn blue shorts. Later night-study proposal: burgundy T-shirt and charcoal casual trousers.",
         "Temper and people-pleasing coexist with ability. Loves singing; writes songs from Form Five. First demo follows boarding high school; later U.S. writing continues this history. See update for language and faith detail.")
    c.showPage()


def grand_page(c: canvas.Canvas) -> None:
    page(c, 4, 8, "Zino / Grand")
    c.setFillColor(INK)
    c.setFont("CastSerifB", 19)
    c.drawString(M, H - 78, "Grand-Chukuchuku")
    c.setFillColor(MUTED)
    c.setFont("CastSans", 9.2)
    c.drawString(M, H - 96, "The man Zino invents when ordinary life needs an impossible answer")
    fit_image(c, image("zino"), M, 195, 246, 437)
    card(c, 312, H - 122, 240, "GRAND-CHUKUCHUKU", "Zino’s fictional adult ideal; never a literal future or supernatural force.",
         "Confirmed foundation: Zino tells friends stories about this man doing what nobody else can. He appears only while Zino actively crosses reality with fiction.",
         "Locked baseline: tapered curls, close beard, warm brown complexion, navy suit, open white shirt and brown shoes. Navy, cream and gold mark imagination; a composed eye line and stillness set him apart.",
         "He may not fly, fight, rescue real consequences or become a superhero. As the story grows darker, he can fail to appear.")
    c.showPage()


def friends_page(c: canvas.Canvas) -> None:
    page(c, 5, 8, "Friends / first love")
    c.setFillColor(INK)
    c.setFont("CastSerifB", 19)
    c.drawString(M, H - 78, "The school orbit")
    c.setFillColor(MUTED)
    c.setFont("CastSans", 9.2)
    c.drawString(M, H - 96, "Distinct friends who make Fiango feel lived in")
    fit_image(c, image("friends"), M, 276, 220, 391)
    x, y, width = 285, H - 122, 267
    y = card(c, x, y, width, "GIDEON", "Business-minded friend and sideline banter; never a football player.",
             "Zino calls him Giddy. Camera gigs, trades and paid services; a market bread place by Form Five. Often pays; seeks Zino’s schoolwork help. Quiet with girls; loves Sophy in Forms Two–Five.",
             "Big head and nose; small front-tooth gap; W hairline and fuller hair. Camera bag. Daytime portrait: sky-blue/navy uniform. Night proposal: green polo and brown casual trousers.")
    y -= 8
    y = card(c, x, y, width, "LUC", "Faithful, candid friend; the group’s conscience.",
             "Small Bible, school preaching and Zino’s maths help. Evening training: mud-formed dumbbells and a sand-filled punching bag. Zino calls him Lucky Luc when meeting him alone. Does not play football.",
             "Muscular build, big hands/ears and high flat-top. Daytime portrait: sky-blue/navy uniform. Night proposal: mustard T-shirt and navy casual trousers. Training onset open; age-ten version stays childlike.")
    y -= 8
    card(c, x, y, width, "ELIANNE", "Previously named first love; identity/place still open.",
         "Lizzy is now confirmed as the school girlfriend: crush Form One, together Form Two, breakup Form Three. Do not merge or delete Elianne without clarification.",
         "Old school-era look is provisional. Girls’ day-school uniform is sky-blue short sleeves with a dark-blue skirt.",
         "Mirabel and Lizzy now have separate three-view model proposals appended. Sophy/Tracey designs remain open; Elianne is not renamed.")
    c.showPage()


def family_page(c: canvas.Canvas) -> None:
    page(c, 6, 8, "Family")
    c.setFillColor(INK)
    c.setFont("CastSerifB", 19)
    c.drawString(M, H - 78, "The people behind the promise")
    c.setFillColor(MUTED)
    c.setFont("CastSans", 9.2)
    c.drawString(M, H - 96, "Mother, uncle and an inherited absence")
    fit_image(c, image("family"), M, 276, 220, 391)
    x, y, width = 285, H - 122, 267
    y = card(c, x, y, width, "ZINO’S MOTHER", "Single mother, primary-school teacher and Zino’s most important promise.",
             "Confirmed: taught from a young age throughout his childhood; believed in him and raised him after his father died.",
             "Wax-print teacher dresses, marked exercise books, practical shoes and controlled upright posture. Care shows in action, not pity.")
    y -= 8
    y = card(c, x, y, width, "PATERNAL UNCLE", "Renowned lawyer, Christian convert and cocoa businessman; supports school at times.",
             "Known for suits. By Form Three, a large Kumba cocoa store ships trailers to Douala. O-Level pride leads to the America promise, later deferred until after a degree.",
             "The updated charcoal suit illustrates his lawyer era. Later store/dispatch dress is open. Cocoa links him to his brother’s farming livelihood.",
             "Conversion/work overlap, support timing and deferral motive remain open; professional success does not prove household cash access.")
    y -= 8
    card(c, x, y, width, "ZINO’S FATHER", "A loss Zino inherited, not a memory he owns.",
         "Limited formal schooling; grew and sold cocoa. Family testimony: fatal snake bite when Zino was two; Zino has no direct recollection.",
         "Use a respectful photo, told memory or restrained symbolic image only. The cocoa-farmer portrait is nonliteral.",
         "No first-person Zino flashback, invented dialogue, injury spectacle or invented character history.")
    c.showPage()


def adults_page(c: canvas.Canvas) -> None:
    page(c, 7, 8, "School / compound adults")
    c.setFillColor(INK)
    c.setFont("CastSerifB", 19)
    c.drawString(M, H - 78, "Adults who shape the frame")
    c.setFillColor(MUTED)
    c.setFont("CastSans", 9.2)
    c.drawString(M, H - 96, "Academic attention and the ordinary pressure of money")
    fit_image(c, image("adults"), M, 195, 246, 437)
    x, y, width = 312, H - 122, 240
    y = card(c, x, y, width, "MISS MUKETE", "Zino’s favourite chemistry teacher.",
             "Confirmed: favourite chemistry teacher. No other biography or exact likeness is yet supplied.",
             "Proposed: gold-rimmed glasses, blue patterned blouse, lab coat, chemistry book and small glass beaker. Exact, observant and encouraging without becoming generic inspiration.",
             "Do not build a personal episode around her until Zino provides a specific classroom memory.")
    y -= 10
    card(c, x, y, width, "THE LANDLORD", "The recurring face of the compound’s rent and electricity calculations.",
         "Confirmed: comes monthly to collect rent and light money from a compound of families, single mothers, bachelors and student tenants.",
         "Proposed: lean older silhouette, silver at the temples, pale shirt, dark trousers, sandals, keys and ledger. His calm routine lets money pressure enter without claiming malice.",
         "No invented debt amount, motive or confrontation presented as fact.")
    c.showPage()


def reserved_page(c: canvas.Canvas) -> None:
    page(c, 8, 8, "Protected future cast")
    y = H - 75
    y = para(c, "Known, but not visually locked", "h1", M, y, W - 2*M) - 8
    y = para(c, "These people and groups belong in the series, but they need details before they receive a visual identity or speak for themselves.", "subtitle", M, y, W - 2*M) - 16
    blocks = [
        ("MATERNAL AUNT", "Confirmed: cooked for and supported Zino, believed in him, and was later attacked and killed. Needed: name, age, memories, date/place/context, visual reference and source boundary."),
        ("U.S. GIRLFRIEND", "Confirmed: Zino identifies a girlfriend during the America years. Needed: name or fictionalisation choice, years together, her perspective, relationship change and consent boundaries."),
        ("BOARDING-SCHOOL CAST", "Confirmed environment: elite students, wealthy parents, white teachers and priests, bullying, strict discipline. Needed: names, individual roles, actual incidents and visual references."),
        ("FOOTBALL FRIENDS / CRYPTO CIRCLE", "Confirmed: Zino pitched Nkap and njangi.xyz to football friends. His account alleges later reporting to immigration and an attempted takeover. Needed: names or fictionalisation plan, records, contributions and a defensible account before anyone is depicted doing harm."),
        ("DUBAI COLLEAGUES", "Confirmed: Zino moved to Dubai in 2020 and worked for a Chinese online retailer of digital products. Needed: work function, people, setting and perspectives."),
        ("UNIVERSITY / IMMIGRATION CHARACTERS", "Confirmed: Oklahoma studies beginning 2012, money, papers, loneliness, racism and deportation in 2019. Needed: dates, documents, names, events and a fictionalisation plan."),
    ]
    for heading, text in blocks:
        c.setFillColor(PALE)
        c.roundRect(M, y - 71, W - 2*M, 62, 6, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.setFont("CastSansB", 8)
        c.drawString(M + 12, y - 23, heading)
        para(c, text, "small", M + 12, y - 29, W - 2*M - 24)
        y -= 78
    y -= 3
    y = label(c, "PRODUCTION RULE", M, y)
    para(c, "A visual design must follow character truth. Until the source is known, preserve the narrative space rather than filling it with a convincing invention.", "quote", M, y, W - 2*M)
    c.showPage()


def build_pdf() -> None:
    fonts()
    c = canvas.Canvas(str(PDF), pagesize=A4, pageCompression=1)
    c.setTitle("Grand-Chukuchuku | Character Bible v2")
    c.setAuthor("Based on the life of Nkeh Nkengzincho (Zino)")
    cover(c)
    cast_system(c)
    zino_page(c)
    grand_page(c)
    friends_page(c)
    family_page(c)
    adults_page(c)
    reserved_page(c)
    c.save()
    # Append the current author's update, including named new cast and adjacency map.
    import fitz
    update = ROOT / "Fiango_Life_and_Characters_Update_2026-10-30.pdf"
    if not update.exists():
        raise FileNotFoundError("Run build_fiango_update.py first")
    with fitz.open(PDF) as core, fitz.open(update) as appendix:
        core.insert_pdf(appendix)
        turnarounds = ROOT / "turnarounds" / "Grand-Chukuchuku_Five_Character_Turnarounds_v1.pdf"
        if not turnarounds.exists():
            raise FileNotFoundError("Run turnarounds/build_turnarounds.py first")
        with fitz.open(turnarounds) as models:
            core.insert_pdf(models)
        comparison = ROOT / "turnarounds" / "Grand-Chukuchuku_Lizzy_Mirabel_Design_Comparison.pdf"
        if not comparison.exists():
            raise FileNotFoundError("Run turnarounds/build_turnarounds.py to build the distance comparison")
        with fitz.open(comparison) as check:
            core.insert_pdf(check)
        uniform_root = ROOT / "turnarounds" / "school-uniforms"
        for name in ["Grand-Chukuchuku_Mirabel_Lizzy_Uniform_Turnarounds.pdf", "Grand-Chukuchuku_Uniform_Comparison.pdf"]:
            with fitz.open(uniform_root / name) as uniform:
                core.insert_pdf(uniform)
        combined = core.tobytes(garbage=4, deflate=True)
    PDF.write_bytes(combined)


def package() -> None:
    readme = ROOT / "README.md"
    md = ROOT / "Grand-Chukuchuku_Character_Bible_v2.md"
    legacy = (ROOT / "Grand-Chukuchuku_Character_Bible_v1.md").read_text()
    replacements = {
        "Character Bible v1 — Fiango and the wider story": "Character Bible v2 — Fiango and the wider story",
        "Illustrated and production-ready for Chapter One age 10; later-life variants remain open.": "Age-ten concept and later-secondary three-view proposal supplied; age-ten/adult turnarounds and rigging remain open.",
        "**Elianne** | Zino’s first love": "**Elianne** | Previously named first love; identity/place unresolved",
        "**C — Foundation:** Elianne is identified as Zino’s first love. Her exact age, years, school, relationship arc and voice have not yet been supplied.": "**C — Foundation:** Elianne was previously named first love. Lizzy is now confirmed as the Form One crush, Form Two girlfriend and Form Three breakup. Their identities must not be merged without clarification.",
        "**P — Distinct visual code:** Lean upright silhouette; neat white school shirt, brown shorts or trousers; compact worn Bible close to his body.": "**C / P — Revised visual code:** Muscular build, big hands/ears, high flat-top and small Bible. Mud-formed dumbbells and sand-filled punching bag. Sky-blue/navy uniform applies to daytime only; night-study model uses proposed mustard T-shirt and navy casual trousers. He does not play football. Training onset is open; keep age-ten proportions childlike.",
        "**P — Distinct visual code:** Compact, guarded posture; olive-green striped polo over school trousers or practical shorts; cross-body camera bag; a small period-appropriate camera becomes his identifying prop.": "**C / P — Revised visual code:** Big head/nose, small front-tooth gap, W-shaped hairline and fuller almost-afro; camera/bag. Daytime sky-blue/navy uniform; proposed night-study green polo and brown casual trousers. No student wears a uniform at night study.",
        "Slim, quick-footed silhouette; short tapered curls; bright, watchful eyes; expressive brow;": "Handsome, clean fade and curly top; slim quick-footed silhouette, bright eyes and expressive brow;",
        "**Elianne** | Illustrated as a proposed school-era design; chronology is open.": "**Elianne** | Provisional school-era design; identity and chronology remain open.",
        "**Zino’s Paternal Uncle** | Occasional school-fee support and promise-maker | Illustrated; name, work and financial circumstances remain open.": "**Zino’s Paternal Uncle** | Occasional school-fee support and promise-maker | Lawyer-era suit illustrated; name and financial circumstances remain open.",
        "Blue is her recurring colour, distinct from Zino’s earth tones, Gideon’s olive, and Luc’s white/brown.": "Her proposed ribbon and books distinguish her within the shared sky-blue/navy uniform. Earlier white/brown school concepts are superseded.",
        "**P — Distinct visual code:** Older than Zino’s mother, understated collared shirt, folded newspaper, plain envelope, careful hands. His visual language is modest responsibility, never automatic wealth.": "**C / P — Visual correction:** He is a renowned lawyer known for suits, later a Christian convert and cocoa trader with a large Kumba store by Form Three, shipping trailers to Douala. The revised illustration shows a charcoal lawyer-era suit; later store/dispatch clothing remains open.",
        "**Continuity hold:** Name, profession, family circumstances, exact contribution, and motive for the deferral remain open.": "**Continuity hold:** Name, conversion date, legal/trading overlap, family circumstances, exact contributions and motive for the deferral remain open. His profession is now supplied.",
    }
    for before,after in replacements.items():legacy=legacy.replace(before,after)
    additions = {
        "- **Props:** Scuffed ball, school bag, folded exercise-book page, small coins, well bucket.": "- **Props:** Scuffed ball, school bag, folded exercise-book page, small coins, well bucket.\n- **C — Learning, music and faith:** Maths is his favourite, puzzle-like subject; he understands science readily. Singing precedes his own songwriting in Form Five; his first demo follows his return from boarding high school, and he writes later in America. Catholic; primary-school altar service stops for lack of time in secondary school, not a supplied loss of faith.",
        "- **Do not do:** Do not make him a comic coward or a sidekick whose only purpose is to pay bills.": "- **C — Later detail:** Zino calls him Giddy. Constant trades and paid services; a market place selling bread by Form Five. He asks Zino to explain schoolwork. Market terms and prices remain open.\n- **Do not do:** Do not make him a comic coward or a sidekick whose only purpose is to pay bills.",
        "- **Do not do:** Never reduce Luc to a punchline, a hypocrite or an automatic judge of his friends.": "- **C — Nickname:** Zino calls him Lucky Luc when meeting him alone; the date this begins is open.\n- **Do not do:** Never reduce Luc to a punchline, a hypocrite or an automatic judge of his friends.",
        "- **Do not do:** Do not turn her into suffering alone.": "- **C — Trust:** Zino’s room is two apartments from hers. He could come, go or sleep late without her always knowing; she trusted him. This does not establish neglect or approval of everything he did.\n- **Do not do:** Do not turn her into suffering alone.",
    }
    for before, after in additions.items():
        if before not in legacy:
            raise ValueError(f"Missing core-text anchor: {before}")
        legacy = legacy.replace(before, after)
    legacy=legacy.replace("**Performance:** His jokes land dry.", "**C — Football correction:** He does not play; he sits watching and bantering, especially when Zino loses.\n- **Performance:** His jokes land dry.")
    md.write_text(legacy + "\n\n---\n\n" + (ROOT / "Fiango_Life_and_Characters_Update_2026-10-30.md").read_text() + "\n\n---\n\n" + (ROOT / "turnarounds" / "README.md").read_text() + "\n\n---\n\n" + (ROOT / "turnarounds" / "school-uniforms" / "README.md").read_text())
    files = [PDF, md, readme, ROOT / "build_character_bible.py", ROOT / "build_fiango_update.py", ROOT / "Fiango_Life_and_Characters_Update_2026-10-30.md", ROOT / "Fiango_Life_and_Characters_Update_2026-10-30.pdf", ROOT / "Fiango_Neighbourhood_Adjacency_2026-10-30.svg", ROOT / "Fiango_Taxi_Motel_Poultry_2026-10-30.svg", SERIES / "writers-room" / "CONTEXT_REVIEW_2026-10-30.md", SERIES / "writers-room" / "LATEST_CHARACTER_CONTINUITY_REVIEW_2026-10-30.md"] + sorted((ROOT / "images").glob("*.png")) + [SERIES / "visual-reference" / "VISUAL_BASELINE_V1.md"]
    files += [p for p in sorted((ROOT / "turnarounds").iterdir()) if p.suffix in {".png", ".pdf", ".md", ".json", ".py"}]
    files += [SERIES / "writers-room" / "NIGHT_WARDROBE_AND_TURNAROUNDS_REVIEW_2026-10-30.md"]
    files += [SERIES / "writers-room" / "LIZZY_MIRABEL_DISTANCE_REVIEW_2026-10-30.md"]
    files += [p for p in sorted((ROOT / "turnarounds" / "school-uniforms").iterdir()) if p.suffix in {".png", ".pdf", ".md", ".json"}]
    files += [SERIES / "writers-room" / "COMPLEXION_AND_UNIFORM_REVIEW_2026-10-31.md"]
    with zipfile.ZipFile(PACKAGE, "w", zipfile.ZIP_DEFLATED) as z:
        for file in files:
            if file.parent == ROOT / "images":
                arc = Path("images") / file.name
            elif file.parent == ROOT / "turnarounds":
                arc = Path("turnarounds") / file.name
            elif file.parent == ROOT / "turnarounds" / "school-uniforms":
                arc = Path("turnarounds") / "school-uniforms" / file.name
            elif file.parent == SERIES / "visual-reference":
                arc = Path("visual-reference") / file.name
            else:
                arc = file.name
            z.write(file, arc)
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
