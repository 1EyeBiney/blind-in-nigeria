"""The pages, as functions that take the loaded data and return the HTML inside <main>.

Rules for prose here: the voice is "we"; blind people are capable people, never objects of pity; no student is
named or pictured; no money figure is typed, every one comes through money.py from the data files; estimates say
they are estimates. Brian approves all public wording.
"""
from __future__ import annotations

import datetime
import html

import brand
import charts
import ledger as lg
import money as m

NAV = [
    ("index.html", "Home"),
    ("story.html", "The story"),
    ("already.html", "What blind Nigerians already do"),
    ("numbers.html", "The numbers"),
    ("ledger.html", "The ledger"),
    ("help.html", "How to help"),
    ("future-studies.html", "Future studies"),
    ("check-our-work.html", "Check our work"),
    ("whats-new.html", "What's new"),
    ("accessibility.html", "Accessibility"),
    ("about.html", "About"),
]

FUTURE_STUDIES = [
    ("How blind Nigerians make a living, and what the begging figures really say",
     "A figure often repeated is that most blind people in Nigeria beg to survive. When we went looking for its source "
     "in October 2026 we did not find a national study behind it. A 2010 paper found that about seven in ten of the "
     "beggars counted in Lagos were blind, which is a statement about beggars, not about blind people; a small survey "
     "in one city found most of its blind participants begged; and fundraising pages repeat larger figures with no "
     "source at all. We will not use the sentence until we can stand behind it. This study will set out what is "
     "actually known, from the national blindness survey and from the people who live it."),
    ("Why people are blind in Nigeria",
     "Cataract, glaucoma, river blindness in the countryside, and what the harmattan dust does and does not do. The "
     "Nigeria National Blindness and Visual Impairment Survey is the starting point."),
    ("Education for blind children in Nigeria, and where Bethesda fits",
     "The schools that exist, who runs them, how they are funded, and what a blind-led school does differently."),
    ("The white cane: what it costs in Lagos and why it wears out",
     "Potholes and public buses break canes. We will publish what a long cane costs from Lagos sellers, with the "
     "listings, and compare it with shipping canes from the United States."),
    ("Screen readers and phones in Nigeria",
     "Smartphones have replaced recorders at Bethesda. What free screen readers offer, why there is no Yoruba voice "
     "yet, and what remote teaching from Indianapolis can and cannot do."),
    ("How money reaches Nigeria, and what it costs on the way",
     "Transfer services, bank rates against street rates, and fees. The ledger shows every rate we used; this study "
     "will explain the choices."),
    ("Bethesda's church life and the Redeemed Christian Church of God",
     "Bethesda worships with the RCCG, one of the largest churches to come out of Nigeria. What that means for the "
     "home, and for us."),
]


def e(s) -> str:
    return html.escape(str(s), quote=True)


def est(d: dict, eid: str) -> dict:
    return next(x for x in d["estimates"]["estimates"] if x["id"] == eid)


def cnt(d: dict, cid: str) -> dict:
    return next(x for x in d["estimates"]["counts"] if x["id"] == cid)


def c(d: dict, cid: str) -> str:
    return m.count(cnt(d, cid))


def goal(d: dict, gid: str) -> dict:
    return next(g for g in d["goals"]["goals"] if g["id"] == gid)


def this_month() -> str:
    return datetime.date.today().strftime("%Y-%m")


# ----------------------------------------------------------------------------------------------- home

def home(d: dict) -> str:
    per = est(d, "third-meal-per-child-monthly")
    return f"""<h1>A school in Lagos run by blind people, and the meal it had to cut</h1>
<p class="lede">{e(brand.PARTNER)}, in {e(brand.PARTNER_PLACE)}, is a home and school where nearly everyone,
staff included, is blind. About {c(d, "boarders")} blind children board there. This year the home had to cut their
meals from {c(d, "meals-before")} a day to {c(d, "meals-now")}. We are a small group of friends in Indiana, led by a
blind man, working to help restore the third meal and to show what blind Nigerians already do when they have the
means.</p>
<p>Restoring a third meal for one child costs {m.estimate(per, with_ngn=False)}.</p>

<section class="door">
<h2>I want to help</h2>
<p>Giving is not open yet. Setting it up properly, so that every dollar can be traced on this site, is near the top
of our list. <a href="help.html">How to help</a> says what is coming, what you can do today, and why we are asking
you to hold on to your used canes and laptops for now.</p>
</section>

<section class="door">
<h2>I want to check the numbers</h2>
<p>Every figure on this site is drawn from data files anyone can download. <a href="numbers.html">The numbers</a>
shows what two meals cost, what a third adds, and where each estimate came from. <a href="ledger.html">The ledger</a>
will list every transfer, purchase, exchange rate and receipt. <a href="check-our-work.html">Check our work</a>
tells you how to verify any of it.</p>
</section>

<section class="door">
<h2>I want to learn what blind Nigerians already do</h2>
<p>Bethesda is run by blind people. Its students study, code, play chess and play audible football. We do not
need anyone's pity on their behalf; we need the means to do things differently than others do them.
<a href="already.html">What blind Nigerians already do</a> is where we are gathering that record.</p>
</section>

<h2>Where things stand</h2>
<p>Nothing has been promised to anyone and no money has moved. We have exchanged letters with Bethesda, had
{e(brand.REPRESENTATIVE)} visit and count, and costed the meals from Lagos market prices. The next steps are a
market check on those prices and a decision on how gifts will be held and sent. <a href="whats-new.html">What's
new</a> records each step as it happens.</p>
"""


# ----------------------------------------------------------------------------------------------- story

def story(d: dict) -> str:
    return f"""<h1>The story</h1>
<p class="lede">{e(brand.PARTNER)} is a home, a school and a congregation in {e(brand.PARTNER_PLACE)}, Nigeria,
run almost entirely by blind people.</p>

<h2>Bethesda</h2>
<p>About {c(d, "people")} people live, study or work at Bethesda: around {c(d, "boarders")} boarding students and
about {c(d, "staff")} staff, of whom only {c(d, "sighted-staff")} are sighted. It is led by Rev. Dr. Chioma Ohakwe,
and the home worships with the Redeemed Christian Church of God. The students learn what any school teaches, and
some of them code, play chess, and play audible football. Bethesda also supports blind students through university.
</p>
<p>These counts come from a visit by {e(brand.REPRESENTATIVE)} on 24 October 2026, and from Bethesda's own
letters. We will correct them here as we learn more.</p>

<h2>The meal that was cut</h2>
<p>In 2026 the home's food money no longer stretched. Meals went from {c(d, "meals-before")} a day to
{c(d, "meals-now")}. The students still eat rice, beans, noodles and semolina, in modest portions, twice a day.
Bethesda did not ask us for food; it told us the facts when we asked. <a href="numbers.html">The numbers</a> sets
out what the meals cost and what a third would add.</p>

<h2>How we came to this</h2>
<p>Brian Clark, who leads this effort, has been blind since 2014 and teaches blind people to use computers for a
living. In 2026 he began asking how a blind man in Indianapolis could be of real use to blind people in Nigeria,
and wrote to schools for the blind in Lagos. Bethesda answered fully, named its needs plainly, and asked for
nothing. We decided to begin there.</p>
<p>We then asked {e(brand.REPRESENTATIVE)} to visit, count, and report, so that nothing on this site rests on a
letter alone. He did, on 24 October 2026, and his report is the source of the figures above.</p>

<h2>What we intend</h2>
<p>Our first goal is to help restore the third daily meal. Feeding is a cost that never ends, so it needs giving
that repeats, not a single gift. We will not promise Bethesda anything until the means are in hand, and the first
step may be a single month, with receipts, to learn how it goes. Everything we send and everything it buys will be
listed on <a href="ledger.html">the ledger</a>.</p>
<p>Beyond food, Bethesda's students wear out white canes on Lagos roads, about {c(d, "canes-per-year")} a year
among the {c(d, "cane-users")} or so who travel outside the school, and they need laptops, accessible calculators
and talking watches. Those come later, and they will be costed and listed in the same way.</p>

<h2>Why no pictures yet</h2>
<p>No student's name, picture or story appears here until Bethesda and the student have agreed to it in writing.
We asked about pictures and recordings on the first visit and did not take any. When they come, they will show
capable people at work.</p>
"""


# ----------------------------------------------------------------------------------------------- already doing

def already(d: dict) -> str:
    coming = ('<p class="pending">We are gathering recordings and pictures of this, with written permission, and '
              "will add them here.</p>")
    return f"""<h1>What blind Nigerians already do</h1>
<p class="lede">This page is the point of the site. Help is only worth giving to people who can use it, and blind
Nigerians use it well. Here is what Bethesda's staff and students already do with what they have.</p>
<p>We will not show anyone as an object of pity. Blind people are capable people, intelligent problem solvers and
engineers of their own lives, and the people at Bethesda prove it daily. What they lack is not ability; it is the
means to do things in the different ways blind people do them.</p>

<h2>A school run by blind people</h2>
<p>Of about {c(d, "staff")} staff, {c(d, "sighted-staff")} are sighted. Blind teachers teach, blind administrators
run the home, and blind leaders have kept it going through a year when the food money ran short.</p>
{coming}

<h2>Students who code</h2>
<p>Some students write software, using screen readers on phones and on the few computers the school has. Brian,
who teaches screen readers for a living, intends to teach alongside them by remote connection.</p>
{coming}

<h2>Chess</h2>
<p>Chess with a tactile board is played at Bethesda as it is in blind clubs around the world.</p>
{coming}

<h2>Audible football</h2>
<p>Football with a ball that rattles, played by ear. Bethesda is preparing for a competition in November 2026.</p>
{coming}

<h2>Through university</h2>
<p>Bethesda supports blind students beyond its own walls, through university. We will publish what we learn about
those students' paths, with their permission, as we learn it.</p>
{coming}

<h2>What this asks of a reader</h2>
<p>Not sympathy. A share of the means: a meal a day, a cane that lasts a few months on a Lagos road, a laptop with
a free screen reader. The <a href="numbers.html">numbers</a> say what each costs.</p>
"""


# ----------------------------------------------------------------------------------------------- numbers

def numbers(d: dict) -> str:
    ids = ["two-meals-staples-monthly", "two-meals-all-in-monthly", "third-meal-staples-monthly",
           "third-meal-all-in-monthly"]
    rows = []
    for eid in ids:
        x = est(d, eid)
        rows.append({"label": x["label"], "lo": x["usd_cents_lo"], "hi": x["usd_cents_hi"],
                     "cells": [m.usd_range(x["usd_cents_lo"], x["usd_cents_hi"]),
                               m.ngn_range(x["ngn_lo"], x["ngn_hi"]), e(x["note"])]})
    chart = charts.range_bars(
        "monthly-costs", "Monthly feeding costs at Bethesda, low to high estimate, in US dollars",
        "Four horizontal bars, one per cost, each running from the low estimate to the high. The table below gives "
        "the same figures.", rows, "Monthly feeding costs, estimates of October 2026",
        ["Cost", "US dollars a month", "Naira a month", "Note"],
        fmt=m.usd_svg)
    counts = "".join(f'<tr><th scope="row">{e(x["label"])}</th><td>{m.count(x)}</td><td>{e(x["source"])}</td>'
                     f'<td><time datetime="{e(x["checked"])}">{e(m.pretty_date(x["checked"]))}</time></td></tr>'
                     for x in d["estimates"]["counts"])
    rate = d["rates"]["rates"][0]
    per = est(d, "third-meal-per-child-monthly")
    year = est(d, "third-meal-yearly")
    third = est(d, "third-meal-staples-monthly")
    third_all = est(d, "third-meal-all-in-monthly")
    two = est(d, "two-meals-staples-monthly")
    return f"""<h1>The numbers</h1>
<p class="lede">What feeding {c(d, "boarders")} blind children costs, what a third meal would add, and where every
figure came from. Every amount here is an estimate until a market check replaces it, and each one says so.</p>

<h2>Who is fed</h2>
<div class="table-scroll" role="region" tabindex="0" aria-label="People at Bethesda, table">
<table><caption>People at Bethesda</caption>
<thead><tr><th scope="col">Count</th><th scope="col">Number</th><th scope="col">Source</th><th scope="col">As of</th></tr></thead>
<tbody>{counts}</tbody></table></div>

<h2>What two meals cost now</h2>
<p>Bethesda told us what it buys each month for two meals a day: rice, beans, Indomie noodles and semolina, in
quantities that match the headcount. At Lagos market prices found online in October 2026, those staples come to
{m.estimate(two)}. Staples are not a meal on their own; soup, stew, oil, fish, seasoning and cooking fuel commonly
add a third to a half again, so the real cost of two meals is likely {m.estimate(est(d, "two-meals-all-in-monthly"))}.
</p>

<h2>What a third meal would add</h2>
<p>A third daily meal is seven more meals a week, half again what the kitchen cooks now. Using the same foods,
the staples alone come to {m.estimate(third)}, and with everything that makes them a meal,
{m.estimate(third_all)}. Over a year that is {m.estimate(year, with_ngn=False)}.</p>
<p>A third meal need not cost what the others do. If it was a lighter breakfast, it may cost about half as much.
We have asked Bethesda what the third meal used to be and when it stopped.</p>
<h3>The costs side by side</h3>
{chart}

<h2>Per child</h2>
<p>Divided among the boarders, a third meal costs {m.estimate(per, with_ngn=False)}. That is the clearest number
on this site: {m.usd_range(per["usd_cents_lo"], per["usd_cents_hi"])} a month restores a third meal for one blind
child at Bethesda.</p>

<h2>How these figures were made</h2>
<ul>
<li>Quantities are Bethesda's own, from a letter of 26 October 2026, and they fit the headcount counted on the
visit of 24 October 2026.</li>
<li>Prices are Lagos and national market figures found online in October 2026. The sources are listed in the
{m.source_link(two["source"], "feeding analysis")} in the repository.</li>
<li>Naira are converted at {m.ngn(rate["ngn_per_usd"])} to the dollar, the bank rate observed on
<time datetime="{e(rate["date"])}">{e(m.pretty_date(rate["date"]))}</time>. Every rate used on this site is listed
on <a href="ledger.html#rates">the ledger</a>.</li>
<li>Each figure carries the date it was last checked. When {e(brand.REPRESENTATIVE)} checks prices at a market,
the figures and dates will change here.</li>
</ul>

<h2>What we still need to find out</h2>
<ul>
<li>What the third meal used to be, and when it stopped.</li>
<li>Whether the boarders' figure is the number fed, or whether staff and day students eat too.</li>
<li>What else is bought each month besides the four staples, and at what cost.</li>
<li>Where Bethesda buys, and at what prices, so our estimates can be checked against receipts.</li>
<li>Whether anyone gives regularly for food now, and what would happen if a gift stopped after a year.</li>
</ul>
"""


# ----------------------------------------------------------------------------------------------- ledger

def _entry_rows(entries, show_running: bool) -> str:
    rows = []
    for x, total in (lg.running(entries) if show_running else [(x, None) for x in entries]):
        receipt = (f'<a href="data/receipts/{e(x["receipt"])}">Receipt</a>' if x.get("receipt") else "Not yet")
        fees = m.usd(x.get("fees_usd_cents", 0))
        cells = [f'<time datetime="{e(x["date"])}">{e(m.pretty_date(x["date"]))}</time>', e(x["type"]),
                 e(x["recipient"]), e(x["purpose"]), m.usd(x["usd_cents"]), m.ngn(x["ngn"]),
                 m.ngn(x["rate_ngn_per_usd"]), fees, e(x["method"]), receipt]
        if show_running:
            cells.append(m.usd(total))
        rows.append(f'<tr><th scope="row">{e(x["id"])}</th>' + "".join(f"<td>{v}</td>" for v in cells) + "</tr>")
    return "".join(rows)


def _entry_table(caption: str, entries, show_running: bool) -> str:
    heads = ["Entry", "Date", "Kind", "Recipient", "Purpose", "US dollars", "Naira", "Rate (naira per dollar)",
             "Fees", "Method", "Receipt"] + (["Running total"] if show_running else [])
    head = "".join(f'<th scope="col">{h}</th>' for h in heads)
    return (f'<div class="table-scroll" role="region" tabindex="0" aria-label="{e(caption)}, table">'
            f"<table><caption>{e(caption)}</caption><thead><tr>{head}</tr></thead>"
            f"<tbody>{_entry_rows(entries, show_running)}</tbody></table></div>")


def ledger_page(d: dict) -> str:
    entries = d["ledger"]["entries"]
    moved = lg.real(entries)
    plans = lg.pending(entries)
    t = lg.totals(entries)
    g = goal(d, "third-meal")
    given, target = lg.progress(g, entries, this_month())
    if moved:
        summary = (f"<p>So far {t['count']} {'transfer has' if t['count'] == 1 else 'transfers have'} been made, "
                   f"{m.usd(t['usd_cents'])} in all ({m.ngn(t['ngn'])} received in naira), with {m.usd(t['fees_usd_cents'])} "
                   f"paid in fees on top. Every entry is below with its exchange rate and, where we have it, its receipt.</p>")
        tables = (_entry_table("Transfers and grants to organizations", lg.by_type(moved, "grant", "transfer"), True)
                  if lg.by_type(moved, "grant", "transfer") else "") + \
                 (_entry_table("Purchases made for organizations", lg.by_type(moved, "purchase"), True)
                  if lg.by_type(moved, "purchase") else "")
    else:
        summary = ('<p class="pending">No money has moved yet. When the first transfer is made it will appear here '
                   "with its date, amount, exchange rate, fees and receipt, and the totals below will be computed "
                   "from it.</p>")
        tables = ""
    planned = (_entry_table("Planned, not yet sent", plans, False) if plans else
               "<p>Nothing is planned yet beyond the goal above.</p>")
    rates = "".join(f'<tr><th scope="row"><time datetime="{e(r["date"])}">{e(m.pretty_date(r["date"]))}</time></th>'
                    f'<td>{m.ngn(r["ngn_per_usd"])}</td><td>{e(r["source"])}{" (estimate)" if r.get("estimate") else ""}</td></tr>'
                    for r in d["rates"]["rates"])
    meter = charts.progress_meter("third-meal-progress", f"Progress toward the monthly target: {g['title']}",
                                  given, target, m.usd(given), m.usd(target),
                                  f"This month toward the goal: {g['title']}")
    return f"""<h1>The ledger</h1>
<p class="lede">Every transfer, purchase, exchange rate and receipt, published as data. The totals are computed
from the entries each time the site is built; nothing here is typed in by hand.</p>

<h2>Summary</h2>
{summary}

<h2>The goal</h2>
<p><b>{e(g["title"])}.</b> {e(g["description"])} The monthly target used here is {m.usd(target)}: {e(g["target_note"])}
It is an estimate, from the {m.source_link(g["source"], "feeding analysis")}.</p>
{meter}

<h2>Money that has moved</h2>
{tables if tables else '<p>None yet.</p>'}

<h2>Planned</h2>
{planned}

<h2 id="rates">Exchange rates used</h2>
<div class="table-scroll" role="region" tabindex="0" aria-label="Exchange rates used, table">
<table><caption>Exchange rates used</caption>
<thead><tr><th scope="col">Date</th><th scope="col">Naira per US dollar</th><th scope="col">Source</th></tr></thead>
<tbody>{rates}</tbody></table></div>

<h2>Download the data</h2>
<ul>
<li><a href="data/ledger.csv">The ledger as a spreadsheet file (CSV)</a>: real and planned entries, one row each.</li>
<li><a href="data/ledger.json">ledger.json</a>, <a href="data/goals.json">goals.json</a>,
<a href="data/rates.json">rates.json</a> and <a href="data/estimates.json">estimates.json</a>: the files the site
is built from, unchanged.</li>
<li>Receipts, once there are any, are linked from their rows and kept in the repository with account details
removed.</li>
</ul>
<p>What is never here: anyone's bank or account details, and anyone's pay or personal arrangement. The ledger
records gifts to organizations and purchases made for them.</p>
"""


# ----------------------------------------------------------------------------------------------- help

def help_page(d: dict) -> str:
    per = est(d, "third-meal-per-child-monthly")
    return f"""<h1>How to help</h1>
<p class="lede">Giving is not open yet. We would rather say so plainly than take a dollar we cannot yet account for
in public.</p>

<h2>Where giving stands</h2>
<p>Setting up giving properly is near the top of our list. Properly means: a way to give that repeats monthly,
because feeding never stops; fees stated honestly; a structure for holding the money that is sound and that we can
name here; and every dollar that arrives and leaves shown on <a href="ledger.html">the ledger</a>. When that is in
place this page will say so, and <a href="whats-new.html">What's new</a> will carry the date.</p>
<p>The figure to keep in mind meanwhile is {m.estimate(per, with_ngn=False)}: what it costs to restore a third
daily meal for one blind child at Bethesda.</p>

<h2>Used canes and laptops</h2>
<p>People have asked whether to send white canes and old laptops. Please hold on to them for now. Canes cost less
bought in Lagos than shipped from the United States, and laptops need the right preparation and a safe route. We are
working out how best to use both and will say here when we are ready to receive them.</p>

<h2>What you can do today</h2>
<ul>
<li>Pray for Bethesda's staff and students, and for us as we work out how to help well.</li>
<li>Read <a href="already.html">what blind Nigerians already do</a> and pass it on. The story we want told is one of
capability.</li>
<li>If you know Lagos, its markets or its suppliers, or you work with blind people in Nigeria, write to us at
<a href="mailto:{e(brand.CONTACT_EMAIL)}">{e(brand.CONTACT_EMAIL)}</a>.</li>
<li>If you find an error on this site, say so. <a href="check-our-work.html">Check our work</a> explains how.</li>
</ul>
"""


# ----------------------------------------------------------------------------------------------- future studies

def future_studies(d: dict) -> str:
    items = "".join(f"<h2>{e(t)}</h2><p>{e(p)}</p>" for t, p in FUTURE_STUDIES)
    return f"""<h1>Future studies</h1>
<p class="lede">Pages we intend to write, each a study with its sources, the way the pages on
<a href="https://blindnessinthebible.com">Not By Sight</a> read a verse. They are listed now so that nothing is
hidden about where the site is going, and so that a reader who knows the ground can tell us what we are missing.</p>
{items}
<h2>Suggest one</h2>
<p>Write to <a href="mailto:{e(brand.CONTACT_EMAIL)}">{e(brand.CONTACT_EMAIL)}</a>.</p>
"""


# ----------------------------------------------------------------------------------------------- about

def about(d: dict) -> str:
    sisters = "".join(f'<li><a href="{e(u)}">{e(n)}</a>: {e(what)}.</li>' for u, n, what in brand.SISTER_SITES)
    return f"""<h1>About</h1>
<p class="lede">We are a small group of friends in Indiana, led by a blind man, working to support blind people in
Nigeria, beginning with one school in Lagos. This site is our public record.</p>

<h2>Who we are</h2>
<p>Brian Clark leads this effort. He has been blind since 2014, was a technology manager in his sighted career,
and has taught blind people to use computers and screen readers since 2018. He builds this site himself with a
screen reader and no mouse, which is why it works the way it does. The work began as part of a conversation at his
church, Hope Christian Church in Indianapolis, about how a small congregation might serve blind people; what form
the church's part takes is still being decided, and we will say here when it is.</p>

<h2>People on the ground</h2>
<p>In Nigeria, {e(brand.REPRESENTATIVE)} visits, counts, prices and reports, so that what we publish rests on
what someone we trust has seen. We will introduce him here properly when he and we have agreed what to say.</p>

<h2>How gifts will be held</h2>
<p>Not decided yet. We are choosing among several sound ways of holding and sending gifts, and we will not open
giving until one is in place and named on this site.</p>

<h2>The sister sites</h2>
<p>This is the third of three connected sites, each a part of the same journey:</p>
<ul>{sisters}</ul>

<h2>The name</h2>
<p>"{e(brand.SITE_NAME)}" is a working name. It will probably change, and when it does, this page will record the
change and the old address will still work.</p>

<h2>Faith</h2>
<p>This is Christian work. We believe blind people bear the image of God as fully as anyone, that the work points
to Jesus, and that it should be done in the open. "We walk by faith, not by sight." (2 Corinthians 5:7)</p>

<h2>Write to us</h2>
<p><a href="mailto:{e(brand.CONTACT_EMAIL)}">{e(brand.CONTACT_EMAIL)}</a>. Corrections are especially welcome.</p>
"""


PAGES = [
    ("index.html", "Home", home),
    ("story.html", "The story", story),
    ("already.html", "What blind Nigerians already do", already),
    ("numbers.html", "The numbers", numbers),
    ("ledger.html", "The ledger", ledger_page),
    ("help.html", "How to help", help_page),
    ("future-studies.html", "Future studies", future_studies),
    ("about.html", "About", about),
]
