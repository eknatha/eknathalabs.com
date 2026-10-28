# EknathaLabs

**Technology, open to everyone.**

Free tools, labs and learning across every kind of technology. No account, no paywall.
Our goal is simple: make great technology free and accessible to everyone.

Live at **https://eknathalabs.com**

## What is on the site

| Line | Tools |
| --- | --- |
| Learn | **MARGA** (featured, structured learning paths), Linux for DevOps, Certifications Hub, Bhasha (spoken-language learning in 10 languages, with English to speech; offline) |
| Career | Resumelytics, InterviewHub (interviewhub.eknathalabs.com) |
| Reference | Linux Command Explainer, Database Encyclopedia |
| Tools | Ganaka (119 offline calculators), Patram (PDF toolkit), Bimba (image toolkit) |

In the workshop (building): Kubernetes Lab, Docker Lab, Terraform Lab, CI/CD Lab, ArchLab.
Planned: Chaos Lab, Troubleshooting Labs, Cloud Operations Track, System Design Playground, Security Track.

## Languages: real URLs

| Language | URL |
| --- | --- |
| English | `/` |
| Hindi | `/hi/` |
| Telugu | `/te/` |
| Kannada | `/kn/` |
| Tamil | `/ta/` |
| Malayalam | `/ml/` |

Each is a complete static page with its own title, description, canonical URL, `hreflang`
alternates, Open Graph locale and structured data, and all are in `sitemap.xml`.
Only `/` ever redirects, and only on a first visit (or a saved choice) to the visitor's own
language; a direct link to `/te/` always stays Telugu. Choosing a language saves it in the
browser. The brand word "Prayogashala" is English on `/` and written in each language's own
script on the other pages.

## Themes

Light, Dark and New (a teal look). The first visit follows the device (light or dark); a
choice is saved in the browser and applies on every page and language.

## Repository layout

```
index.html, hi/ te/ kn/ ta/ ml/      one page per language (generated)
404.html                             not-found page
assets/fonts/                        self-hosted fonts (Poppins, JetBrains Mono, Noto Sans per Indic script)
favicon.svg, icon-*.png, apple-touch-icon.png, site.webmanifest
og-image.png                         social sharing image (1200x630)
robots.txt, sitemap.xml
CNAME, LICENSE
```

No third-party requests: fonts are served from this site and there is no visit counter or
analytics script.

## Regenerating the pages

The pages are generated from one template and one dictionary per language (source in
`_build/`):

```
python3 _build/build.py .            # writes index.html, hi/ te/ kn/ ta/ ml/ and sitemap.xml
python3 _build/verify.py .           # runs every check (needs Playwright, fontTools, brotli)
```

To change wording edit `_build/i18n/<lang>.py`. When a tool is added or renamed, edit
`LINES` or `DRAWERS` in `_build/build.py` and add its description to every dictionary; the
card, footer and structured data update together.

## Translation review

`python3 _build/review_kit.py export review` writes one spreadsheet-friendly CSV per
language. Reviewers fill only the "Corrected" column.
`python3 _build/review_kit.py import review-ta.csv ta` applies it.

## Licence

MIT. See `LICENSE`.
