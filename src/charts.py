"""Charts that a screen reader can use. Each one is a small inline SVG with a title and a description, announced as
one graphic, followed at once by a table that carries every figure. No script, no library, colours from the page's
own colour set so dark mode and high contrast carry through.
"""
from __future__ import annotations

import html


def _e(s) -> str:
    return html.escape(str(s), quote=True)


def _table(caption: str, headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f'<th scope="col">{_e(h)}</th>' for h in headers)
    body = "".join("<tr>" + f'<th scope="row">{r[0]}</th>' + "".join(f"<td>{c}</td>" for c in r[1:]) + "</tr>"
                   for r in rows)
    return (f'<div class="table-scroll" role="region" tabindex="0" aria-label="{_e(caption)}, table">'
            f"<table><caption>{_e(caption)}</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>")


def range_bars(cid: str, title: str, desc: str, rows: list[dict], caption: str, headers: list[str],
               fmt=lambda v: str(v)) -> str:
    """Horizontal bars from a low to a high figure, one per row.

    rows: {"label": str, "lo": int, "hi": int, "cells": [html...]} where cells are the table cells after the label
    (already rendered, money included). The chart shows lo..hi; the table shows the cells. fmt returns the label
    for the high value as SVG-safe markup (a tspan), never plain text that a reader could mistake for prose."""
    top = max(r["hi"] for r in rows) or 1
    label_w, w, row_h, pad = 220, 720, 34, 8
    svg = [f'<svg class="chart" role="img" aria-labelledby="{cid}-title {cid}-desc" viewBox="0 0 {w} {row_h * len(rows) + 2 * pad}" '
           f'width="100%" preserveAspectRatio="xMinYMin meet">',
           f'<title id="{cid}-title">{_e(title)}</title><desc id="{cid}-desc">{_e(desc)}</desc>']
    scale = (w - label_w - 90) / top
    for i, r in enumerate(rows):
        y = pad + i * row_h
        x0 = label_w + r["lo"] * scale
        x1 = label_w + r["hi"] * scale
        svg.append(f'<text x="{label_w - 8}" y="{y + 22}" text-anchor="end">{_e(r["label"])}</text>')
        svg.append(f'<rect class="track" x="{label_w}" y="{y + 9}" width="{w - label_w - 90:.0f}" height="16" rx="3"/>')
        svg.append(f'<rect class="bar" x="{x0:.1f}" y="{y + 9}" width="{max(x1 - x0, 3):.1f}" height="16" rx="3"/>')
        svg.append(f'<text x="{x1 + 6:.1f}" y="{y + 22}">{fmt(r["hi"])}</text>')
    svg.append("</svg>")
    table = _table(caption, headers, [[_e(r["label"])] + r["cells"] for r in rows])
    return "\n".join(svg) + "\n" + table


def progress_meter(cid: str, title: str, given: int, target: int, given_html: str, target_html: str,
                   caption: str) -> str:
    """One bar: how far this month's giving has come toward a monthly target, then the figures as a table."""
    pct = 0 if target <= 0 else min(100, round(100 * given / target))
    w, h = 720, 44
    fill = round((w - 80) * pct / 100)
    desc = f"{pct} percent of the monthly target. The table below gives the figures."
    svg = (f'<svg class="chart" role="img" aria-labelledby="{cid}-title {cid}-desc" viewBox="0 0 {w} {h}" width="100%" '
           f'preserveAspectRatio="xMinYMin meet"><title id="{cid}-title">{_e(title)}</title>'
           f'<desc id="{cid}-desc">{_e(desc)}</desc>'
           f'<rect class="track" x="0" y="12" width="{w - 80}" height="20" rx="4"/>'
           f'<rect class="bar" x="0" y="12" width="{fill}" height="20" rx="4"/>'
           f'<text x="{w - 72}" y="28">{pct}%</text></svg>')
    table = _table(caption, ["Measure", "Amount"],
                   [["Given this month toward the goal", given_html], ["Monthly target", target_html],
                    ["Share of target", f"{pct}%"]])
    return svg + "\n" + table
