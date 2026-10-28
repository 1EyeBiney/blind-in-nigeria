"""Checks on the built site: structure a screen reader depends on, colours, the reading panel, what's new, charts."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import build_site  # noqa: E402
import content  # noqa: E402

EXPECTED_PAGES = ["about.html", "accessibility.html", "already.html", "check-our-work.html", "future-studies.html",
                  "help.html", "index.html", "ledger.html", "numbers.html", "story.html", "whats-new.html"]

# Words that must never appear in a built page. Extend as the hard rules in CLAUDE.md require.
FORBIDDEN = ["account number", "routing", "iban", "sort code", "salary", "salaries", "wire details"]


def test_site_builds_and_is_accessible(tmp_path):
    build_site.render_all(tmp_path)
    assert sorted(p.name for p in tmp_path.glob("*.html")) == EXPECTED_PAGES
    assert (tmp_path / ".nojekyll").is_file() and not (tmp_path / "CNAME").exists()   # no domain yet
    for p in sorted(tmp_path.rglob("*.html")):
        h = p.read_text(encoding="utf-8")
        assert '<html lang="en">' in h and h.count("<h1>") == 1, p.name
        assert 'href="#main"' in h and 'id="main"' in h, p.name
        assert h.count('aria-current="page"') == 1, p.name
        assert '<nav aria-label="Site">' in h and "<footer>" in h and '<header class="site">' in h, p.name
        assert re.findall(r"<script[^>]*>", h) == ['<script src="static/display.js">'], p.name
        assert all(re.search(r'\balt="', m) for m in re.findall(r"<img[^>]*>", h)), p.name
        assert "style=" not in h, p.name
        for src in re.findall(r'<img[^>]*\bsrc="([^"]+)"', h):
            assert (p.parent / src).resolve().is_file(), f"{p.name}: missing picture {src}"
        for fig in re.findall(r"<figure.*?</figure>", h, flags=re.S):
            assert "<figcaption>" in fig and re.search(r'alt="[^"]{20,}"', fig), p.name
        for m in re.finditer(r"<iframe[^>]*>", h):
            assert 'title="' in m.group(0), p.name
        for href in re.findall(r'href="([^"#]+)"', h):
            if href.startswith(("http", "mailto:", "tel:")):
                continue
            assert (p.parent / href).resolve().exists(), f"{p.name}: broken link {href}"
        levels = [int(x) for x in re.findall(r"<h([1-6])", h)]
        assert all(b - a <= 1 for a, b in zip(levels, levels[1:])), p.name
        assert h.count("<table>") == h.count("<caption>"), p.name
        for t in re.findall(r"<table>.*?</table>", h, flags=re.S):
            assert 'scope="col"' in t and 'scope="row"' in t, p.name
        assert h.count('class="table-scroll" role="region" tabindex="0" aria-label="') == h.count("<table>"), p.name
        low = h.lower()
        for word in FORBIDDEN:
            assert word not in low, f"{p.name}: forbidden word {word!r}"


def test_navigation_lists_every_page_once():
    assert sorted(href for href, _ in content.NAV) == EXPECTED_PAGES
    assert len({href for href, _ in content.NAV}) == len(content.NAV)


def test_every_chart_is_a_described_graphic_followed_by_its_table(tmp_path):
    build_site.render_all(tmp_path)
    seen = 0
    for p in tmp_path.rglob("*.html"):
        h = p.read_text(encoding="utf-8")
        for m in re.finditer(r"<svg[^>]*>", h):
            tag = m.group(0)
            assert 'role="img"' in tag and 'aria-labelledby="' in tag, p.name
            ids = re.search(r'aria-labelledby="([^"]+)"', tag).group(1).split()
            end = h.index("</svg>", m.end())
            inner = h[m.end():end]
            for i in ids:
                assert f'id="{i}"' in inner, (p.name, i)
            assert "<title " in inner and "<desc " in inner, p.name
            after = h[end + len("</svg>"):].lstrip()
            assert after.startswith('<div class="table-scroll"'), f"{p.name}: chart not followed by its table"
            seen += 1
    assert seen >= 2


def _luminance(hex_colour):
    def chan(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def _contrast(a, b):
    hi, lo = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def test_every_colour_set_meets_enhanced_contrast():
    """WCAG AAA asks 7 to 1 for text. Every colour set meets it for text, quiet text and links, on the page
    background and on the table-head background. Rules and borders meet the 3 to 1 asked of non-text parts."""
    import display
    for name, t in display.THEMES.items():
        for part in ("fg", "muted", "link"):
            for ground in ("bg", "head"):
                assert _contrast(t[part], t[ground]) >= 7, f"{name}: {part} on {ground} is {_contrast(t[part], t[ground]):.2f}"
        assert _contrast(t["rule"], t["bg"]) >= 3, f"{name}: rule on bg"
        assert _contrast(t["link"], t["head"]) >= 3, f"{name}: chart bar on track"
    for name in ("contrast-light", "contrast-dark", "yellow"):
        assert _contrast(display.THEMES[name]["fg"], display.THEMES[name]["bg"]) >= 15, name


def test_reading_settings_panel_is_on_every_page_and_is_labelled(tmp_path):
    import display
    build_site.render_all(tmp_path)
    js = (tmp_path / "static" / "display.js").read_text(encoding="utf-8")
    css = (tmp_path / "static" / "style.css").read_text(encoding="utf-8")
    for key, (legend, choices) in display.OPTIONS.items():
        assert choices[0][0] == "", key
        for value, _ in choices[1:]:
            assert f'data-{key}="{value}"' in css, (key, value)
    assert set(v for v, _ in display.OPTIONS["theme"][1] if v) == set(display.THEMES)
    assert "localStorage" in js and "http" not in js
    for p in tmp_path.rglob("*.html"):
        h = p.read_text(encoding="utf-8")
        panel = h[h.index('<details class="display"'):h.index("</details>", h.index('<details class="display"'))]
        assert " hidden>" in panel.split("<summary>")[0], p.name
        assert panel.count("<fieldset>") == panel.count("<legend>") == len(display.OPTIONS), p.name
        assert panel.count("<label>") == panel.count('type="radio"'), p.name
        assert 'role="status"' in panel and "accessibility.html" in panel, p.name
        assert h.index("</nav>") < h.index('<details class="display"') < h.index('<main id="main">'), p.name


def test_whats_new_is_dated_linked_and_fed(tmp_path):
    import datetime
    import xml.etree.ElementTree as ET
    import whats_new as wn
    build_site.render_all(tmp_path)
    dates = [datetime.date.fromisoformat(d) for d, *_ in wn.ENTRIES]
    assert dates == sorted(dates, reverse=True) and len(wn.ENTRIES) >= 1
    for date, title, text, href in wn.ENTRIES:
        assert (tmp_path / href).is_file(), href
        assert title and len(text) > 30 and not text.endswith(" ")
    h = (tmp_path / "whats-new.html").read_text(encoding="utf-8")
    assert h.count('<li data-date="') == len(wn.ENTRIES) and 'role="status"' in h and "feed.xml" in h
    assert 'id="nav-whats-new" data-latest="' + wn.ENTRIES[0][0] + '"' in h
    root = ET.fromstring((tmp_path / "feed.xml").read_text(encoding="utf-8"))
    assert len(root.findall("./channel/item")) == len(wn.ENTRIES)
    home = (tmp_path / "index.html").read_text(encoding="utf-8")
    assert 'type="application/rss+xml"' in home and "bin-visit" in (tmp_path / "static" / "display.js").read_text(encoding="utf-8")


def test_no_student_is_named_and_the_representative_is_a_role(tmp_path):
    """Until consents exist, no page names a student; the representative is referred to by role only."""
    import brand
    build_site.render_all(tmp_path)
    assert brand.REPRESENTATIVE.startswith("our ")
    for p in tmp_path.rglob("*.html"):
        h = p.read_text(encoding="utf-8")
        assert re.search(r"Jay", h) is None, p.name     # first name of the representative, by agreement not yet used
