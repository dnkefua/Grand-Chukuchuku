#!/usr/bin/env python3
"""Assemble the reviewed 60-episode Chapter One shooting script from room drafts."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "scripts" / "Grand-Chukuchuku_Chapter_01_Full_Shooting_Script_v2.md"
SOURCES = [
    ROOT / "writers-room" / "v2-drafts" / "WRITER_A_EPS_01_10.md",
    ROOT / "writers-room" / "v2-drafts" / "WRITER_B_EPS_13_24.md",
    ROOT / "writers-room" / "v2-drafts" / "WRITER_C_EPS_25_36.md",
    ROOT / "writers-room" / "v2-drafts" / "WRITER_D_EPS_37_48.md",
    ROOT / "writers-room" / "v2-drafts" / "WRITER_E_EPS_49_60.md",
]

GRID = [
    ("I", "01", "The Courtyard Keeps Score", "A disputed football call gives Zino his first Grand-Chukuchuku story."),
    ("I", "02", "Well Water", "Four buckets, the bathroom queue and 200 CFA turn dawn into a transport decision."),
    ("I", "03", "Lunch Money", "Zino saves lunch money for a bottle-game stake and hides the cost."),
    ("I", "04", "First Bottle", "Nacking Bottle's three-hit rule turns one coin into a real risk."),
    ("I", "05", "The Deciding Pass", "Zino has to pass rather than take the glory shot."),
    ("I", "06", "Rent and Light", "A landlord's notebook makes adult money pressure visible."),
    ("I", "07", "Gideon's First Gig", "Gideon treats a birthday camera job as a business."),
    ("I", "08", "The Message", "Zino opens a harmless conversation for Gideon, then makes room."),
    ("I", "09", "Luc's One Minute", "Luc risks public embarrassment to preach to one student."),
    ("I", "10", "The Maths Pass", "Zino helps Luc work through a problem without taking the pencil."),
    ("I", "11", "The Money Match", "A pooled football game teaches Zino that a pass can be a win."),
    ("I", "12", "Between Bells", "School social life meets the price of talent without discipline."),
    ("II", "13", "The Lunch Bell", "Hunger stretches the day as Zino saves for another street game."),
    ("II", "14", "Nacking Bottle", "The fully defined bottle game tests Zino against a better player."),
    ("II", "15", "The Cup", "An unattended pot of contributions tests Zino's justice."),
    ("II", "16", "Gideon's Angle", "Gideon finds a camera opportunity in a football evening."),
    ("II", "17", "The Gig", "A birthday job asks Zino to help without making it his show."),
    ("II", "18", "The Corridor", "Gideon needs an opening with a girl, not a performance in his place."),
    ("II", "19", "Say It Yourself", "Zino learns that silence can be support."),
    ("II", "20", "One Minute", "Luc accepts a small audience rather than chase a public victory."),
    ("II", "21", "The Last Line", "Luc's maths problem matters more than arriving early to the game."),
    ("II", "22", "Slippers for Posts", "A contribution match turns Zino's showmanship into a team problem."),
    ("II", "23", "The Strap", "Gideon's camera accident tests whether Zino can be responsible."),
    ("II", "24", "The Well List", "Routine at the well carries the same money calculations as the street."),
    ("III", "25", "The Workshop Gate", "Professional School's daytime vocation corrects the boys' assumption."),
    ("III", "26", "The Excuse", "Night revision is both study and a reason to leave home."),
    ("III", "27", "Room One", "A silent study room tests Zino's hunger for attention."),
    ("III", "28", "After the Shutter", "Gideon's camera hustle brushes against the revision world."),
    ("III", "29", "The Group", "Collaborative study exposes different kinds of pride."),
    ("III", "30", "The Third Strike", "A final bottle-game variation makes money, hunger and ego collide."),
    ("III", "31", "Home Too Early", "A primary-school fee memory returns as pressure interrupts study."),
    ("III", "32", "The Last Light", "Zino has to choose careful work over a night he cannot control."),
    ("III", "33", "The Shout", "An ordinary evening changes when a crowd begins to form."),
    ("III", "34", "The Crowd", "A labelled composite witness event destroys certainty without proving guilt."),
    ("III", "35", "Ash at the Well", "Smoke and silence follow Zino home and change his behaviour."),
    ("III", "36", "The Study List", "Ten O-Level subjects become an answer to fear, not an escape from it."),
    ("IV", "37", "Ten on the Table", "Zino enters the O-Level run with work, not fantasy."),
    ("IV", "38", "The Last Bell", "The final paper leaves Zino with no immediate answer."),
    ("IV", "39", "Static", "Radio waiting makes ordinary Fiango sounds unbearable."),
    ("IV", "40", "His Name", "O-Level release belongs to the people who waited with Zino."),
    ("IV", "41", "The Offer", "Uncle's pride gives school choice and America a condition."),
    ("IV", "42", "The School He Chose", "Zino chooses boarding and the cost of distance."),
    ("IV", "43", "A Day Away", "Mountains and valleys make the journey a day long."),
    ("IV", "44", "The Gate", "A new school exposes wealth, authority and uncertainty."),
    ("IV", "45", "First Bell", "Routine becomes a test Zino cannot outtalk."),
    ("IV", "46", "The Table", "A meal reveals how belonging has unspoken rules."),
    ("IV", "47", "Who Belongs", "Zino begins to decide when not to perform his temper."),
    ("IV", "48", "The First Term", "Adaptation begins without making boarding feel safe."),
    ("V", "49", "Before First Bell", "Second-year routine shows what Zino has learned to suppress."),
    ("V", "50", "The Water Basin", "A small hierarchy tests Zino's temper and restraint."),
    ("V", "51", "The Fee Matter", "A distinct high-school fee exclusion is staged within its factual limits."),
    ("V", "52", "Outside the Class", "Humiliation cannot stop Zino from continuing the work alone."),
    ("V", "53", "The Fence", "Zino witnesses returned students and an unfilled-in punishment."),
    ("V", "54", "After the Fence", "Dormitory silence makes hunger and fear communal."),
    ("V", "55", "Five Subjects", "The maximum five A-Level papers become a new road to America."),
    ("V", "56", "The Study Lamp", "Zino studies through the night without an impossible hero."),
    ("V", "57", "The Last Paper", "After the final paper, nothing remains for Zino's hand."),
    ("V", "58", "One Hundred Percent", "A 100% school pass rate changes fear into anticipation."),
    ("V", "59", "Results on Air Again", "Zino's A-Level radio result brings joy without an invented grade."),
    ("V", "60", "The Promise Moves", "America shifts to after a first degree; Chapter Two begins."),
]

HEADER = """# GRAND-CHUKUCHUKU
## Chapter One: **Fiango** — Full Shooting Script v2

**Format:** 60 vertical episodes, each **1:35–2:00 maximum**; original adult 2D animation; English and Cameroon Pidgin with English subtitles.

**Season premise:** This expanded first chapter lets the audience live in Fiango before it asks them to fear for Zino. Football money, Nacking Bottle, compound water, camera work, school corridors, church language, revision and radio results are not detours from the plot. They are the life that makes each later loss, win and deferred promise matter.

**Locked working chronology:** Episode 31 is an explicitly labelled **1999 primary-school memory**. The main Fiango timeline runs through five day-school years, approximately **2000–2005**, with Gideon and Luc. Episodes 37–41 cover the O-Level threshold: **10 subjects of a maximum 11**, radio results and the uncle's promise. Episodes 42–48 begin the remote boarding school in approximately **2005**. Episodes 49–60 cover the second boarding year and 2007 A-Level threshold: **5 subjects of a maximum 5**, a school with a reported 100% pass rate, radio results, and America's deferment until after a first university degree. The approximate years follow Zino's supplied dates and must be revised together if he corrects any one of them.

### Provenance key

- **C — Confirmed recollection:** fact supplied directly by Zino.
- **FT — Family testimony:** history Zino did not witness, including his father's death when he was two.
- **R — Reported/incomplete:** supplied event with unknown date, order, people, wording or method.
- **P — Proposed composite:** dialogue, staging, visual transition, exact sequence or individual action written for drama. It is never a claimed transcript or literal record.

### Character and visual rules

- Updated 31 October 2026: the author's `character-bible/Fiango_Life_and_Characters_Update_2026-10-30.md` controls daily routine, named school peers, GBHS campus and neighbourhood corrections. Earlier proposed actions lose precedence when they conflict with it.
- Day school is Government Bilingual High School Kumba (GBHS), reported 10.7 km from the compound; route and travel time remain open. Form Three is two storeys. The GBHS Sixth Form campus facilities do not change Zino's separate two-year remote boarding-school attendance. Professional School remains a separate vocational/night-revision location.
- Luc and Gideon do not play football. Gideon watches and banters; Luc evangelises or chats. Ayuk, Arey, Noge, Bismark and Robi are the supplied street-playing circle. They are not identified as the later crypto associates.
- Gideon has a W-shaped hairline, almost-afro hair, a noticeably large head and nose, and a small front-tooth gap; Zino calls him **Giddy**. Constant gigs, trading and paid services lead to a bread-selling place in the market by Form Five; he also comes to Zino for schoolwork explanations. Luc has a high flat-top, large hands and ears, and a muscular older-secondary silhouette from evening training with mud-formed dumbbells and a sand-filled punching bag. The training's starting year is unknown: do not give his ten-year-old version adult bodybuilding proportions. **Lucky Luc** is Zino's greeting when he meets Luc alone. Zino's supplied appearance is handsome with a clean fade. These identifying traits are not comic defects.
- Maths is Zino's favourite: he understands scientific concepts quickly and enjoys solving a puzzle more than memorising reading-heavy material. He loves singing, begins writing songs in **Form Five**, records his first demo after returning home from boarding high school, and continues making music in America. Music does not begin in the USA. The first-demo sequence belongs at the Chapter One/Two bridge, after the boarding years; studio, song and recording companions remain open.
- Zino is Catholic and served at Mass throughout primary school. Secondary-school demands left no time to continue altar service; this does not establish a loss of faith. Mother's trust and the separate room gave him freedom to come, go or sleep late without her always noticing; this is not proof of neglect or approval of every action.
- Author-supplied GCE minimum pass thresholds are **4 O-Level subjects / 2 A-Level subjects**. Keep these separate from Zino's **10 / 5 subjects taken**, the **11 / 5 maxima**, the uncle's **all-five** condition and the school's **100% A-Level pass rate**. These are the author's story facts, not independently verified exam regulations.
- Forms One–Five **daytime** uniform: light sky-blue short-sleeved shirts for both sexes; boys wear dark-blue trousers and girls dark-blue skirts. Wearer's left-chest pocket carries the circular GBHS badge: Government Bilingual High School Kumba around a lit candle. Exact badge colours/art are proposed. **Night revision at Professional School has no student uniforms:** everyone wears regular house/casual clothes, and some dress to impress. This later correction supersedes the earlier pilot's uniform-at-night treatment. Exact casual garments are proposed design choices; boarding colours remain unconfirmed.
- Current proposed pilot night wardrobe: Zino — plain burgundy short-sleeved T-shirt, charcoal casual trousers, dark sneakers and backpack; Gideon — forest-green plain polo, dark-brown casual trousers and camera bag; Luc — mustard/ochre plain T-shirt, loose deep-navy casual trousers and small Bible, no bag. Carry these outfits through the same-night crowd, cold open and return home; they do not replace daytime school uniforms or every casual outfit across the chapter.
- Dawn: about 5:30, four buckets in two rounds, one in each hand; two shared bathrooms; Zino's room two apartments from Mother's front room. Her bedside drawer usually has 200 CFA: 100 for one taxi ride and 100 at school, or walk early and keep 200 for school. Taxis are taken on three mornings a week.
- Lizzy: crush Form One, girlfriend Form Two, breakup Form Three. Mirabel's maths friendship starts Form Three and continues to U.S. departure. Mirabel is described as beautiful and slim; Lizzy has a pretty face. Their school-age model sheets use ordinary adolescent proportions, fully clothed neutral poses and confirmed low-cut natural hair. Mirabel is darker than Lizzy; exact faces, shades and crop styling remain proposed. Gideon/Giddeon and Mirabel/Mirable are spelling variants of the existing characters, not new cast members. Sophy is Gideon's interest Forms Two–Five; Zino refuses her advances from loyalty. Elianne remains a separate unresolved identity, not an assumed alias. All school-age relationships remain non-graphic; Tracey's reported Form Three experience is retained in neutral notes pending exact context. Tracey had already sat the GCE twice unsuccessfully and saw Zino teach maths to students who later passed; this does not establish her exact age, private motive, a transaction or the sole cause of anyone's results.
- The uncle is a renowned lawyer known for suits, later a Christian convert and cocoa trader with a Kumba store by Form Three, shipping to Douala. Do not invent why support was intermittent or why the America promise changed.
- Zino speaks Pidgin with friends, English at home and French/English in school. Every line below is P until Zino confirms it as remembered speech.
- The compound and Grand-Chukuchuku's adult design follow `series-development/visual-reference/VISUAL_BASELINE_V1.md`. Grand-Chukuchuku appears only after Zino begins an impossible story; he is exuberant early, silent before the crowd, and increasingly absent at boarding school.
- The Christmas memory of Gideon paying for drinks while Zino helps him approach girls remains unplaced pending its year, ages and sequence. It can be developed at its actual age with age-appropriate, non-graphic relationships, without moving it simply to fill a gap. Do not invent ages or events; no explicit sexual portrayal of school-age characters.
- The jungle-justice composite retains the harm Zino supplied while leaving the accused unnamed, unheard over the crowd and never established as guilty. It shows no body, verdict, motive, police result, replay or triumphal score.

## Five-act overview

| Act | Episodes | Movement |
| --- | ---: | --- |
| I. **The Compound Keeps Score** | 01–12 | Grand-Chukuchuku, rent pressure, childhood money and the friendship triangle take root. |
| II. **The Street Keeps Score** | 13–24 | Football stakes, Nacking Bottle, camera work, school attention and faith become daily tests. |
| III. **Night School, Day Fear** | 25–36 | Professional School, O-Level pressure and a witness event turn ordinary nights unstable. |
| IV. **The Road He Chooses** | 37–48 | Radio success, the uncle's condition and boarding-school arrival widen Zino's world. |
| V. **Five Papers, Another Gate** | 49–60 | Fees, discipline, the fence, A-Levels and a deferred promise define the next journey. |

## 60-episode season grid

| Act | Ep. | Title | Dramatic use |
| --- | ---: | --- | --- |
"""

TAIL = """

---

## Continuity questions before voice recording, final boarding or release

1. Confirm the exact start/end years of the five Fiango day-school years and two boarding-school years.
2. Confirm Miss Mukete's school and class level before any scene presents her placement as fact.
3. Record the distinct primary- and high-school fee-exclusion days: location, person who spoke, route, response and return to school.
4. Confirm GCE subject lists, radio locations, people present and the exact wording of the uncle's O-Level and post-A-Level conversations.
5. Record the exact fence-punishment details Zino witnessed before adding an action, authority, food or student identity.
6. Record individual jungle-justice incidents separately; this script uses only an explicitly labelled composite witness scene.
7. Confirm Gideon's camera type and photo process before an animation shows a print, screen or delivery.
8. Record the Christmas club/drinks/girls memory's year, ages and sequence before placing it at its actual point in the story; do not presume it happened after eighteen.
9. Lizzy's breakup is resolved as Form Three; Elianne's identity/place, Tracey's exact age/context and the exact year of Ayuk's TV purchase remain open. Working peer-age estimates are not birthdays.
10. Confirm when Luc began training, the materials/construction of his homemade weights, and Gideon's bread-market arrangement before final prop layouts. Do not substitute commercial weights or a modern gym.
11. Record Zino's first Form Five song and first post-boarding demo: title, lyrics, recording place, collaborators and date. A later U.S. songwriting scene must acknowledge the earlier music history.

## Production guardrails

- Primary-school and high-school fee exclusions are separate confirmed events. This v2 never blends them.
- Nacking Bottle uses the author-supplied beer bottles as game markers. It does not show school-age drinking.
- Professional School remains a daytime vocational campus for construction, building and electrical training. Its night access is mixed: serious study, social life and distraction; no group is written as inherently delinquent.
- Do not invent grades, rankings, school names, fee amounts, unknown travel stages, verbatim uncle quotations or family objects. Use the supplied named school peers only at their confirmed forms; unrecorded action and dialogue remain proposed.
- A Chapter One scene earns its hard-R force through consequence, not spectacle. Keep the camera with the witness and the changed child.
"""


def episode_chunks(source: Path) -> list[tuple[int, str]]:
    text = source.read_text(encoding="utf-8")
    matches = list(re.finditer(r"(?m)^# EPISODE (\d{2}) —", text))
    chunks = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        number = int(match.group(1))
        chunk = text[match.start():end].strip()
        if number == 60:
            chunk = chunk.split("\n## Placement note for the Christmas holiday memory", 1)[0].rstrip()
        chunks.append((number, chunk))
    return chunks


def polish(number: int, chunk: str) -> str:
    changes = {
        10: [("EPISODE 11 — THE EMPTY SEAT", "EPISODE 11 — THE MONEY MATCH")],
        3: [("EPISODE 04 — NACKING BOTTLE", "EPISODE 04 — FIRST BOTTLE")],
        4: [("# EPISODE 04 — “NACKING BOTTLE”", "# EPISODE 04 — “FIRST BOTTLE”"),
            ("EPISODE 05 — THREE HITS", "EPISODE 05 — THE DECIDING PASS")],
        5: [("# EPISODE 05 — “THREE HITS”", "# EPISODE 05 — “THE DECIDING PASS”")],
        12: [("EPISODE 13 — [WRITER B CONTINUES]", "EPISODE 13 — THE LUNCH BELL")],
        24: [("EPISODE 25 — RENT DAY AGAIN", "EPISODE 25 — THE WORKSHOP GATE")],
        29: [("EPISODE 30 — “THREE HITS”", "EPISODE 30 — “THE THIRD STRIKE”")],
        30: [("# EPISODE 30 — “THREE HITS”", "# EPISODE 30 — “THE THIRD STRIKE”")],
        35: [("EPISODE 36 — “TEN PAPERS”", "EPISODE 36 — “THE STUDY LIST”")],
        36: [("# EPISODE 36 — “TEN PAPERS”", "# EPISODE 36 — “THE STUDY LIST”"),
             ("EPISODE 37 — “THE FIRST PAPER”", "EPISODE 37 — TEN ON THE TABLE")],
        48: [("EPISODE 49 — THE FENCE", "EPISODE 49 — BEFORE FIRST BELL")],
    }
    for before, after in changes.get(number, []):
        chunk = chunk.replace(before, after)
    return chunk


def main() -> None:
    episodes: dict[int, str] = {}
    for source in SOURCES:
        for number, chunk in episode_chunks(source):
            if number in episodes:
                raise ValueError(f"Duplicate episode {number:02d}")
            episodes[number] = polish(number, chunk)
    expected = list(range(1, 61))
    if sorted(episodes) != expected:
        raise ValueError(f"Expected 01–60, got {sorted(episodes)}")
    grid = "\n".join(f"| {act} | {number} | **{title}** | {beat} |" for act, number, title, beat in GRID)
    script = HEADER + grid + "\n\n---\n\n" + "\n\n---\n\n".join(episodes[number] for number in expected) + TAIL
    OUT.write_text(script, encoding="utf-8")
    print(f"Wrote {OUT} ({len(script.split())} words; {len(episodes)} episodes)")


if __name__ == "__main__":
    main()
