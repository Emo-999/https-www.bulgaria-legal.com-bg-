"""Scrape bulgaria-legal.com: collect page links + the site's OWN asset URLs (logo, images).
Per instruction: reuse only assets already on the live site."""
import json, os, re, sys
import requests
sys.stdout.reconfigure(encoding='utf-8')
from config import SRC_URL, DATA_DIR

HEAD = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def get(url):
    try:
        r = requests.get(url, headers=HEAD, timeout=25)
        r.encoding = r.apparent_encoding or "utf-8"
        return r.text if r.status_code == 200 else ""
    except Exception as e:
        print("  ! fetch fail", url, e); return ""

home = get(SRC_URL + "/bg/")
print(f"home html: {len(home)} chars")

# --- internal links ---
links = sorted(set(re.findall(r'href="(https?://[^"]*bulgaria-legal\.com[^"]*)"', home)
                 + ["%s%s" % (SRC_URL, m) for m in re.findall(r'href="(/[^"]*)"', home)]))
links = [l for l in links if not re.search(r'\.(jpg|jpeg|png|gif|svg|css|js|webp|ico|pdf)(\?|$)', l, re.I)]

# --- images (the site's own assets) ---
imgs = re.findall(r'(?:src|data-src|data-lazy-src)="([^"]+\.(?:jpg|jpeg|png|webp|svg|gif)[^"]*)"', home, re.I)
imgs += re.findall(r'background-image:\s*url\(([^)]+)\)', home, re.I)
def norm(u):
    u = u.strip(' \'"')
    if u.startswith("//"): return "https:" + u
    if u.startswith("/"): return SRC_URL + u
    return u
imgs = sorted(set(norm(u) for u in imgs if "data:" not in u))

# logo guess
logo = [u for u in imgs if re.search(r'logo', u, re.I)]

# css files (to inspect brand colors/fonts if needed)
css = sorted(set(norm(u) for u in re.findall(r'href="([^"]+\.css[^"]*)"', home)))

out = {"home_len": len(home), "links": links, "images": imgs, "logo_candidates": logo, "css": css}
os.makedirs(DATA_DIR, exist_ok=True)
with open(os.path.join(DATA_DIR, "site_map.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
# save raw home for content extraction
with open(os.path.join(DATA_DIR, "home.html"), "w", encoding="utf-8") as f:
    f.write(home)

print(f"\nINTERNAL LINKS ({len(links)}):"); [print("  ", l) for l in links[:40]]
print(f"\nIMAGES ({len(imgs)}):"); [print("  ", u) for u in imgs[:50]]
print(f"\nLOGO CANDIDATES:"); [print("  ", u) for u in logo]
print(f"\nCSS:"); [print("  ", u) for u in css[:10]]
