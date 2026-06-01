"""Inspect current state of the CloudCart store: store info, pages, navigation, theme."""
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
from cc_graphql import gql

def show(title, result):
    print(f"\n{'='*60}\n{title}\n{'='*60}")
    print(json.dumps(result, indent=2, ensure_ascii=False)[:4000])

# 1. Store basics
show("STORE", gql("""query {
  store { id name domain currency { code } }
}"""))

# 2. Pages
show("PAGES", gql("""query {
  pages { id name url_handle is_published }
}"""))

# 3. Navigation groups
show("NAV (header)", gql('query { navigation(group: "header") { items { id name type order url } } }'))
show("NAV (footer)", gql('query { navigation(group: "footer") { items { id name type order url } } }'))

# 4. Custom CSS/JS length
r = gql("query { customCssJs }")
css = (r.get("data") or {}).get("customCssJs") or ""
print(f"\ncustomCssJs length: {len(css)} chars")
