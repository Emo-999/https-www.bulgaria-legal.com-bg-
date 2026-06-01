"""Consolidate scraped copy + assets into one clean dataset (data/site.json)."""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
from config import DATA_DIR

c = json.load(open(os.path.join(DATA_DIR, "content.json"), encoding="utf-8"))

def body(key):
    """Text after the last nav boilerplate marker."""
    t = c.get(key, "")
    seg = t.split("-->")[-1].strip()
    return seg

def intro(key, title):
    """First substantive paragraph (after the H1 title line)."""
    b = body(key)
    lines = [l for l in b.splitlines() if l.strip()]
    # skip lines that are the title or footer/contact noise
    skip = title.lower()
    for l in lines:
        ll = l.strip()
        if len(ll) < 60: continue
        if ll.lower().startswith(skip[:10]): continue
        if "контакт" in ll.lower() or "варна" in ll.lower(): continue
        return ll
    return ""

SRC = "https://www.bulgaria-legal.com/share/images/site"

# 12 practice areas: (key, title BG, url_handle, icon)
SERVICES = [
    ("veshchno-pravo",          "Вещно право",                               "veshtno-pravo",            f"{SRC}/serv1-bg.png"),
    ("trgovsko-pravo",          "Търговско право",                           "targovsko-pravo",          f"{SRC}/serv2-bg.png"),
    ("zastrahovatelno",         "Застрахователно право, претенции за вреди", "zastrahovatelno-pravo",    f"{SRC}/serv3-bg.png"),
    ("semeyno-nasledstveno",    "Семейно и наследствено право",              "semeyno-nasledstveno-pravo", f"{SRC}/serv4-bg.png"),
    ("mezhdunarodno-es",        "Международно частно право и право на ЕС",    "mezhdunarodno-pravo-es",   f"{SRC}/serv5-bg.png"),
    ("bankovo-pravo",           "Банково право",                             "bankovo-pravo",            f"{SRC}/serv6-bg.png"),
    ("danchno-administrativno", "Данъчно и административно право",            "danachno-administrativno-pravo", f"{SRC}/serv7-bg.png"),
    ("nakazatelno-pravo",       "Наказателно право",                         "nakazatelno-pravo",        f"{SRC}/serv8-bg.png"),
    ("energiya",                "Енергия и природни ресурси",                "energiya-prirodni-resursi", f"{SRC}/serv9-bg.png"),
    ("schetovodni",             "Счетоводни услуги",                         "schetovodni-uslugi",       f"{SRC}/serv1-bg.png"),
    ("ptp",                     "Претенции при ПТП, инциденти",              "pretentsii-ptp",           f"{SRC}/serv3-bg.png"),
    ("angliya-uels",            "Адвокат Англия и Уелс",                     "advokat-angliya-uels",     f"{SRC}/serv5-bg.png"),
]

# Curated one-line card blurbs (premium, consistent length), grounded in the real page copy
BLURBS = {
    "veshchno-pravo": "Сделки с недвижими имоти, прехвърляне и придобиване, ипотеки и вещноправен статус — с прецизност на всеки етап.",
    "trgovsko-pravo": "Учредяване и управление на дружества, корпоративни сделки и трудови отношения за български и чуждестранни клиенти.",
    "zastrahovatelno": "Застрахователни претенции и обезщетения за вреди — защитаваме правата ви пред застрахователя.",
    "semeyno-nasledstveno": "Развод, издръжка, осиновяване и наследствени въпроси — деликатно и компетентно отношение към личните дела.",
    "mezhdunarodno-es": "Трансгранични казуси, право на Европейския съюз и международно частно право за бизнеса и гражданите.",
    "bankovo-pravo": "Банкови сделки, кредитиране и обезпечения — правна сигурност във взаимоотношенията с финансови институции.",
    "danchno-administrativno": "Данъчни консултации и обжалване, представителство пред администрацията и данъчните органи.",
    "nakazatelno-pravo": "Защита по наказателни дела с опитен екип — отдадена и енергична защита на вашите права и свобода.",
    "energiya": "Енергетика и природни ресурси — регулаторни и договорни решения за устойчив и сигурен бизнес.",
    "schetovodni": "Счетоводно обслужване за оптимален финансов резултат, интегрирано с правните ви решения.",
    "ptp": "Претенции при ПТП и инциденти — пълно съдействие за справедливо обезщетение след пътен инцидент.",
    "angliya-uels": "Правни услуги по правото на Англия и Уелс — мост между българската и британската юрисдикция.",
}

services = []
for key, title, handle, icon in SERVICES:
    full = body(key)
    services.append({
        "key": key, "title": title, "url_handle": handle, "icon": icon,
        "blurb": BLURBS.get(key, ""),
        "intro": intro(key, title),
        "full": full,
    })
    print(f"  {title}: blurb {len(services[-1]['blurb'])}, full {len(full)}")

site = {
    "firm": "Адвокатско дружество „ГС Георгиева и партньори“",
    "brand": "Bulgaria Legal",
    "tagline": "Висококачествени правни услуги. Дългосрочно партньорство.",
    "about_short": "Ние сме млади, ние сме амбициозни и наша основна цел е да направим промяна. Вие искате да успеете във вашите лични и бизнес начинания, а за нас вашият успех е нашата репутация.",
    "about_full": body("za-nas"),
    "mission": "Мисията ни е да предоставим висококачествена услуга на клиентите си и да създаваме дългосрочно сътрудничество с всеки един от тях. Ние съчетаваме бизнес проницателност и правен опит при разглеждането на всеки отделен случай, за да го решим преди да прерасне в скъпоструващ правен проблем.",
    "offices": [
        {"city": "Варна", "addr": "ул. „Стефан Стамболов“ 8, ет.1, офис 1, 9000 Варна", "tel": "+359 (0)52 604422", "fax": "+359 (0)52 617226"},
        {"city": "София", "addr": "бул. „Васил Левски“ 46, ет.3, офис 6, 1142 София", "tel": "+359 (0)2 995 0628", "fax": "+359 (0)2 995 0539"},
        {"city": "Великобритания", "addr": "United Kingdom", "tel": "+44 (0)191 640 8899", "fax": "+44 (0)709 288 5817"},
    ],
    "email": "call@bulgaria-legal.com",
    "mobile": "+359 886 46 2040",
    "languages": ["Български", "Русский", "English"],
    "social": {"facebook": "https://www.facebook.com/", "linkedin": "https://www.linkedin.com/"},
    "assets": {
        "logo": f"{SRC}/logo1.png",
        "logo_bg": f"{SRC}/logo-bg.png",
        "fb": f"{SRC}/fb.png", "linkedin": f"{SRC}/linkedin.png",
        "heroes": [
            "https://www.bulgaria-legal.com/files/actual_images/new-banner.jpg",
            "https://www.bulgaria-legal.com/files/actual_images/22171580_m.jpg",
            "https://www.bulgaria-legal.com/files/actual_images/33562939_m.jpg",
        ],
        "contacts_img": f"{SRC}/contacts.jpg",
    },
    "services": services,
}
with open(os.path.join(DATA_DIR, "site.json"), "w", encoding="utf-8") as f:
    json.dump(site, f, ensure_ascii=False, indent=2)
print("\nsaved data/site.json")
