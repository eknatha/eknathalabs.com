#!/usr/bin/env python3
"""Generate the EknathaLabs static site: one real page per language (/, /hi/, /te/, /kn/, /ta/, /ml/)
from one template and one set of dictionaries, plus sitemap. Cards, footer and JSON-LD share one data set."""
import html, json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from i18n import en, hi, te, kn, ta, ml

OUT = pathlib.Path(sys.argv[1])
HERE = pathlib.Path(__file__).parent
SITE = "https://eknathalabs.com"
LASTMOD = "2026-10-28"

DICTS = {"en": en.T, "hi": hi.T, "te": te.T, "kn": kn.T, "ta": ta.T, "ml": ml.T}
NATIVE = {"en": "English", "hi": "हिन्दी", "te": "తెలుగు", "kn": "ಕನ್ನಡ", "ta": "தமிழ்", "ml": "മലയാളം"}
OGLOCALE = {"en": "en_US", "hi": "hi_IN", "te": "te_IN", "kn": "kn_IN", "ta": "ta_IN", "ml": "ml_IN"}
CODES = list(DICTS)
EN = DICTS["en"]


def path(code):  # URL path of a language home
    return "/" if code == "en" else f"/{code}/"


# Each stop: (name, subdomain, description key, chip key or None, featured)
LINES = [
    {"name": "Learn", "key": "learn", "color": "#2456b8", "app": "EducationalApplication",
     "stops": [
         ("MARGA", "marga", "d.marga", None, True),
         ("Linux for DevOps", "linux", "d.linux", None, False),
         ("Certifications Hub", "certs", "d.certs", None, False),
     ]},
    {"name": "Career", "key": "career", "color": "#c62833", "app": "BusinessApplication",
     "stops": [
         ("Resumelytics", "resumelytics", "d.resumelytics", None, False),
         ("InterviewHub", "interviewhub", "d.interviewhub", None, False),
     ]},
    {"name": "Reference", "key": "ref", "color": "#1a7a48", "app": "ReferenceApplication",
     "stops": [
         ("Linux Command Explainer", "linux-command-explainer", "d.linux-command-explainer", None, False),
         ("Database Encyclopedia", "db", "d.db", None, False),
         ("Ganaka", "ganaka", "d.ganaka", "chip.offline", False),
     ]},
    {"name": "Files", "key": "files", "color": "#6a3fc0", "app": "UtilitiesApplication",
     "stops": [
         ("Patram", "patram", "d.patram", "chip.offline", False),
         ("Bimba", "bimba", "d.bimba", "chip.offline", False),
     ]},
]

# (slug, state). Building first, then planned. Text lives in i18n under w.<slug>.t / .d
DRAWERS = [
    ("kubernetes", "building"), ("docker", "building"), ("terraform", "building"), ("cicd", "building"),
    ("archlab", "building"),
    ("chaos", "planned"), ("troubleshooting", "planned"), ("cloudops", "planned"),
    ("systemdesign", "planned"), ("security", "planned"),
]

e = html.escape
all_stops = [s for l in LINES for s in l["stops"]]
tools = [(l["app"], s) for l in LINES for s in l["stops"]]
TOOL_COUNT = len(all_stops)

ARROW = ('<svg class="arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>')
_SV = 'width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
ICONS = {
    "light": f'<svg {_SV}><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    "dark": f'<svg {_SV}><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
    "new": f'<svg {_SV}><path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 16l.7 1.8L21.5 18.5l-1.8.7L19 21l-.7-1.8-1.8-.7 1.8-.7z"/></svg>',
}


def i18n(key, n=None):
    return f'data-i18n="{key}"' + (f' data-n="{n}"' if n is not None else "")


def line_html(l):
    stops = []
    for name, sub, dkey, chip, feat in l["stops"]:
        host = f"{sub}.eknathalabs.com"
        chip_html = f'<span class="chip" {i18n(chip)}>x</span>' if chip else ""
        badge = f'<span class="feat-badge"><span {i18n("feat")}>x</span></span>' if feat else ""
        native = f' <span class="native" {i18n("brand.marga")}></span>' if feat else ""
        cls = ' class="feat"' if feat else ""
        stops.append(
            f'''          <li{cls}><a class="stop" href="https://{host}">
            <span class="dot" aria-hidden="true"></span>
            <span>{badge}<span class="stop-name">{e(name)}{native}</span><span class="stop-desc" {i18n(dkey)}>x</span>
            <span class="stop-meta"><span class="host">{host}</span>{chip_html}</span></span>
            {ARROW}
          </a></li>''')
    n, k = len(l["stops"]), l["key"]
    return f'''      <article class="line reveal" style="--lc:{l["color"]}">
        <div class="line-head"><h3 {i18n("ln." + k)}>x</h3><span {i18n("stops.n", n)}>x</span></div>
        <p class="line-blurb" {i18n("bl." + k)}>x</p>
        <ul class="stops">
{chr(10).join(stops)}
        </ul>
      </article>'''


def drawer_html(i, d):
    slug, state = d
    lk = "dr.building" if state == "building" else "dr.planned"
    return f'''      <div class="drawer {state} reveal">
        <div class="handle" aria-hidden="true"><i></i></div>
        <div class="drawer-body">
          <div class="drawer-tag"><span {i18n("dr.tag", f"{i:02d}")}>x</span><span {i18n(lk)}>x</span></div>
          <h3 {i18n(f"w.{slug}.t")}>x</h3>
          <p {i18n(f"w.{slug}.d")}>x</p>
        </div>
      </div>'''


half = (len(all_stops) + 1) // 2
foot = lambda part: "\n".join(
    f'          <li><a href="https://{s[1]}.eknathalabs.com">{e(s[0])}</a></li>' for s in part)

# ---------- per-language page assembly
LEAF = re.compile(r'<(?P<tag>[a-zA-Z0-9]+)(?P<attrs>(?:[^>"]|"[^"]*")*?\sdata-i18n="(?P<key>[^"]+)"(?:[^>"]|"[^"]*")*)>(?P<inner>[^<]*)</(?P=tag)>')


def localize(page, T):
    """Fill every data-i18n leaf element with the dictionary text ({n} from data-n)."""
    def sub(m):
        n = re.search(r'data-n="([^"]*)"', m.group("attrs"))
        text = T[m.group("key")].replace("{n}", n.group(1) if n else "")
        return f'<{m.group("tag")}{m.group("attrs")}>{e(text, quote=False)}</{m.group("tag")}>'
    return LEAF.sub(sub, page)


def jsonld(code, T):
    url = SITE + path(code)
    return {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "@id": f"{SITE}/#website", "url": SITE + "/", "name": "EknathaLabs",
             "description": T["meta.desc"], "inLanguage": code,
             "publisher": {"@id": f"{SITE}/#org"}},
            {"@type": "WebPage", "@id": url + "#page", "url": url, "name": T["meta.title"], "inLanguage": code,
             "isPartOf": {"@id": f"{SITE}/#website"}},
            {"@type": "Organization", "@id": f"{SITE}/#org", "name": "EknathaLabs",
             "alternateName": T["brand.lab"], "url": SITE + "/", "logo": f"{SITE}/icon-512.png",
             "founder": {"@type": "Person", "name": "Eknatha Reddy Puli"},
             "sameAs": ["https://www.linkedin.com/in/eknathareddypuli"]},
            {"@type": "ItemList", "name": "Free EknathaLabs tools", "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "item": {
                    "@type": "SoftwareApplication", "name": s[0], "url": f"https://{s[1]}.eknathalabs.com/",
                    "description": T[s[2]], "applicationCategory": cat, "operatingSystem": "Any (web browser)",
                    "inLanguage": code, "isAccessibleForFree": True,
                    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}}
                for i, (cat, s) in enumerate(tools)]},
        ],
    }


def hreflangs():
    rows = [f'<link rel="alternate" hreflang="{c}" href="{SITE}{path(c)}">' for c in CODES]
    rows.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}/">')
    return "\n".join(rows)


def langlist(code):
    out = []
    for c in CODES:
        cur = ' aria-current="true"' if c == code else ""
        out.append(f'            <li><a href="{path(c)}" hreflang="{c}" lang="{c}" data-lang="{c}"{cur}>{NATIVE[c]}<span class="code">{c.upper()}</span></a></li>')
    return "\n".join(out)


def footlangs(code):
    return "\n".join(
        f'          <a href="{path(c)}" hreflang="{c}" lang="{c}" data-lang="{c}"' + (' aria-current="true"' if c == code else "") + f'>{NATIVE[c]}</a>'
        for c in CODES)


template = (HERE / "template.html").read_text(encoding="utf-8")
lines_html = "\n".join(line_html(l) for l in LINES)
drawers_html = "\n".join(drawer_html(i + 1, d) for i, d in enumerate(DRAWERS))


def build(code):
    T = DICTS[code]
    page = template
    for k, v in {
        "%%LANG%%": code, "%%CANON%%": SITE + path(code), "%%HREFLANG%%": hreflangs(), "%%OGLOCALE%%": OGLOCALE[code],
        "%%HOME%%": path(code), "%%CODE%%": code.upper(), "%%LANGLIST%%": langlist(code), "%%FOOTLANGS%%": footlangs(code),
        "%%LINES%%": lines_html, "%%DRAWERS%%": drawers_html,
        "%%FOOT_TOOLS_A%%": foot(all_stops[:half]), "%%FOOT_TOOLS_B%%": foot(all_stops[half:]),
        "%%TOOL_COUNT%%": str(TOOL_COUNT),
        "%%JSONLD%%": json.dumps(jsonld(code, T), ensure_ascii=False, indent=2),
    }.items():
        page = page.replace(k, v)
    page = re.sub(r"%%ICON:(\w+)%%", lambda m: ICONS[m.group(1)], page)
    page = re.sub(r"%%T:([\w.\-]+)%%", lambda m: e(T[m.group(1)], quote=True), page)
    page = localize(page, T)
    assert "%%" not in page, re.findall(r".{20}%%.{20}", page)[:3]
    return page


sizes = {}
for code in CODES:
    out = OUT / ("index.html" if code == "en" else f"{code}/index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    text = build(code)
    out.write_text(text, encoding="utf-8")
    sizes[code] = len(text.encode())

# sitemap with language alternates
alts = "\n".join(f'    <xhtml:link rel="alternate" hreflang="{c}" href="{SITE}{path(c)}"/>' for c in CODES)
alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>'
urls = "\n".join(f'''  <url>
    <loc>{SITE}{path(c)}</loc>
    <lastmod>{LASTMOD}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{"1.0" if c == "en" else "0.9"}</priority>
{alts}
  </url>''' for c in CODES)
(OUT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + urls + "\n</urlset>\n", encoding="utf-8")

# the old client-side language files are gone
old = OUT / "assets" / "i18n"
if old.exists():
    for f in old.glob("*.json"): f.unlink()
    old.rmdir()
print("tools:", TOOL_COUNT, "drawers:", len(DRAWERS), "pages:", sizes)
