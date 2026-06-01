# -*- coding: utf-8 -*-
"""Populate the native CloudCart page builder for Home (page id 2) with the premium
homepage as editable, reorderable widgets — one `code` widget per section.

Why code widgets: this theme's storefront renders the homepage ONLY via the grid
builder (no native layout theme-vars), and the GraphQL builder API stores but does not
itself render (verified). Putting the design here makes the Home page builder fully
populated & editable in the admin; the live look meanwhile comes from the Custom CSS/JS
injection, which AUTO-DEFERS (skips) once these sections render natively (.bl-sx guard).
So: edit/reorder sections in the admin builder, Publish there to go fully native."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
from cc_graphql import gql
import home_content as HC

# one row per section -> each is an independently reorderable block in the admin builder
rows = []
for key, label, html in HC.home_sections():
    rows.append({"columns": [{"widgets": [
        {"map": "code", "settings": {"enabled": True, "code": html}}
    ]}]})
design = {"rows": rows}

print(f"Pushing {len(rows)} native builder sections to Home (page 2):")
for key, label, _ in HC.home_sections():
    print(f"   • {label}")

r = gql('mutation($pageId:ID!,$input:SaveBuilderDesignInput!){ savePageBuilderDesign(pageId:$pageId,input:$input){ id pageId published } }',
        {"pageId": "2", "input": {"design": design, "publish": True}})
if r.get("errors"):
    print("ERROR:", json.dumps(r["errors"], ensure_ascii=False)[:300])
else:
    print("\nsaved native builder design:", json.dumps(r.get("data"), ensure_ascii=False))

# verify stored
v = gql("query{ pageBuilderDesign(pageId:2) }")
rows_back = ((v.get("data") or {}).get("pageBuilderDesign") or {}).get("rows") or []
print(f"verified stored rows: {len(rows_back)}")
