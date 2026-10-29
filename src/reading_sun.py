"""Reading SUN: the page about Symbolic Universal Notation and the screen-reader dictionary built for it.

Figures on this page are counts from our own processing of the published SUN New Testament (sun/ in the repo), or
Wycliffe Associates' own published claims, said to be theirs. Nothing evaluative about the organisation appears here.
The James text is read at build time from sun/james_glossed.txt so the page and the data file cannot drift apart.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

import brand

TITLE = "Reading SUN"
SLUG = "reading-sun.html"
ROOT = Path(__file__).resolve().parents[1]
JAMES = ROOT / "sun" / "james_glossed.txt"


def e(s) -> str:
    return html.escape(str(s), quote=True)


def repo(path: str, title: str) -> str:
    return f'<a href="{brand.REPO}/blob/main/{e(path)}">{e(title)}</a>'


def james_tables() -> str:
    """One table per chapter of James: verse, SUN read through glosses, the ULB verse it was made from."""
    text = JAMES.read_text(encoding="utf-8")
    pairs = re.findall(r"^(\d+):(\d+) SUN: (.*)\n\s+ULB: (.*)$", text, flags=re.M)
    chapters: dict[str, list[tuple[str, str, str]]] = {}
    for ch, v, sun, ulb in pairs:
        chapters.setdefault(ch, []).append((v, sun.strip(), ulb.strip()))
    out = []
    for ch, verses in chapters.items():
        rows = "".join(f'<tr><th scope="row">{ch}:{v}</th><td>{e(sun)}</td><td>{e(ulb)}</td></tr>'
                       for v, sun, ulb in verses)
        cap = f'James chapter {ch}: SUN read through inferred glosses, beside the English it was made from'
        out.append(f'<div class="table-scroll" role="region" tabindex="0" aria-label="{e(cap)}, table">'
                   f'<table><caption>{e(cap)}</caption><thead><tr><th scope="col">Verse</th>'
                   f'<th scope="col">SUN, as the dictionary speaks it</th><th scope="col">Unlocked Literal Bible</th>'
                   f'</tr></thead><tbody>{rows}</tbody></table></div>')
    assert len(pairs) == 108, f"James should have 108 verses, found {len(pairs)}"
    return "".join(out)


def body(d: dict) -> str:
    n36 = repo("source-material/36-sun-introduction.md", "an introduction to SUN for people who know braille")
    n38 = repo("source-material/38-sun-taken-apart.md", "SUN taken apart")
    n39 = repo("source-material/39-sun-glossed.md", "SUN glossed")
    files = repo("sun/README.md", "the files and what each one is")
    dic = repo("sun/sun-symbols-nvda.dic", "the NVDA dictionary file")
    return f"""<h1>Reading SUN</h1>
<p class="lede">Symbolic Universal Notation, SUN, is a Bible written in symbols instead of words, made by Wycliffe
Associates for Deaf people who have no written or signed language. Its New Testament is published as a PDF that no
screen reader could read. In October 2026 we took it apart, worked out what most of its symbols mean, and built a
dictionary that lets NVDA, the free screen reader, speak it. This page explains SUN, shows what we found, lets you
read the Epistle of James the way the dictionary reads it, and gives you the files.</p>

<h2>What SUN is</h2>
<p>SUN was not built for blind people. Wycliffe Associates built it for Deaf people, and especially for Deaf
people who have no language at all: no national sign language, no literacy, no schooling. By the organisation's own
account there are about seventy million Deaf people in the world, most of whom know no sign language, and about six
hundred thousand people who are both deaf and blind. SUN gives them Scripture in a form that bypasses spoken
language entirely. Each symbol stands for an idea rather than a word of any language: person, write, God, water,
go. A core of about a hundred symbols is taught first, with pictures, and the rest are built from them. Because the
symbols encode meaning rather than sound, the same page is read by a Deaf person in Tanzania and one in Brazil.</p>
<p>The New Testament in SUN was dedicated in Orlando in February 2020, rendered by about four hundred volunteers
from the Unlocked Literal Bible, an openly licensed English text. The organisation reports SUN in use in about
thirty countries, most of them in Africa, including a programme in Nigeria with a Deaf partner and a Yoruba
teaching resource. A raised, three-dimensional version for Deaf-Blind readers is described as in progress. Those
figures and results are Wycliffe Associates' own; no independent evaluation of SUN has been published, which is not
a mark against it, only the state of the evidence. For teachers, there is {n36}.</p>

<h2>Why a blind man wanted to read it</h2>
<p>Brian cannot read braille by touch and has no prospect of reading raised symbols. He can read anything a screen
reader can speak. SUN mattered to him for three reasons: Deaf-Blind readers are people for whom neither audio nor
ordinary braille works, and anything that makes SUN checkable by touch-reading experts helps them; Wycliffe
Associates works in Nigeria, where this ministry does; and the published SUN New Testament looked, to a programmer,
like a text file wearing a costume. If the symbols were characters rather than pictures, a screen reader could be
taught to say them.</p>

<h2>What we found when we took it apart</h2>
<p>They are characters. The PDF was set in a custom font, and each symbol is a character of that font in the
Unicode Private Use Area, a reserved range that fonts may use for their own glyphs. Extracting the text with the
PDF's own character maps gave the whole New Testament as a stream of those characters, with ordinary verse numbers
and ordinary punctuation. A separately published file of the Epistle of James, in the standard Bible markup format,
uses exactly the same character codes, so the codes are stable across the organisation's materials.</p>
<p>The New Testament uses 1,306 distinct symbols across 162,679 symbol occurrences in 7,955 verses. The hundred
most frequent symbols account for about 73 percent of all occurrences, which matches the organisation's description
of a core of about a hundred symbols plus extensions. Many words are a base symbol followed by a modifier symbol,
written as a separate character, which is good news for a speaking dictionary: a modifier can simply be spoken as a
suffix. Sentence ends are marked by a small hollow circle, the SUN period, the most frequent symbol of all.
The working paper {n38} gives the full account, with the sixteen most frequent symbols described shape by shape.</p>

<h2>Working out what the symbols mean</h2>
<p>No dictionary of SUN has been published. But the New Testament was made verse by verse from an English text we
have, so the meanings can be inferred: a symbol that appears wherever "God" appears, and nowhere else, has named
itself. We paired the 7,955 SUN verses with their English verses and aligned the symbols to English words
statistically, with no help from the organisation. The result: 73 percent of all the words in the text are glossed
with high confidence, another 16 percent with medium confidence, 8 percent low, and 3 percent not at all, mostly
names. The working paper {n39} explains the method and its limits.</p>
<p>The grammar fell out of the data. The most frequent symbols are pronouns and function words: you, I, we, they,
not, and, in, to, if, because, all, many. The crown on a cross is Jesus; the crowned head with a heart is God; Lord
is the symbol for a master with a small arrow added. A filled circle after a word is the possessive: you plus the
circle is your, God plus the circle is God's. Plural is writing a symbol twice: man twice is men. Verbs carry no
tense; time words such as "when" do that work. None of this is written down anywhere public, and a braille reader
will recognise every one of these devices.</p>

<h2>Read James</h2>
<p>Here is the Epistle of James as the dictionary speaks it, every verse, beside the English verse it was made
from. Words in square brackets are low-confidence guesses; a question mark is a symbol we could not gloss. Each
chapter is a table, so a screen reader can move verse by verse and column by column. Read a verse in the middle
column first, then the right-hand column, and you are reading SUN.</p>
{james_tables()}

<h2>Hear it</h2>
<p class="pending">Brian is recording NVDA reading verses of James from the SUN text with the dictionary installed.
The recordings will be added here.</p>

<h2>Make your own screen reader speak SUN</h2>
<p>Install {dic} and any SUN text becomes speech. In NVDA, open your user symbol dictionary, the file named
symbols-en.dic in the NVDA user configuration folder, paste in the lines from the dictionary file, save, and restart
NVDA. Then open a SUN document in Word, Notepad or a browser, with or without the SUN font installed, and NVDA
speaks it word by word: "james god servant period lord jesus christ servant period". The same mapping would give
JAWS a dictionary; we have not built that one.</p>

<h2>What the files are, and what they are not</h2>
<p>Everything we made is in the sun folder of the public repository, under the same Creative Commons
Attribution-ShareAlike licence as the texts it was derived from: the NVDA dictionary, the full inferred gloss table,
the symbol inventory, the New Testament as characters, the New Testament read through the glosses, and the two
scripts that produced them, so the work can be rerun the day a real dictionary appears. The folder's README lists {files}.</p>
<p>Every gloss is a statistical inference, not a reading of the organisation's dictionary, and none has been
confirmed by Wycliffe Associates. Verbs are glossed in whichever English form was most frequent, so "asked" may stand
where "ask" is meant. The SUN font and images of its glyphs are not published here, because the font carries no
stated licence. The right next step is the organisation's own symbol list, which would turn the inferred table into
a cross-check and make all of the New Testament readable, by every blind person with a free screen reader.</p>

<h2>Sources</h2>
<p>The SUN New Testament PDF, published with Wycliffe Associates' permission under CC BY-SA 4.0; the Epistle of
James in SUN as a USFM resource container from Bible Translation Tools, March 2021, CC BY-SA 4.0; the English
Unlocked Literal Bible, CC BY-SA 4.0; the SUN pages at sun.bible and the SUN process page at
bibleineverylanguage.org; Wycliffe Associates' blog and press releases on SUN, 2020 to 2024; and Mission Network
News and The Christian Post reports of February 2020. Each is cited with its link and the date read in the three
working papers above.</p>
"""
