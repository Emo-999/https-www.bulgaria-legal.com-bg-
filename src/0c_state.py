"""Fetch current store state (corrected syntax: no-arg fields take no parens)."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
from cc_graphql import gql

def dump(title, r):
    print(f"\n{'='*60}\n{title}\n{'='*60}")
    if r.get("errors"):
        print("ERRORS:", json.dumps(r["errors"], ensure_ascii=False)[:500])
    print(json.dumps(r.get("data"), indent=2, ensure_ascii=False)[:3000])

dump("PAGES", gql("query { pages(first: 50) { edges { node { id name urlHandle systemPage type private active } } } }"))
dump("NAVIGATIONS", gql("query { navigations }"))
dump("NAV header", gql('query { navigation(group: "header") { group items { id name type order url parentId } } }'))
dump("themeSettings", gql("query { themeSettings }"))
dump("generalSettings", gql("query { generalSettings }"))

# return-type kinds for ambiguous root fields
def rtype(field):
    q='''query{__type(name:"Query"){fields{name type{name kind ofType{name kind}}}}}'''
    r=gql(q);
    for f in (r.get("data") or {}).get("__type",{}).get("fields",[]):
        if f["name"]==field:
            return f["type"]
    return None
for f in ["navigations","themeSettings","generalSettings","availableWidgets","customCssJs","availableFonts"]:
    print(f"  {f} -> {rtype(f)}")

# NavigationGroup shape
q='''query($n:String!){__type(name:$n){name kind fields{name type{name kind ofType{name}}}}}'''
print("\nNavigationGroup:", json.dumps(gql(q,{"n":"NavigationGroup"}).get("data"), ensure_ascii=False)[:800])
