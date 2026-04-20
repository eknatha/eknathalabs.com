# eknathalabs.com

> Hands-on DevOps, Kubernetes & Platform Engineering — built by a practitioner, for practitioners.

![Status](https://img.shields.io/badge/status-under%20construction-yellow)
![License](https://img.shields.io/badge/license-MIT-blue)
![Built With](https://img.shields.io/badge/built%20with-HTML%20%2F%20CSS%20%2F%20JS-38bdf8)
![No Framework](https://img.shields.io/badge/framework-none-lightgrey)

---

## Overview

`eknathalabs.com` is the main homepage of the EknathaLabs platform — a practical DevOps and Platform Engineering learning hub. The site is **under active construction** and serves as the central hub linking all EknathaLabs properties, capturing early access sign-ups, and featuring a **Daily Lab Challenge** that rotates automatically every day with no backend required.

---

## Page Sections

| Section | Description |
|---------|-------------|
| Construction banner | Amber top bar signalling active development with a link to GitHub |
| Sticky nav | Links to live tools, coming-soon subdomains, and Get Early Access CTA |
| Hero | Value proposition with primary and secondary CTAs |
| Email capture | Early access sign-up box (`#early-access`) |
| Terminal block | Animated terminal showing platform build status |
| Live Tools | Cards linking to all active EknathaLabs tools |
| About / Credibility | Experience, certifications, and stats (CKA+CKS, AWS, Azure) |
| Coming Soon | Upcoming tracks — Kubernetes, Terraform, Platform Engineering, Cloud Ops |
| Today's Lab | Daily rotating challenge with answer checking and streak tracking |
| Footer | Live / Coming Soon / Connect columns with all ecosystem links |

---

## Today's Lab — Daily Challenge

A fully client-side interactive challenge that rotates every day using a date-seeded index. No backend, no API, no sign-up required.

### How it works

- **30 challenges** across 4 tracks: Linux, Kubernetes, Terraform, Platform Engineering
- **Date-seeded rotation** — epoch from `2025-01-01`, modulo challenge count; same challenge for all visitors on the same day
- **Answer validation** — normalises input (trims whitespace, lowercases) and checks against a primary answer plus an `alt[]` array of accepted variants
- **Streak tracking** — persisted in `localStorage` under keys `el_streak` and `el_last_date`; increments once per day on a correct answer for today's challenge
- **Hint toggle** — reveals a contextual hint without showing the answer
- **Reveal Answer** — fallback that shows the canonical answer
- **Prev / Next navigation** — browse the full 30-challenge bank
- **Progress bar** — shows position in the bank as a percentage

### Challenge bank

| # | Track | Title | Difficulty |
|---|-------|-------|------------|
| 1 | Linux | Find large files eating disk space | Easy |
| 2 | Linux | Kill all processes by name | Easy |
| 3 | Linux | Check which process is using port 8080 | Easy |
| 4 | Linux | Count lines in all log files | Easy |
| 5 | Linux | Show real-time disk I/O per process | Medium |
| 6 | Linux | Extract lines between two patterns | Medium |
| 7 | Linux | Schedule a job to run every 5 minutes | Easy |
| 8 | Linux | Find files modified in last 24 hours | Easy |
| 9 | Linux | Archive and compress a directory | Easy |
| 10 | Linux | Monitor a log file in real time | Easy |
| 11 | Kubernetes | Get all pods across every namespace | Easy |
| 12 | Kubernetes | Describe a crashlooping pod | Easy |
| 13 | Kubernetes | Get logs from a previous container crash | Medium |
| 14 | Kubernetes | Scale a deployment to 5 replicas | Easy |
| 15 | Kubernetes | Exec into a running container | Easy |
| 16 | Kubernetes | Cordon a node before maintenance | Medium |
| 17 | Kubernetes | Force delete a stuck terminating pod | Medium |
| 18 | Kubernetes | View resource usage across all nodes | Easy |
| 19 | Terraform | Initialise a new working directory | Easy |
| 20 | Terraform | Preview changes before applying | Easy |
| 21 | Terraform | Target a single resource for apply | Medium |
| 22 | Terraform | Import an existing resource into state | Medium |
| 23 | Terraform | List all resources in state | Easy |
| 24 | Platform Eng | Check GitHub Actions workflow run history | Easy |
| 25 | Platform Eng | Check ArgoCD application sync status | Easy |
| 26 | Linux | Find top 10 memory-consuming processes | Easy |
| 27 | Linux | Check open file handles for a process | Medium |
| 28 | Kubernetes | Create a temporary debug pod | Medium |
| 29 | Terraform | Destroy a single resource | Medium |
| 30 | Platform Eng | View recent Helm release history | Easy |

### Adding more challenges

Extend the `LABS` array in the `<script>` block near the bottom of `index.html`:

```js
{
  track: 'Linux',           // Linux | Kubernetes | Terraform | Platform Eng
  title: 'Your challenge title',
  diff: 'Easy',             // Easy | Medium | Hard
  scenario: 'The real-world situation the user is solving.',
  hint: 'A nudge toward the right approach without giving the answer.',
  answer: 'the-canonical-command',
  alt: ['alternative-valid-command', 'another-valid-form']
}
```

---

## Live Tools (linked from homepage)

| Tool | URL | Status |
|------|-----|--------|
| GitHub Profile Analyzer | [eknatha.github.io/github-profile-analyzer](https://eknatha.github.io/github-profile-analyzer/) | Live |
| Linux Command Explainer | [eknatha.github.io/linux-command-explainer](https://eknatha.github.io/linux-command-explainer) | Live |
| Interview Prep Portal | [eknatha.github.io/interview-prep](https://eknatha.github.io/interview-prep) | Live |
| Interactive Labs | [labs.eknathalabs.com](https://labs.eknathalabs.com) | Building |
| Terraform Challenges | [terraform.eknathalabs.com](https://terraform.eknathalabs.com) | Building |
| Learn Platform | [learn.eknathalabs.com](https://learn.eknathalabs.com) | Building |
| Blog | [blog.eknathalabs.com](https://blog.eknathalabs.com) | Building |

---

## Tech Stack

- **Pure HTML / CSS / JavaScript** — no frameworks, no build step, no dependencies
- **Fonts** via Google Fonts:
  - [Fraunces](https://fonts.google.com/specimen/Fraunces) — headings
  - [DM Sans](https://fonts.google.com/specimen/DM+Sans) — body text
  - [JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono) — terminal, code, labels
- **localStorage** — streak and last-solved date (keys: `el_streak`, `el_last_date`)
- **SVG favicon** — inline data URI, no external file needed
- **SEO** — meta description, keywords, Open Graph, Twitter Card, canonical URL

---

## Project Structure

```
eknathalabs.com/
├── index.html        # Entire site — single file, self-contained
├── README.md         # This file
└── og-image.png      # Recommended — Open Graph preview image (1200×630px)
```

---

## Author

**EknathaLabs**
- Site: [eknathalabs.com](https://eknathalabs.com)
- GitHub: [@eknatha](https://github.com/eknatha)

---

## License

MIT — free to use, fork, and learn from.
