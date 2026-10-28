# Build source (not published by GitHub Pages: folders starting with `_` are skipped)

Run from the repository root:

    python3 _build/build.py .        # regenerates index.html, hi/ te/ kn/ ta/ ml/, sitemap.xml
    python3 _build/verify.py .       # runs every check (pip install playwright fonttools brotli; playwright install chromium)
    python3 _build/render.py .       # re-renders og-image.png and icons

Wording: `_build/i18n/<lang>.py`. Tools and drawers: `LINES` / `DRAWERS` in `_build/build.py`.
Native-speaker review: `_build/review/*.csv`, then
`python3 _build/review_kit.py import <file.csv> <lang>`.
