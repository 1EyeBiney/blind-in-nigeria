# SUN Glossed: The New Testament Read by Statistics

Prepared for Brian, October 16, 2026, continuing "SUN Taken Apart." With the English ULB in hand (Wycliffe Associates' own copy, the text SUN was made from), the 7,955 SUN verses were paired with their English verses (7,953 matched; the two leftovers are versification differences) and the symbols were aligned to English words statistically, with no help from the organization. Files are in wycliffe_associates/sun_data.

## What came out

SUN has 5,057 distinct "words" in the New Testament, where a word is a space-separated group of one or more symbols. For each, the alignment proposes an English gloss with a confidence level. The result: 73 percent of all words in the text are now glossed with high confidence, another 16 percent with medium confidence, 8 percent low, and 3 percent not at all. Reading James 1 through those glosses gives, for example: "my brothers . when you have many [plagues] . think joy ." where the ULB has "Consider it all joy, my brothers, when you experience various troubles," and "if you need wisdom asked god . god give many . person asked god not rebuked . god give wisdom to person ." for James 1:5. That is readable, and it is the first time a hearing blind person has been able to read SUN at all.

The grammar fell out of the data as a bonus, and it is simpler than the organization's description suggested.

Pronouns and function words are the most frequent symbols: U+E314 is you (the circle with a tail), U+E166 is I, U+E167 is we, U+E125 is they, U+E17C (the X) is not, U+E11C (two triangles) is and, U+E240 (the framed picture) is in, U+E318 (the arrow) is to, U+E111 is if, U+E066 is because, U+E251 is all, U+E198 is many.

The crown-cross U+E037 is Jesus, not Lord; the crowned head with a heart, U+E036, is God. Lord is the base symbol U+E028 (master, king) with the small arrow-and-dot modifier U+ED11. Christ is U+E334, Paul is U+E377.

The filled circle U+E390 is the possessive: you plus circle is your, I plus circle is my, we plus circle is our, God plus circle is God's. It is a true suffix character, never a word on its own.

Plural is reduplication, writing the symbol twice: U+E105 twice is things, U+E142 twice is disciples, U+E000 (man) twice is men. This is the kind of rule that a braille reader will recognize instantly and that nobody has written down in public.

Verbs are concepts without tense: U+E03F is said or say, U+E25A is came or come, U+E381 is went or go, U+E062 is know or knew, U+E086 is give or gave. Tense is carried by context or by time words such as U+E16A, when.

## Files

sun_gloss_inferred.csv: every SUN word, its code points, its count, the proposed gloss and two alternates, the alignment score, and a confidence rating. This is the dictionary the organization has not published, with the caveat that it is inferred.

sun-symbols-nvda.dic: an NVDA symbol-pronunciation file with 596 single-symbol entries (high and medium confidence), 43 common compound words (your, my, our, Lord, things, disciples, men, and so on) as complex symbols, the period, and the possessive suffix. Copy its lines into the user symbol dictionary (symbols-en.dic in the NVDA user configuration folder) and restart NVDA; then any SUN text displayed in the SUN font, or even without it, is spoken word by word. This is the deliverable to demonstrate.

sun_nt_glossed.txt: the whole New Testament as gloss lines with the ULB beneath each verse, 1.8 megabytes, readable with any screen reader today. james1_glossed.txt is the one-chapter sample.

parse_sun.py and align.py: the two scripts, so the work can be rerun when the organization supplies a real dictionary or the Old Testament.

## Caveats, stated plainly

Every gloss is a statistical inference from co-occurrence, not a reading of the organization's dictionary. High-confidence entries are almost certainly right; medium ones are usually right; low ones are guesses, and the 3 percent unglossed are mostly names and rare words. Verbs are glossed in whichever English form was most frequent, so "asked" may stand where "ask" is meant. Compound words beyond the 43 most common are glossed only as wholes in the CSV, not in the NVDA file. And none of this has been seen by anyone at Wycliffe Associates. When they supply the real inventory, the scripts regenerate everything in minutes and the inferred file becomes a cross-check on theirs rather than a substitute.

## What to show Wycliffe Associates

James 1:5 spoken by NVDA from a SUN text, then the sentence: the SUN New Testament contains 1,306 symbols and about 5,000 words, we can already read three quarters of it with no dictionary from you, and with your dictionary we can read all of it and so can every blind person with a free screen reader. Then the ask: the dictionary, the font, and the USFM sources.
