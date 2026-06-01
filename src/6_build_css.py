# -*- coding: utf-8 -*-
"""Assemble and deploy the master customCssJs: the reliable layer that themes the store,
injects a premium homepage, dark footer, topbar and logo. (Builder API does not render,
theme-variable mutation errors out — per repo readme stepping stones.)"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
from cc_graphql import gql
import brand as B
import home_content as HC
from config import OUTPUT_DIR

S = B.site()
SV = S["services"]
A = S["assets"]
HERO = HC.HERO
ABOUT_IMG = HC.ABOUT_IMG
ICONS = B.ICONS

# ============================================================ CSS
def css():
    return f"""{B.FONT_IMPORT}
:root{{--ink:{B.INK};--ink2:{B.INK_2};--crimson:{B.CRIMSON};--crimson-d:{B.CRIMSON_D};
--gold:{B.GOLD};--gold-d:{B.GOLD_D};--slate:{B.SLATE};--paper:{B.PAPER};--paper2:{B.PAPER_2};
--line:{B.LINE};--text:{B.TEXT};--muted:{B.MUTED};--serif:{B.SERIF};--sans:{B.SANS};}}

/* ---- Base typography & palette ---- */
body,._wrapper{{font-family:var(--sans)!important;color:var(--text)!important;background:var(--paper)!important;}}
h1,h2,h3,h4,._section-title,._page-title,.bl-h{{font-family:var(--serif)!important;color:var(--ink)!important;letter-spacing:.2px;}}
a{{color:var(--crimson);}} a:hover{{color:var(--crimson-d);}}
._button,._button-primary,button._button{{background:var(--crimson)!important;border-color:var(--crimson)!important;color:#fff!important;
border-radius:2px!important;letter-spacing:.4px;font-weight:600!important;}}
._button:hover{{background:var(--crimson-d)!important;border-color:var(--crimson-d)!important;}}
._header,._navbar,._navbar-inner{{background:var(--paper)!important;border-color:var(--line)!important;}}
._navigation a,._navigation-main-list-item>a{{color:var(--ink)!important;font-family:var(--sans)!important;font-weight:600!important;
letter-spacing:.3px;text-transform:uppercase;font-size:13px!important;}}
._navigation a:hover,._navigation-main-list-item.active>a{{color:var(--crimson)!important;}}
/* Top-nav item hover/active: keep header white (no dark box), crimson text + gold underline */
._navigation-main-list-item,._navigation-main-list-item>a,._navigation-main-list-item-link,
._navigation-main-list-item ._figure-stack{{background:transparent!important;background-color:transparent!important;}}
._navigation-main-list-item:hover,._navigation-main-list-item.active,
._navigation-main-list-item:hover>a,._navigation-main-list-item.active>a,
._navigation-main-list-item:hover ._figure-stack,._navigation-main-list-item.active ._figure-stack,
._navigation-main-list-item-link:hover{{background:#fff!important;background-color:#fff!important;color:var(--crimson)!important;}}
._navigation-main-list-item:hover ._figure-stack-label,._navigation-main-list-item.active ._figure-stack-label{{color:var(--crimson)!important;}}
._content{{background:var(--paper);}}
/* Dropdown / megamenu panel — white & readable for consistency */
._navigation-dropdown,._navigation-dropdown-level-1,._navbar ._navigation-dropdown,
._type-megamenu ._navigation-dropdown,._type-megamenu-two ._navigation-dropdown{{
  background:#ffffff!important;box-shadow:0 22px 54px rgba(21,23,28,.16)!important;
  border-top:2px solid var(--gold)!important;padding:24px 10px!important;}}
._navigation-dropdown-list-item>a,._navigation-dropdown a{{color:var(--ink)!important;
  font-weight:600!important;text-transform:none!important;font-size:14px!important;letter-spacing:.2px;}}
._navigation-dropdown-list-item>a:hover,._navigation-dropdown a:hover{{color:var(--crimson)!important;}}
._navigation-dropdown-list-item{{border:0!important;}}

/* ---- Topbar ---- */
.bl-topbar{{background:var(--ink);color:#E9E6E1;font-family:var(--sans);font-size:13px;}}
.bl-topbar .bl-tb-in{{max-width:1200px;margin:0 auto;padding:8px 20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;}}
.bl-topbar a{{color:#E9E6E1;text-decoration:none;margin-right:18px;transition:.2s;}}
.bl-topbar a:hover{{color:var(--gold);}}
.bl-topbar i{{color:var(--gold);margin-right:7px;}}
.bl-topbar .bl-langs a{{margin:0 4px;font-weight:600;}}

/* ---- Logo ---- */
._logo img{{max-height:58px!important;width:auto!important;}}

/* =========================================================== HOMEPAGE */
.bl-home{{font-family:var(--sans);}}
.bl-home section{{position:relative;}}
.bl-wrap{{max-width:1200px;margin:0 auto;padding:0 22px;}}
.bl-eyebrow{{display:inline-block;font-size:13px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--gold);margin-bottom:18px;}}
.bl-rule{{width:54px;height:2px;background:var(--gold);border:0;margin:0 0 22px;}}
.bl-center .bl-rule{{margin:0 auto 22px;}}

/* Hero */
.bl-hero{{min-height:640px;display:flex;align-items:center;
background:linear-gradient(100deg,rgba(15,16,20,.96) 0%,rgba(15,16,20,.92) 46%,rgba(15,16,20,.80) 72%,rgba(15,16,20,.72) 100%),url('{HERO}');
background-size:cover;background-position:center right;}}
.bl-hero .bl-wrap{{padding-top:90px;padding-bottom:90px;}}
.bl-hero-card{{max-width:640px;}}
.bl-hero h1{{color:#fff!important;font-size:54px;line-height:1.08;font-weight:700;margin:0 0 22px;}}
.bl-hero h1 em{{font-style:normal;color:var(--gold)!important;}}
.bl-hero p{{color:#D9DBDF;font-size:18px;line-height:1.65;margin:0 0 34px;max-width:540px;}}
.bl-btn{{display:inline-block;padding:15px 30px;border-radius:2px;font-weight:700;font-size:14px;letter-spacing:.6px;
text-transform:uppercase;text-decoration:none;transition:.22s;border:2px solid transparent;}}
.bl-btn-primary{{background:var(--crimson);color:#fff;border-color:var(--crimson);}}
.bl-btn-primary:hover{{background:var(--crimson-d);border-color:var(--crimson-d);color:#fff;}}
.bl-btn-ghost{{background:transparent;color:#fff;border-color:rgba(255,255,255,.45);margin-left:14px;}}
.bl-btn-ghost:hover{{background:var(--gold);border-color:var(--gold);color:var(--ink);}}

/* Stats bar */
.bl-stats{{background:var(--ink2);}}
.bl-stats .bl-wrap{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;padding:34px 22px;}}
.bl-stat{{text-align:center;color:#fff;border-right:1px solid rgba(255,255,255,.1);}}
.bl-stat:last-child{{border-right:0;}}
.bl-stat b{{display:block;font-family:var(--serif);font-size:38px;color:var(--gold);line-height:1;}}
.bl-stat span{{display:block;margin-top:8px;font-size:13px;letter-spacing:1px;text-transform:uppercase;color:#B9BCC2;}}

/* Section shell */
.bl-sec{{padding:88px 0;}}
.bl-sec.alt{{background:var(--paper2);}}
.bl-sec-head{{margin-bottom:48px;}}
.bl-center{{text-align:center;}}
.bl-sec h2{{font-size:40px;line-height:1.12;margin:0 0 14px;color:var(--ink)!important;}}
.bl-sec .bl-lead{{color:var(--muted);font-size:17px;max-width:680px;line-height:1.7;margin:0;}}
.bl-center .bl-lead{{margin:0 auto;}}

/* Services grid */
.bl-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;}}
.bl-card{{background:var(--paper);border:1px solid var(--line);padding:36px 30px;transition:.25s;position:relative;overflow:hidden;}}
.bl-card:before{{content:"";position:absolute;top:0;left:0;width:100%;height:3px;background:var(--gold);transform:scaleX(0);transform-origin:left;transition:.3s;}}
.bl-card:hover{{box-shadow:0 18px 48px rgba(21,23,28,.13);transform:translateY(-4px);border-color:transparent;}}
.bl-card:hover:before{{transform:scaleX(1);}}
.bl-card .bl-ic{{font-size:30px;color:var(--crimson);margin-bottom:20px;display:block;}}
.bl-card h3{{font-size:21px;margin:0 0 12px;color:var(--ink)!important;line-height:1.25;}}
.bl-card p{{color:var(--muted);font-size:14.5px;line-height:1.65;margin:0 0 18px;}}
.bl-card a.bl-more{{font-weight:700;font-size:13px;letter-spacing:.6px;text-transform:uppercase;color:var(--crimson);text-decoration:none;}}
.bl-card a.bl-more i{{transition:.2s;margin-left:6px;}}
.bl-card:hover a.bl-more i{{margin-left:11px;}}

/* About split */
.bl-split{{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center;}}
.bl-split img{{width:100%;height:100%;max-height:460px;object-fit:cover;display:block;}}
.bl-split .bl-imgwrap{{position:relative;}}
.bl-split .bl-imgwrap:after{{content:"";position:absolute;inset:14px -14px -14px 14px;border:2px solid var(--gold);z-index:-1;}}
.bl-split h2{{font-size:38px;margin:0 0 18px;}}
.bl-split p{{color:var(--muted);font-size:16px;line-height:1.8;margin:0 0 18px;}}
.bl-split .bl-sign{{font-family:var(--serif);font-style:italic;color:var(--ink);font-size:18px;border-left:3px solid var(--gold);padding-left:16px;margin:24px 0;}}

/* Values */
.bl-vals{{display:grid;grid-template-columns:repeat(4,1fr);gap:30px;}}
.bl-val{{text-align:center;}}
.bl-val i{{font-size:34px;color:var(--gold);margin-bottom:18px;}}
.bl-val h4{{font-family:var(--serif);font-size:20px;color:var(--ink);margin:0 0 10px;}}
.bl-val p{{color:var(--muted);font-size:14px;line-height:1.6;margin:0;}}

/* Offices */
.bl-offices{{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;}}
.bl-office{{background:var(--paper);border:1px solid var(--line);padding:32px 30px;}}
.bl-office .bl-ic{{color:var(--crimson);font-size:24px;margin-bottom:14px;}}
.bl-office h4{{font-family:var(--serif);font-size:23px;color:var(--ink);margin:0 0 10px;}}
.bl-office p{{color:var(--muted);font-size:14.5px;line-height:1.7;margin:0 0 6px;}}
.bl-office a{{color:var(--ink);font-weight:700;text-decoration:none;}}
.bl-office a:hover{{color:var(--crimson);}}

/* CTA band */
.bl-cta{{background:linear-gradient(rgba(15,16,20,.9),rgba(15,16,20,.9)),url('{ABOUT_IMG}');background-size:cover;background-position:center;text-align:center;padding:84px 0;}}
.bl-cta h2{{color:#fff!important;font-size:42px;margin:0 0 16px;}}
.bl-cta p{{color:#D9DBDF;font-size:18px;margin:0 0 30px;}}

/* =========================================================== FOOTER */
._footer,._footer *{{font-family:var(--sans)!important;}}
.bl-footer{{background:var(--ink);color:#C7C9CE;}}
.bl-footer .bl-wrap{{padding:64px 22px 30px;}}
.bl-fcols{{display:grid;grid-template-columns:1.4fr 1fr 1fr 1.1fr;gap:40px;}}
.bl-footer h5{{font-family:var(--serif);color:#fff;font-size:19px;margin:0 0 20px;position:relative;padding-bottom:12px;}}
.bl-footer h5:after{{content:"";position:absolute;left:0;bottom:0;width:36px;height:2px;background:var(--gold);}}
.bl-footer p,.bl-footer li,.bl-footer a{{color:#AEB1B8;font-size:14px;line-height:1.9;text-decoration:none;}}
.bl-footer a:hover{{color:var(--gold);}}
.bl-footer ul{{list-style:none;padding:0;margin:0;}}
.bl-footer .bl-flogo{{font-family:var(--serif);font-size:24px;color:#fff;margin-bottom:14px;display:block;}}
.bl-footer .bl-flogo span{{color:var(--crimson);}}
.bl-footer .bl-fcontact i{{color:var(--gold);width:20px;}}
.bl-fsoc{{margin-top:18px;}}
.bl-fsoc a{{display:inline-flex;width:38px;height:38px;border:1px solid #2E323A;border-radius:50%;align-items:center;justify-content:center;margin-right:8px;color:#C7C9CE;transition:.2s;}}
.bl-fsoc a:hover{{background:var(--gold);border-color:var(--gold);color:var(--ink);}}
.bl-fbottom{{border-top:1px solid #2A2D34;margin-top:46px;padding-top:24px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;font-size:13px;color:#8A8D94;}}

/* Native page-builder compatibility: when sections render as grid widgets, sit flush */
._grid-row .bl-sx,._grid-section .bl-sx,._widget .bl-sx,.cc-widget .bl-sx{{margin:0!important;}}
._content ._grid-row:has(.bl-sx),._content ._grid-section:has(.bl-sx){{padding:0!important;max-width:none!important;}}
.bl-sx{{width:100%;}}

/* =========================================================== Content pages */
.bl-page{{max-width:1000px;margin:0 auto;padding:18px 4px 40px;font-family:var(--sans);}}
.bl-page h1{{font-size:40px;margin:0 0 8px;}}
.bl-page .bl-rule{{margin-bottom:28px;}}
.bl-page h2{{font-size:27px;margin:34px 0 14px;}}
.bl-page p,.bl-page li{{color:var(--text);font-size:16px;line-height:1.85;}}
.bl-page ul{{padding-left:0;list-style:none;}}
.bl-page ul li{{position:relative;padding-left:26px;margin-bottom:8px;}}
.bl-page ul li:before{{content:"\\2014";position:absolute;left:0;color:var(--gold);font-weight:700;}}
.bl-lede{{font-size:19px!important;color:var(--ink)!important;line-height:1.7!important;border-left:3px solid var(--gold);padding-left:20px;margin:0 0 26px!important;}}
.bl-svc-cta{{background:var(--paper2);border:1px solid var(--line);padding:30px;margin-top:36px;text-align:center;}}
.bl-svc-cta h3{{font-family:var(--serif);font-size:24px;color:var(--ink);margin:0 0 8px;}}
.bl-svc-cta p{{color:var(--muted);margin:0 0 18px;}}

/* =========================================================== Responsive */
@media(max-width:992px){{.bl-grid,.bl-offices{{grid-template-columns:repeat(2,1fr);}}.bl-vals{{grid-template-columns:repeat(2,1fr);}}
.bl-split{{grid-template-columns:1fr;gap:34px;}}.bl-stats .bl-wrap{{grid-template-columns:repeat(2,1fr);}}.bl-fcols{{grid-template-columns:1fr 1fr;}}}}
@media(max-width:640px){{.bl-hero h1{{font-size:36px;}}.bl-sec h2,.bl-cta h2{{font-size:30px;}}.bl-grid,.bl-offices,.bl-vals{{grid-template-columns:1fr;}}
.bl-btn-ghost{{margin-left:0;margin-top:12px;}}.bl-sec{{padding:60px 0;}}.bl-fcols{{grid-template-columns:1fr;}}}}
"""

# ============================================================ JS (topbar, logo, home, footer)
def js():
    home = HC.home_html().replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    foot = HC.footer_html().replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    o = S["offices"]
    return f"""
(function(){{
  function ready(fn){{ if(document.readyState!='loading') fn(); else document.addEventListener('DOMContentLoaded',fn); }}
  ready(function(){{
    // ---- Topbar ----
    if(!document.querySelector('.bl-topbar')){{
      var tb=document.createElement('div'); tb.className='bl-topbar';
      tb.innerHTML='<div class="bl-tb-in"><div class="bl-tb-left">'+
        '<a href="tel:{o[0]["tel"].replace(" ","")}"><i class="fal fa-phone"></i>{o[0]["tel"]}</a>'+
        '<a href="mailto:{S["email"]}"><i class="fal fa-envelope"></i>{S["email"]}</a></div>'+
        '<div class="bl-langs"><i class="fal fa-globe" style="color:var(--gold)"></i> '+
        '<a href="/">BG</a><a href="/ru">RU</a><a href="/en">EN</a></div></div>';
      var hdr=document.querySelector('._header'); if(hdr) hdr.parentNode.insertBefore(tb,hdr);
    }}
    // ---- Logo ----
    var lg=document.querySelector('._logo img'); if(lg) lg.src='{A["logo_bg"]}';
    // ---- Homepage (only on '/'). Auto-defers: if the native page-builder version
    //      (sections marked .bl-sx) is already rendered, we DON'T inject. ----
    var p=location.pathname.replace(/\\/+$/,'');
    if(p===''||p==='/'){{
      var main=document.querySelector('main._content')||document.querySelector('._content');
      if(main && !main.querySelector('.bl-sx')){{ main.innerHTML=`{home}`; }}
      document.title='{S["firm"]} | Bulgaria Legal';
    }}
    // ---- Footer ----
    var ft=document.querySelector('._footer');
    if(ft && !document.querySelector('.bl-footer')){{
      ft.innerHTML=`{foot}`; ft.style.background='{B.INK}'; ft.style.padding='0';
    }}
  }});
}})();"""

def build():
    content = "<style>\n" + css() + "\n</style>\n<script>" + js() + "</script>"
    return content

if __name__ == "__main__":
    content = build()
    print(f"customCssJs total: {len(content)} chars  (limit ~65000)")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    open(os.path.join(OUTPUT_DIR, "custom_css_js.txt"), "w", encoding="utf-8").write(content)
    if len(content) > 64000:
        print("!! TOO LARGE — trim before deploy"); sys.exit(1)
    r = gql('mutation($content:String!){ updateCustomCssJs(content:$content) }', {"content": content})
    print("deploy:", "OK" if not r.get("errors") else json.dumps(r["errors"], ensure_ascii=False)[:300])
