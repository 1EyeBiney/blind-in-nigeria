"""The ledger: totals are computed, examples never show, real entries show with rate, receipt and running total."""
import copy
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import build_site  # noqa: E402
import ledger as lg  # noqa: E402


def test_data_loads_and_validates():
    d = lg.load()
    assert d["ledger"]["entries"] and d["goals"]["goals"] and d["rates"]["rates"] and d["estimates"]["estimates"]
    for name in ("ledger.json", "goals.json"):
        text = (ROOT / "data" / name).read_text(encoding="utf-8")
        for key in ('"total"', '"progress"', '"raised"'):
            assert key not in text, (name, key)


def test_totals_are_computed_from_entries():
    d = lg.load()
    entries = d["ledger"]["entries"] + [
        {"id": "t1", "status": "sent", "date": "2026-11-01", "type": "grant", "recipient": "X", "purpose": "food",
         "usd_cents": 10000, "ngn": 1330000, "rate_ngn_per_usd": 1330, "fees_usd_cents": 250, "method": "m", "goal": "third-meal"},
        {"id": "t2", "status": "received", "date": "2026-11-05", "type": "purchase", "recipient": "X", "purpose": "canes",
         "usd_cents": 5000, "ngn": 665000, "rate_ngn_per_usd": 1330, "fees_usd_cents": 0, "method": "m"},
        {"id": "t3", "status": "pending", "date": "2026-12-01", "type": "grant", "recipient": "X", "purpose": "food",
         "usd_cents": 99999, "ngn": 1, "rate_ngn_per_usd": 1330, "fees_usd_cents": 0, "method": "m"},
    ]
    t = lg.totals(entries)
    assert t == {"count": 2, "usd_cents": 15000, "fees_usd_cents": 250, "ngn": 1995000}
    assert [total for _, total in lg.running(entries)] == [10000, 15000]
    assert lg.progress({"id": "third-meal", "monthly_target_usd_cents": 140000}, entries, "2026-11") == (10000, 140000)
    assert lg.progress({"id": "third-meal", "monthly_target_usd_cents": 140000}, entries, "2026-12") == (0, 140000)


def test_example_entries_never_render_as_real(tmp_path):
    d = lg.load()
    build_site.render_all(tmp_path, d)
    h = (tmp_path / "ledger.html").read_text(encoding="utf-8")
    assert "No money has moved yet" in h
    for x in d["ledger"]["entries"]:
        if x["status"] == "example":
            assert x["id"] not in h and x["purpose"] not in h, x["id"]
    rows = list(csv.DictReader((tmp_path / "data" / "ledger.csv").open(encoding="utf-8")))
    assert rows == []


def test_a_real_entry_renders_with_rate_receipt_and_running_total(tmp_path, monkeypatch):
    receipts = tmp_path / "receipts"
    receipts.mkdir()
    (receipts / "2026-11-01-r1.pdf").write_bytes(b"%PDF-1.4 test")
    monkeypatch.setattr(lg, "RECEIPTS", receipts)
    d = copy.deepcopy(lg.load())
    d["ledger"]["entries"] += [
        {"id": "r1", "status": "received", "date": "2026-11-01", "type": "grant", "recipient": "Bethesda Home and School for the Blind",
         "purpose": "Food, trial month", "usd_cents": 30000, "ngn": 399000, "rate_ngn_per_usd": 1330, "fees_usd_cents": 350,
         "method": "bank transfer to the organization", "goal": "third-meal", "receipt": "2026-11-01-r1.pdf", "notes": ""},
        {"id": "r2", "status": "sent", "date": "2026-11-20", "type": "purchase", "recipient": "Bethesda Home and School for the Blind",
         "purpose": "Forty long white canes", "usd_cents": 36000, "ngn": 478800, "rate_ngn_per_usd": 1330, "fees_usd_cents": 0,
         "method": "paid to a Lagos seller", "goal": None, "receipt": None, "notes": ""},
        {"id": "p1", "status": "pending", "date": "2026-12-01", "type": "grant", "recipient": "Bethesda Home and School for the Blind",
         "purpose": "Food, second month", "usd_cents": 30000, "ngn": 399000, "rate_ngn_per_usd": 1330, "fees_usd_cents": 0,
         "method": "bank transfer to the organization", "goal": "third-meal", "receipt": None, "notes": ""},
    ]
    lg.validate(d)
    out = tmp_path / "site"
    build_site.render_all(out, d)
    h = (out / "ledger.html").read_text(encoding="utf-8")
    assert "No money has moved yet" not in h
    assert 'data-cents="66000"' in h            # the total and the final running total
    assert h.count('data-cents="30000"') >= 2 and 'data-cents="36000"' in h and 'data-cents="350"' in h
    assert 'data-ngn="1330"' in h and 'href="data/receipts/2026-11-01-r1.pdf"' in h
    assert (out / "data" / "receipts" / "2026-11-01-r1.pdf").is_file()
    assert "Planned, not yet sent" in h and "Food, second month" in h
    rows = list(csv.DictReader((out / "data" / "ledger.csv").open(encoding="utf-8")))
    assert [r["id"] for r in rows] == ["r1", "r2", "p1"]
    for name in lg.FILES:
        assert (out / "data" / name).read_bytes() == (ROOT / "data" / name).read_bytes()
    goals = json.loads((out / "data" / "goals.json").read_text(encoding="utf-8"))
    assert goals["goals"][0]["id"] == "third-meal"


def test_a_bad_entry_is_refused():
    import pytest
    d = copy.deepcopy(lg.load())
    d["ledger"]["entries"].append({"id": "bad", "status": "sent", "date": "2026-11-01", "type": "grant", "recipient": "X",
                                   "purpose": "p", "usd_cents": 100, "ngn": 1, "rate_ngn_per_usd": 999, "fees_usd_cents": 0,
                                   "method": "m"})
    with pytest.raises(AssertionError):
        lg.validate(d)
    d = copy.deepcopy(lg.load())
    d["ledger"]["entries"].append({"id": "bad2", "status": "sent", "date": "2026-11-01", "type": "grant", "recipient": "X",
                                   "purpose": "p", "usd_cents": 100, "ngn": 1330, "rate_ngn_per_usd": 1330, "fees_usd_cents": 0,
                                   "method": "m", "receipt": "missing.pdf"})
    with pytest.raises(AssertionError):
        lg.validate(d)
