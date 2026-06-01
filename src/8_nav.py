# -*- coding: utf-8 -*-
"""Build header navigation: За нас, Услуги (dropdown of 12 practices), Новини, Контакти."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
from cc_graphql import gql
import brand as B

S = B.site(); SV = S["services"]

# page ids by handle
ex = gql("query{ pages(first:100){ edges{ node{ id urlHandle } } } }")
pid = {e["node"]["urlHandle"]: e["node"]["id"] for e in (ex.get("data") or {}).get("pages",{}).get("edges",[])}

# clear existing header items
cur = gql('query{ navigation(group:"main"){ items{ id } } }')
items = ((cur.get("data") or {}).get("navigation") or {}).get("items") or []
for it in items:
    gql('mutation($id:ID!){ deleteNavigationItem(id:$id) }', {"id": it["id"]})
print(f"cleared {len(items)} existing header items")

def add(name, handle, order, parent=None):
    inp = {"name": name, "type": "page", "linkId": pid.get(handle)}
    if parent: inp["parentId"] = parent
    r = gql('mutation($g:String!,$input:CreateNavigationItemInput!){ createNavigationItem(group:$g,input:$input){ id name } }',
            {"g": "main", "input": inp})
    if r.get("errors"):
        print(f"  ! {name}: {json.dumps(r['errors'],ensure_ascii=False)[:160]}"); return None
    return ((r.get("data") or {}).get("createNavigationItem") or {}).get("id")

add("За нас", "za-nas", 1)
uid = add("Услуги", "uslugi", 2)
print("Услуги id:", uid)
for i, sv in enumerate(SV, 1):
    add(sv["title"], sv["url_handle"], i, parent=uid)
add("Новини", "news", 3)
add("Контакти", "kontakti", 4)

# verify
v = gql('query{ navigation(group:"main"){ items{ id name order parentId } } }')
vi = ((v.get("data") or {}).get("navigation") or {}).get("items") or []
print(f"\nheader now has {len(vi)} items:")
for it in vi:
    pre = "   └ " if it.get("parentId") else " • "
    print(f"{pre}{it['name']}")
