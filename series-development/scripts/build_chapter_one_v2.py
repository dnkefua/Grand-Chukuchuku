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
    ("I", "02", "Well Water", "A water chore teaches Zino that compound duty comes before street play."),
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

- Zino speaks Pidgin with friends, English at home and French/English in school. Every line below is P until Zino confirms it as remembered speech.
- The compound and Grand-Chukuchuku's adult design follow `series-development/visual-reference/VISUAL_BASELINE_V1.md`. Grand-Chukuchuku appears only after Zino begins an impossible story; he is exuberant early, silent before the crowd, and increasingly absent at boarding school.
- The school-age season does not depict drinking, sexual activity or nightclub attendance. The Christmas memory of Gideon paying for drinks while Zino helps him approach girls is held as an **18+ Chapter Two/post-secondary placement question** until Zino supplies its year and age.
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
8. Place the Christmas club/drinks/girls memory only after Zino gives its year and confirms he was 18 or older.

## Production guardrails

- Primary-school and high-school fee exclusions are separate confirmed events. This v2 never blends them.
- Nacking Bottle uses the author-supplied beer bottles as game markers. It does not show school-age drinking.
- Professional School remains a daytime vocational campus for construction, building and electrical training. Its night access is mixed: serious study, social life and distraction; no group is written as inherently delinquent.
- Do not add grades, rankings, school names, fee amounts, travel method, uncle quotation, named girls, or a literal family object unless Zino confirms it.
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
