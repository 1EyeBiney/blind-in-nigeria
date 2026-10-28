"""Reading settings for low-vision readers: text size, colours, letter style and spacing.

Everything here is optional. The site reads the same with the script switched off; the panel simply stays
hidden. Choices are kept in the reader's own browser (localStorage) and nowhere else.

The colour sets are data, so the tests can measure every pair of colours for contrast.
"""

# Each set: page background, text, quieter text, links, rules and borders, table-head background,
# and whether the browser's own controls (radio buttons) should be drawn light or dark.
THEMES = {
    "light": {"bg": "#ffffff", "fg": "#1a1a1a", "muted": "#4a4a4a", "link": "#0b3d91", "rule": "#767676",
              "head": "#f0f0f0", "scheme": "light"},
    "dark": {"bg": "#121212", "fg": "#f2f2f2", "muted": "#cfcfcf", "link": "#9cc4ff", "rule": "#8a8a8a",
             "head": "#222222", "scheme": "dark"},
    "contrast-light": {"bg": "#ffffff", "fg": "#000000", "muted": "#000000", "link": "#00008b", "rule": "#000000",
                       "head": "#e6e6e6", "scheme": "light"},
    "contrast-dark": {"bg": "#000000", "fg": "#ffffff", "muted": "#ffffff", "link": "#ffff00", "rule": "#ffffff",
                      "head": "#1a1a1a", "scheme": "dark"},
    "yellow": {"bg": "#000000", "fg": "#ffff00", "muted": "#ffff00", "link": "#ffffff", "rule": "#ffff00",
               "head": "#1a1a00", "scheme": "dark"},
    "cream": {"bg": "#f6edd3", "fg": "#1a1a1a", "muted": "#3d3d3d", "link": "#0b3d91", "rule": "#6f6748",
              "head": "#ebe0bf", "scheme": "light"},
}

# What the reader is offered. "" is the default: follow the device.
OPTIONS = {
    "size": ("Text size", [("", "Standard"), ("125", "Large"), ("150", "Larger"), ("175", "Very large"),
                           ("200", "Largest")]),
    "theme": ("Colours", [("", "Match my device"), ("light", "Dark text on white"), ("dark", "Light text on dark"),
                          ("contrast-light", "High contrast, black on white"),
                          ("contrast-dark", "High contrast, white on black"),
                          ("yellow", "Yellow on black"), ("cream", "Low glare, dark text on cream")]),
    "font": ("Letter style", [("", "Serif, like a book"), ("sans", "Plain, without serifs")]),
    "spacing": ("Spacing", [("", "Standard"), ("wide", "Wider lines, letters and words")]),
}


def _vars(t: dict) -> str:
    return (f"--bg:{t['bg']}; --fg:{t['fg']}; --muted:{t['muted']}; --link:{t['link']}; --rule:{t['rule']}; "
            f"--head:{t['head']}; color-scheme:{t['scheme']};")


def theme_css() -> str:
    """Colour sets. With nothing chosen the page follows the device: light or dark, and high contrast if the
    device asks for more contrast. A choice in the panel overrides the device."""
    out = [f":root {{ {_vars(THEMES['light'])} }}",
           f"@media (prefers-color-scheme: dark) {{ :root:not([data-theme]) {{ {_vars(THEMES['dark'])} }} }}",
           f"@media (prefers-contrast: more) {{ :root:not([data-theme]) {{ {_vars(THEMES['contrast-light'])} }} }}",
           "@media (prefers-contrast: more) and (prefers-color-scheme: dark) { :root:not([data-theme]) { "
           f"{_vars(THEMES['contrast-dark'])} }} }}"]
    out += [f':root[data-theme="{name}"] {{ {_vars(t)} }}' for name, t in THEMES.items()]
    return "\n".join(out)


CSS = """
:root[data-size="125"] { font-size: 125%; }
:root[data-size="150"] { font-size: 150%; }
:root[data-size="175"] { font-size: 175%; }
:root[data-size="200"] { font-size: 200%; }
:root[data-font="sans"] body { font-family: Verdana, Tahoma, "Segoe UI", Arial, sans-serif; }
:root[data-spacing="wide"] body { line-height: 2; letter-spacing: .12em; word-spacing: .16em; }
:root[data-spacing="wide"] main p, :root[data-spacing="wide"] main li { margin-bottom: 2em; }
details.display { margin-top: .75rem; }
details.display summary { cursor: pointer; display: inline-block; padding: .35rem .6rem; border: 2px solid var(--rule);
  border-radius: .25rem; font-weight: bold; }
details.display fieldset { border: 1px solid var(--rule); margin: .75rem 0; padding: .5rem .75rem; }
details.display legend { font-weight: bold; padding: 0 .35rem; }
details.display label { display: inline-block; margin: .25rem 1.25rem .25rem 0; padding: .2rem 0; }
details.display input[type="radio"] { width: 1.1em; height: 1.1em; margin-right: .35em; vertical-align: -0.1em;
  accent-color: var(--link); }
details.display button { font: inherit; color: var(--fg); background: var(--head); border: 2px solid var(--rule);
  border-radius: .25rem; padding: .35rem .75rem; cursor: pointer; }
details.display p.note { margin: .5rem 0; color: var(--muted); }
"""


def panel_html(root: str) -> str:
    """The panel in the page header. Plain radio buttons in labelled groups, so a screen reader announces each
    group and choice. It starts hidden and the script reveals it, so nobody is shown controls that do nothing."""
    groups = []
    for key, (legend, choices) in OPTIONS.items():
        radios = "".join(
            f'<label><input type="radio" name="{key}" value="{value}"{" checked" if value == "" else ""}> {label}</label>'
            for value, label in choices)
        groups.append(f"<fieldset><legend>{legend}</legend>{radios}</fieldset>")
    return (f'<details class="display" id="display" hidden><summary>Text size and colours</summary>'
            f'<form id="display-form">{"".join(groups)}'
            f'<p><button type="button" id="display-reset">Put everything back to standard</button></p>'
            f'<p class="note" id="display-status" role="status"></p>'
            f'<p class="note">Your choices are remembered on this device only. '
            f'More on the <a href="{root}accessibility.html">accessibility page</a>.</p>'
            f"</form></details>")


def script() -> str:
    """One small script. The first half runs before the page is drawn, so a chosen size or colour set never
    flashes in late. The second half wires up the panel."""
    import json
    allowed = {k: [v for v, _ in choices if v] for k, (_, choices) in OPTIONS.items()}
    names = {k: {v: label for v, label in choices} for k, (_, choices) in OPTIONS.items()}
    legends = {k: legend for k, (legend, _) in OPTIONS.items()}
    return """(function () {
  var KEY = 'bin-display';
  var ALLOWED = %s;
  var NAMES = %s;
  var LEGENDS = %s;
  var root = document.documentElement;
  function read() {
    try {
      var s = JSON.parse(window.localStorage.getItem(KEY));
      return (s && typeof s === 'object') ? s : {};
    } catch (err) { return {}; }
  }
  function save(s) {
    try { window.localStorage.setItem(KEY, JSON.stringify(s)); } catch (err) { /* private window: this page only */ }
  }
  function apply(s) {
    for (var k in ALLOWED) {
      if (s[k] && ALLOWED[k].indexOf(s[k]) >= 0) { root.setAttribute('data-' + k, s[k]); }
      else { root.removeAttribute('data-' + k); delete s[k]; }
    }
  }
  var state = read();
  apply(state);
  // What's new: remember the date of the reader's last visit, on this device only. A visit ends after six quiet
  // hours. Entries dated after the last visit are marked, and the menu link shows how many.
  var VISIT = 'bin-visit';
  function readVisit() {
    try { var v = JSON.parse(window.localStorage.getItem(VISIT)); return (v && typeof v === 'object') ? v : {}; }
    catch (err) { return {}; }
  }
  function saveVisit(v) { try { window.localStorage.setItem(VISIT, JSON.stringify(v)); } catch (err) { /* this page only */ } }
  var visit = readVisit();
  var now = Date.now();
  if (!visit.current || now - visit.current > 6 * 3600 * 1000) {
    if (visit.current) { visit.last = new Date(visit.current).toISOString().slice(0, 10); }
    visit.current = now;
    saveVisit(visit);
  } else {
    visit.current = now;
    saveVisit(visit);
  }
  document.addEventListener('DOMContentLoaded', function () {
    // What counts as new: anything dated after the newest entry the reader has already seen on the What's new
    // page. Before they have ever opened that page, anything dated on or after their last visit.
    var since = visit.last || '';
    var seen = visit.seenUpTo || '';
    function isNew(d) { return seen ? d > seen : (since ? d >= since : false); }
    var nav = document.getElementById('nav-whats-new');
    var items = document.querySelectorAll('#changes li[data-date]');
    var count = 0;
    for (var i = 0; i < items.length; i++) {
      if (isNew(items[i].getAttribute('data-date'))) {
        count++;
        items[i].className += ' is-new';
        var mark = document.createElement('span');
        mark.className = 'new-mark';
        mark.textContent = ' New since your last visit.';
        items[i].appendChild(mark);
      }
    }
    if (nav && isNew(nav.getAttribute('data-latest'))) {
      // on other pages the count is not known; say that there is something new
      nav.textContent = items.length ? "What's new (" + count + ")" : "What's new (new)";
    }
    if (items.length && nav) {
      // the reader has now seen everything on the page; next time only newer entries are marked
      visit.seenUpTo = nav.getAttribute('data-latest');
      saveVisit(visit);
    }
    var status = document.getElementById('whats-new-status');
    var mark = document.getElementById('whats-new-mark');
    if (status) {
      status.textContent = since
        ? (count ? count + (count === 1 ? ' entry is' : ' entries are') + ' new since your last visit on this device, ' + since + '.'
                 : 'Nothing new since your last visit on this device, ' + since + '.')
        : 'This is your first visit on this device, or your browser does not keep the date. All entries are shown.';
    }
    if (mark) {
      mark.hidden = false;
      mark.addEventListener('click', function () {
        visit.last = new Date().toISOString().slice(0, 10);
        visit.seenUpTo = nav ? nav.getAttribute('data-latest') : visit.last;
        saveVisit(visit);
        for (var j = 0; j < items.length; j++) {
          items[j].className = items[j].className.replace(' is-new', '');
          var m = items[j].querySelector('.new-mark'); if (m) { m.parentNode.removeChild(m); }
        }
        if (nav) { nav.textContent = "What's new"; }
        status.textContent = 'Everything is marked as read. Next time, only newer entries will be marked.';
      });
    }
    var box = document.getElementById('display');
    if (!box) { return; }
    var form = document.getElementById('display-form');
    var status = document.getElementById('display-status');
    function show() {
      var radios = form.querySelectorAll('input[type=radio]');
      for (var i = 0; i < radios.length; i++) {
        radios[i].checked = (radios[i].value === (state[radios[i].name] || ''));
      }
    }
    show();
    box.hidden = false;
    form.addEventListener('change', function (ev) {
      var t = ev.target;
      if (!t || t.type !== 'radio' || !(t.name in ALLOWED)) { return; }
      state[t.name] = t.value;
      apply(state);
      save(state);
      status.textContent = LEGENDS[t.name] + ': ' + NAMES[t.name][t.value] + '. Saved.';
    });
    document.getElementById('display-reset').addEventListener('click', function () {
      state = {};
      apply(state);
      save(state);
      show();
      status.textContent = 'Everything is back to standard.';
    });
  });
})();
""" % (json.dumps(allowed), json.dumps(names), json.dumps(legends))


TITLE = "Accessibility"
SLUG = "accessibility.html"


def body(contact_email: str) -> str:
    return f"""<h1>Accessibility</h1>
<p class="lede">This site was made by a blind man, and it is meant to be used by blind and low-vision readers
first. This page says what has been done to make that so, what you can change, and where the limits are.</p>

<h2>Change how the pages look</h2>
<p>Near the top of every page, just after the list of pages, is a button called <b>Text size and colours</b>.
Open it and you can change four things. Each change takes effect at once and is remembered on the device you
are using. Nothing about your choices is sent anywhere.</p>
<ul>
<li><b>Text size.</b> Five sizes, from standard up to twice as large. The page reflows as the text grows, so
you do not have to scroll sideways to read a line.</li>
<li><b>Colours.</b> Dark text on white, light text on dark, two high-contrast sets, yellow on black, and a
low-glare set with dark text on cream. Left alone, the site follows your device: if your device is set to dark
mode or to increased contrast, the site matches it.</li>
<li><b>Letter style.</b> The standard is a serif face, like a printed book. The other choice is a plain face
without serifs, which many low-vision readers find easier.</li>
<li><b>Spacing.</b> Wider gaps between lines, letters, words and paragraphs.</li>
</ul>
<p>The button <b>Put everything back to standard</b> undoes all four.</p>
<p>The same browser memory holds one more thing: the date of your last visit, so that the
<a href="whats-new.html">What's new</a> page can mark the entries you have not seen. It stays on your device, like the
rest.</p>
<p>The panel needs JavaScript. If your browser has it switched off, the panel does not appear, and everything
else on the site works as before. Your browser's own zoom still works: hold Control and press plus to enlarge,
Control and minus to shrink, Control and zero to reset. On a Mac, use Command in place of Control.</p>

<h2>With a screen reader</h2>
<ul>
<li>Every page has one main heading, and the headings below it go in order, so you can move by heading.</li>
<li>The first link on every page skips the list of pages and goes straight to the main content.</li>
<li>The list of pages is a navigation landmark, and the page you are on is marked as the current page.</li>
<li>Tables have captions, and row and column headers, so a cell is announced with its headers.</li>
<li>Links say where they go. There are no links that only say "click here".</li>
<li>The settings panel is made of ordinary radio buttons in labelled groups, and it announces each change.</li>
</ul>
<p>The site is tested with NVDA on Windows, by its author, as it is built.</p>

<h2>With a keyboard</h2>
<p>Everything can be reached and worked with the keyboard alone. Whatever has the focus is shown with a thick
outline. Wide tables can be scrolled with the arrow keys once you tab to them.</p>

<h2>Charts and tables</h2>
<p>Where a page shows a chart, the same figures are always in a table directly under it, with a caption and
headers. The chart is announced as a graphic with its title and a one-line description; the table carries every
number. Nothing is said only in a chart, and nothing is told by colour alone. The charts take their colours from
the colour set you choose, so they stay readable in high contrast and in dark mode.</p>

<h2>Money</h2>
<p>Every amount of money on this site is drawn from the data files in the repository, never typed into a page by
hand. Estimates are marked as estimates, with the date they were last checked and a link to the document they
come from. The <a href="ledger.html">ledger</a> can be downloaded as a spreadsheet file or as the raw data.</p>

<h2>Pictures and video</h2>
<p>There are no pictures or video yet. When there are, every picture will have a written description and nothing
will be said only in a picture. Nothing on the site moves, flashes, or plays by itself.</p>

<h2>If something does not work for you</h2>
<p>Write to <a href="mailto:{contact_email}">{contact_email}</a> and say what you were using and what went
wrong. A site about blind people that a blind or low-vision reader cannot use has a fault, and it will be fixed.</p>
"""
