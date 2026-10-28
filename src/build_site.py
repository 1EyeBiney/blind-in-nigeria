"""Build the site into site/. Standard library only.

Screen reader first: one h1 per page, headings in order, a skip link, landmarks, real tables with captions and
scoped headers, charts followed by their tables, nothing conveyed by colour alone, and no script the page needs.
Every money figure comes from data/ through money.py.

    python src/build_site.py        -> writes site/
"""
from __future__ import annotations

import html
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
OUT = ROOT / "site"

import brand  # noqa: E402
import check_our_work  # noqa: E402
import content  # noqa: E402
import display  # noqa: E402
import ledger as lg  # noqa: E402
import money  # noqa: E402
import whats_new  # noqa: E402

CSS = display.theme_css() + """
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); color:var(--fg); font: 1.125rem/1.6 Georgia, "Times New Roman", serif; }
.wrap { max-width: 60rem; margin: 0 auto; padding: 0 1rem; }
a { color: var(--link); text-decoration: underline; text-decoration-thickness: .08em; text-underline-offset: .15em; }
a:hover { text-decoration-thickness: .16em; }
:focus-visible { outline: 3px solid var(--link); outline-offset: 2px; }
.skip { position:absolute; left:-999px; }
.skip:focus { position:static; display:inline-block; padding:.5rem; font-weight:bold; }
main p, main li, main blockquote, main dd { max-width: 44rem; }
img { max-width: 100%; height: auto; }
header.site { border-bottom: 2px solid var(--rule); padding: 1rem 0; }
header.site .brand { display: flex; align-items: center; gap: .75rem; }
header.site img.emblem { width: 3rem; height: 3rem; flex: none; }
header.site p.name { font-size: 1.5rem; font-weight: bold; margin: 0; }
header.site p.tag { margin: 0; color: var(--muted); }
header.site p.notice { margin: .75rem 0 0; padding: .5rem .75rem; border: 1px dashed var(--rule); color: var(--muted); font-size: 1rem; max-width: 44rem; }
nav ul { list-style: none; padding: 0; margin: .5rem 0 0; display: flex; flex-wrap: wrap; gap: .25rem 1rem; }
nav a { display: inline-block; padding: .2rem 0; }
nav a[aria-current="page"] { font-weight: bold; text-decoration-thickness: .16em; }
h1 { font-size: 2rem; line-height: 1.25; }
h2 { font-size: 1.5rem; margin-top: 2.5rem; border-top: 1px solid var(--rule); padding-top: 1rem; }
h3 { font-size: 1.2rem; }
.lede { font-size: 1.25rem; }
section.door { border: 2px solid var(--rule); border-radius: .35rem; padding: 0 1rem 1rem; margin: 1.5rem 0; }
section.door h2 { border-top: 0; margin-top: 1rem; padding-top: 0; }
p.pending { border: 1px dashed var(--rule); padding: .75rem; color: var(--muted); }
.estimate .est-note { color: var(--muted); font-size: .95em; }
.money, .count { white-space: nowrap; }
ol.changes { list-style: none; padding: 0; }
ol.changes li { margin: 0 0 1.25rem; padding-left: 1rem; border-left: 4px solid var(--rule); }
ol.changes time { color: var(--muted); font-size: 1rem; display: block; }
ol.changes .new-mark { font-weight: bold; }
ol.changes li.is-new { border-left-color: var(--link); }
blockquote { margin: 1rem 0; padding: .25rem 1rem; border-left: 4px solid var(--rule); }
code { font-family: ui-monospace, Consolas, "Courier New", monospace; font-size: .95em; background: var(--head); padding: .1rem .3rem; }
pre { background: var(--head); border: 1px solid var(--rule); padding: .75rem; overflow-x: auto; font-size: 1rem; }
pre code { background: none; padding: 0; }
.table-scroll { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
caption { text-align: left; font-weight: bold; padding: .5rem 0; }
th, td { border: 1px solid var(--rule); padding: .5rem; text-align: left; vertical-align: top; }
thead th { background: var(--head); }
svg.chart { display: block; max-width: 48rem; margin: 1rem 0 0; font-family: Georgia, "Times New Roman", serif; }
svg.chart text { fill: var(--fg); font-size: 15px; }
svg.chart .track { fill: var(--head); stroke: var(--rule); stroke-width: 1; }
svg.chart .bar { fill: var(--link); }
@media (forced-colors: active) { details.display summary, thead th { border: 2px solid CanvasText; }
  svg.chart .bar { fill: CanvasText; } svg.chart .track { fill: Canvas; stroke: CanvasText; } svg.chart text { fill: CanvasText; } }
footer { border-top: 2px solid var(--rule); margin-top: 3rem; padding: 1rem 0 2rem; color: var(--muted); font-size: 1rem; }
""" + display.CSS


def e(s) -> str:
    return html.escape(str(s), quote=True)


def page(title: str, body: str, current: str, root: str = "") -> str:
    links = "".join(
        f'<li><a href="{root}{href}"{" aria-current=\"page\"" if href == current else ""}'
        f'{" id=\"nav-whats-new\" data-latest=\"" + whats_new.ENTRIES[0][0] + "\"" if href == whats_new.SLUG else ""}>{e(label)}</a></li>'
        for href, label in content.NAV)
    notice = ('<p class="notice">A new site, still being built. Its name is provisional and giving is not yet open; '
              'what is here is true as far as we know it, and dated.</p>' if brand.PROVISIONAL else "")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | {e(brand.SITE_NAME)}</title>
<meta name="description" content="{e(brand.TAGLINE)}.">
<link rel="icon" href="{root}media/emblem.svg" type="image/svg+xml">
<meta property="og:site_name" content="{e(brand.SITE_NAME)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)} | {e(brand.SITE_NAME)}">
<meta property="og:description" content="{e(brand.TAGLINE)}.">
<link rel="alternate" type="application/rss+xml" title="{e(brand.SITE_NAME)}: what's new" href="{root}feed.xml">
<link rel="stylesheet" href="{root}static/style.css">
<script src="{root}static/display.js"></script>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header class="site"><div class="wrap">
<div class="brand"><img class="emblem" src="{root}media/emblem.svg" alt="" width="48" height="48">
<div><p class="name">{e(brand.SITE_NAME)}</p>
<p class="tag">{e(brand.TAGLINE)}</p></div></div>
<nav aria-label="Site"><ul>{links}</ul></nav>
{notice}
{display.panel_html(root)}
</div></header>
<main id="main"><div class="wrap">
{body}
</div></main>
<footer><div class="wrap">
<p>This site is the work of Brian Clark and friends, and we count it a gift from God through us. So it is given on:
free to copy, quote and share, under a <a href="https://creativecommons.org/licenses/by/4.0/">Creative Commons
Attribution licence</a>. The data is public too. The rest is on <a href="{root}check-our-work.html">Check our work</a>.</p>
<p>Nothing here names a student, shows a bank detail, or states anyone's pay, by rule. If you find otherwise, write to
<a href="mailto:{e(brand.CONTACT_EMAIL)}">{e(brand.CONTACT_EMAIL)}</a>.</p>
</div></footer>
</body>
</html>
"""


def whats_new_page() -> str:
    import datetime
    wn = whats_new
    parts = [f"<h1>{e(wn.TITLE)}</h1>", f'<p class="lede">{e(wn.INTRO[0])}</p>'] + [f"<p>{e(x)}</p>" for x in wn.INTRO[1:]]
    parts.append('<p id="whats-new-status" role="status"></p>')
    parts.append('<p><button type="button" id="whats-new-mark" hidden>Mark everything as read</button> '
                 f'<a href="{wn.FEED}">Follow this page as an RSS feed</a>.</p>')
    parts.append('<ol class="changes" id="changes">')
    for date, title, text, href in wn.ENTRIES:
        pretty = datetime.date.fromisoformat(date).strftime("%d %B %Y").lstrip("0")
        parts.append(f'<li data-date="{date}"><time datetime="{date}">{e(pretty)}</time>'
                     f'<b>{e(title)}.</b> {e(text)} <a href="{e(href)}">Go to the page</a>.</li>')
    parts.append("</ol>")
    return "\n".join(parts)


def feed_xml() -> str:
    import datetime
    wn = whats_new
    items = []
    for date, title, text, href in wn.ENTRIES:
        d = datetime.datetime.fromisoformat(date).replace(tzinfo=datetime.timezone.utc)
        items.append(f"<item><title>{e(title)}</title><link>{wn.SITE}{e(href)}</link>"
                     f"<guid isPermaLink=\"false\">{date}-{e(href)}</guid>"
                     f"<pubDate>{d.strftime('%a, %d %b %Y 00:00:00 +0000')}</pubDate>"
                     f"<description>{e(text)}</description></item>")
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>{e(brand.SITE_NAME)}: what\'s new</title>'
            f"<link>{wn.SITE}{wn.SLUG}</link><description>{e(brand.TAGLINE)}. Changes to the site, newest first.</description>"
            f"<language>en</language>{''.join(items)}</channel></rss>\n")


def render_all(out: Path = OUT, data: dict | None = None) -> None:
    d = data or lg.load()
    money.RENDERED.clear()
    out.mkdir(parents=True, exist_ok=True)
    if brand.DOMAIN:
        (out / "CNAME").write_text(brand.DOMAIN + "\n", encoding="utf-8", newline="\n")
    (out / "static").mkdir(exist_ok=True)
    media = ROOT / "media"
    if media.is_dir():
        (out / "media").mkdir(exist_ok=True)
        for f in media.iterdir():
            if f.is_file():
                shutil.copy(f, out / "media" / f.name)
    (out / "static" / "style.css").write_text(CSS, encoding="utf-8")
    (out / "static" / "display.js").write_text(display.script(), encoding="utf-8", newline="\n")
    lg.publish(d, out)
    for slug, title, build in content.PAGES:
        (out / slug).write_text(page(title, build(d), slug), encoding="utf-8")
    (out / display.SLUG).write_text(page(display.TITLE, display.body(brand.CONTACT_EMAIL), display.SLUG), encoding="utf-8")
    (out / check_our_work.SLUG).write_text(page(check_our_work.TITLE, check_our_work.body(), check_our_work.SLUG), encoding="utf-8")
    (out / whats_new.SLUG).write_text(page(whats_new.TITLE, whats_new_page(), whats_new.SLUG), encoding="utf-8")
    (out / whats_new.FEED).write_text(feed_xml(), encoding="utf-8", newline="\n")
    (out / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    render_all()
    print(f"Site written to {OUT}")
