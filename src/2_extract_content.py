"""Pull text content from the key pages of bulgaria-legal.com for authentic copy."""
import json, os, re, sys, html
import requests
sys.stdout.reconfigure(encoding='utf-8')
from config import SRC_URL, DATA_DIR

HEAD = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
PAGES = {
    "za-nas": "/bg/za-nas/",
    "uslugi": "/bg/uslugi/",
    "kontakti": "/bg/kontakti/",
    "preporaki": "/bg/preporaki/",
    "bezplaten-suvet": "/bg/bezplaten-suvet/",
    "veshchno-pravo": "/bg/veshchno-pravo/",
    "trgovsko-pravo": "/bg/trgovsko-pravo/",
    "zastrahovatelno": "/bg/zastrahovatelno-pravo-pretentsii-za-vredi/",
    "semeyno-nasledstveno": "/bg/semeyno-i-nasledstveno-pravo/",
    "mezhdunarodno-es": "/bg/mezhdunarodno-chastno-pravo-i-pravo-na-es/",
    "bankovo-pravo": "/bg/bankovo-pravo/",
    "danchno-administrativno": "/bg/danchno-i-administrativno-pravo/",
    "nakazatelno-pravo": "/bg/nakazatelno-pravo/",
    "energiya": "/bg/energiya-i-prirodni-resursi/",
    "schetovodni": "/bg/schetovodni-uslugi/",
    "ptp": "/bg/pretentsii-pri-ptp-intsidenti/",
    "angliya-uels": "/bg/advokat-angliya-i-uels/",
}

def to_text(h):
    h = re.sub(r'(?is)<(script|style|noscript|head|nav|footer|header|form).*?</\1>', ' ', h)
    # grab the main content area if present
    h = re.sub(r'(?is)<br\s*/?>', '\n', h)
    h = re.sub(r'(?is)</(p|div|h[1-6]|li|tr)>', '\n', h)
    txt = re.sub(r'(?is)<[^>]+>', ' ', h)
    txt = html.unescape(txt)
    txt = re.sub(r'[ \t]+', ' ', txt)
    txt = re.sub(r'\n\s*\n\s*\n+', '\n\n', txt)
    lines = [l.strip() for l in txt.splitlines()]
    # drop nav/boilerplate-ish short repeated lines
    lines = [l for l in lines if l]
    return "\n".join(lines)

content = {}
for key, path in PAGES.items():
    try:
        r = requests.get(SRC_URL + path, headers=HEAD, timeout=25)
        r.encoding = r.apparent_encoding or "utf-8"
        if r.status_code != 200:
            print(f"  {key}: HTTP {r.status_code}"); continue
        t = to_text(r.text)
        content[key] = t
        print(f"  {key}: {len(t)} chars")
    except Exception as e:
        print(f"  {key}: ERR {e}")

with open(os.path.join(DATA_DIR, "content.json"), "w", encoding="utf-8") as f:
    json.dump(content, f, ensure_ascii=False, indent=2)
print("\nsaved data/content.json")
