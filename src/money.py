"""Money on the page. Every amount shown on the site passes through here, and nowhere else.

Amounts arrive as whole cents (US dollars) or whole naira, as the data files store them. Each one is wrapped in a
span that carries the raw figure as a data attribute, so a test can scan the built pages and prove that no figure
was typed into prose by hand. Estimates carry their source and the date they were last checked, always.
"""
from __future__ import annotations

import datetime
import html

import brand

RENDERED: set[tuple[str, int]] = set()      # ("usd", cents) or ("ngn", naira) for everything rendered this build


def _e(s) -> str:
    return html.escape(str(s), quote=True)


def _usd_text(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    cents = abs(int(cents))
    dollars, rest = divmod(cents, 100)
    return f"{sign}${dollars:,}" if rest == 0 else f"{sign}${dollars:,}.{rest:02d}"


def _ngn_text(n: int) -> str:
    return f"₦{int(n):,}"


def usd(cents: int) -> str:
    RENDERED.add(("usd", int(cents)))
    return f'<span class="money" data-cents="{int(cents)}">{_usd_text(cents)}</span>'


def usd_svg(cents: int) -> str:
    """The same figure inside an SVG text element, where span is not allowed but tspan is."""
    RENDERED.add(("usd", int(cents)))
    return f'<tspan class="money" data-cents="{int(cents)}">{_usd_text(cents)}</tspan>'


def ngn(n: int) -> str:
    RENDERED.add(("ngn", int(n)))
    return f'<span class="money" data-ngn="{int(n)}">{_ngn_text(n)}</span>'


def usd_range(lo: int, hi: int) -> str:
    if lo == hi:
        return usd(lo)
    RENDERED.update({("usd", int(lo)), ("usd", int(hi))})
    return (f'<span class="money" data-cents="{int(lo)}" data-cents-hi="{int(hi)}">'
            f"{_usd_text(lo)} to {_usd_text(hi)}</span>")


def ngn_range(lo: int, hi: int) -> str:
    if lo == hi:
        return ngn(lo)
    RENDERED.update({("ngn", int(lo)), ("ngn", int(hi))})
    return (f'<span class="money" data-ngn="{int(lo)}" data-ngn-hi="{int(hi)}">'
            f"{_ngn_text(lo)} to {_ngn_text(hi)}</span>")


def pretty_date(iso: str) -> str:
    return datetime.date.fromisoformat(iso).strftime("%d %B %Y").lstrip("0")


def source_link(path: str, title: str | None = None) -> str:
    """A link to a source document in the public repository."""
    if path.startswith("http"):
        return f'<a href="{_e(path)}">{_e(title or path)}</a>'
    return f'<a href="{brand.REPO}/blob/main/{_e(path)}">{_e(title or path)}</a>'


def estimate(est: dict, with_ngn: bool = True) -> str:
    """One estimated figure from data/estimates.json, with its range, its source and when it was last checked.

    The figure itself is rendered through usd_range and ngn_range, so the test that looks for money outside money
    spans is satisfied by the same rule as everywhere else."""
    assert est.get("source") and est.get("checked"), f"estimate {est.get('id')} needs a source and a checked date"
    datetime.date.fromisoformat(est["checked"])          # a real date, or the build fails
    parts = [usd_range(est["usd_cents_lo"], est["usd_cents_hi"])]
    if with_ngn and est.get("ngn_lo") is not None:
        parts.append(f"(about {ngn_range(est['ngn_lo'], est['ngn_hi'])})")
    unit = f" {_e(est['unit'])}" if est.get("unit") else ""
    note = (f'<span class="est-note">(estimate; source: {source_link(est["source"], est.get("source_title"))}; '
            f'last checked <time datetime="{_e(est["checked"])}">{_e(pretty_date(est["checked"]))}</time>)</span>')
    return f'<span class="estimate">{" ".join(parts)}{unit} {note}</span>'


def count(c: dict) -> str:
    """A counted figure (people, canes) from data/estimates.json: the number with its date in a tooltip-free span."""
    assert c.get("source") and c.get("checked"), f"count {c.get('id')} needs a source and a checked date"
    approx = "about " if c.get("approximate") else ""
    return f'<span class="count" data-count="{int(c["value"])}">{approx}{int(c["value"]):,}</span>'
