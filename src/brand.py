"""Everything about the site that may change its name lives here, so a rename touches one file.

The name and the domain are provisional (Brian, 27 October 2026). Until a domain is bought DOMAIN stays empty, no
CNAME is written, and the site is served at PAGES_URL.
"""

SITE_NAME = "Blind in Nigeria"
TAGLINE = "Supporting blind people in Nigeria, beginning with a school in Lagos"
PROVISIONAL = True            # shows a short note under the header that the name and site are still being built

DOMAIN = ""                   # for example "blindinnigeria.com"; when set, the build writes site/CNAME
PAGES_URL = "https://1eyebiney.github.io/blind-in-nigeria/"
REPO = "https://github.com/1EyeBiney/blind-in-nigeria"

CONTACT_EMAIL = "brian@blindnessinthebible.com"   # until this site has an address of its own

# The person who visits and verifies on the ground. How he is named publicly is his and Brian's decision;
# until then the pages refer to him by role only.
REPRESENTATIVE = "our representative in Nigeria"

PARTNER = "Bethesda Home and School for the Blind"
PARTNER_PLACE = "Surulere, Lagos"
PARTNER_EMAIL = "info@bethesdahomefortheblind.com"

SISTER_SITES = [
    ("https://blindnessinthebible.com", "Not By Sight", "studies on blindness in the Bible"),
    ("https://asojn.com", "asojn.com", "a music album delivered as a website"),
]


def site_url() -> str:
    return f"https://{DOMAIN}/" if DOMAIN else PAGES_URL
