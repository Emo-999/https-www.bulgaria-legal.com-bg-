"""Introspect the live GraphQL schema for the shapes we need."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
from cc_graphql import gql

def type_fields(name):
    q = '''query($n:String!){ __type(name:$n){ name kind
        fields { name args{name type{name kind ofType{name kind ofType{name}}}}
                 type{ name kind ofType{ name kind ofType{ name } } } }
        inputFields { name type{ name kind ofType{name kind ofType{name}} } }
    } }'''
    r = gql(q, {"n": name})
    t = (r.get("data") or {}).get("__type")
    if not t:
        print(f"\n## {name}: NOT FOUND  {r.get('errors')}")
        return
    print(f"\n## {name} ({t['kind']})")
    for f in (t.get("fields") or []):
        ty = f["type"]
        tn = ty.get("name") or (ty.get("ofType") or {}).get("name") or ((ty.get("ofType") or {}).get("ofType") or {}).get("name")
        args = ",".join(a["name"] for a in (f.get("args") or []))
        argstr = f"({args})" if args else ""
        print(f"   {f['name']}{argstr} -> {tn}")
    for f in (t.get("inputFields") or []):
        ty = f["type"]
        tn = ty.get("name") or (ty.get("ofType") or {}).get("name")
        print(f"   [in] {f['name']} : {tn}")

# Root query + mutation field lists
for root in ["Query", "Mutation"]:
    q = '''query($n:String!){ __type(name:$n){ fields{ name args{name} type{name kind ofType{name}} } } }'''
    r = gql(q, {"n": root})
    t = (r.get("data") or {}).get("__type")
    print(f"\n{'='*60}\n{root} FIELDS\n{'='*60}")
    for f in (t.get("fields") or []):
        args = ",".join(a["name"] for a in (f.get("args") or []))
        print(f"   {f['name']}({args})")

for name in ["Store", "Page", "PageConnection", "Navigation", "NavigationItem", "Theme"]:
    type_fields(name)
