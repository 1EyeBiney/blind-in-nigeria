# SUN Taken Apart: What the Published New Testament Contains

Prepared for Brian, October 16, 2026, from the SUN New Testament PDF (freechristianebooks.org, Creative Commons BY-SA 4.0) and the James USFM file from Bible Translation Tools, both supplied by Brian. Everything below was computed, not read from a description; the working files are in wycliffe_associates/sun_data.

## The findings, in order of importance

SUN is already a Unicode text, not a picture. The PDF was made in LibreOffice in February 2020 from a document set in a font called SUN7_24. Each symbol is a character of that font, and the PDF's own character maps assign every symbol a Unicode Private Use Area code point in the range U+E000 to U+ED12. Extracting the text with those maps yields the whole New Testament as a stream of PUA characters with ordinary verse numbers and ordinary punctuation. The James USFM file from Bible Translation Tools uses exactly the same code points; James 1:1 extracted from the PDF and James 1:1 in the USFM match symbol for symbol. So Wycliffe Associates' internal representation of SUN is a Private Use Area font, which is the best possible case for a screen reader: NVDA's symbol dictionary mechanism handles PUA characters directly, and a SUN document in Word or a browser, with the font installed, is already text that a dictionary can speak.

The inventory. The New Testament uses 1,306 distinct symbols across 162,679 symbol occurrences in 7,955 verses (the complete New Testament, which has 7,957 in most reckonings; two were likely merged by the layout). Of the 1,306, 178 occur only once and 257 occur a hundred times or more; the hundred most frequent symbols account for 72.6 percent of all occurrences. That matches the organization's description of a core of about a hundred symbols plus extensions: a learner who knows the top hundred can follow most of the text, and the long tail is names, places, and rare concepts.

Word structure. Spaces between words are not reliably in the text stream (the layout program positioned words by spacing rather than by space characters), so word boundaries were recovered from the geometry of the glyphs and checked against the USFM, which does carry spaces; the two agree. Words are mostly a single symbol, but many are a base symbol followed by a modifier symbol: James 1:1 contains "E036 E390" and "E334 E390" (a base plus the filled-circle modifier U+E390, the second most frequent symbol in the whole text) and "E028 ED11" (a base plus the small arrow-with-dot modifier U+ED11, which attaches to the symbol used where English has "God"). The modifiers are how "extensions" are written: they are separate characters, not separate glyph designs, which is good news for a speaking dictionary because a modifier can simply be spoken as a suffix.

Punctuation. Sentence and clause ends are marked by a small hollow circle, U+E37E, the most frequent symbol by far (22,872 occurrences, one or more per verse). Commas, question marks, and quotation marks are ordinary Latin characters set in an ordinary font. Verse numbers are red Arabic numerals in a separate font; chapters are not numbered in the text and were recovered from the verse-number resets. The layout is two columns per page, read left to right, 506 pages.

## The sixteen most frequent symbols, described

These descriptions are from the rendered glyphs and are shape descriptions only; meanings are not known yet, except where the James verse makes one nearly certain. The number is the count in the New Testament.

U+E37E, 22,872: a small hollow circle at the baseline. Sentence or clause end, the SUN period.

U+E390, 6,073: a solid filled circle. A modifier that follows a base symbol to form a word; never a word on its own.

U+E314, 5,371: a circle with a straight line running out from its top to the right, like a lowercase sigma or a key. Very common on its own; a candidate for a pronoun or a grammatical particle.

U+E166, 4,191: a circle with a line entering from the left at the top, with a small tick mark after it; related in shape to E314 and to E167 below.

U+E037, 3,740: a crown sitting on top of a vertical post with a crossbar, like a crowned cross. In James 1:1 it stands where English has "Lord."

U+E17C, 3,637: a large X of two diagonal strokes.

U+E03F, 3,452: a plain hollow square.

U+E036, 2,905: a head in profile wearing a crown, with a heart drawn on it. In James 1:1 "E036 E390" stands where English has "servant," which suggests the crowned head is a status or role base and the circle modifier changes it; this is the kind of pair the gloss table has to settle.

U+E125, 2,770: a stick figure of a person with arms raised and legs apart.

U+E127, 2,288: two tall narrow figures side by side with a dot after them; likely a plural or group form of a person symbol.

U+E11C, 2,054: two hollow triangles side by side, overlapping slightly, like two peaks.

U+E167, 2,015: two small circles stacked, each with a line to the left, with a tick; the same family as E166 and E314.

U+E240, 2,002: a tall rectangle containing a small triangle and a dot, like a framed picture or a doorway with something inside.

U+E000, 1,995: a bracket-like shape, a vertical bar with short horizontal arms and dashes to its right.

U+ED11, 1,925: a small upward arrow with a dot beside it, drawn high and small. A modifier; it follows U+E028 where English has "God."

U+E318, 1,839: a plain arrow pointing right.

## What this makes possible now

A speaking dictionary is a mapping from 1,306 code points to words. We have the code points, their frequencies, an image of every one, and the entire New Testament aligned by verse. What we do not have is the meanings. There are two ways to get them, and both are now mechanical. The honest way is to ask Wycliffe Associates for the symbol dictionary or the font's glyph names; a single spreadsheet from them finishes the job. The independent way is alignment: with the English ULB (or any verse-aligned English Bible) beside the 7,955 SUN verses, a symbol that occurs wherever "God" occurs and nowhere else identifies itself, and the top few hundred symbols will resolve this way with high confidence. The SUN Lessons app, if its assets are examined, would confirm the core hundred directly. Inferred glosses should be labeled as inferred until the organization confirms them.

Once glosses exist, the first deliverable is a few hours' work: an NVDA symbol-pronunciation file that speaks each PUA character, so that James opened in Notepad with the SUN font installed reads aloud as "James servant-[modifier] ... Lord ... God ...". From there a small add-on can speak base-plus-modifier pairs as single words and handle the period.

## Files

sun_data/sun_symbol_inventory.csv: every symbol, its code point, count, first page, and glyph size. sun_data/sun_nt_verses.json: the New Testament as book, chapter, verse, and symbol text with word spaces, 7,955 records. sun_data/glyphs/all: one PNG per symbol, named by code point. sun_data/glyphs/top16_sheet.png and page12.png: a labeled sheet of the sixteen most frequent symbols and a sample page for sighted helpers. sources/extracted_fonts: the six Type 1 subsets and one TrueType subset as embedded in the PDF, with the glyph-to-code maps; the glyph names inside them are placeholders ("bad1234"), so the meanings are not in the font files.

## What to ask Wycliffe Associates, now with specifics

The SUN7_24 font file itself (the PDF carries only subsets). The symbol dictionary, or the font's glyph-name table, which would give meanings for all 1,306 code points at once. The USFM source for the other 26 books, since James shows they exist. And whether the code-point assignments are stable across their materials, which the James file suggests they are.
