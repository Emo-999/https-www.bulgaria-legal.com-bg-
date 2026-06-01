"""Test: do regular pages render their `content` HTML on the storefront?
Also check the existing Terms page render."""
import json, sys, requests
sys.stdout.reconfigure(encoding='utf-8')
from cc_graphql import gql
from config import CC_STORE

H = {"User-Agent": "Mozilla/5.0"}
M = "BL_PAGE_CONTENT_TEST_42"

# Create a regular page with marker content
r = gql('mutation($input:CreatePageInput!){ createPage(input:$input){ id name urlHandle } }',
        {"input": {"name": "BL Test", "type": "regular", "url_handle": "bl-test-42",
                   "content": f"<h2>{M}</h2><p>render check</p>", "active": "yes"}})
print("createPage:", json.dumps(r.get("data") or r.get("errors"), ensure_ascii=False)[:400])
pid = ((r.get("data") or {}).get("createPage") or {}).get("id")

import time
def check(url):
    try:
        h = requests.get(url, headers=H, timeout=25).text
        return len(h), (M in h)
    except Exception as e:
        return 0, f"ERR {e}"

for path in ["/bl-test-42", "/bl-test-42/", f"/page/bl-test-42"]:
    ln, found = check(f"https://{CC_STORE}{path}")
    print(f"  {path}: len={ln} marker={found}")

# existing terms page
print("\nTerms page (id 1) content:")
t = gql('query{ page(id:1){ name urlHandle content } }')
td = (t.get("data") or {}).get("page") or {}
print("  urlHandle:", td.get("urlHandle"), "content len:", len(td.get("content") or ""))
ln, found = check(f"https://{CC_STORE}/{td.get('urlHandle')}")
print(f"  live /{td.get('urlHandle')}: len={ln}")

# cleanup test page
if pid:
    d = gql('mutation($id:ID!){ deletePage(id:$id) }', {"id": pid})
    print("\ncleanup deletePage:", json.dumps(d.get("data") or d.get("errors"), ensure_ascii=False)[:200])
