#!/usr/bin/env python3
"""Static site generator for the mining corporate website.
Run: python3 build.py <output_dir>
Edit SITE below and the page functions to change content. All company-specific facts are placeholders."""
import os, random, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "site"
SITE = {
    "name": "Lundana Mining Company",
    "short": "Lundana",
    "tag": "MINING COMPANY",
    "domain": "https://www.lundanamining.co.ao",  # replace with the real domain before deployment
    "year": "2026",
    "founded": "2009",
}
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
IMGS = {}  # name -> (kind, seed, ratio) registered by photo(); rendered after build
# Where your licensed photos live. Put "min 1.jpg" ... "min 8.jpg" in this folder, or set a full CDN URL ending in "/".
_AUTO = {}
MIN_BASE = "assets/img/"
# photo slot -> which of your min N.jpg files it uses. Edit the numbers to re-order.
MIN_MAP = {
    "hero-open-pit": 1, "header-contact": 1, "header-about": 1,
    "home-intro-operations": 2, "about-who": 2, "header-sustainability": 2,
    "project-1": 3, "home-careers": 3, "news-9": 3,
    "project-3": 4, "ops-processing": 4, "careers-why": 4, "sus-safety": 4, "news-8": 4,
    "ops-open-cast": 5, "header-operations": 5, "news-featured": 5, "news-6": 5,
    "equip-plant": 6, "header-investors": 6, "careers-safety": 6, "news-4": 6,
    "equip-trucks": 7, "header-careers": 7, "careers-graduates": 7,
    "header-news": 8, "news-1": 8,
}

def ed(text):
    return f'<span class="editable">{text}</span>'

# ------------------------------------------------------------------ icons
ICON = {
    "arrow": '<path d="M4 12h15M13 6l6 6-6 6"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.2 8-8 9-4.8-1-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "leaf": '<path d="M5 19c0-9 5-14 15-14 0 10-5 15-14 15"/><path d="M5 19c3-5 6-8 10-10"/>',
    "drop": '<path d="M12 3s6 6.2 6 11a6 6 0 0 1-12 0c0-4.800 6-11 6-11z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.900 4.900l1.400 1.400M17.700 17.700l1.400 1.400M4.900 19.100l1.400-1.400M17.700 6.300l1.400-1.400"/>',
    "co2": '<path d="M7 18a4 4 0 0 1-.5-8 5.500 5.500 0 0 1 10.500 1A3.500 3.500 0 0 1 17 18z"/><path d="M9 14.500h6"/>',
    "tree": '<path d="M12 21v-6"/><path d="M12 15c-4 0-6-2.500-6-5.500C6 6 8.500 3 12 3s6 3 6 6.500c0 3-2 5.500-6 5.500z"/>',
    "users": '<circle cx="9" cy="8" r="3.500"/><path d="M2.500 20c.5-3.500 3-5.500 6.500-5.500S15 16.500 15.500 20"/><path d="M16 4.700a3.500 3.500 0 0 1 0 6.600M18 14.800c2 .7 3.200 2.500 3.500 5.200"/>',
    "hat": '<path d="M3 17h18"/><path d="M5 17a7 7 0 0 1 14 0"/><path d="M12 6v5M9 8.500V11M15 8.500V11"/>',
    "heart": '<path d="M12 20s-8-4.800-8-10.500A4.500 4.500 0 0 1 12 7a4.500 4.500 0 0 1 8 2.500C20 15.200 12 20 12 20z"/><path d="M7 12h3l1.500-2.500 2 4 1.500-1.500H17"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M19.400 15a1.700 1.700 0 0 0 .3 1.900l.1.1a2 2 0 1 1-2.800 2.800l-.1-.1a1.700 1.700 0 0 0-1.900-.3 1.700 1.700 0 0 0-1 1.500V21a2 2 0 1 1-4 0v-.1a1.700 1.700 0 0 0-1.100-1.500 1.700 1.700 0 0 0-1.900.3l-.1.1a2 2 0 1 1-2.800-2.800l.1-.1a1.700 1.700 0 0 0 .3-1.900 1.700 1.700 0 0 0-1.500-1H3a2 2 0 1 1 0-4h.1a1.700 1.700 0 0 0 1.500-1.100 1.700 1.700 0 0 0-.3-1.900l-.1-.1a2 2 0 1 1 2.800-2.800l.1.100a1.700 1.700 0 0 0 1.900.3H9a1.700 1.700 0 0 0 1-1.500V3a2 2 0 1 1 4 0v.1a1.700 1.700 0 0 0 1 1.500 1.700 1.700 0 0 0 1.900-.3l.1-.1a2 2 0 1 1 2.800 2.800l-.1.1a1.700 1.700 0 0 0-.3 1.900V9a1.700 1.700 0 0 0 1.500 1H21a2 2 0 1 1 0 4h-.1a1.700 1.700 0 0 0-1.500 1z"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 12.500l9 5 9-5M3 17l9 5 9-5"/>',
    "truck": '<path d="M2 6h11v10H2zM13 9h4.500l3.500 3.500V16H13z"/><circle cx="6.500" cy="17.500" r="2"/><circle cx="17" cy="17.500" r="2"/>',
    "factory": '<path d="M3 21V10l6 3.500V10l6 3.500V6h4v15z"/><path d="M7 17h2M13 17h2"/>',
    "mountain": '<path d="M2 20l7-12 4 6 3-4 6 10z"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    "file": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    "download": '<path d="M12 4v11M7 11l5 5 5-5M5 20h14"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "phone": '<path d="M5 4h4l2 5-2.500 1.500a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    "pin": '<path d="M12 21s7-6.200 7-11.500A7 7 0 0 0 5 9.500C5 14.800 12 21 12 21z"/><circle cx="12" cy="9.500" r="2.500"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.500v.1"/>',
    "cap": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11.500V16c0 1.500 3 3 6 3s6-1.500 6-3v-4.500"/>',
    "chart": '<path d="M4 20V4M4 20h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>',
    "scale": '<path d="M12 4v16M6 20h12M5 7h14"/><path d="M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "handshake": '<path d="M2 12l5-5 4 2 4-2 5 5-7 7z"/><path d="M8 15l2 2M11 13l3 3"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-5-5"/>',
    "cog2": '<path d="M12 2v3M12 19v3M4.900 4.900L7 7M17 17l2.100 2.100M2 12h3M19 12h3M4.900 19.100L7 17M17 7l2.100-2.100"/><circle cx="12" cy="12" r="4"/>',
    "li": '<path d="M5 9v10M5 5v.1M10 19V9M10 13c0-2.500 2-4 4-4s4 1.500 4 4v6"/>',
    "fb": '<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v6h4v-6h3l1-4h-4V8.500c0-.3.200-.5.500-.5z"/>',
    "x": '<path d="M4 4l16 16M20 4L4 20"/>',
    "yt": '<rect x="2.500" y="6" width="19" height="12" rx="3.500"/><path d="M10.500 9.500v5l4.500-2.500z"/>',
    "ig": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.500 6.500v.1"/>',
}

def ic(name):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[name]}</svg>'

LOGO = ('<svg viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" rx="8" fill="#073B70"/>'
        '<path d="M15 11v25h20" fill="none" stroke="#fff" stroke-width="4.6" stroke-linejoin="round" stroke-linecap="round"/><path d="M26 24l8-8" stroke="#5FA8E0" stroke-width="3" stroke-linecap="round"/>'
        '</svg>')

# ------------------------------------------------------------------ placeholder artwork
_gid = [0]
SKY = ("#2E7FB9", "#A9CDE9")
LAYERS = ["#6FA3CC", "#4C88B8", "#2C6BA3", "#144F86", "#083A6C", "#052B52"]

def _ridge(rng, base, amp, step=100, w=1600, h=900):
    pts, y = [], base
    for x in range(0, w + step, step):
        y = max(base - amp, min(base + amp, y + rng.uniform(-amp * .55, amp * .55)))
        pts.append((x, y))
    d = "M0,%d " % h + " ".join("L%d,%d" % (x, y) for x, y in pts) + " L%d,%d Z" % (w, h)
    return d

def art(kind, seed):
    _gid[0] += 1
    g = f"g{_gid[0]}"
    rng = random.Random(seed)
    s = [f'<svg viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" role="presentation">'
         f'<defs><linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SKY[0]}"/><stop offset="1" stop-color="{SKY[1]}"/></linearGradient></defs>'
         f'<rect width="1600" height="900" fill="url(#{g})"/>']
    if kind == "pit":
        s.append(f'<path d="{_ridge(rng, 430, 40)}" fill="{LAYERS[0]}"/>')
        s.append(f'<path d="{_ridge(rng, 500, 45)}" fill="{LAYERS[1]}"/>')
        cx, cy = 880, 560
        n = 13
        for i in range(n):
            rx = 880 - i * 60
            ry = rx * .30
            c = cy + i * 17
            fill = LAYERS[2] if i % 2 == 0 else LAYERS[3]
            if i == 0:
                fill = "#3A7AAF"
            s.append(f'<ellipse cx="{cx}" cy="{c}" rx="{rx}" ry="{ry:.0f}" fill="{fill}"/>')
            s.append(f'<ellipse cx="{cx}" cy="{c - 3}" rx="{rx}" ry="{ry:.0f}" fill="none" stroke="#9CC8E8" stroke-opacity=".35" stroke-width="2"/>')
        s.append(f'<path d="M1500,560 C1300,640 1100,610 900,700 C760,760 700,720 640,770" fill="none" stroke="#A9CDE9" stroke-opacity=".5" stroke-width="7" stroke-linecap="round"/>')
        s.append(f'<path d="M0,900 L0,820 C300,790 600,850 900,840 C1200,830 1400,800 1600,830 L1600,900Z" fill="{LAYERS[5]}"/>')
    elif kind == "plant":
        s.append(f'<path d="{_ridge(rng, 520, 50)}" fill="{LAYERS[0]}"/>')
        s.append(f'<path d="{_ridge(rng, 600, 40)}" fill="{LAYERS[1]}"/>')
        for x, wd, hh in [(250, 150, 230), (430, 110, 170), (1020, 170, 260), (1230, 120, 190)]:
            s.append(f'<rect x="{x}" y="{700 - hh}" width="{wd}" height="{hh + 200}" fill="{LAYERS[3]}"/>')
            s.append(f'<rect x="{x + 14}" y="{700 - hh + 20}" width="{wd - 28}" height="10" fill="#7FB8E6" fill-opacity=".5"/>')
        for x, hh in [(640, 330), (720, 290), (1450, 300)]:
            s.append(f'<rect x="{x}" y="{700 - hh}" width="34" height="{hh + 200}" fill="{LAYERS[4]}"/>')
        s.append(f'<path d="M300,610 L1000,420" stroke="{LAYERS[4]}" stroke-width="16"/><path d="M300,640 L1000,450" stroke="#7FB8E6" stroke-opacity=".4" stroke-width="4"/>')
        s.append(f'<path d="{_ridge(rng, 760, 30)}" fill="{LAYERS[5]}"/>')
    elif kind == "underground":
        s.append(f'<rect width="1600" height="900" fill="{LAYERS[5]}"/>')
        for i in range(10):
            rx, ry = 760 - i * 70, 600 - i * 52
            s.append(f'<ellipse cx="800" cy="520" rx="{rx}" ry="{ry}" fill="{LAYERS[2] if i % 2 == 0 else LAYERS[4]}" fill-opacity="{.95 - i * .06:.2f}"/>')
        s.append('<ellipse cx="800" cy="520" rx="60" ry="46" fill="#CFE6F7" fill-opacity=".9"/>')
        s.append(f'<path d="M0,900 L560,640 L1040,640 L1600,900Z" fill="{LAYERS[5]}" fill-opacity=".9"/>')
        s.append('<path d="M640,900 L740,640M960,900 L860,640" stroke="#7FB8E6" stroke-opacity=".5" stroke-width="5"/>')
    elif kind == "solar":
        s.append(f'<path d="{_ridge(rng, 470, 35)}" fill="{LAYERS[1]}"/>')
        s.append(f'<rect y="560" width="1600" height="340" fill="{LAYERS[4]}"/>')
        for r in range(6):
            y = 590 + r * 52
            sc = 1 + r * .22
            for c in range(-2, 14):
                x = c * 140 * sc - 120 + r * 10
                s.append(f'<path d="M{x:.0f},{y} l{110 * sc:.0f},0 l{18 * sc:.0f},{34 * sc:.0f} l-{110 * sc:.0f},0z" fill="#1B6DB0" stroke="#9CC8E8" stroke-opacity=".6" stroke-width="2"/>')
    elif kind == "water":
        s.append(f'<path d="{_ridge(rng, 480, 60)}" fill="{LAYERS[1]}"/>')
        s.append(f'<path d="{_ridge(rng, 560, 40)}" fill="{LAYERS[2]}"/>')
        s.append(f'<rect y="640" width="1600" height="260" fill="#2F7DB8"/>')
        for i in range(8):
            y = 665 + i * 28
            s.append(f'<path d="M0,{y} C200,{y - 10} 400,{y + 10} 600,{y} S1000,{y - 10} 1200,{y} S1500,{y + 8} 1600,{y}" stroke="#CFE6F7" stroke-opacity=".5" stroke-width="3" fill="none"/>')
    else:  # hills / green / default
        top = 400 if kind != "green" else 440
        for i, base in enumerate([top, top + 80, top + 170, top + 260, top + 340]):
            col = LAYERS[i + 1] if kind != "green" else ["#7CB0D6", "#5B97C6", "#3F83B8", "#236EA5", "#0F5590"][i]
            s.append(f'<path d="{_ridge(rng, base, 55 - i * 5)}" fill="{col}"/>')
        if kind == "green":
            for _ in range(46):
                x, y = rng.randint(0, 1600), rng.randint(560, 860)
                r = rng.randint(10, 24)
                s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#CFE6F7" fill-opacity="{rng.uniform(.18, .4):.2f}"/>')
    s.append("</svg>")
    return "".join(s)

def photo(name, label, kind="hills", ratio="ratio-3-2", alt="", eager=False, cls=""):
    seed = sum(ord(c) for c in name)
    IMGS[name] = (("portrait" if ratio == "ratio-4-5" else kind), seed, ratio)
    a = alt or label
    e = " data-eager" if eager else ""
    w, h = (800, 1000) if kind == "portrait" or ratio == "ratio-4-5" else (1600, 900)
    load = "eager" if eager else "lazy"
    gen = f"assets/img/{name}.jpg"
    n = MIN_MAP.get(name)
    if not n and kind != "portrait" and ratio != "ratio-4-5":  # every other photo slot cycles through your 8 photos
        if name not in _AUTO: _AUTO[name] = (len(_AUTO) % 8) + 1
        n = _AUTO[name]
    if n:  # your own licensed photo (min 1.jpg ... min 8.jpg); the generated image is the fallback if the file is missing
        src = f"{MIN_BASE}min%20{n}.jpg"
        return (f'<div class="photo {ratio} {cls} has-img"><img src="{src}" data-fallback="{gen}" alt="{a}" width="{w}" height="{h}" loading="{load}" decoding="async"></div>')
    return (f'<div class="photo {ratio} {cls} has-img"><img src="{gen}" alt="{a}" width="{w}" height="{h}" loading="{load}" decoding="async"></div>')

def divider(frm, to):
    return (f'<div class="divider" style="background:{frm}" aria-hidden="true"><svg viewBox="0 0 1600 56" preserveAspectRatio="none">'
            f'<polygon points="0,56 1600,0 1600,56" fill="{to}"/></svg></div>')

# ------------------------------------------------------------------ chrome
NAV = [
    ("Home", "index.html", None),
    ("About Us", "about.html", [("Overview", "about.html"), ("Who we are", "about.html#who"), ("Our history", "about.html#history"),
                                ("Vision and mission", "about.html#vision"), ("Our values", "about.html#values"),
                                ("Leadership", "about.html#leadership"), ("Responsible mining", "about.html#responsible")]),
    ("Operations", "operations.html", [("Overview", "operations.html"), ("Mining operations", "operations.html#mining"), ("Projects", "operations.html#projects"),
                                       ("Mineral resources", "operations.html#resources"), ("Processing facilities", "operations.html#processing"),
                                       ("Equipment and infrastructure", "operations.html#equipment"), ("Operational capabilities", "operations.html#capabilities")]),
    ("Sustainability", "sustainability.html", [("Overview", "sustainability.html"), ("Environment", "sustainability.html#environment"),
                                               ("Water and biodiversity", "sustainability.html#water"), ("Climate and energy", "sustainability.html#climate"),
                                               ("Communities", "sustainability.html#communities"), ("Health and safety", "sustainability.html#safety")]),
    ("Investors", "investors.html", [("Overview", "investors.html"), ("Financial reports", "investors.html#financial"),
                                     ("Annual reports", "investors.html#annual"), ("Corporate governance", "investors.html#governance"),
                                     ("Shareholder information", "investors.html#shareholders"), ("Investor presentations", "investors.html#presentations")]),
    ("News & Media", "news.html", None),
    ("Careers", "careers.html", [("Overview", "careers.html"), ("Why work with us", "careers.html#why"), ("Career opportunities", "careers.html#opportunities"),
                                 ("Graduate programmes", "careers.html#graduates"), ("Skills development", "careers.html#skills"),
                                 ("Workplace safety", "careers.html#safety"), ("Employee development", "careers.html#development")]),
    ("Contact Us", "contact.html", None),
]

def nav_html(current):
    items = []
    for label, href, sub in NAV:
        if sub:
            cur = " current" if href == current else ""
            lis = "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in sub)
            items.append(f'<li class="has-sub" data-open="false"><button type="button" class="{cur.strip()}" aria-expanded="false" aria-haspopup="true">{label}<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON["chev"]}</svg></button><ul class="sub">{lis}</ul></li>')
        else:
            c = ' aria-current="page"' if href == current else ""
            items.append(f'<li><a href="{href}"{c}>{label}</a></li>')
    return (f'<header class="nav"><div class="wrap nav-inner">'
            f'<a class="brand" href="index.html" aria-label="{SITE["name"]} home">{LOGO}<span class="brand-name">{SITE["short"]}<small>{SITE["tag"]}</small></span></a>'
            f'<button class="burger" aria-expanded="false" aria-controls="menu" aria-label="Open menu"><span></span></button>'
            f'<nav aria-label="Primary"><ul class="menu" id="menu">{"".join(items)}'
            f'<li><a class="btn btn-primary nav-cta" href="contact.html">Make an enquiry</a></li></ul></nav></div></header>')

def socials():
    links = [("LinkedIn", "li"), ("Facebook", "fb"), ("X", "x"), ("YouTube", "yt"), ("Instagram", "ig")]
    return '<div class="socials">' + "".join(f'<a href="#" aria-label="{n} (add company link)" title="{n}: add company link">{ic(i)}</a>' for n, i in links) + '</div>'

def footer_html():
    def col(title, items):
        return f'<div><h4>{title}</h4><ul>' + "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in items) + '</ul></div>'
    return (f'<footer class="footer"><div class="wrap"><div class="foot-grid">'
            f'<div><a class="brand" href="index.html">{LOGO}<span class="brand-name">{SITE["short"]}<small>{SITE["tag"]}</small></span></a>'
            f'<p>Angolan diamond producer based in Luanda, operating in Lunda Norte. Founded 2009. Mining responsibly for lasting value.</p>{socials()}</div>'
            + col("Company", [("About us", "about.html"), ("Leadership", "about.html#leadership"), ("Operations", "operations.html"), ("Sustainability", "sustainability.html")])
            + col("Stakeholders", [("Investors", "investors.html"), ("News & media", "news.html"), ("Careers", "careers.html"), ("Contact us", "contact.html")])
            + f'<div><h4>Contact</h4><ul><li>Edifício Lundana, Rua Rainha Ginga<br>Luanda, Angola</li><li>+244 222 555 010</li><li>info@lundanamining.co.ao</li></ul></div>'
            f'</div><div class="foot-base"><span>&copy; {SITE["year"]} {SITE["name"]}. All rights reserved.</span>'
            f'<ul><li><a href="#">Privacy policy</a></li><li><a href="#">Terms of use</a></li><li><a href="#">Accessibility</a></li></ul></div></div></footer>'
            f'<button class="to-top" aria-label="Back to top">{ic("up")}</button>')

def page(fname, title, desc, body, current, extra_head=""):
    full_title = f"{title} | {SITE['name']}" if title != "Home" else f"{SITE['name']} | Responsible mining for lasting value"
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#073B70">
<link rel="canonical" href="{SITE["domain"]}/{fname if fname != "index.html" else ""}">
<meta property="og:type" content="website">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE["domain"]}/assets/img/og-image.jpg">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data: https:; frame-src https://www.google.com https://maps.google.com; connect-src 'self' https:; form-action 'self' https:; base-uri 'self'; object-src 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" href="assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="manifest" href="assets/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700&display=swap">
<link rel="stylesheet" href="assets/style.css">
{extra_head}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{nav_html(current)}
<main id="main">
{body}
</main>
{footer_html()}
<script src="assets/main.js" defer></script>
</body>
</html>
'''
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(html)

def head(title, intro, crumb, pname, kind="pit", seed=None):
    return (f'<section class="page-head">{photo("header-" + pname, title + " header image", kind, ratio="", eager=True)}'
            f'<div class="wrap"><div class="crumbs"><a href="index.html">Home</a><span>/</span>{crumb}</div>'
            f'<h1>{title}</h1><p>{intro}</p></div></section>')

def subnav(items):
    return '<nav class="subnav" aria-label="On this page"><div class="wrap">' + "".join(f'<a href="#{i}">{t}</a>' for i, t in items) + '</nav>'.replace("</nav>", "</div></nav>") if False else \
        '<nav class="subnav" aria-label="On this page"><div class="wrap">' + "".join(f'<a href="#{i}">{t}</a>' for i, t in items) + '</div></nav>'

def sec_head(kicker, h2, p="", center=False):
    c = " center" if center else ""
    return f'<div class="sec-head{c} reveal"><div class="kicker">{kicker}</div><h2>{h2}</h2>{"<p class=lead>" + p + "</p>" if p else ""}</div>'

def cta(h, p, label, href):
    return (f'<section class="cta"><div class="wrap"><div><h2>{h}</h2><p>{p}</p></div>'
            f'<a class="btn btn-light" href="{href}">{label}{ic("arrow")}</a></div></section>')

def notice(text):
    return f'<div class="notice" role="note">{ic("info")}<p>{text}</p></div>'

def checks(items):
    return '<ul class="checks">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def tile(icon, h, p, d=0):
    return f'<div class="reveal" data-d="{d}"><div class="icon-tile"><div class="ic">{ic(icon)}</div><h3>{h}</h3><p>{p}</p></div></div>'

def card(img, kind, tag, title, text, href="#", meta="", cat="", label=None):
    c = f' data-cat="{cat}"' if cat else ""
    m = f'<div class="meta">{meta}</div>' if meta else ""
    return (f'<article class="card reveal"{c}>{photo(img, label or title, kind, "ratio-3-2")}'
            f'<div class="card-body"><span class="tag">{tag}</span>{m}<h3>{title}</h3><p>{text}</p>'
            f'<a class="link-arrow" href="{href}">Learn more{ic("arrow")}</a></div></article>')

def doc(title, meta):
    return (f'<a class="doc reveal" href="#" aria-label="{title}: document to be uploaded"><div class="ic">{ic("file")}</div>'
            f'<div><b>{title}</b><small>{meta}</small></div><span class="dl">{ic("download")}</span></a>')

def stat(num, label, unit=""):
    u = f"<small>{unit}</small>" if unit else ""
    return f'<div class="stat reveal"><div class="num"><span data-count="{num}">{num}</span>{u}</div><div class="lbl">{label}</div></div>'

LEADERS = [("Mariana Kiala", "Chief Executive Officer"), ("Carlos Domingos", "Chief Financial Officer"),
           ("Dra. Teresa Bunga", "Chief Operating Officer"), ("Joaquim Katumbi", "Head of Sustainability and Community")]
def person(i, d=0):
    n, t = LEADERS[i - 1]
    return (f'<div class="person reveal" data-d="{d}">{photo("leader-" + str(i), n + ", " + t, "portrait", "ratio-4-5", alt=n + ", " + t)}'
            f'<h4>{n}</h4><p>{t}</p></div>')

# ---- illustrative company content (replace with approved facts before launch)
PROJECTS = [
    ("project-1", "pit", "Open-cast", "Mukanda Ridge Kimberlite Mine", "Our flagship open-cast operation in Lunda Norte, recovering gem-quality and industrial diamonds from kimberlite since 2012.", "Lunda Norte · Kimberlite diamonds"),
    ("project-2", "water", "Alluvial", "Cacuilo Valley Alluvial Operation", "Alluvial diamond recovery from river gravels in the Cacuilo valley, in production since 2016 under strict water and land controls.", "Lunda Norte · Alluvial diamonds"),
    ("project-3", "plant", "Processing", "Dundo Treatment Plant", "Our central dense-media separation and sorting plant, commissioned in 2019, serving both mining operations.", "Lunda Norte · Treatment and sorting"),
    ("project-4", "solar", "Development", "Sol Nascente Solar Project", "A planned on-site solar plant to supply a growing share of Mukanda Ridge's electricity. Construction began in 2026.", "Lunda Norte · Renewable energy"),
]
def pcard(i, href="operations.html#projects"):
    n, k, t, h, p, m = PROJECTS[i]
    return card(n, k, t, h, p, href, m)
PROJ1, PROJ2, PROJ3 = pcard(0), pcard(1), pcard(2)
_NEWS = [
    ("news-1", "hills", "Company news", "company", "Lundana Mining Company marks 17 years of responsible production", "From a single open-cast pit in 2009 to two operations and a treatment plant in Lunda Norte, we look back on the people and milestones that shaped the company.", "14 October 2026"),
    ("news-2", "green", "Community", "community", "New bursary programme supports 40 learners from Lunda Norte", "The Lundana Bursary Fund will cover university and technical institute fees for engineering, geology and environmental studies.", "2 October 2026"),
    ("news-3", "solar", "Project updates", "project", "Construction begins on the Sol Nascente Solar Project", "Site works have started at Mukanda Ridge on our first on-site solar plant, designed to cut reliance on diesel generation.", "21 September 2026"),
    ("news-4", "plant", "Industry", "industry", "What diamond buyers are watching in the rough market", "Our commercial team outlines the trends in demand, certification and traceability that matter to customers this year.", "9 September 2026"),
    ("news-5", "hills", "Announcements", "announcement", "Dra. Teresa Bunga appointed Chief Operating Officer", "Dra. Bunga joins the executive team to lead operations across both mines and the Dundo plant.", "28 August 2026"),
    ("news-6", "pit", "Press releases", "press", "Mukanda Ridge reaches one million fatality-free shifts", "A milestone for our open-cast team, achieved through critical-control management and a stop-work culture.", "12 August 2026"),
    ("news-7", "water", "Community", "community", "Water-wise schools project completes second phase", "Twelve schools near our operations now have rainwater harvesting and water-saving fittings installed.", "30 July 2026"),
    ("news-8", "plant", "Company news", "company", "Dundo Treatment Plant upgrade improves energy efficiency", "A new screening circuit and variable-speed drives reduce the energy used for every tonne processed.", "17 July 2026"),
    ("news-9", "pit", "Project updates", "project", "Mukanda Ridge begins progressive rehabilitation of the north bench", "Topsoil placement and seeding start on mined-out areas, months ahead of the original closure schedule.", "3 July 2026"),
]
def ncard_i(i):
    img, k, tag, cat, title, text, date = _NEWS[i]
    return card(img, k, tag, title, text, "news.html", date, cat)
NEWS = [ncard_i(i) for i in range(9)]

VACANCIES = [("Mine Planning Engineer", "Mukanda Ridge, Lunda Norte · Full-time · Applications open"),
             ("Alluvial Operations Supervisor", "Cacuilo Valley, Lunda Norte · Full-time · Applications open"),
             ("Process Engineer", "Dundo Treatment Plant, Lunda Norte · Full-time · Applications open"),
             ("SHE Officer", "Mukanda Ridge, Lunda Norte · Full-time · Applications open")]

# ================================================================== PAGES
def build():
    os.makedirs(os.path.join(OUT, "assets", "img"), exist_ok=True)

    # ---------------- HOME
    hero = f'''<section class="hero">{photo("hero-open-pit", "Open-pit mine at first light, wide landscape", "pit", ratio="", alt="Open-pit mining operation with terraced benches", eager=True)}
<div class="wrap hero-inner"><h1><span>Powering Progress.</span><span>Mining Responsibly.</span><span>Building Tomorrow.</span></h1>
<p class="lead">We are committed to responsible resource development, operational excellence and creating lasting value through innovative and sustainable mining solutions.</p>
<div class="actions"><a class="btn btn-primary" href="about.html">Discover Our Company{ic("arrow")}</a><a class="btn btn-ghost" href="operations.html">Explore Our Operations{ic("arrow")}</a></div></div>
<div class="hero-stats"><div class="wrap">
<div class="hero-stat"><b>Safety first</b><span>Every shift, every site</span></div>
<div class="hero-stat"><b>Operational excellence</b><span>Disciplined, data-led mining</span></div>
<div class="hero-stat"><b>Sustainable value</b><span>For land, water and climate</span></div>
<div class="hero-stat"><b>Community partnership</b><span>Shared, lasting benefit</span></div>
</div></div></section>'''

    intro = f'''<section class="sec"><div class="wrap split">
<div class="reveal"><div class="kicker">Who we are</div><h2>A mining company built on discipline, care and long-term thinking.</h2>
<p class="lead">Founded in 2009 and headquartered in Luanda, Lundana Mining Company produces gem-quality and industrial diamonds from the Lunda Norte province, in the north-east of Angola.</p>
<p>We run two mining operations and a treatment plant in Lunda Norte. Our approach joins proven operating practice with new technology, so that every tonne is mined safely, efficiently and with a clear plan for the land afterwards.</p>
<a class="btn btn-outline" href="about.html">About our company{ic("arrow")}</a></div>
<div class="stack-photo reveal" data-d="1">{photo("home-intro-operations", "Haul trucks and excavator working an open-cast bench", "pit", "ratio-4-3")}</div></div></section>'''

    caps = f'''<section class="sec tint"><div class="wrap">{sec_head("What we do", "From orebody to market, run with care", "Four capabilities sit behind everything we deliver.")}
<div class="grid g4">{tile("mountain", "Mining", "Open-cast and alluvial methods planned around safety, recovery and rehabilitation.")}{tile("factory", "Processing", "Dense-media separation, sorting and quality control that turn run-of-mine material into saleable rough diamonds.", 1)}{tile("cog2", "Technology", "Fleet, plant and geological data used to cut waste and make better decisions earlier.", 2)}{tile("leaf", "Stewardship", "Water, energy, land and biodiversity managed as part of the plan, not an afterthought.", 3)}</div></div></section>'''

    stats = f'''<section class="sec navy"><div class="wrap">{sec_head("Our operations at a glance", "Seventeen years of steady growth")}
<div class="stats">{stat("2400", "Employees and contractors", "+")}{stat("3", "Operating sites in Lunda Norte, Angola")}{stat("17", "Years of operation since 2009")}{stat("12", "Lunda Norte communities supported")}</div></div></section>'''

    projects = f'''<section class="sec"><div class="wrap">{sec_head("Operations and projects", "Where we operate", "Producing and developing operations across Lunda Norte province.")}
<div class="grid g3">
{PROJ1}{PROJ2}{PROJ3}
</div><p style="margin-top:36px"><a class="link-arrow" href="operations.html">See all operations{ic("arrow")}</a></p></div></section>'''

    band = f'''<section class="band">{photo("home-rehabilitation", "Rehabilitated mine land with new vegetation", "green", ratio="", alt="Rehabilitated mining landscape")}
<div class="wrap"><div class="kicker" style="color:#8CC2EE">Sustainability</div><h2>Leave the land better than we found it.</h2><p>Rehabilitation is planned before the first blast. Water, energy and biodiversity targets sit alongside production targets in every site plan.</p>
<a class="btn btn-light" href="sustainability.html">Our approach to sustainability{ic("arrow")}</a></div></section>'''

    news = f'''<section class="sec tint"><div class="wrap">{sec_head("News and media", "Latest from the company")}
<div class="grid g3">
{NEWS[0]}{NEWS[1]}{NEWS[2]}
</div><p style="margin-top:36px"><a class="link-arrow" href="news.html">All news and media{ic("arrow")}</a></p></div></section>'''

    careers = f'''<section class="sec"><div class="wrap split flip">
<div class="stack-photo reveal">{photo("home-careers", "Mining team in PPE reviewing plans on site", "underground", "ratio-4-3")}</div>
<div class="reveal" data-d="1"><div class="kicker">Careers</div><h2>Build a career that builds something lasting.</h2>
<p class="lead">We hire for care and curiosity, then invest in training, safety and progression.</p>{checks(["Structured graduate and apprenticeship pathways", "Skills development at every level", "A safety culture where everyone can stop work"])}
<a class="btn btn-primary" href="careers.html#opportunities">Explore Opportunities{ic("arrow")}</a></div></div></section>'''

    body = hero + intro + caps + divider("#F5F7FA", "#073B70") + stats + divider("#073B70", "#FFFFFF") + projects + band + news + careers + cta("Talk to us about your enquiry", "Investors, partners, suppliers and communities: tell us how we can help.", "Contact us", "contact.html")
    page("index.html", "Home", "A responsible mining company: operations, sustainability, investor information, news and careers.", body, "index.html")

    # ---------------- ABOUT
    sn = subnav([("who", "Who we are"), ("history", "Our history"), ("vision", "Vision and mission"), ("values", "Our values"), ("leadership", "Leadership"), ("responsible", "Responsible mining")])
    who = f'''<section class="sec" id="who"><div class="wrap split">
<div class="reveal">{sec_head("Who we are", "A responsible mining company with an eye on the long term")}
<p>Lundana Mining Company is an Angolan diamond producer, founded in 2009 and headquartered in Luanda. We employ around 2,400 people and contractors across two mining operations and a treatment plant in Lunda Norte province.</p>
<p>Our rough diamonds are sold through authorised Angolan channels to buyers who expect certified, traceable supply. We earn that trust by running safe, efficient mines and by treating our people, our neighbours and the land with respect.</p></div>
<div class="reveal" data-d="1">{photo("about-who", "Mining operation overview, wide aerial view", "pit", "ratio-4-3")}</div></div></section>'''
    history = f'''<section class="sec tint" id="history"><div class="wrap split top"><div class="reveal">{sec_head("Our history", "How we got here")}<p>From one open-cast pit to a three-site producer, our growth has been steady and deliberate.</p></div>
<ol class="timeline reveal" data-d="1">
<li><div class="yr">2009</div><p>Lundana Mining Company is founded in Luanda by a team of Angolan mining engineers and geologists, with a prospecting licence in Lunda Norte.</p></li>
<li><div class="yr">2012</div><p>First kimberlite ore is produced at Mukanda Ridge Mine.</p></li>
<li><div class="yr">2016</div><p>The Cacuilo Valley Alluvial Operation begins recovering diamonds from river gravels.</p></li>
<li><div class="yr">2019</div><p>The Dundo Treatment Plant is commissioned, bringing dense-media separation and sorting under one roof.</p></li>
<li><div class="yr">2022</div><p>The Lundana Community Foundation is established to channel funding into education, water and local enterprise.</p></li>
<li><div class="yr">2026</div><p>Construction starts on the Sol Nascente Solar Project, our first on-site renewable energy plant.</p></li></ol></div></section>'''
    vision = f'''<section class="sec" id="vision"><div class="wrap">{sec_head("Vision and mission", "Where we are going, and how", center=True)}
<div class="grid g2"><div class="reveal"><div class="icon-tile" style="padding:44px"><div class="ic">{ic("globe")}</div><h3>Our vision</h3><p class="lead" style="margin:0">To be a trusted mining company whose operations leave people, communities and the environment better off.</p></div></div>
<div class="reveal" data-d="1"><div class="icon-tile" style="padding:44px"><div class="ic">{ic("gear")}</div><h3>Our mission</h3><p class="lead" style="margin:0">To mine safely and efficiently, develop our people, partner with communities and deliver reliable returns.</p></div></div></div>
</div></section>'''
    values = f'''<section class="sec soft" id="values"><div class="wrap">{sec_head("Our values", "The principles behind every decision")}
<div class="grid g3">{tile("shield", "Safety", "Nothing we do is worth someone getting hurt. We stop, fix and restart.")}{tile("scale", "Integrity", "We do what we say, report honestly and hold ourselves to the highest standards.", 1)}{tile("users", "Respect", "We value every person and every community we work with.", 2)}{tile("chart", "Excellence", "We measure results, learn quickly and keep improving how we operate.", 3)}{tile("leaf", "Stewardship", "We protect land, water and biodiversity for those who come after us.", 1)}{tile("handshake", "Partnership", "We build long-term relationships with communities, customers and investors.", 2)}</div>
</div></section>'''
    leadership = f'''<section class="sec" id="leadership"><div class="wrap">{sec_head("Our leadership", "The people who guide the company")}
<div class="grid g4">{person(1)}{person(2, 1)}{person(3, 2)}{person(4, 3)}</div></div></section>'''
    resp = f'''<section class="band" id="responsible">{photo("about-responsible", "Environmental monitoring on a rehabilitated mine site", "green", ratio="", alt="Environmental monitoring at a mine site")}
<div class="wrap"><div class="kicker" style="color:#8CC2EE">Our commitment</div><h2>Responsible mining is how we work, not an add-on.</h2><p>We plan for closure from day one, report openly and involve communities before decisions are made.</p>
<a class="btn btn-light" href="sustainability.html">See how we manage sustainability{ic("arrow")}</a></div></section>'''
    body = head("About Us", "Who we are, where we come from and what we stand for.", "About Us", "about", "pit") + sn + who + history + vision + values + leadership + resp + cta("Work with us", "Explore careers or get in touch with our team.", "Explore Opportunities", "careers.html")
    page("about.html", "About Us", "Learn who we are: our history, vision, mission, values, leadership and commitment to responsible mining.", body, "about.html")

    # ---------------- OPERATIONS
    sn = subnav([("mining", "Mining"), ("projects", "Projects"), ("resources", "Mineral resources"), ("processing", "Processing"), ("equipment", "Equipment"), ("capabilities", "Capabilities")])
    mining = f'''<section class="sec" id="mining"><div class="wrap">{sec_head("Mining operations", "Open-cast and alluvial mining, planned for safety and recovery")}
<div class="split"><div class="reveal">{photo("ops-open-cast", "Open-cast bench with haul trucks and excavators", "pit", "ratio-4-3")}</div>
<div class="reveal" data-d="1"><h3>Open-cast mining</h3><p>Open-cast operations use drilling, blasting, loading and hauling in carefully designed benches. Mine plans balance recovery, stability, water management and the final landform.</p>{checks(["Bench design set by geotechnical data", "Fleet dispatch to cut idle time and fuel use", "Progressive rehabilitation behind the working face"])}</div></div>
<div class="split flip" style="margin-top:72px"><div class="reveal">{photo("ops-alluvial", "Alluvial diamond recovery on a river terrace", "water", "ratio-4-3")}</div>
<div class="reveal" data-d="1"><h3>Alluvial mining</h3><p>Alluvial operations recover diamonds from river gravels using excavators, wet screening and dense-media separation. Water, riverbank and land controls are designed in from the first plan.</p>{checks(["Settling ponds and closed-loop water recycling", "Riverbank buffers and erosion control", "Strict access control and secure handling of recovered stones"])}</div></div></div></section>'''
    projects = f'''<section class="sec tint" id="projects"><div class="wrap">{sec_head("Mining projects", "Our operations and development projects")}
<div class="grid g2">{pcard(0, "#mining")}{pcard(1, "#mining")}{pcard(2, "#processing")}{pcard(3, "sustainability.html#climate")}</div></div></section>'''
    resources = f'''<section class="sec" id="resources"><div class="wrap">{sec_head("Mineral resources", "What we produce")}
<div class="grid g3">{tile("layers", "Kimberlite diamonds", "Gem-quality and industrial rough diamonds recovered at Mukanda Ridge and sorted at the Dundo plant.")}{tile("layers", "Alluvial diamonds", "Rough stones recovered from river gravels in the Cacuilo valley, prized for their quality and character.", 1)}{tile("layers", "Sorted and certified parcels", "Parcels sorted, valued and documented at Dundo, with traceability from mine to sale.", 2)}</div>
<p style="margin-top:24px;color:#5A6D7E">Formal resource and reserve statements are published in our annual reporting, available in the <a href="investors.html#annual">Investors</a> section.</p></div></section>'''
    processing = f'''<section class="sec soft" id="processing"><div class="wrap split">
<div class="reveal">{sec_head("Processing facilities", "From run-of-mine ore to certified rough diamonds")}<p>Our treatment plant crushes, screens and concentrates ore, then sorts recovered stones under strict security. Plant control systems track throughput and quality continuously, so problems are caught early.</p>{checks(["Crushing and screening circuits", "Dense-media separation", "Sorting, valuation and certification", "Secure storage and dispatch"])}</div>
<div class="reveal" data-d="1">{photo("ops-processing", "Mineral processing plant at dusk", "plant", "ratio-4-3")}</div></div></section>'''
    equipment = f'''<section class="sec" id="equipment"><div class="wrap">{sec_head("Equipment and infrastructure", "The machines and systems that keep sites productive")}
<div class="grid g2">
<a class="tile-photo reveal" href="#capabilities">{photo("equip-trucks", "Large haul trucks", "pit", ratio="")}<div><h3>Haul fleet and loading</h3><p>Large trucks, excavators and loaders matched to each pit.</p></div></a>
<a class="tile-photo reveal" href="#capabilities" data-d="1">{photo("equip-plant", "Crushing and conveying infrastructure", "plant", ratio="")}<div><h3>Plant and conveying</h3><p>Crushers, conveyors and stockyards built for uptime.</p></div></a>
<a class="tile-photo reveal" href="#capabilities">{photo("equip-power", "Power and water infrastructure", "solar", ratio="")}<div><h3>Power and water</h3><p>Reliable electricity and water systems, increasingly renewable.</p></div></a>
<a class="tile-photo reveal" href="#capabilities" data-d="1">{photo("equip-logistics", "Rail and road logistics", "hills", ratio="")}<div><h3>Logistics</h3><p>Road, rail and port links that move product to market.</p></div></a></div></div></section>'''
    capab = f'''<section class="sec tint" id="capabilities"><div class="wrap split top"><div class="reveal">{sec_head("Operational capabilities", "What we can deliver")}<p>Capabilities our teams bring to every site.</p></div>
<div class="acc reveal" data-d="1">
<details open><summary>Mine planning and geology</summary><div><p>Geological modelling, mine design and scheduling that balance recovery, cost and safety.</p></div></details>
<details><summary>Drilling, blasting and load-and-haul</summary><div><p>Controlled blasting and an optimised fleet to lift productivity while cutting energy use.</p></div></details>
<details><summary>Processing and quality assurance</summary><div><p>Plant optimisation and laboratory control so product meets customer specifications.</p></div></details>
<details><summary>Maintenance and engineering</summary><div><p>Planned maintenance and engineering support that raises equipment availability.</p></div></details>
<details><summary>Health, safety and environment</summary><div><p>Integrated management systems that make safe, clean operation the default.</p></div></details></div></div></section>'''
    body = head("Our Operations", "Mining, processing and infrastructure run safely and efficiently.", "Operations", "operations", "pit") + sn + mining + projects + resources + processing + equipment + capab + cta("Interested in working with us?", "Suppliers, customers and partners can reach our operations team directly.", "Contact operations", "contact.html")
    page("operations.html", "Our Operations", "Explore our mining operations, projects, mineral resources, processing facilities, equipment and operational capabilities.", body, "operations.html")

    # ---------------- SUSTAINABILITY
    sn = subnav([("environment", "Environment"), ("water", "Water and biodiversity"), ("climate", "Climate and energy"), ("communities", "Communities"), ("safety", "Health and safety")])
    env = f'''<section class="sec" id="environment"><div class="wrap split">
<div class="reveal">{photo("sus-environment", "Rehabilitated mine land with grassland regrowing", "green", "ratio-4-3")}</div>
<div class="reveal" data-d="1">{sec_head("Environmental protection", "Protecting land from first plan to final closure")}<p>We design every site with its closure in mind. That means managing dust, noise and waste carefully, and rehabilitating land progressively instead of waiting until the end.</p>{checks(["Environmental impact assessment before development", "Progressive rehabilitation behind active mining", "Waste, tailings and dust management systems"])}
<h3 style="margin-top:36px">Responsible resource management</h3><p>We aim to recover more of each orebody with less waste, using better planning, sorting and processing, and by reusing materials where we can.</p></div></div></section>'''
    water = f'''<section class="sec tint" id="water"><div class="wrap split flip">
<div class="reveal">{photo("sus-water", "Water monitoring dam on a mine site", "water", "ratio-4-3")}</div>
<div class="reveal" data-d="1">{sec_head("Water conservation", "Using less water, and returning it clean")}<p>Water is shared with communities and ecosystems. We measure, recycle and treat water at every site and report on our performance.</p>{checks(["Closed-loop recycling in processing plants", "Monitoring of surface and ground water", "Treatment before any discharge"])}
<h3 style="margin-top:36px">Biodiversity</h3><p>We map habitats before we disturb land, avoid sensitive areas where possible and rehabilitate with locally appropriate species.</p></div></div></section>'''
    climate = f'''<section class="sec" id="climate"><div class="wrap split">
<div class="reveal">{photo("sus-solar", "Solar array supplying a mining operation", "solar", "ratio-4-3")}</div>
<div class="reveal" data-d="1">{sec_head("Climate and energy", "Cutting carbon and moving to renewable power")}<p>Energy and fuel are our largest sources of emissions. We are working to use less, switch to cleaner sources and measure progress transparently.</p>{checks(["Renewable energy projects at and near our sites", "Fleet and plant efficiency programmes", "Greenhouse gas measurement and reporting"])}
<p>The Sol Nascente Solar Project, now under construction at Mukanda Ridge, is the first step in our roadmap to bring renewable power to all our operations.</p></div></div></section>'''
    comm = f'''<section class="sec soft" id="communities"><div class="wrap">{sec_head("Community development", "Mining should leave communities stronger", "We work with our neighbours to agree priorities, create local opportunity and share benefit.")}
<div class="grid g3">{tile("users", "Local employment", "Training and hiring from host communities wherever we operate.")}{tile("handshake", "Local business", "Procurement that gives local suppliers a fair chance to compete.", 1)}{tile("cap", "Education and skills", "Bursaries, learnerships and skills programmes for young people.", 2)}</div></div></section>
<section class="sec" id="safety"><div class="wrap split flip"><div class="reveal">{photo("sus-safety", "Mining employees in PPE at a safety briefing", "underground", "ratio-4-3")}</div>
<div class="reveal" data-d="1">{sec_head("Health and safety", "Everyone goes home safe, every day")}<p>Safety is our first value. Every employee and contractor has the authority and the duty to stop work they believe is unsafe.</p>{checks(["Critical-control management for the highest-risk activities", "Visible felt leadership from site managers", "Occupational health and wellness programmes", "Open reporting and shared learning from incidents"])}
<a class="btn btn-outline" href="investors.html#annual">Read our reports{ic("arrow")}</a></div></div></section>'''
    body = head("Sustainability", "Responsible resource management, climate action and community benefit.", "Sustainability", "sustainability", "green") + sn + env + water + climate + comm + cta("Read our sustainability reporting", "Find sustainability and annual reports in our investor library.", "Go to reports", "investors.html#annual")
    page("sustainability.html", "Sustainability", "How we protect the environment, conserve water, cut carbon, support biodiversity, develop communities and keep people safe.", body, "sustainability.html")

    # ---------------- INVESTORS
    sn = subnav([("financial", "Financial reports"), ("annual", "Annual reports"), ("governance", "Governance"), ("shareholders", "Shareholders"), ("presentations", "Presentations")])
    ann = f'''<section class="sec" id="announcements"><div class="wrap">{sec_head("Company announcements", "Official announcements")}<div class="grid g2">{doc("Appointment of Chief Operating Officer", "28 August 2026 · PDF")}{doc("Mukanda Ridge safety milestone", "12 August 2026 · PDF")}{doc("Sol Nascente Solar Project: construction start", "21 September 2026 · PDF")}{doc("Notice of annual general meeting", "Published by the company secretary · PDF")}</div></div></section>'''
    fin = f'''<section class="sec tint" id="financial"><div class="wrap">{sec_head("Financial reports", "Results and financial statements")}<div class="grid g3">{doc("Interim results", "Latest half-year · PDF")}{doc("Annual financial statements", "Latest financial year · PDF")}{doc("Quarterly operational update", "Latest quarter · PDF")}</div></div></section>'''
    annual = f'''<section class="sec" id="annual"><div class="wrap">{sec_head("Annual reports", "Integrated and sustainability reporting")}<div class="grid g3">{doc("Integrated annual report", "Latest year · PDF")}{doc("Sustainability report", "Latest year · PDF")}{doc("Mineral resource and reserve statement", "Latest year · PDF")}</div></div></section>'''
    gov = f'''<section class="sec soft" id="governance"><div class="wrap split top"><div class="reveal">{sec_head("Corporate governance", "Accountable leadership", "Strong governance underpins trust. Publish the structures and policies that guide the company.")}</div>
<div class="acc reveal" data-d="1"><details open><summary>Board of directors</summary><div><p>Our board combines executive and independent non-executive directors, led by an independent chairperson. It sets strategy, oversees risk and holds management to account.</p></div></details>
<details><summary>Board committees</summary><div><p>Audit and risk, remuneration and nominations, and social, ethics and sustainability committees each operate under written terms of reference.</p></div></details>
<details><summary>Codes and policies</summary><div><p>Our code of conduct, anti-bribery and corruption policy, human rights policy and supplier code apply to all employees and contractors.</p></div></details>
<details><summary>Ethics and whistleblowing</summary><div><p>Concerns can be raised confidentially through an independent ethics line. Reports are reviewed by the audit and risk committee.</p></div></details></div></div></section>'''
    sh = f'''<section class="sec" id="shareholders"><div class="wrap split top"><div class="reveal">{sec_head("Shareholder information", "Information for shareholders")}<p>Key details for shareholders and prospective investors. Listing and share details are published only once confirmed by the company.</p></div>
<div class="reveal" data-d="1"><div class="icon-tile"><dl style="margin:0;display:grid;gap:14px">
<div><dt style="font-weight:700;color:var(--navy)">Listing and ticker</dt><dd style="margin:0">{ed("To be confirmed by the company")}</dd></div>
<div><dt style="font-weight:700;color:var(--navy)">Financial year-end</dt><dd style="margin:0">{ed("To be confirmed")}</dd></div>
<div><dt style="font-weight:700;color:var(--navy)">Annual general meeting</dt><dd style="margin:0">Notice issued to shareholders ahead of each meeting</dd></div>
<div><dt style="font-weight:700;color:var(--navy)">Share registrar</dt><dd style="margin:0">Contact the company secretary via the details below</dd></div>
<div><dt style="font-weight:700;color:var(--navy)">Investor relations contact</dt><dd style="margin:0">investors@lundanamining.co.ao</dd></div></dl></div></div></div></section>'''
    pres = f'''<section class="sec tint" id="presentations"><div class="wrap">{sec_head("Investor presentations", "Presentations and briefings")}<div class="grid g3">{doc("Corporate presentation", "Company overview · PDF")}{doc("Results presentation", "Latest results · PDF")}{doc("Operations and projects presentation", "Mukanda Ridge, Cacuilo Valley and Dundo · PDF")}</div></div></section>'''
    body = head("Investor Relations", "Reports, governance and shareholder information in one place.", "Investors", "investors", "plant") + sn + fin + annual + gov + sh + pres + cta("Investor enquiries", "Contact our investor relations team.", "Contact investor relations", "contact.html")
    page("investors.html", "Investor Relations", "Financial reports, annual reports, corporate governance, shareholder information and investor presentations.", body, "investors.html")

    # ---------------- NEWS
    cats = [("all", "All"), ("company", "Company news"), ("industry", "Industry"), ("announcement", "Announcements"), ("project", "Project updates"), ("community", "Community"), ("press", "Press releases")]
    chips = "".join(f'<button type="button" class="chip" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{v}</button>' for k, v in cats)
    grid_cards = "".join(NEWS)
    feat = f'''<section class="sec"><div class="wrap"><article class="split reveal"><div>{photo("news-featured", "Featured story image", "pit", "ratio-3-2")}</div>
<div><span class="tag">Featured story</span><div class="meta">14 October 2026</div><h2>Seventeen years of responsible production</h2><p class="lead">From one open-cast pit in 2009 to two operations, a treatment plant and 2,400 people, we look back on what has shaped Lundana Mining Company, and on what comes next.</p><a class="btn btn-primary" href="#">Read the story{ic("arrow")}</a></div></article></div></section>
<section class="sec tint" style="padding-top:64px"><div class="wrap">{sec_head("All updates", "News and media")}<div class="filters" role="group" aria-label="Filter news">{chips}</div><div class="grid g3">{grid_cards}</div></div></section>
<section class="sec"><div class="wrap split"><div class="reveal">{sec_head("Media enquiries", "Speak to our communications team")}<p>Journalists can request interviews, images and background information from our media team.</p><a class="btn btn-outline" href="contact.html">Contact media team{ic("arrow")}</a></div>
<div class="reveal" data-d="1"><div class="contact-card"><ul class="contact-list" style="margin:0"><li>{ic("mail")}<div><b>Media email</b>media@lundanamining.co.ao</div></li><li>{ic("phone")}<div><b>Media telephone</b>+244 222 555 010</div></li></ul></div></div></div></section>'''
    body = head("News & Media", "Company news, industry developments, announcements and press releases.", "News & Media", "news", "hills") + feat
    page("news.html", "News & Media", "Latest company news, mining industry developments, project updates, community initiatives and press releases.", body, "news.html")

    # ---------------- CAREERS
    sn = subnav([("why", "Why work with us"), ("opportunities", "Opportunities"), ("graduates", "Graduates"), ("skills", "Skills"), ("safety", "Safety"), ("development", "Development")])
    why = f'''<section class="sec" id="why"><div class="wrap split"><div class="reveal">{sec_head("Why work with us", "Meaningful work, with people who care how it is done")}<p class="lead">Our people make safe, efficient and responsible mining possible. We invest in them, listen to them and give them room to grow.</p>{checks(["Safety that comes first, always", "Clear development and progression", "Diverse, inclusive teams", "Work that matters to communities"])}<a class="btn btn-primary" href="#opportunities">Explore Opportunities{ic("arrow")}</a></div>
<div class="reveal" data-d="1">{photo("careers-why", "Diverse mining team in PPE on site", "underground", "ratio-4-3")}</div></div></section>'''
    opp = f'''<section class="sec tint" id="opportunities"><div class="wrap">{sec_head("Career opportunities", "Current vacancies")}<div class="grid" style="gap:14px">''' + "".join(
        f'<a class="doc reveal" href="contact.html" aria-label="{t}"><div class="ic">{ic("hat")}</div><div><b>{t}</b><small>{m}</small></div><span class="dl">{ic("arrow")}</span></a>' for t, m in VACANCIES) + '</div></div></section>'
    grad = f'''<section class="band" id="graduates">{photo("careers-graduates", "Graduates learning on site with a mentor", "pit", ratio="", alt="Graduates learning with a mentor")}<div class="wrap"><div class="kicker" style="color:#8CC2EE">Graduate programmes</div><h2>Start your career on site, with a mentor beside you.</h2><p>Our two-year graduate programme places engineers, geologists, process engineers and environmental scientists on rotation across Mukanda Ridge, the Cacuilo Valley and Dundo, with a mentor and a personal development plan from day one.</p><a class="btn btn-light" href="contact.html">Ask about graduate roles{ic("arrow")}</a></div></section>'''
    skills = f'''<section class="sec" id="skills"><div class="wrap">{sec_head("Skills development", "Learn, qualify and move forward")}<div class="grid g3">{tile("cap", "Learnerships and apprenticeships", "Structured pathways into trades and technical careers.")}{tile("cog2", "Technical training", "Hands-on training in equipment, systems and new technology.", 1)}{tile("users", "Leadership development", "Coaching and programmes for supervisors and managers.", 2)}</div></div></section>'''
    safety = f'''<section class="sec soft" id="safety"><div class="wrap split flip"><div class="reveal">{photo("careers-safety", "Safety briefing before a shift", "plant", "ratio-4-3")}</div>
<div class="reveal" data-d="1">{sec_head("Workplace safety", "Your safety is not negotiable")}<p>Every person can stop work they believe is unsafe, without penalty. We train, equip and listen so that everyone goes home safely.</p>{checks(["Induction and role-specific safety training", "Proper PPE and well-maintained equipment", "Wellness and employee assistance support"])}</div></div></section>'''
    dev = f'''<section class="sec" id="development"><div class="wrap">{sec_head("Employee development", "Careers that keep growing")}<div class="grid g3">{tile("chart", "Clear career paths", "Transparent progression with regular performance conversations.")}{tile("handshake", "Mentoring", "Experienced colleagues who share what they know.", 1)}{tile("globe", "Mobility", "Opportunities to move across sites and disciplines.", 2)}</div></div></section>'''
    body = head("Careers", "Join a team that takes safety, craft and community seriously.", "Careers", "careers", "underground") + sn + why + opp + grad + skills + safety + dev + cta("Ready to join us?", "See what is open now or tell us about the role you want.", "Explore Opportunities", "#opportunities")
    page("careers.html", "Careers", "Why work with us, current opportunities, graduate programmes, skills development, workplace safety and employee development.", body, "careers.html")

    # ---------------- CONTACT
    form = f'''<form id="contact-form" class="form" novalidate data-endpoint="">
<div class="form-row"><div class="field"><label for="name">Full name <span class="req" aria-hidden="true">*</span></label><input id="name" name="name" type="text" autocomplete="name" required><div class="err" role="alert"></div></div>
<div class="field"><label for="email">Email address <span class="req" aria-hidden="true">*</span></label><input id="email" name="email" type="email" autocomplete="email" required><div class="err" role="alert"></div></div></div>
<div class="field"><label for="subject">Subject <span class="req" aria-hidden="true">*</span></label><select id="subject" name="subject" required><option value="">Choose a subject</option><option>General enquiry</option><option>Investor relations</option><option>Media enquiry</option><option>Careers</option><option>Suppliers and procurement</option><option>Community and sustainability</option></select><div class="err" role="alert"></div></div>
<div class="field"><label for="message">Message <span class="req" aria-hidden="true">*</span></label><textarea id="message" name="message" required></textarea><div class="err" role="alert"></div></div>
<div class="hp" aria-hidden="true"><label>Leave empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
<div class="field"><label style="font-weight:500;display:flex;gap:10px;align-items:flex-start"><input type="checkbox" name="consent" style="width:auto;margin-top:5px"> <span>I agree to {SITE["name"]} contacting me about this enquiry. <span class="req" aria-hidden="true">*</span></span></label><div class="err" role="alert"></div></div>
<div id="form-status" class="form-status" role="status" aria-live="polite"></div>
<div><button class="btn btn-primary" type="submit">Send enquiry{ic("arrow")}</button></div></form>'''
    info = f'''<div class="contact-card"><h3>Company details</h3><ul class="contact-list">
<li>{ic("pin")}<div><b>Head office</b>Lundana Mining Company<br>Edifício Lundana, Rua Rainha Ginga<br>Luanda<br>Angola</div></li>
<li>{ic("mail")}<div><b>Email</b>info@lundanamining.co.ao</div></li>
<li>{ic("phone")}<div><b>Telephone</b>+244 222 555 010</div></li>
<li>{ic("clock")}<div><b>Office hours</b>Monday to Friday, 08:00 to 17:00 (WAT)</div></li></ul>
<h4>Follow us</h4>{socials()}</div>'''
    mapsvg = '<svg class="ph-map" viewBox="0 0 800 400" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="800" height="400" fill="#E8F2FA"/><g stroke="#B8D3EA" stroke-width="14" fill="none"><path d="M0 120H800M0 280H800M200 0V400M560 0V400"/></g><g stroke="#fff" stroke-width="6" fill="none"><path d="M0 200L800 160M380 0L420 400"/></g></svg>'
    mp = f'''<section class="sec tint"><div class="wrap">{sec_head("Find us", "Our location")}<div class="map reveal">{mapsvg}<iframe title="Map showing the Lundana Mining Company head office in Luanda, Angola" src="https://www.google.com/maps?q=Rua+Rainha+Ginga,+Luanda,+Angola&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div></div></section>'''
    body = head("Contact Us", "Send us an enquiry and the right person will reply within two business days.", "Contact Us", "contact", "hills") + f'<section class="sec"><div class="wrap split top"><div class="reveal">{sec_head("Send an enquiry", "How can we help?")}{form}</div><div class="reveal" data-d="1">{info}</div></div></section>' + mp
    page("contact.html", "Contact Us", "Contact the company: address, email, telephone, enquiry form, map and social media links.", body, "contact.html")

    # ---------------- assets
    with open(os.path.join(OUT, "assets", "favicon.svg"), "w") as f:
        f.write(LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))
    pages = ["index", "about", "operations", "sustainability", "investors", "news", "careers", "contact"]
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE['domain']}/{'' if p == 'index' else p + '.html'}</loc></url>\n" for p in pages) + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE['domain']}/sitemap.xml\n")

def render_assets():
    import imggen
    from PIL import Image, ImageDraw
    imgdir = os.path.join(OUT, "assets", "img")
    for name, (kind, seed, ratio) in IMGS.items():
        size = (800, 1000) if kind == "portrait" else (1600, 900)
        imggen.render(kind, seed, os.path.join(imgdir, name + ".jpg"), size)
    imggen.render("pit", 7, os.path.join(imgdir, "og-image.jpg"), (1200, 630))
    # favicon set drawn from the same monogram as the logo
    def icon(px):
        im = Image.new("RGBA", (px * 4, px * 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im); u = px * 4 / 48
        d.rounded_rectangle((0, 0, px * 4, px * 4), radius=8 * u, fill=(7, 59, 112, 255))
        pts = [(15 * u, 11 * u), (15 * u, 36 * u), (35 * u, 36 * u)]
        d.line(pts, fill=(255, 255, 255, 255), width=int(4.6 * u), joint="curve")
        for p in (pts[0], pts[-1]): d.ellipse((p[0] - 2.3 * u, p[1] - 2.3 * u, p[0] + 2.3 * u, p[1] + 2.3 * u), fill=(255, 255, 255, 255))
        d.line([(26 * u, 24 * u), (34 * u, 16 * u)], fill=(95, 168, 224, 255), width=int(3 * u))
        return im.resize((px, px), Image.LANCZOS)
    a = os.path.join(OUT, "assets")
    icon(32).save(os.path.join(a, "favicon-32.png")); icon(180).save(os.path.join(a, "apple-touch-icon.png"))
    icon(192).save(os.path.join(a, "icon-192.png")); icon(512).save(os.path.join(a, "icon-512.png"))
    icon(64).save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    with open(os.path.join(a, "site.webmanifest"), "w") as f:
        f.write('{"name":"Lundana Mining Company","short_name":"Lundana","icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"}],"theme_color":"#073B70","background_color":"#ffffff","display":"browser"}')

build()
render_assets()
print("built", OUT, len(IMGS), "images")
