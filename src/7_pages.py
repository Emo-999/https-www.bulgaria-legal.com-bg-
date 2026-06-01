# -*- coding: utf-8 -*-
"""Create/update the content pages (regular pages render at /page/{handle}).
Pages: За нас, Услуги, 12 service pages, Контакти, Новини, Политика."""
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
from cc_graphql import gql
import brand as B

S = B.site(); SV = S["services"]; O = S["offices"]
CUT = ["Контакти\nВарна", "\nКонтакти\n", "Социални мрежи", "Всички права запазени",
       "Мисията ни е да предоставим висококачествена услуга на клиентите си."]

def esc(t): return (t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))

def clean_body(body, title):
    # cut footer noise
    idx = len(body)
    for m in CUT:
        i = body.find(m)
        if i != -1: idx = min(idx, i)
    body = body[:idx].strip()
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    # drop leading title duplicate
    if lines and lines[0].lower().strip(" .").startswith(title.lower().split()[0][:6]):
        lines = lines[1:]
    return lines

def body_to_html(body, title):
    lines = clean_body(body, title)
    html, ul = [], []
    def flush():
        if ul: html.append("<ul>" + "".join(f"<li>{esc(x)}</li>" for x in ul) + "</ul>"); ul.clear()
    for ln in lines:
        if ln.startswith("•") or ln.startswith("-"):
            ul.append(ln.lstrip("•-").strip().rstrip(";"))
        else:
            flush()
            html.append(f"<p>{esc(ln)}</p>")
    flush()
    return "".join(html)

def page_shell(title, inner, seo_desc=""):
    return (f'<div class="bl-page"><h1>{esc(title)}</h1><hr class="bl-rule">{inner}</div>')

def svc_cta():
    return ('<div class="bl-svc-cta"><h3>Нуждаете се от правен съвет?</h3>'
            '<p>Свържете се с нас за консултация по вашия случай.</p>'
            '<a class="bl-btn bl-btn-primary" href="/page/kontakti">Безплатна консултация</a></div>')

def about_page():
    vals = [("Експертиза","Дълбок правен опит в широк кръг практики."),
            ("Ангажираност","Отдаваме се изцяло на всеки случай."),
            ("Дискретност","Пълна конфиденциалност и доверие."),
            ("Резултат","Решаваме проблемите рано и ефективно.")]
    body = body_to_html(S["about_full"], "за нас")
    vh = "".join(f'<div class="bl-val"><i class="fal fa-gem"></i><h4>{t}</h4><p>{d}</p></div>' for t,d in vals)
    inner = (f'<p class="bl-lede">{esc(S["about_short"])}</p>{body}'
             f'<div class="bl-sign" style="font-family:var(--serif);font-style:italic;border-left:3px solid var(--gold);padding-left:18px;margin:26px 0;font-size:18px;color:var(--ink)">{esc(S["mission"])}</div>'
             f'<h2>Нашите ценности</h2><div class="bl-vals" style="margin-top:24px">{vh}</div>{svc_cta()}')
    return page_shell("За нас", inner)

def uslugi_page():
    cards = "".join(
        f'<div class="bl-card"><i class="fal {B.ICONS.get(sv["key"],"fa-scale-balanced")} bl-ic"></i><h3>{esc(sv["title"])}</h3>'
        f'<p>{esc(sv["blurb"])}</p><a class="bl-more" href="/page/{sv["url_handle"]}">Научете повече <i class="fal fa-arrow-right"></i></a></div>'
        for sv in SV)
    inner = (f'<p class="bl-lede">Предлагаме пълно правно съдействие за бизнеса и гражданите. '
             f'Изберете практика, за да научите повече.</p>'
             f'<div class="bl-grid" style="margin-top:30px">{cards}</div>{svc_cta()}')
    return page_shell("Услуги", inner)

def kontakti_page():
    offs = "".join(
        f'<div class="bl-office"><i class="fal fa-location-dot bl-ic"></i><h4>{esc(o["city"])}</h4>'
        f'<p>{esc(o["addr"])}</p><p>Тел.: <a href="tel:{o["tel"].replace(" ","")}">{esc(o["tel"])}</a></p>'
        + (f'<p>Факс: {esc(o["fax"])}</p>' if o.get("fax") else "") + '</div>'
        for o in O)
    inner = (f'<p class="bl-lede">Свържете се с нас или ни посетете в някой от офисите ни във Варна, София и Великобритания. '
             f'Моля, не изпращайте поверителна информация по имейл.</p>'
             f'<div class="bl-offices" style="margin:30px 0">{offs}</div>'
             f'<div class="bl-svc-cta"><h3>Запазете час за среща</h3>'
             f'<p><i class="fal fa-envelope"></i> <a href="mailto:{S["email"]}">{S["email"]}</a> &nbsp;·&nbsp; '
             f'<i class="fal fa-phone"></i> <a href="tel:{S["mobile"].replace(" ","")}">{S["mobile"]}</a></p>'
             f'<a class="bl-btn bl-btn-primary" href="mailto:{S["email"]}">Пишете ни</a></div>')
    return page_shell("Контакти", inner)

def privacy_page():
    inner = ('<p class="bl-lede">Ние се отнасяме отговорно към защитата на вашите лични данни в съответствие с '
             'Регламент (ЕС) 2016/679 (GDPR) и приложимото българско законодателство.</p>'
             '<p>Личните данни, които ни предоставяте, се обработват единствено за целите на предоставяните '
             'правни услуги и комуникацията с вас. Не предоставяме вашите данни на трети лица без вашето съгласие, '
             'освен когато това се изисква по закон.</p>'
             '<h2>Вашите права</h2><ul><li>Достъп до събраните за вас лични данни</li>'
             '<li>Коригиране на неточни данни</li><li>Изтриване („право да бъдеш забравен“)</li>'
             '<li>Ограничаване на обработването и възражение</li></ul>'
             f'<p>За въпроси относно личните ви данни: <a href="mailto:{S["email"]}">{S["email"]}</a>.</p>')
    return page_shell("Политика за защита на личните данни", inner)

def news_page():
    inner = ('<p class="bl-lede">Актуални новини, правни анализи и коментари от екипа на Bulgaria Legal.</p>'
             '<p>Очаквайте скоро нашите публикации. За въпроси и консултации сме на ваше разположение.</p>'
             + svc_cta())
    return page_shell("Новини", inner)

# ---- assemble page set ----
PAGES = [
    ("За нас", "za-nas", about_page(), "Адвокатско дружество ГС Георгиева и партньори — за нас."),
    ("Услуги", "uslugi", uslugi_page(), "Правни услуги на Bulgaria Legal."),
    ("Контакти", "kontakti", kontakti_page(), "Контакти и офиси на Bulgaria Legal — Варна, София, UK."),
    ("Новини", "news", news_page(), "Новини и правни анализи."),
    ("Политика за защита на личните данни", "privacy", privacy_page(), "Политика за поверителност."),
]
for sv in SV:
    inner = (f'<p class="bl-lede">{esc(sv["blurb"])}</p>{body_to_html(sv["full"], sv["title"])}{svc_cta()}')
    PAGES.append((sv["title"], sv["url_handle"], page_shell(sv["title"], inner),
                  f'{sv["title"]} — Bulgaria Legal'))

# existing pages by handle
ex = gql("query{ pages(first:100){ edges{ node{ id name urlHandle } } } }")
by_handle = {e["node"]["urlHandle"]: e["node"]["id"] for e in (ex.get("data") or {}).get("pages",{}).get("edges",[])}

for name, handle, content, seo in PAGES:
    pid = by_handle.get(handle)
    if pid:
        r = gql('mutation($id:ID!,$input:UpdatePageInput!){ updatePage(id:$id,input:$input){ id } }',
                {"id": pid, "input": {"name": name, "content": content, "seo_description": seo, "active": "yes"}})
        act = "updated"
    else:
        r = gql('mutation($input:CreatePageInput!){ createPage(input:$input){ id urlHandle } }',
                {"input": {"name": name, "type": "regular", "url_handle": handle,
                           "content": content, "seo_description": seo, "active": "yes"}})
        act = "created"
    ok = "OK" if not r.get("errors") else json.dumps(r["errors"], ensure_ascii=False)[:160]
    print(f"  [{act}] /page/{handle}  ({len(content)} chars)  {ok}")
print("\nDone — pages built.")
