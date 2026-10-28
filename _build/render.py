import sys, pathlib
from playwright.sync_api import sync_playwright

S = pathlib.Path(sys.argv[1])
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.goto((S / "_build/og.html").as_uri())
    pg.wait_for_timeout(600)
    pg.screenshot(path=str(S / "og-image.png"))
    svg = (S / "favicon.svg").read_text()
    for name, size in [("icon-192.png", 192), ("icon-512.png", 512), ("apple-touch-icon.png", 180)]:
        q = b.new_page(viewport={"width": size, "height": size})
        q.set_content(f'<body style="margin:0;background:transparent">{svg.replace("<svg ", f"<svg width={chr(34)}{size}{chr(34)} height={chr(34)}{size}{chr(34)} ", 1)}</body>')
        q.screenshot(path=str(S / name), omit_background=True)
    b.close()
print("ok")
