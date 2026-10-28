# EknathaLabs

**Technology, open to everyone.**

Free tools, labs and learning across every kind of technology. No account, no paywall.
Our goal is simple: make great technology free and accessible to everyone.

Live at **https://eknathalabs.com**

## What is on the site

| Line | Tools |
| --- | --- |
| Learn | **MARGA** (featured, structured learning paths), Linux for DevOps, Docker Lab, Certifications Hub |
| Career | Resumelytics, InterviewHub (interviewhub.eknathalabs.com) |
| Reference | Linux Command Explainer, Database Encyclopedia |
| Files | Patram (PDF toolkit), Bimba (image toolkit), both fully offline |

ArchLab, Kubernetes Lab, Terraform Lab and CI/CD Lab are in the workshop (building).

## Languages

English, Hindi, Telugu, Kannada, Tamil and Malayalam. English is the page markup (so search
engines and no-JS visitors always get it). The other five are JSON files in `assets/i18n/`,
loaded only when chosen. The choice is remembered, `?lang=ta` shares a language, and the
browser language is used on a first visit. To change wording, edit the JSON and keep the
keys and `{n}` / `{name}` placeholders. Translations should be reviewed by native speakers.

## This repository

A static site with no build step needed to deploy.

```
index.html          home page (HTML, CSS and a small script in one file)
404.html            not-found page
assets/fonts/       self-hosted fonts (Poppins, JetBrains Mono, Noto Sans for each Indic script)
assets/i18n/        hi.json te.json kn.json ta.json ml.json
favicon.svg, icon-*.png, apple-touch-icon.png, site.webmanifest
og-image.png        social sharing image (1200x630)
robots.txt, sitemap.xml
CNAME, LICENSE
```

Fonts are served from this site, so visiting it makes no third-party font requests.

## Updating the tool list

Each tool appears in three places on the home page: its card, the footer list and the
structured data (JSON-LD) in the page head, plus its description in every language file.
When a tool is added or renamed, update all of them. When a workshop drawer goes live, change its `<div class="drawer ...">` into a link
and move it into the right line.

## Licence

MIT. See `LICENSE`.
