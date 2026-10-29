# Reading SUN: the data files

Symbolic Universal Notation (SUN) is Wycliffe Associates' symbol-based Scripture for Deaf and Deaf-Blind readers.
Its New Testament is published as a PDF under Creative Commons Attribution-ShareAlike 4.0, and the Epistle of James
is published as a USFM file under the same licence by Bible Translation Tools. The English Unlocked Literal Bible
(ULB), the text SUN was made from, is also CC BY-SA 4.0.

The files here were derived from those three sources on 16 October 2026 and are published under the same licence,
CC BY-SA 4.0, as the licence requires. The page that explains them is reading-sun.html on the site.

| File | What it is |
|---|---|
| `sun-symbols-nvda.dic` | NVDA symbol-pronunciation entries: 596 single symbols, 43 common compound words, the period and the possessive suffix. Copy the lines into your user symbol dictionary (`symbols-en.dic` in the NVDA user configuration folder) and restart NVDA. |
| `sun_gloss_inferred.csv` | Every SUN word in the New Testament (5,057), its code points, count, proposed English gloss, two alternates, alignment score and confidence. |
| `sun_symbol_inventory.csv` | Every one of the 1,306 symbols: code point, count, first page, glyph size. |
| `sun_nt_verses.json` | The New Testament as book, chapter, verse and SUN text (Private Use Area characters with word spaces), 7,955 records. |
| `sun_nt_glossed.txt` | The whole New Testament read through the glosses, with the ULB verse beneath each SUN verse. |
| `james_glossed.txt` | The Epistle of James alone, in the same form. |
| `parse_sun.py`, `align.py` | The two scripts that produced everything above from the PDF, the USFM and the ULB. Paths inside them are the ones used on the machine that ran them. |

Every gloss is a statistical inference from where symbols and English words occur together. None has been confirmed
by Wycliffe Associates. High-confidence entries are almost certainly right, medium ones usually, low ones are
guesses, and words marked unknown are mostly names. When a confirmed dictionary exists, the scripts regenerate
these files from it.

Not included, deliberately: the SUN font, the font subsets embedded in the PDF, and images of the glyphs. The font
carries no stated licence, so those stay out until Wycliffe Associates says otherwise.
