"""The data behind every figure: the ledger, the goals, the exchange rates and the estimates.

Nothing here is summed in advance. Totals, running totals and progress are computed from the entries each time the
site is built, so the page can never disagree with the data it was built from.
"""
from __future__ import annotations

import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RECEIPTS = DATA / "receipts"

STATUSES = ("example", "pending", "sent", "received")
TYPES = ("grant", "transfer", "purchase")
FILES = ("ledger.json", "goals.json", "rates.json", "estimates.json")
CSV_COLUMNS = ("id", "status", "date", "type", "recipient", "purpose", "usd_cents", "ngn", "rate_ngn_per_usd",
               "fees_usd_cents", "method", "goal", "receipt", "notes")


def _read(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def validate(d: dict) -> None:
    entries = d["ledger"]["entries"]
    ids = [x["id"] for x in entries]
    assert len(ids) == len(set(ids)), "ledger ids must be unique"
    rates = {r["date"]: r["ngn_per_usd"] for r in d["rates"]["rates"]}
    goals = {g["id"] for g in d["goals"]["goals"]}
    for x in entries:
        assert x["status"] in STATUSES, (x["id"], x["status"])
        assert x["type"] in TYPES, (x["id"], x["type"])
        assert isinstance(x["usd_cents"], int) and isinstance(x["ngn"], int), x["id"]
        assert isinstance(x.get("fees_usd_cents", 0), int), x["id"]
        assert x["rate_ngn_per_usd"] in rates.values(), f"{x['id']}: rate {x['rate_ngn_per_usd']} is not in rates.json"
        assert x.get("goal") in goals or x.get("goal") is None, (x["id"], x.get("goal"))
        if x.get("receipt"):
            assert (RECEIPTS / x["receipt"]).is_file(), f"{x['id']}: receipt {x['receipt']} is not in data/receipts/"
        for key in ("total", "progress", "raised"):
            assert key not in x, f"{x['id']}: {key} is computed, never stored"
    for g in d["goals"]["goals"]:
        for key in ("total", "progress", "raised", "given"):
            assert key not in g, f"goal {g['id']}: {key} is computed, never stored"
        assert g.get("source") and g.get("estimate") is not None, g["id"]
    for est in d["estimates"]["estimates"]:
        assert est["usd_cents_lo"] <= est["usd_cents_hi"], est["id"]
        assert est.get("source") and est.get("checked"), est["id"]
    for c in d["estimates"]["counts"]:
        assert isinstance(c["value"], int) and c.get("source") and c.get("checked"), c["id"]


def load() -> dict:
    d = {name.split(".")[0]: _read(name) for name in FILES}
    validate(d)
    return d


def real(entries: list[dict]) -> list[dict]:
    """Entries that describe money that has actually moved. Examples and plans are not among them."""
    return [x for x in entries if x["status"] in ("sent", "received")]


def pending(entries: list[dict]) -> list[dict]:
    return [x for x in entries if x["status"] == "pending"]


def totals(entries: list[dict]) -> dict:
    moved = real(entries)
    return {
        "count": len(moved),
        "usd_cents": sum(x["usd_cents"] for x in moved),
        "fees_usd_cents": sum(x.get("fees_usd_cents", 0) for x in moved),
        "ngn": sum(x["ngn"] for x in moved),
    }


def running(entries: list[dict]) -> list[tuple[dict, int]]:
    """Each real entry, oldest first, with the running total in cents after it."""
    out, total = [], 0
    for x in sorted(real(entries), key=lambda x: (x["date"], x["id"])):
        total += x["usd_cents"]
        out.append((x, total))
    return out


def by_type(entries: list[dict], *types: str) -> list[dict]:
    return [x for x in entries if x["type"] in types]


def progress(goal: dict, entries: list[dict], month: str) -> tuple[int, int]:
    """(given this month in cents, monthly target in cents) for entries tagged with the goal in a YYYY-MM month."""
    given = sum(x["usd_cents"] for x in real(entries) if x.get("goal") == goal["id"] and x["date"].startswith(month))
    return given, goal["monthly_target_usd_cents"]


def to_csv(entries: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CSV_COLUMNS, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    for x in real(entries) + pending(entries):
        w.writerow({k: ("" if x.get(k) is None else x.get(k)) for k in CSV_COLUMNS})
    return buf.getvalue()


def publish(d: dict, out: Path) -> None:
    """Copy the data files, unchanged, and the CSV into site/data/ so a reader can download them."""
    (out / "data").mkdir(parents=True, exist_ok=True)
    for name in FILES:
        (out / "data" / name).write_bytes((DATA / name).read_bytes())
    (out / "data" / "ledger.csv").write_text(to_csv(d["ledger"]["entries"]), encoding="utf-8", newline="\n")
    if RECEIPTS.is_dir():
        (out / "data" / "receipts").mkdir(exist_ok=True)
        for f in RECEIPTS.iterdir():
            if f.is_file() and f.name != ".gitkeep":
                (out / "data" / "receipts" / f.name).write_bytes(f.read_bytes())
