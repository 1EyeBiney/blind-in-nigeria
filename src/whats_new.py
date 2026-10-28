"""What's new: the changes a returning reader would notice, by date, newest first; and an RSS feed of the same.

Entries are written by hand, for readers, not copied from commit messages. Each one: the date (YYYY-MM-DD), a
short title, a sentence or two, and the page to go to (relative to the site root). Add new entries at the top.

A small script (static/display.js) remembers the date of the reader's last visit in their own browser and marks
the entries newer than that. With the script off, the page is simply the dated list.
"""
import brand

TITLE = "What's new"
SLUG = "whats-new.html"
FEED = "feed.xml"
SITE = brand.site_url()

ENTRIES = [
    ("2026-10-27", "The site begins",
     "The first pages: the story of Bethesda Home and School for the Blind, the numbers behind feeding its students, "
     "an empty ledger waiting for the first transfer, and an honest note that giving is not open yet. The name of the "
     "site is provisional.",
     "index.html"),
]

INTRO = [
    "What has changed on the site, newest first, for anyone who comes back.",
    "Each entry names the page to go to. The same list is available as an RSS feed.",
]
