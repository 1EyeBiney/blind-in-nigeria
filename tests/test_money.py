"""No money figure reaches a page except through money.py, and every estimate says where it came from."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import build_site  # noqa: E402
import money  # noqa: E402

CURRENCY = re.compile(r"[$₦]\s?\d")
MONEY_SPAN = re.compile(r'<(span|tspan) class="money"[^>]*>(.*?)</\1>', re.S)


def test_no_hand_typed_money_in_any_page(tmp_path):
    build_site.render_all(tmp_path)
    for p in tmp_path.rglob("*.html"):
        h = p.read_text(encoding="utf-8")
        for _tag, inner in MONEY_SPAN.findall(h):
            assert "<" not in inner, inner                        # money spans hold text only
        stripped = MONEY_SPAN.sub("", h)
        hit = CURRENCY.search(stripped)
        assert not hit, f"{p.name}: money outside a money span near {stripped[max(0, hit.start() - 60):hit.end() + 40]!r}"


def test_no_money_typed_in_prose_sources():
    for name in ("content.py", "check_our_work.py", "display.py", "whats_new.py", "brand.py"):
        src = (ROOT / "src" / name).read_text(encoding="utf-8")
        assert not CURRENCY.search(src), name
    for name in ("estimates.json", "goals.json"):
        import json
        d = json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))
        for s in re.findall(r'"(?:note|description|label|target_note|comment)": "([^"]*)"', json.dumps(d)):
            assert not CURRENCY.search(s), (name, s)


def test_every_estimate_carries_source_and_checked_date(tmp_path):
    build_site.render_all(tmp_path)
    seen = 0
    for p in tmp_path.rglob("*.html"):
        h = p.read_text(encoding="utf-8")
        for m in re.finditer(r'<span class="estimate">', h):
            end = h.index("</span></span>", m.end())
            block = h[m.start():end]
            assert "(estimate; source: <a href=" in block and "last checked <time datetime=" in block, p.name
            seen += 1
    assert seen >= 5


def test_money_renders_cents_and_naira_plainly():
    assert money._usd_text(128000) == "$1,280" and money._usd_text(30050) == "$300.50" and money._usd_text(450) == "$4.50"
    assert money._ngn_text(399000) == "₦399,000"
    assert 'data-cents="450" data-cents-hi="650"' in money.usd_range(450, 650)
    assert money.usd_range(100, 100) == money.usd(100)


def test_estimate_without_source_or_date_fails():
    import pytest
    with pytest.raises(AssertionError):
        money.estimate({"id": "x", "usd_cents_lo": 1, "usd_cents_hi": 2, "source": "", "checked": "2026-01-01"})
    with pytest.raises(AssertionError):
        money.estimate({"id": "x", "usd_cents_lo": 1, "usd_cents_hi": 2, "source": "a.md", "checked": ""})
