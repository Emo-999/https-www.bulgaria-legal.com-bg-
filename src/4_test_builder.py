"""Empirically test whether the page builder renders on this store, and learn the design shape."""
import json, sys, requests
sys.stdout.reconfigure(encoding='utf-8')
from cc_graphql import gql
from config import CC_STORE

MARKER = "BL_BUILDER_RENDER_TEST_9X7"
code_widget = {"map": "code", "settings": {"enabled": True, "code": f"<div id='bltest'>{MARKER}</div>"}}

# Candidate design structures (grid builder shapes)
candidates = {
    "rows.columns.widgets": {"rows": [{"columns": [{"widgets": [code_widget]}]}]},
    "rows.sections.widgets": {"rows": [{"sections": [{"widgets": [code_widget]}]}]},
    "widgets_flat": {"widgets": [code_widget]},
    "blocks_flat": {"blocks": [code_widget]},
}

def publish(design):
    r = gql('mutation($pageId:ID!,$input:SaveBuilderDesignInput!){ savePageBuilderDesign(pageId:$pageId,input:$input){ id pageId published } }',
            {"pageId": "2", "input": {"design": design, "publish": True}})
    return r

# Try first candidate, read back normalized shape
name, design = list(candidates.items())[0]
print(f"Publishing candidate: {name}")
r = publish(design)
print("save result:", json.dumps(r.get("data") or r.get("errors"), ensure_ascii=False)[:400])

# Read back what the server stored/normalized
rb = gql('query{ pageBuilderDesign(pageId:2) }')
print("\nstored design shape:", json.dumps(rb.get("data"), ensure_ascii=False)[:1500])

# Fetch live homepage and look for marker
try:
    html = requests.get(f"https://{CC_STORE}/", headers={"User-Agent":"Mozilla/5.0"}, timeout=25).text
    print(f"\nlive home length: {len(html)}")
    print("MARKER FOUND ON LIVE PAGE:", MARKER in html)
    print("'_grid' classes present:", html.count("_grid-"))
except Exception as e:
    print("fetch error:", e)
