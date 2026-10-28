"""Check our work: how to verify a figure, rebuild the site, and tell us we are wrong."""
import brand

TITLE = "Check our work"
SLUG = "check-our-work.html"


def body() -> str:
    repo = brand.REPO
    name = repo.rstrip("/").split("/")[-1]
    return f"""<h1>Check our work</h1>
<p class="lede">Everything behind this site is public: the data files every figure is drawn from, the source
documents, the code that builds the pages, and the tests that check it. If you want to verify a number, download
the ledger, or rebuild the site yourself, this page tells you how.</p>

<h2>The site checks its own numbers</h2>
<p>No amount of money on this site is typed into a page. Each one is rendered from the data files in the
repository by one small piece of code, and a test reads every built page looking for a dollar or naira figure that
did not come that way. Totals and running totals are computed from the entries at build time and are never stored.
Estimates must carry a source and the date they were last checked, or the build fails. <b>If any of this is
broken, the site does not publish.</b></p>
<p>You can run those checks yourself in about a minute:</p>
<pre><code>git clone {repo}
cd {name}
python -m pytest tests</code></pre>
<p>It needs Python 3.12 or later and pytest, and nothing else. No account, no key, no network once the clone is
done. To rebuild the whole site into a local folder called site, run <code>python src/build_site.py</code>; that
is the same command the publishing workflow runs.</p>

<h2>Checking a figure without installing anything</h2>
<ul>
<li><b>Download the data.</b> <a href="data/ledger.csv">The ledger as a spreadsheet file</a>, or the raw files:
<a href="data/ledger.json">ledger.json</a>, <a href="data/goals.json">goals.json</a>,
<a href="data/rates.json">rates.json</a>, <a href="data/estimates.json">estimates.json</a>.</li>
<li><b>Read the source behind an estimate.</b> Every estimate names its source document in brackets after the
figure, with a link into the repository, and the date it was last checked.</li>
<li><b>Look at the receipts.</b> Once there are transfers, each row of the ledger links to its receipt where we
have one, with account details removed.</li>
<li><b>Read the history.</b> The repository keeps every change to every file, with its date, so you can see what a
figure was and when it changed.</li>
</ul>

<h2>What is deliberately not here</h2>
<p>Bank, transfer and account details of anyone. The pay of anyone who works with us. The names, pictures or stories
of any student or individual in Nigeria without their written consent and Bethesda's. Our private notes on the
organizations we have talked to. The repository stands alone and contains only what is meant to be public.</p>

<h2>If you think something is wrong</h2>
<p>Please say so. A mistake nobody reports stays on the page. Write to
<a href="mailto:{brand.CONTACT_EMAIL}">{brand.CONTACT_EMAIL}</a>, no account needed, or open an issue on
<a href="{repo}/issues">the repository</a>. The most useful corrections name the page and quote the sentence.</p>

<h2>Reuse</h2>
<p>The writing on this site is offered under the <a href="https://creativecommons.org/licenses/by/4.0/">Creative
Commons Attribution 4.0 licence</a>, the data likewise, and the code under the MIT licence. The repository's NOTICE
file sets out the terms and how to cite.</p>
"""
