"""Shared brand system for the Bulgaria Legal CloudCart redesign.
Palette is derived from the firm's OWN identity:
  - crimson  = logo monogram red
  - charcoal = logo dark + premium base
  - gold     = hero ('Your success is our reputation') champagne accent
  - slate    = logo background block
Photographic assets are the firm's own images (per instruction: no external/stock)."""
import json, os
from config import DATA_DIR

# ---- Palette ----
INK      = "#15171C"   # near-black charcoal (footer, dark sections, display text)
INK_2    = "#1E2127"   # raised dark surface
CRIMSON  = "#9E1B20"   # primary action / brand red (from logo)
CRIMSON_D= "#7C1418"   # crimson hover
GOLD     = "#C0A062"   # champagne accent (rules, details, hover on dark)
GOLD_D   = "#A98A4E"
SLATE    = "#8A96A0"
PAPER    = "#FFFFFF"
PAPER_2  = "#F7F5F2"   # warm off-white section bg
LINE     = "#E7E2DB"   # hairline borders
TEXT     = "#26272B"   # body text
MUTED    = "#6E7177"   # secondary text

# Fonts (both support Cyrillic — required for Bulgarian)
FONT_IMPORT = ("@import url('https://fonts.googleapis.com/css2?"
               "family=Playfair+Display:wght@500;600;700;800&"
               "family=Manrope:wght@400;500;600;700;800&display=swap&subset=cyrillic,cyrillic-ext');")
SERIF = "'Playfair Display', Georgia, 'Times New Roman', serif"
SANS  = "'Manrope', 'Segoe UI', system-ui, sans-serif"

# FontAwesome Pro icon per practice (theme's own icon font — premium thin 'fal' weight)
ICONS = {
    "veshchno-pravo": "fa-house-chimney", "trgovsko-pravo": "fa-handshake",
    "zastrahovatelno": "fa-shield-halved", "semeyno-nasledstveno": "fa-people-roof",
    "mezhdunarodno-es": "fa-earth-europe", "bankovo-pravo": "fa-building-columns",
    "danchno-administrativno": "fa-file-invoice-dollar", "nakazatelno-pravo": "fa-gavel",
    "energiya": "fa-bolt", "schetovodni": "fa-calculator",
    "ptp": "fa-car-burst", "angliya-uels": "fa-scale-balanced",
}

def site():
    return json.load(open(os.path.join(DATA_DIR, "site.json"), encoding="utf-8"))
