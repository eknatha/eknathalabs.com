import sys, pathlib, threading, http.server, socketserver, functools, re, json, csv, subprocess, tempfile, shutil
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from i18n import en, hi, te, kn, ta, ml

S = pathlib.Path(sys.argv[1]); SITE = S; SHOTS = pathlib.Path(tempfile.gettempdir()) / "el-shots"; SHOTS.mkdir(exist_ok=True)
DICT = {"en": en.T, "hi": hi.T, "te": te.T, "kn": kn.T, "ta": ta.T, "ml": ml.T}
CODES = list(DICT); OTHER = CODES[1:]
NAMES = {"en": "English", "hi": "हिन्दी", "te": "తెలుగు", "kn": "ಕನ್ನಡ", "ta": "தமிழ்", "ml": "മലയാളം"}
SCRIPT = {"hi": r"[ऀ-ॿ]", "te": r"[ఀ-౿]", "kn": r"[ಀ-೿]", "ta": r"[஀-௿]", "ml": r"[ഀ-ൿ]"}
FAILS = []
def check(ok, msg):
    print(("  PASS " if ok else "  FAIL ") + msg)
    if not ok: FAILS.append(msg)
def url(c): return "/" if c == "en" else f"/{c}/"

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k): pass
httpd = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(SITE)))
base = f"http://127.0.0.1:{httpd.server_address[1]}"
threading.Thread(target=httpd.serve_forever, daemon=True).start()
def read(c): return (SITE / ("index.html" if c == "en" else f"{c}/index.html")).read_text(encoding="utf-8")

# ---------- 1. dictionaries ----------
print("1. DICTIONARIES")
EN = DICT["en"]
src = "".join(read(c) for c in CODES)
used = set(re.findall(r'data-i18n="([^"]+)"', src)) | set(re.findall(r"%%T:([\w.\-]+)%%", (S / "_build/template.html").read_text(encoding="utf-8")))
used |= {"meta.title", "meta.desc", "brand.aria", "menu.open", "menu.close", "theme.aria"}
check(used <= set(EN), "every key used in the pages exists in English")
check(set(EN) <= used, f"every English key is used (unused: {sorted(set(EN)-used) or 'none'})")
for c in OTHER:
    T = DICT[c]
    check(set(T) == set(EN), f"{c}: same {len(EN)} keys as English")
    check(all(sorted(re.findall(r"\{\w+\}", EN[k])) == sorted(re.findall(r"\{\w+\}", T[k])) for k in EN), f"{c}: placeholders preserved")
    check(all(v.strip() for k, v in T.items() if k != "brand.marga") and T["brand.marga"].strip(), f"{c}: no empty strings")
    check(re.search(SCRIPT[c], T["brand.lab"]) is not None, f"{c}: brand word 'Prayogashala' is in {c} script ({T['brand.lab']})")
check(EN["brand.lab"] == "Prayogashala" and EN["brand.marga"] == "", "English shows 'Prayogashala' and no native MARGA word")

# ---------- 2. glyph coverage ----------
print("2. GLYPH COVERAGE")
from fontTools.ttLib import TTFont
F = SITE / "assets/fonts"
FONT = {"hi": "devanagari", "te": "telugu", "kn": "kannada", "ta": "tamil", "ml": "malayalam"}
latin = [set(TTFont(F / f).getBestCmap()) for f in ["poppins-latin-400-normal.woff2", "jetbrains-mono-latin-400-normal.woff2"]]
for c in OTHER:
    for w in (400, 700):
        cm = set(TTFont(F / f"noto-sans-{FONT[c]}-{FONT[c]}-{w}-normal.woff2").getBestCmap())
        missing = {ch for v in list(DICT[c].values()) + [NAMES[c]] for ch in v if ord(ch) not in (0x200C, 0x200D, 0x20, 0xA0) and ord(ch) not in cm and not any(ord(ch) in l for l in latin)}
        check(not missing, f"{c} weight {w}: font covers every character" + (f" missing {[hex(ord(x)) for x in missing]}" if missing else ""))

# ---------- 3. pages as files ----------
print("3. PAGES, SEO, CONTENT")
sm = (SITE / "sitemap.xml").read_text(encoding="utf-8")
for c in CODES:
    h = read(c); T = DICT[c]
    check(f'<html lang="{c}"' in h, f"{url(c)}: <html lang={c}>")
    check(f'<link rel="canonical" href="https://eknathalabs.com{url(c)}">' in h, f"{url(c)}: self-referencing canonical")
    hl = re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', h)
    check(sorted(x[0] for x in hl) == sorted(CODES + ["x-default"]) and dict(hl)["x-default"] == "https://eknathalabs.com/", f"{url(c)}: hreflang for all 6 languages + x-default")
    check(f"<title>{T['meta.title']}</title>" in h and T["meta.desc"] in h, f"{url(c)}: translated <title> and description")
    check(f'og:locale" content="{ {"en":"en_US","hi":"hi_IN","te":"te_IN","kn":"kn_IN","ta":"ta_IN","ml":"ml_IN"}[c] }"' in h, f"{url(c)}: og:locale")
    check(f"https://eknathalabs.com{url(c)}</loc>" in sm, f"sitemap lists {url(c)}")
    ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S).group(1))
    org = [g for g in ld["@graph"] if g["@type"] == "Organization"][0]
    items = [i["item"] for g in ld["@graph"] if g["@type"] == "ItemList" for i in g["itemListElement"]]
    check(org["alternateName"] == T["brand.lab"] and [g for g in ld["@graph"] if g["@type"] == "WebSite"][0]["inLanguage"] == c, f"{url(c)}: JSON-LD language and brand word")
    check(len(items) == 10 and all(i["description"] == T[k] for i, k in zip(items, [s for s in re.findall(r'data-i18n="(d\.[^"]+)"', h)])), f"{url(c)}: JSON-LD lists 10 tools with localized descriptions")
    # Telugu script ONLY on the Telugu page; every page only its own script
    for c2, rx in SCRIPT.items():
        found = re.search(rx, re.sub(r'<ul class="lang-list" id="lang-list".*?</ul>|<details class="foot-lang">.*?</details>|<script type="application/ld\+json">.*?</script>', "", h, flags=re.S))
        if c2 == c: check(found, f"{url(c)}: contains {c2} script")
        else: check(not found, f"{url(c)}: no {c2} script leaks in")
    if c != "en":
        eng = [v for k, v in EN.items() if len(v.split()) >= 4 and v in h]
        check(not eng, f"{url(c)}: no untranslated English sentences ({eng[:2]})")
check("ప్రయోగశాల" not in read("en") and "Prayogashala" in read("en"), "English page shows 'Prayogashala', never the Telugu word")
check("ప్రయోగశాల" in read("te"), "Telugu page shows ప్రయోగశాల")
for c in CODES:
    check(DICT[c]["brand.lab"] in re.search(r'class="brandword te"[^>]*>([^<]*)<', read(c)).group(1), f"{url(c)}: hero brand word = {DICT[c]['brand.lab']}")
check(all(not re.search(r"countapi|visit-count|id=.visits|fetch\(", read(c)) for c in CODES), "visit counter and third-party count API removed from every page")
check((SITE / "assets/i18n").exists() is False, "old client-side language JSON removed")

h = read("en")
links = re.findall(r'href="([^"]+)"', h)
check("https://interviewhub.eknathalabs.com" in links and "interview-prep" not in src, "InterviewHub linked; old URL gone")
check(not any(("arch." in l or "docker." in l) for l in links if l.startswith("http")), "ArchLab and Docker Lab have no live links")
check("Docker Lab" in EN["w.docker.t"] and re.search(r'drawer building[^§]*?data-i18n="w.docker.t"', h) is not None, "Docker Lab is a drawer in the Building state")
check(len(re.findall(r'class="drawer building', h)) == 5 and len(re.findall(r'class="drawer planned', h)) == 5, "workshop: 5 building + 5 planned drawers")
check(len(re.findall(r'class="stop"', h)) == 10, "10 live tools")
check(re.search(r'Learn line.*?(MARGA).*?Linux for DevOps.*?Certifications Hub', h, re.S) is not None and 'Docker' not in re.search(r'<article class="line.*?</article>', h, re.S).group(0), "Learn line = MARGA (featured), Linux for DevOps, Certifications Hub")
foot = re.search(r'<footer.*?</footer>', h, re.S).group(0)
check("docker" not in foot.lower().replace("docker lab", "") or "docker.eknathalabs" not in foot, "footer has no Docker Lab link")
ft = re.findall(r'<a href="(https://[^"]+)"', foot)
check(len([x for x in ft if "eknathalabs.com" in x and "blog" not in x]) == 10, "footer lists the 10 live tools")
sm_alts = re.findall(r'hreflang="([^"]+)"', sm)
check(len(sm_alts) == 7 * 6, "sitemap: every URL carries all 7 alternates")
check(all(re.search(r"github|afford|rupee", read(c), re.I) is None for c in CODES), "no GitHub / afford wording on any page")

# ---------- 4. contrast table ----------
print("4. CONTRAST (token pairs)")
def lum(hx):
    hx = hx.lstrip("#"); r, g, b = [int(hx[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def ratio(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True); return (la + 0.05) / (lb + 0.05)
TH = {
 "light": dict(bg="#fff9ee", surface="#fffdf7", text="#1c1b4b", muted="#4a4880", host="#5b5a8f", kick="#b4231a", feat="#fff1c9", native="#2456b8", band="#1c1b4b", onband="#d8d7f5"),
 "dark":  dict(bg="#0c0b26", surface="#17163f", text="#fff9ee", muted="#bdbce6", host="#a8a7dc", kick="#ff9d8f", feat="#26245a", native="#9bbcff", band="#1c1b4b", onband="#d8d7f5"),
 "new":   dict(bg="#eefaf5", surface="#fbfffd", text="#0b2f2d", muted="#3a5f5c", host="#46696a", kick="#0d6759", feat="#fff0c2", native="#1b5aa6", band="#0b3d3a", onband="#cdeee7"),
}
for th, t in TH.items():
    for name, (fg, bg) in {"text/bg": (t["text"], t["bg"]), "muted/surface": (t["muted"], t["surface"]), "muted/bg": (t["muted"], t["bg"]), "host/surface": (t["host"], t["surface"]),
        "kicker/bg": (t["kick"], t["bg"]), "text/feat": (t["text"], t["feat"]), "muted/feat": (t["muted"], t["feat"]), "native/feat": (t["native"], t["feat"]),
        "cream/band": ("#fff9ee", t["band"]), "on-band/band": (t["onband"], t["band"]), "gold/band": ("#ffb400", t["band"]), "on-band/band-2": (t["onband"], "#14133a" if th != "new" else "#072b29"),
        "gold/ink badge": ("#ffb400", "#1c1b4b"), "ink/gold": ("#1c1b4b", "#ffb400")}.items():
        check(ratio(fg, bg) >= 4.5, f"{th:5} {ratio(fg, bg):5.2f}  {name}")
for name, (fg, bg) in {"white/Learn": ("#ffffff", "#2456b8"), "white/Career": ("#ffffff", "#c62833"), "white/Ref": ("#ffffff", "#1a7a48"), "white/Files": ("#ffffff", "#6a3fc0"),
    "drawer gold tag": ("#ffb400", "#2b2d31"), "drawer text": ("#d3d4cd", "#2b2d31"), "planned tag": ("#c3c5cc", "#2b2d31"), "ink/pill": ("#1c1b4b", "#7be0ad")}.items():
    check(ratio(fg, bg) >= 4.5, f"all   {ratio(fg, bg):5.2f}  {name}")

# ---------- 5. browser ----------
OVERFLOW_JS = """() => {
  const bad = [];
  document.querySelectorAll('h1,h2,h3,p,a,span,li,button,b,.stop,.btn,.chip,.pill').forEach(e => {
    const cs = getComputedStyle(e); if (cs.display === 'none' || e.closest('[hidden]') || e.closest('.sr') || e.classList.contains('sr') || e.closest('.skip')) return;
    const r = e.getBoundingClientRect(); if (!r.width) return;
    if (r.right > innerWidth + 1 || r.left < -1) bad.push((e.className||e.tagName)+':'+Math.round(r.left)+'-'+Math.round(r.right)+' '+e.textContent.trim().slice(0,30));
    if (e.scrollWidth > e.clientWidth + 2 && cs.display !== 'inline' && cs.overflow !== 'visible') bad.push('clip:'+e.textContent.trim().slice(0,30));
  });
  return bad.slice(0, 8);
}"""
AUDIT_JS = """() => {
  const parse = s => { const m = s.match(/rgba?\\(([^)]+)\\)/); if (!m) return null; const p = m[1].split(',').map(x => parseFloat(x)); return {r:p[0], g:p[1], b:p[2], a: p.length > 3 ? p[3] : 1}; };
  const blend = (f, b) => ({r: f.r*f.a + b.r*(1-f.a), g: f.g*f.a + b.g*(1-f.a), b: f.b*f.a + b.b*(1-f.a), a: 1});
  const L = c => { const f = v => { v/=255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4) }; return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b) };
  const bgOf = el => { let stack = []; for (let n = el; n; n = n.parentElement) { const c = parse(getComputedStyle(n).backgroundColor); if (c && c.a > 0) { stack.push(c); if (c.a === 1) break; } } let base = {r:255,g:255,b:255,a:1}; stack.reverse().forEach(c => base = blend(c, base)); return base; };
  const out = [], seen = new Set();
  document.querySelectorAll('body *').forEach(el => {
    if (el.closest('.sr') || el.closest('[hidden]') || el.closest('svg') || el.closest('.skip')) return;
    const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const own = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).map(n => n.textContent.trim()).join(' ');
    if (!own) return;
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) return;
    let fg = parse(cs.color); const bg = bgOf(el); fg = blend(fg, bg);
    const a = L(fg), b = L(bg), cr = (Math.max(a,b)+0.05)/(Math.min(a,b)+0.05);
    const px = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight) >= 700, large = px >= 24 || (px >= 18.66 && bold);
    const need = large ? 3 : 4.5;
    if (cr < need) { const k = own.slice(0, 30) + cs.color; if (!seen.has(k)) { seen.add(k); out.push(cr.toFixed(2) + ' ' + cs.color + ' on bg ' + 'rgb('+Math.round(bg.r)+','+Math.round(bg.g)+','+Math.round(bg.b)+') "' + own.slice(0, 28) + '" ' + el.className); } }
  });
  return out;
}"""
errors = []; ext_requests = []
def hook(pg, tag):
    pg.on("console", lambda m: errors.append((tag, m.text)) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errors.append((tag, "pageerror " + str(e))))
    pg.on("request", lambda r: ext_requests.append(r.url) if not r.url.startswith(base) and not r.url.startswith("data:") else None)

def ctx_new(b, w=1440, h=900, **kw):
    kw.setdefault("locale", "en-US"); kw.setdefault("color_scheme", "light")
    return b.new_context(viewport={"width": w, "height": h}, **kw)

def settle(pg):
    pg.wait_for_load_state("load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(350)

def texts(pg):
    return pg.evaluate("[...document.querySelectorAll('[data-i18n]')].map(e => [e.dataset.i18n, e.textContent, e.dataset.n || null])")

with sync_playwright() as p:
    b = p.chromium.launch()

    print("5a. EVERY LANGUAGE PAGE x VIEWPORT (real URLs)")
    for c in CODES:
        T = DICT[c]
        for name, w, hgt in [("desktop", 1440, 900), ("laptop", 1100, 800), ("tablet", 820, 1100), ("mobile", 390, 844), ("small", 320, 700)]:
            ctx = ctx_new(b, w, hgt, locale="en-US"); pg = ctx.new_page(); hook(pg, f"{c}-{name}")
            pg.add_init_script("try{localStorage.setItem('el-lang','%s')}catch(e){}" % c)   # stay on this language
            r = pg.goto(base + url(c)); settle(pg); tag = f"{url(c)}@{name}"
            loaded = pg.evaluate("[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family)")   # read BEFORE any layout queries
            check(r.status == 200 and pg.url.endswith(url(c)), f"{tag}: loads and stays on its own URL")
            wrong = [(k, t[:20]) for k, t, n in texts(pg) if t != T[k].replace("{n}", n or "")]
            check(not wrong, f"{tag}: all {len(texts(pg))} text nodes match the dictionary" + (f" {wrong[:2]}" if wrong else ""))
            ov = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            check(ov <= 0, f"{tag}: no horizontal overflow ({ov}px)")
            bad = pg.evaluate(OVERFLOW_JS); check(not bad, f"{tag}: nothing clipped or off-screen" + (f" {bad}" if bad else ""))
            if w > 1040:
                nav = pg.evaluate("""() => { const n=document.querySelector('.nav-in'); const ls=[...document.querySelectorAll('.nav-links a')];
                  return {h:n.getBoundingClientRect().height, wrap: ls.some(a=>a.getBoundingClientRect().height>46), over: n.scrollWidth>n.clientWidth+1} }""")
                check(nav["h"] <= 70 and not nav["wrap"] and not nav["over"], f"{tag}: header on one line {nav}")
            if name == "desktop" and c != "en":
                fam = FONT[c].capitalize()
                others = sorted({f for f in loaded if "Noto" in f and fam not in f})
                check(any(fam in f for f in loaded) and not others, f"{tag}: loads only the {fam} font (extra: {others or 'none'})")
            if name in ("desktop", "mobile"):
                pg.screenshot(path=str(SHOTS / f"{c}-{name}-top.png"))
                pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))"); pg.wait_for_timeout(500)
                pg.screenshot(path=str(SHOTS / f"{c}-{name}-full.png"), full_page=True)
            if name == "mobile":
                pg.click("#burger"); pg.wait_for_timeout(250)
                check(pg.get_attribute("#burger", "aria-label") == T["menu.close"], f"{tag}: burger label '{pg.get_attribute('#burger','aria-label')}' (open)")
                check(pg.is_visible(".theme-row"), f"{tag}: theme buttons are in the mobile menu")
                pg.screenshot(path=str(SHOTS / f"{c}-mobile-menu.png"))
                pg.keyboard.press("Escape")
                check(pg.get_attribute("#burger", "aria-label") == T["menu.open"], f"{tag}: burger label back after Esc")
            ctx.close()

    print("5b. THEMES (light / dark / new) x LANGUAGES")
    for th in TH:
        for c in CODES:
            ctx = ctx_new(b, 1440, 900); pg = ctx.new_page(); hook(pg, f"{th}-{c}")
            pg.add_init_script("try{localStorage.setItem('el-lang','%s');localStorage.setItem('el-theme','%s')}catch(e){}" % (c, th))
            pg.goto(base + url(c)); settle(pg)
            pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))"); pg.wait_for_timeout(400)
            check(pg.get_attribute("html", "data-theme") == th, f"{th}/{c}: data-theme applied before paint")
            bad = pg.evaluate(AUDIT_JS)
            check(not bad, f"{th}/{c}: every visible text meets WCAG contrast (computed)" + (f" -> {bad[:4]}" if bad else ""))
            if c in ("en", "ml"):
                pg.screenshot(path=str(SHOTS / f"theme-{th}-{c}-full.png"), full_page=True)
            ctx.close()
        ctx = ctx_new(b, 390, 844); pg = ctx.new_page()
        pg.add_init_script("try{localStorage.setItem('el-theme','%s')}catch(e){}" % th)
        pg.goto(base + "/ta/"); settle(pg); pg.screenshot(path=str(SHOTS / f"theme-{th}-ta-mobile.png")); ctx.close()

    print("5c. THEME SWITCHER BEHAVIOUR")
    ctx = ctx_new(b, color_scheme="light"); pg = ctx.new_page(); hook(pg, "theme")
    pg.goto(base + "/"); settle(pg)
    check(pg.get_attribute("html", "data-theme") == "light", "first visit with a light device -> Light")
    bgs = {}
    for th in ("dark", "new", "light"):
        pg.click("#theme-btn"); pg.wait_for_timeout(100)
        check(pg.get_attribute("#theme-btn", "aria-expanded") == "true", f"theme list opens")
        pg.click(f'#theme-list [data-theme-set="{th}"]'); pg.wait_for_timeout(150)
        bgs[th] = pg.evaluate("getComputedStyle(document.body).backgroundColor")
        check(pg.get_attribute("html", "data-theme") == th and pg.evaluate("localStorage.getItem('el-theme')") == th, f"choosing {th} applies and stores it")
        check(pg.get_attribute("meta[name=theme-color]", "content") == {"light": "#1c1b4b", "dark": "#1c1b4b", "new": "#0b3d3a"}[th], f"{th}: browser theme-color meta updated")
        check(pg.evaluate("document.getElementById('theme-list').querySelector('[aria-current=true]').dataset.themeSet") == th, f"{th}: current option marked")
    check(len(set(bgs.values())) == 3, f"three distinct page backgrounds {bgs}")
    pg.click("#theme-btn"); pg.click('#theme-list [data-theme-set="new"]'); pg.reload(); settle(pg)
    check(pg.get_attribute("html", "data-theme") == "new", "theme survives a reload")
    pg.click("#lang-btn"); pg.click('#lang-list a[data-lang="ta"]'); settle(pg)
    check(pg.url.endswith("/ta/") and pg.get_attribute("html", "data-theme") == "new", "theme survives switching language (to /ta/)")
    check(pg.get_attribute("#theme-btn", "aria-expanded") == "false" and pg.inner_text("#theme-list [data-theme-set=dark]").strip() == DICT["ta"]["theme.dark"], "theme labels are translated (Tamil)")
    ctx.close()
    for scheme, want in (("dark", "dark"), ("light", "light")):
        ctx = ctx_new(b, color_scheme=scheme); pg = ctx.new_page(); pg.goto(base + "/"); settle(pg)
        check(pg.get_attribute("html", "data-theme") == want, f"device prefers {scheme} -> {want} by default"); ctx.close()
    ctx = ctx_new(b, color_scheme="dark"); pg = ctx.new_page()
    pg.add_init_script("try{localStorage.setItem('el-theme','light')}catch(e){}"); pg.goto(base + "/"); settle(pg)
    check(pg.get_attribute("html", "data-theme") == "light", "saved choice beats the device preference"); ctx.close()
    ctx = ctx_new(b); pg = ctx.new_page(); hook(pg, "blocked")
    pg.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked')}})")
    pg.goto(base + "/"); settle(pg); pg.click("#theme-btn"); pg.click('#theme-list [data-theme-set="dark"]')
    check(pg.get_attribute("html", "data-theme") == "dark", "theme works with storage blocked")
    pg.click("#lang-btn"); pg.click('#lang-list a[data-lang="kn"]'); settle(pg)
    check(pg.url.endswith("/kn/"), "language links work with storage blocked"); ctx.close()
    ctx = ctx_new(b, 390, 844); pg = ctx.new_page(); pg.goto(base + "/"); settle(pg)
    check(not pg.is_visible("#theme-btn"), "phone: header theme button hidden (no room), menu has it")
    pg.click("#burger"); pg.click('.theme-row [data-theme-set="dark"]'); pg.wait_for_timeout(150)
    check(pg.get_attribute("html", "data-theme") == "dark" and pg.get_attribute('.theme-row [data-theme-set="dark"]', "aria-pressed") == "true", "phone: theme chosen from the menu"); ctx.close()

    print("5d. LANGUAGE ROUTING")
    ctx = ctx_new(b); pg = ctx.new_page(); hook(pg, "route"); pg.goto(base + "/"); settle(pg)
    pg.click("#lang-btn"); check(pg.get_attribute("#lang-btn", "aria-expanded") == "true" and pg.evaluate("document.activeElement.dataset.lang") == "en", "language list opens on the current language")
    pg.click('#lang-list a[data-lang="hi"]'); settle(pg)
    check(pg.url == base + "/hi/" and pg.get_attribute("html", "lang") == "hi" and pg.evaluate("localStorage.getItem('el-lang')") == "hi", "clicking हिन्दी navigates to /hi/ and remembers it")
    pg.goto(base + "/"); settle(pg); check(pg.url == base + "/hi/", "visiting / later redirects to the saved language (/hi/)")
    pg.click("#lang-btn"); pg.click('#lang-list a[data-lang="en"]'); settle(pg)
    check(pg.url == base + "/" and pg.get_attribute("html", "lang") == "en", "choosing English returns to / and sticks (no redirect loop)")
    pg.goto(base + "/#workshop"); settle(pg); check(pg.url == base + "/#workshop", "saved English keeps #workshop")
    pg.click("#lang-btn"); pg.click('#lang-list a[data-lang="te"]'); settle(pg)
    check(pg.url == base + "/te/#workshop", f"switching language keeps the section (#workshop): {pg.url}")
    check(pg.get_attribute("#lang-btn", "aria-expanded") == "false", "list closed after navigation")
    ctx.close()
    for loc, want in [("ta-IN", "ta"), ("hi", "hi"), ("ml-IN", "ml"), ("kn-IN", "kn"), ("te-IN", "te"), ("fr-FR", "en"), ("en-GB", "en")]:
        ctx = ctx_new(b, locale=loc); pg = ctx.new_page(); pg.goto(base + "/"); settle(pg)
        check(pg.get_attribute("html", "lang") == want, f"first visit, browser language {loc} -> {want} ({pg.url.replace(base,'')})"); ctx.close()
    ctx = ctx_new(b, locale="hi-IN"); pg = ctx.new_page(); pg.add_init_script("try{localStorage.setItem('el-lang','en')}catch(e){}"); pg.goto(base + "/"); settle(pg)
    check(pg.get_attribute("html", "lang") == "en", "saved English beats a Hindi browser"); ctx.close()
    ctx = ctx_new(b, locale="hi-IN"); pg = ctx.new_page(); pg.goto(base + "/te/"); settle(pg)
    check(pg.get_attribute("html", "lang") == "te", "an explicit /te/ URL is never redirected (shared links stay in their language)"); ctx.close()
    ctx = ctx_new(b); pg = ctx.new_page(); pg.goto(base + "/hi/"); settle(pg)
    check(pg.get_attribute("a.brand", "href") == "/hi/", "logo links to the language home (/hi/)")
    pg.evaluate("document.querySelector('.foot-lang').open = true")
    check(pg.evaluate("[...document.querySelectorAll('.foot-langs a')].map(a=>a.getAttribute('href')).join()") == "/,/hi/,/te/,/kn/,/ta/,/ml/", "footer has plain links to all 6 languages")
    ctx.close()

    print("5e. KEYBOARD / NO-JS / MOTION / THIRD PARTIES")
    ctx = ctx_new(b); pg = ctx.new_page(); hook(pg, "kbd"); pg.goto(base + "/"); settle(pg)
    pg.focus("#lang-btn"); pg.keyboard.press("Enter"); pg.keyboard.press("ArrowDown"); pg.keyboard.press("ArrowDown")
    check(pg.evaluate("document.activeElement.dataset.lang") == "te", "arrow keys move through languages")
    pg.keyboard.press("Escape"); check(pg.get_attribute("#lang-btn", "aria-expanded") == "false" and pg.evaluate("document.activeElement.id") == "lang-btn", "Esc closes and returns focus")
    pg.focus("#theme-btn"); pg.keyboard.press("Enter"); pg.keyboard.press("ArrowDown"); pg.keyboard.press("Enter"); pg.wait_for_timeout(150)
    check(pg.get_attribute("html", "data-theme") == "dark" and pg.evaluate("document.activeElement.id") == "theme-btn", "keyboard: Enter, arrow, Enter picks Dark and returns focus")
    pg.click("#lang-btn"); pg.click("#theme-btn")
    check(pg.get_attribute("#lang-btn", "aria-expanded") == "false", "opening one popover closes the other")
    pg.mouse.click(600, 700); check(pg.get_attribute("#theme-btn", "aria-expanded") == "false", "click outside closes")
    check(pg.evaluate("[...document.querySelectorAll('.lang-list a')].map(a=>a.lang).join()") == "en,hi,te,kn,ta,ml", "each language name carries its own lang attribute")
    check(pg.evaluate("Math.min(document.querySelector('#lang-btn').getBoundingClientRect().height, document.querySelector('#theme-btn').getBoundingClientRect().height)") >= 44, "both header buttons are at least 44px tall")
    ctx.close()
    ctx = ctx_new(b, reduced_motion="reduce"); pg = ctx.new_page(); pg.goto(base + "/")
    check(pg.evaluate("[...document.querySelectorAll('.reveal')].every(e=>getComputedStyle(e).opacity==='1')"), "reduced motion: all content visible"); ctx.close()
    ctx = ctx_new(b, java_script_enabled=False); pg = ctx.new_page(); pg.goto(base + "/ml/")
    check(pg.evaluate("[...document.querySelectorAll('.reveal')].every(e=>getComputedStyle(e).opacity==='1')"), "no-JS: all content visible")
    check(pg.evaluate("getComputedStyle(document.getElementById('lang')).display") == "none" and not pg.is_visible(".foot-langs"), "no-JS: popovers hidden; footer Language is a closed <details>")
    pg.click(".foot-lang summary"); check(pg.is_visible(".foot-langs"), "no-JS: <details> opens without scripts")
    pg.click('.foot-langs a[hreflang="en"]'); pg.wait_for_load_state(); check(pg.url == base + "/", "no-JS: footer link switches language (real navigation)")
    pg.screenshot(path=str(SHOTS / "nojs.png")); ctx.close()
    ctx = ctx_new(b, 1280, 720); pg = ctx.new_page(); pg.goto(base + "/404.html"); pg.screenshot(path=str(SHOTS / "404.png")); ctx.close()
    b.close()

check(not ext_requests, f"NO third-party requests on any page ({sorted(set(ext_requests))[:3] or 'none'})")

# ---------- 6. review kit round-trip ----------
print("6. REVIEW KIT")
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run([sys.executable, str(S / "_build/review_kit.py"), "export", str(tmp)], check=True, capture_output=True)
rows = list(csv.reader(open(tmp / "review-ta.csv", encoding="utf-8-sig")))
check(len(rows) == len(EN) + 1 and rows[0][0] == "Key" and all(r[2] == DICT["ta"][r[0]] for r in rows[1:]), f"CSV exports all {len(EN)} Tamil strings with English beside them")
check(all(len(list(csv.reader(open(tmp / f"review-{c}.csv", encoding="utf-8-sig")))) == len(EN) + 1 for c in OTHER), "CSVs for all 5 languages")
# import test on a scratch copy of the build dir
scratch = pathlib.Path(tempfile.mkdtemp()); shutil.copytree(S / "_build", scratch / "_build")
rows[1][3] = "TEST-CORRECTION"; w = csv.writer(open(tmp / "fixed.csv", "w", encoding="utf-8-sig", newline="")); w.writerows(rows)
subprocess.run([sys.executable, str(scratch / "_build/review_kit.py"), "import", str(tmp / "fixed.csv"), "ta"], check=True, capture_output=True)
check("TEST-CORRECTION" in (scratch / "_build/i18n/ta.py").read_text(encoding="utf-8") and "TEST-CORRECTION" not in (S / "_build/i18n/ta.py").read_text(encoding="utf-8"), "importing a corrected CSV updates only the copy")
r = subprocess.run([sys.executable, str(scratch / "_build/build.py"), str(scratch / "out")], capture_output=True, text=True)
check(r.returncode == 0 and "TEST-CORRECTION" in (scratch / "out/ta/index.html").read_text(encoding="utf-8"), "correction flows through build.py into /ta/")

print("7. LINKS AND CONSOLE")
for h_ in sorted({x for c in CODES for x in re.findall(r'href="(https?://[^"]+)"', read(c))}): print("     ", h_)
check(all(all(a[1:] in set(re.findall(r'id="([^"]+)"', read(c))) for a in set(re.findall(r'href="(#[^"]+)"', read(c)) ) if len(a) > 1) for c in CODES), "all in-page anchors resolve on every page")
unexpected = [m for _, m in errors]
check(not unexpected, f"no console or page errors ({sorted(set(unexpected))[:3] or 'none'})")
print("\nRESULT:", "ALL PASS" if not FAILS else f"{len(FAILS)} FAILURES")
for f in FAILS: print("  -", f)
httpd.shutdown()
