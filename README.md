<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 220" width="860" height="220">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0a0c0f"/>
      <stop offset="100%" style="stop-color:#0f1520"/>
    </linearGradient>
    <linearGradient id="wordGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"   style="stop-color:#00ff88"/>
      <stop offset="40%"  style="stop-color:#00e5ff"/>
      <stop offset="100%" style="stop-color:#a855f7"/>
    </linearGradient>
    <linearGradient id="labsGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   style="stop-color:#ff6b35"/>
      <stop offset="100%" style="stop-color:#ff3b8a"/>
    </linearGradient>
    <filter id="glow" x="-10%" y="-30%" width="120%" height="160%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glowLabs" x="-10%" y="-30%" width="120%" height="160%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M 30 0 L 0 0 0 30" fill="none" stroke="rgba(0,255,136,0.04)" stroke-width="0.8"/>
    </pattern>
    <pattern id="scanlines" width="1" height="4" patternUnits="userSpaceOnUse">
      <rect width="1" height="1" fill="rgba(0,0,0,0.15)"/>
    </pattern>
    <radialGradient id="cornerGlow" cx="0%" cy="0%" r="60%">
      <stop offset="0%" style="stop-color:#00ff88;stop-opacity:0.12"/>
      <stop offset="100%" style="stop-color:#00ff88;stop-opacity:0"/>
    </radialGradient>
    <radialGradient id="cornerGlow2" cx="100%" cy="100%" r="60%">
      <stop offset="0%" style="stop-color:#a855f7;stop-opacity:0.1"/>
      <stop offset="100%" style="stop-color:#a855f7;stop-opacity:0"/>
    </radialGradient>
    <clipPath id="roundClip">
      <rect width="860" height="220" rx="14"/>
    </clipPath>
  </defs>
  <rect width="860" height="220" rx="14" fill="url(#bgGrad)"/>
  <rect width="860" height="220" rx="14" fill="url(#grid)" clip-path="url(#roundClip)"/>
  <rect width="860" height="220" rx="14" fill="url(#cornerGlow)" clip-path="url(#roundClip)"/>
  <rect width="860" height="220" rx="14" fill="url(#cornerGlow2)" clip-path="url(#roundClip)"/>
  <rect width="860" height="220" rx="14" fill="none" stroke="rgba(0,255,136,0.18)" stroke-width="1.2"/>
  <rect x="6" y="6" width="848" height="208" rx="10" fill="none" stroke="rgba(0,255,136,0.06)" stroke-width="1"/>
  <rect x="14" y="0" width="220" height="2" rx="1" fill="url(#wordGrad)" opacity="0.9"/>
  <rect x="626" y="218" width="220" height="2" rx="1" fill="url(#labsGrad)" opacity="0.9"/>
  <rect x="36" y="60" width="64" height="64" rx="8" fill="rgba(0,255,136,0.08)" stroke="rgba(0,255,136,0.3)" stroke-width="1.2"/>
  <text x="68" y="103" font-family="'Courier New', monospace" font-size="30" font-weight="700" text-anchor="middle" fill="url(#wordGrad)" filter="url(#glow)">EL</text>
  <line x1="118" y1="65" x2="118" y2="119" stroke="rgba(0,255,136,0.2)" stroke-width="1"/>
  <text x="138" y="108" font-family="'Courier New', monospace" font-size="62" font-weight="700" letter-spacing="6" fill="url(#wordGrad)" filter="url(#glow)">EKNATHA</text>
  <text x="651" y="108" font-family="'Courier New', monospace" font-size="62" font-weight="700" letter-spacing="6" fill="url(#labsGrad)" filter="url(#glowLabs)">LABS</text>
  <text x="138" y="148" font-family="'Courier New', monospace" font-size="11.5" letter-spacing="3.5" fill="rgba(107,122,141,0.9)">DEVOPS  ·  KUBERNETES  ·  PLATFORM  ENGINEERING</text>
  <text x="760" y="186" font-family="'Courier New', monospace" font-size="10" letter-spacing="1" fill="rgba(0,255,136,0.35)">$ ./init-platform.sh</text>
  <rect x="776" y="22" width="62" height="18" rx="4" fill="rgba(0,255,136,0.08)" stroke="rgba(0,255,136,0.25)" stroke-width="0.8"/>
  <text x="807" y="34.5" font-family="'Courier New', monospace" font-size="9" letter-spacing="1" fill="rgba(0,255,136,0.7)" text-anchor="middle">v2  BETA</text>
  <circle cx="36" cy="36" r="2.5" fill="rgba(0,255,136,0.5)"/>
  <circle cx="48" cy="36" r="2.5" fill="rgba(0,212,255,0.4)"/>
  <circle cx="60" cy="36" r="2.5" fill="rgba(168,85,247,0.4)"/>
  <text x="36" y="190" font-family="'Courier New', monospace" font-size="9.5" letter-spacing="2" fill="rgba(107,122,141,0.6)">BUILT IN PUBLIC  ·  eknathalabs.com</text>
  <rect width="860" height="220" rx="14" fill="url(#scanlines)" opacity="0.4" clip-path="url(#roundClip)"/>
</svg>

<br/><br/>

[![Website](https://img.shields.io/badge/🌐_Website-eknathalabs.com-00ff88?style=for-the-badge&labelColor=0a0c0f)](https://eknathalabs.com)
[![GitHub](https://img.shields.io/badge/GitHub-eknatha-181717?style=for-the-badge&logo=github&logoColor=white&labelColor=0a0c0f)](https://github.com/eknatha)
[![Status](https://img.shields.io/badge/Status-Building_in_Public_🚧-febc2e?style=for-the-badge&labelColor=0a0c0f)](https://eknathalabs.com)
[![License](https://img.shields.io/badge/License-MIT-a855f7?style=for-the-badge&labelColor=0a0c0f)](LICENSE)

<br/>

*Real terminal labs. Production-grade scenarios. Hands-on playgrounds for Linux, Kubernetes, Terraform, CI/CD, and Cloud.*
*Built by a practitioner with 13+ years in the field — not a content farm.*

</div>

<br/>

---

## 📖 Table of Contents

- [What is EknathaLabs?](#-what-is-eknathalabs)
- [Live Tools](#-live-tools)
- [Labs in Progress](#️-labs-in-progress)
- [What's Coming](#️-whats-coming)
- [About the Builder](#-about-the-builder)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🧪 What is EknathaLabs?

EknathaLabs is a hands-on learning platform for **DevOps and Platform Engineering** — built from real production experience, not copied from documentation.

```bash
eknatha@labs:~$ ./what-is-this.sh

  ► Real terminal labs mapped to production scenarios
  ► Interactive tools you can use today — free, no sign-up
  ► Structured tracks for Linux, K8s, Terraform, CI/CD, Cloud
  ► Built in public at github.com/eknatha

STATUS: Core content always free ✓
```

Every guide, lab, and scenario comes from actual time spent in the trenches — cloud operations, incident response, Kubernetes at scale, and multi-cloud migrations across AWS, Azure, and OpenStack.

---

## ⚡ Live Tools

> Use these right now — **no account, no paywall.**

| | Tool | What it does | Link |
|--|------|-------------|------|
| 📊 | **GitHub Profile Analyzer** | 0–100 score across 5 dimensions · radar chart · hirability score · shareable PNG scorecard | [→ Open](https://eknatha.github.io/github-profile-analyzer/) |
| 🎯 | **ATS Resume Analyzer** | Beat applicant tracking systems · keyword gap analysis · format scoring · targeted fixes | [→ Open](https://eknatha.github.io/resumelytics/) |
| 🐧 | **Linux Command Explainer** | Plain-English breakdowns · pipe chain visualiser · regex decoder · ELI5 mode · danger checklist | [→ Open](https://eknatha.github.io/linux-command-explainer/) |
| 📚 | **DevOps Interview Prep** | 12+ guides · interview mode · flashcard mode · K8s, Terraform, Linux, CI/CD, Cloud | [→ Open](https://eknatha.github.io/interview-prep/) |

---

## 🏗️ Labs in Progress

> Terminal-based, production-grade labs — real scenarios, not toy examples.

| | Lab | Stack | Status | URL |
|--|-----|-------|--------|-----|
| ☸️ | **Kubernetes Lab** | CKA · CKS · RBAC · Network Policies · ArgoCD | 🔨 Building | [kubelab.eknathalabs.com](https://kubelab.eknathalabs.com/) |
| 🏗️ | **Terraform Lab** | AWS · Azure · GCP · Modules · State · CI/CD | 🔨 Building | [terraform.eknathalabs.com](https://terraform.eknathalabs.com/) |
| 🐳 | **Docker Lab** | Compose · Networking · Volumes · Multi-stage · Security | 🔨 Building | [docker.eknathalabs.com](https://docker.eknathalabs.com/) |
| ⚙️ | **CI/CD Lab** | GitHub Actions · ArgoCD · GitOps · Deploy Pipelines | 🔨 Building | [cicd.eknathalabs.com](https://cicd.eknathalabs.com/) |

---

## 🛣️ What's Coming

```
┌──────────────────────────────────────────────────────────────────────┐
│  EKNATHALABS ROADMAP                                                 │
├────────────────────────────────────┬───────────┬────────────────────┤
│  Track                             │  Status   │  Description       │
├────────────────────────────────────┼───────────┼────────────────────┤
│  ☸️  Kubernetes Track               │ BUILDING  │ CKA + CKS mapped   │
│  🏗️  Terraform & IaC                │ BUILDING  │ Multi-cloud IaC    │
│  ⚙️  Platform Engineering           │ PLANNED   │ IDPs, golden paths │
│  ☁️  Cloud Operations (AWS + Azure) │ PLANNED   │ Incident response  │
│  💥  Kubernetes Chaos Simulator     │ PLANNED   │ Break things safely│
│  🧩  System Design Playground       │ PLANNED   │ Distributed canvas │
└────────────────────────────────────┴───────────┴────────────────────┘
```

<details>
<summary><b>💥 Kubernetes Chaos Simulator</b></summary>
<br/>

Inject real failures into live clusters — pod crashes, network partitions, node evictions, resource exhaustion. Learn resilience engineering by intentionally breaking things in a safe, controlled environment. Based on real incident patterns from production on-call experience.

</details>

<details>
<summary><b>🧩 System Design Playground</b></summary>
<br/>

An interactive drag-and-drop canvas to design distributed systems. Model components, estimate throughput, simulate failure modes, and get instant architecture feedback. Great for system design interview prep and real architectural decision-making.

</details>

---

## 👨‍💻 About the Builder

**13+ years in IT. 7+ years in cloud operations.**

Built and operated infrastructure at scale across AWS, Azure, and OpenStack — cloud operations, incident response, multi-cloud migrations, and Kubernetes in production.

Every lab and guide here maps to a real scenario encountered in the field. Not a content farm — battle-tested knowledge, shared in public.

> *"Core content stays free. Always."*

<br/>

### 🎓 Certifications

| Certification | Issuer | Status |
|---------------|--------|--------|
| **CKA** — Certified Kubernetes Administrator | CNCF / Linux Foundation | 🔄 In Progress |
| **CKS** — Certified Kubernetes Security Specialist | CNCF / Linux Foundation | 🔄 In Progress |
| **GCP Professional** — Google Cloud Certification | Google Cloud | 🔄 In Progress |

<br/>

### 🛠️ Technologies

![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazon-aws&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-0078D4?style=flat-square&logo=microsoft-azure&logoColor=white)
![GCP](https://img.shields.io/badge/GCP-4285F4?style=flat-square&logo=google-cloud&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)
![ArgoCD](https://img.shields.io/badge/ArgoCD-EF7B4D?style=flat-square&logo=argo&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white)
![OpenStack](https://img.shields.io/badge/OpenStack-ED1944?style=flat-square&logo=openstack&logoColor=white)

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Vanilla HTML · CSS · JavaScript |
| **Typography** | JetBrains Mono · Syne |
| **Hosting** | GitHub Pages · Custom subdomains |
| **DNS / CDN** | Cloudflare |
| **CI/CD** | GitHub Actions |

---

## 📁 Project Structure

```
eknathalabs/
│
├── index.html                      # Main landing page (eknathalabs.com)
├── eknathalabs-logo.svg            # Brand logo
├── README.md
│
├── tools/                          # Live tools on GitHub Pages
│   ├── github-profile-analyzer/   #  → eknatha.github.io/github-profile-analyzer
│   ├── resumelytics/              #  → eknatha.github.io/resumelytics
│   ├── linux-command-explainer/   #  → eknatha.github.io/linux-command-explainer
│   └── interview-prep/            #  → eknatha.github.io/interview-prep
│
└── labs/                           # Subdomain labs (in progress)
    ├── kubelab/                   #  → kubelab.eknathalabs.com
    ├── terraform/                 #  → terraform.eknathalabs.com
    ├── docker/                    #  → docker.eknathalabs.com
    └── cicd/                      #  → cicd.eknathalabs.com
```

---

## 🚀 Getting Started

### Run locally

```bash
# Clone the repo
git clone https://github.com/eknatha/eknathalabs.git
cd eknathalabs

# Option 1 — Node
npx serve .

# Option 2 — Python
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080) in your browser.

### Deploy

The site is deployed via GitHub Pages. Push to `main` — GitHub Actions handles the rest.

```bash
git add .
git commit -m "feat: describe your change"
git push origin main
```

---

## 🤝 Contributing

Built in public — contributions, issues, and ideas are welcome.

```bash
# 1. Fork & clone
git clone https://github.com/YOUR_USERNAME/eknathalabs.git

# 2. Branch
git checkout -b feat/your-feature

# 3. Commit
git commit -m "feat: describe your change"

# 4. Push & open a PR
git push origin feat/your-feature
```

Good first contributions: fixing typos, adding lab scenarios, writing new guides, improving mobile layout.

---

## 🔔 Get Early Access

<div align="center">

Labs launching soon — be the first to know.

**[→ eknathalabs.com/#early-access](https://eknathalabs.com/#early-access)**

No spam. Unsubscribe anytime.

</div>

---

## 📄 License

```
MIT License — © 2026 EknathaLabs
Free to use, share, and build upon with attribution.
```

---

<div align="center">

**[🌐 Website](https://eknathalabs.com)** &nbsp;·&nbsp;
**[💻 GitHub](https://github.com/eknatha)** &nbsp;·&nbsp;
**[⚡ Live Tools](https://eknathalabs.com/#live-tools)** &nbsp;·&nbsp;
**[🧪 Labs](https://eknathalabs.com/#coming-soon)** &nbsp;·&nbsp;
**[🔔 Early Access](https://eknathalabs.com/#early-access)**

<br/>

*Cloud · DevOps · Platform Engineering · Built in public 🚧*

<br/>

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=eknatha.eknathalabs&style=flat-square&color=00ff88&labelColor=0a0c0f)

</div>
