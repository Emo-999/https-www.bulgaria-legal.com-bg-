# -*- coding: utf-8 -*-
"""Shared homepage + footer markup, as discrete sections.
Used by 6_build_css.py (CSS/JS injection — live render) AND 9_native_home.py
(pushes each section as a native, editable page-builder widget)."""
import brand as B

S = B.site(); SV = S["services"]; A = S["assets"]
HERO = "https://www.bulgaria-legal.com/files/actual_images/new-banner.jpg"
ABOUT_IMG = "https://www.bulgaria-legal.com/files/actual_images/22171580_m.jpg"
ICONS = B.ICONS

def service_cards():
    out = []
    for sv in SV:
        ic = ICONS.get(sv["key"], "fa-scale-balanced")
        out.append(
            f'<div class="bl-card"><i class="fal {ic} bl-ic"></i>'
            f'<h3>{sv["title"]}</h3><p>{sv["blurb"]}</p>'
            f'<a class="bl-more" href="/page/{sv["url_handle"]}">Научете повече <i class="fal fa-arrow-right"></i></a></div>'
        )
    return "".join(out)

def offices_html(cls="bl-office"):
    out = []
    icons = ["fa-location-dot", "fa-location-dot", "fa-earth-europe"]
    for o, ic in zip(S["offices"], icons):
        tel = o["tel"].replace(" ", "")
        out.append(
            f'<div class="{cls}"><i class="fal {ic} bl-ic"></i><h4>{o["city"]}</h4>'
            f'<p>{o["addr"]}</p><p>Тел.: <a href="tel:{tel}">{o["tel"]}</a></p>'
            + (f'<p>Факс: {o["fax"]}</p>' if o.get("fax") else "") + '</div>'
        )
    return "".join(out)

def _vals():
    vals = [
        ("fa-award", "Експертиза", "Дълбок правен опит в широк кръг от практики — от вещно до наказателно право."),
        ("fa-handshake-angle", "Ангажираност", "Вашият успех е нашата репутация. Отдаваме се изцяло на всеки случай."),
        ("fa-user-shield", "Дискретност", "Пълна конфиденциалност и доверие във всяко взаимоотношение с клиента."),
        ("fa-scale-balanced", "Резултат", "Решаваме проблемите рано — преди да прераснат в скъпоструващ правен спор."),
    ]
    return "".join(f'<div class="bl-val"><i class="fal {i}"></i><h4>{t}</h4><p>{d}</p></div>' for i,t,d in vals)

def home_sections():
    """Ordered list of (key, label, html). Each becomes one editable builder widget."""
    o = S["offices"]
    return [
        ("hero", "Hero банер",
         '<section class="bl-hero bl-sx"><div class="bl-wrap"><div class="bl-hero-card">'
         '<span class="bl-eyebrow">Адвокатско дружество · Варна · София · UK</span>'
         '<h1>Вашият успех е <em>нашата репутация</em></h1>'
         f'<p>{S["tagline"]} Съчетаваме бизнес проницателност и правен опит, за да защитим интересите ви на всеки етап.</p>'
         '<div><a class="bl-btn bl-btn-primary" href="/page/kontakti">Безплатна консултация</a>'
         '<a class="bl-btn bl-btn-ghost" href="/page/uslugi">Нашите услуги</a></div>'
         '</div></div></section>'),
        ("stats", "Статистика лента",
         '<section class="bl-stats bl-sx"><div class="bl-wrap">'
         '<div class="bl-stat"><b>12</b><span>Правни практики</span></div>'
         '<div class="bl-stat"><b>3</b><span>Офиса · BG &amp; UK</span></div>'
         '<div class="bl-stat"><b>3</b><span>Езика на обслужване</span></div>'
         '<div class="bl-stat"><b>100%</b><span>Индивидуален подход</span></div>'
         '</div></section>'),
        ("services", "Услуги (12 практики)",
         '<section class="bl-sec bl-sx"><div class="bl-wrap"><div class="bl-sec-head bl-center">'
         '<span class="bl-eyebrow">Какво предлагаме</span><hr class="bl-rule"><h2>Нашите правни услуги</h2>'
         '<p class="bl-lead">Пълно правно съдействие за бизнеса и гражданите — компетентно, прецизно и ориентирано към резултат.</p>'
         f'</div><div class="bl-grid">{service_cards()}</div></div></section>'),
        ("about", "За нас (секция)",
         '<section class="bl-sec alt bl-sx"><div class="bl-wrap"><div class="bl-split">'
         f'<div class="bl-imgwrap"><img src="{ABOUT_IMG}" alt="Bulgaria Legal"></div>'
         '<div><span class="bl-eyebrow">За нас</span><hr class="bl-rule"><h2>Млади, амбициозни и отдадени на резултата</h2>'
         f'<p>{S["about_short"]}</p><div class="bl-sign">{S["mission"]}</div>'
         '<a class="bl-btn bl-btn-primary" href="/page/za-nas">Повече за нас</a>'
         '</div></div></div></section>'),
        ("values", "Ценности",
         '<section class="bl-sec bl-sx"><div class="bl-wrap"><div class="bl-sec-head bl-center">'
         '<span class="bl-eyebrow">Защо да изберете нас</span><hr class="bl-rule"><h2>Принципите, които ни водят</h2></div>'
         f'<div class="bl-vals">{_vals()}</div></div></section>'),
        ("offices", "Офиси",
         '<section class="bl-sec alt bl-sx"><div class="bl-wrap"><div class="bl-sec-head bl-center">'
         '<span class="bl-eyebrow">Намерете ни</span><hr class="bl-rule"><h2>Нашите офиси</h2></div>'
         f'<div class="bl-offices">{offices_html()}</div></div></section>'),
        ("cta", "Призив за действие",
         '<section class="bl-cta bl-sx"><div class="bl-wrap">'
         '<h2>Имате правен въпрос?</h2><p>Свържете се с нас за консултация — ние сме насреща.</p>'
         '<a class="bl-btn bl-btn-primary" href="/page/kontakti">Запазете час за среща</a> '
         f'<a class="bl-btn bl-btn-ghost" href="tel:{S["mobile"].replace(" ","")}">{S["mobile"]}</a>'
         '</div></section>'),
    ]

def home_html():
    return '<div class="bl-home">' + "".join(h for _, _, h in home_sections()) + '</div>'

def footer_html():
    svc_links = "".join(f'<li><a href="/page/{sv["url_handle"]}">{sv["title"]}</a></li>' for sv in SV[:7])
    o = S["offices"]
    return (
        '<div class="bl-footer"><div class="bl-wrap"><div class="bl-fcols">'
        '<div><span class="bl-flogo">Bulgaria<span>.</span>Legal</span>'
        f'<p>{S["firm"]}</p><p>Висококачествени правни услуги и дългосрочно партньорство с всеки клиент.</p>'
        f'<div class="bl-fsoc"><a href="{S["social"]["facebook"]}" target="_blank" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>'
        f'<a href="{S["social"]["linkedin"]}" target="_blank" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a></div></div>'
        f'<div><h5>Услуги</h5><ul>{svc_links}<li><a href="/page/uslugi">Всички услуги &rarr;</a></li></ul></div>'
        '<div><h5>Фирма</h5><ul>'
        '<li><a href="/page/za-nas">За нас</a></li><li><a href="/page/uslugi">Услуги</a></li>'
        '<li><a href="/page/kontakti">Контакти</a></li><li><a href="/obshti-uslovia">Общи условия</a></li></ul></div>'
        '<div class="bl-fcontact"><h5>Контакти</h5><ul>'
        f'<li><i class="fal fa-location-dot"></i> {o[0]["city"]}: {o[0]["addr"]}</li>'
        f'<li><i class="fal fa-location-dot"></i> {o[1]["city"]}: {o[1]["addr"]}</li>'
        f'<li><i class="fal fa-phone"></i> <a href="tel:{o[0]["tel"].replace(" ","")}">{o[0]["tel"]}</a></li>'
        f'<li><i class="fal fa-envelope"></i> <a href="mailto:{S["email"]}">{S["email"]}</a></li>'
        '</ul></div>'
        '</div><div class="bl-fbottom">'
        f'<span>© 2026 {S["firm"]}. Всички права запазени.</span>'
        '<span><a href="/page/privacy">Политика за защита на личните данни</a></span>'
        '</div></div></div>'
    )
