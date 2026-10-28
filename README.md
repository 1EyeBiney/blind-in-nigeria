# Blind in Nigeria (working name)

A public, transparent record of a small ministry effort supporting blind people in Nigeria, beginning with Bethesda Home and School for the Blind in Surulere, Lagos. Built by Brian Clark, who is blind, with Claude Code, in the same way as [Not By Sight](https://blindnessinthebible.com).

**Live site: https://1eyebiney.github.io/blind-in-nigeria/** (the name and domain are provisional)

The site shows what the need is, what we are doing about it, and where every dollar goes. Blind people appear on it as the capable people they are. Faith is present and unforced.

## The site checks its own numbers

No money figure is typed into a page. Every amount is rendered from the files in `data/` by one small module, and a test reads every built page for a dollar or naira figure that did not come that way. Totals are computed from the ledger entries at build time, never stored. Every estimate must carry a source and the date it was last checked. If any of this is broken, **the site does not publish.**

You can run the checks yourself:

```
git clone https://github.com/1EyeBiney/blind-in-nigeria
cd blind-in-nigeria
python -m pytest tests
```

Python 3.12 or later and pytest. Nothing else, and no network once the clone is done.

To rebuild the whole site into a local `site/` folder:

```
python src/build_site.py
```

That is the same command the publish workflow runs. To look at it locally, `python -m http.server 8766 --directory site` and open http://localhost:8766/.

## What is here

| Path | What it holds |
|---|---|
| `data/` | The ledger, goals, exchange rates and estimates every figure renders from; `receipts/` for scanned receipts. See `data/README.md` |
| `source-material/` | Public-safe copies of the documents the figures rest on, brought over one file at a time |
| `src/` | The build: `brand.py` (every name in one place), `build_site.py`, `content.py` (the pages), `money.py`, `ledger.py`, `charts.py`, `display.py` (reading settings) |
| `tests/` | The checks described above, plus accessibility checks on every built page |

## Accessibility

The site is made by a screen-reader user for screen-reader users first: one heading per page in order, landmarks, a skip link, captioned tables with scoped headers, charts announced as graphics and followed by their tables, a reading-settings panel for size, colours, letter style and spacing, and AAA contrast in every colour set, tested on every build. See the Accessibility page on the site.

## What is never published

Bank or account details of anyone. The pay of anyone who works with us. Names, pictures or stories of students or individuals in Nigeria without documented consent. Private notes on partner organizations. The repository stands alone and contains only what is meant to be public.

## If you think something is wrong

Please say so. Write to **brian@blindnessinthebible.com** (no GitHub account needed) or open an [issue](https://github.com/1EyeBiney/blind-in-nigeria/issues). The most useful corrections name the page and quote the sentence.

## Licence

| What | Licence |
|---|---|
| The writing: site pages and `docs/` | [CC BY 4.0](LICENSE) |
| The data in `data/` | [CC BY 4.0](LICENSE) |
| The code: `src/`, `tests/`, the workflow | [MIT](LICENSE-CODE) |
| Documents in `source-material/` and receipts | See [NOTICE](NOTICE) |

### How to cite

> Brian Clark, "Blind in Nigeria" (working name), https://1eyebiney.github.io/blind-in-nigeria/, accessed *date*.
