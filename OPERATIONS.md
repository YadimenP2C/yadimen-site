# Yadimen Site — Canonical Operations Reference

<!--
VERSION: 1.0
DATE: March 2026
STATUS: CANONICAL — load this at the start of every session
PURPOSE: Single reference for all site operations. Defines repo structure,
  deploy pipeline, content refresh workflow, and BAU operations.
  Supersedes all previous deployment protocols.
-->

---

## 1. THE PIPELINE — HOW IT WORKS

```
Claude (this project)
    ↓ edits files via GitHub MCP
GitHub repo: github.com/YadimenP2C/yadimen-site
    ↓ every push to main triggers GitHub Actions
FTP → Network Solutions server (IP: 66.96.131.109)
    ↓ files land on disk
yadimen.com serves them live
```

**The site HTML (`site/index.html`) fetches JSON data files at runtime.**
Content updates = editing a JSON file. No HTML changes needed.

---

## 2. REPO STRUCTURE

```
yadimen-site/
│
├── site/
│   └── index.html              ← Full site SPA (master HTML)
│                                  Edit only for design/structural changes
│
├── data/
│   ├── compass.json            ← Compass roles, signals, bands
│   ├── insights.json           ← Research report cards + PDF URLs
│   ├── jobs.json               ← Live job postings
│   ├── blog.json               ← Blog post cards
│   └── test.json               ← Pipeline health check file
│
├── reports/
│   └── *.pdf                   ← Research PDFs (binary FTP)
│
├── .github/
│   └── workflows/
│       └── deploy.yml          ← GitHub Actions FTP workflow
│
├── OPERATIONS.md               ← THIS FILE — load every session
└── README.md
```

**Server path mapping:**
```
repo: site/index.html         → server: /public_html/yadimen-pipeline/site/index.html
repo: data/compass.json       → server: /public_html/yadimen-pipeline/data/compass.json
repo: data/insights.json      → server: /public_html/yadimen-pipeline/data/insights.json
repo: data/jobs.json          → server: /public_html/yadimen-pipeline/data/jobs.json
repo: data/blog.json          → server: /public_html/yadimen-pipeline/data/blog.json
repo: reports/*.pdf           → server: /public_html/yadimen-pipeline/reports/*.pdf
```

**Live URLs:**
```
yadimen.com/yadimen-pipeline/data/compass.json
yadimen.com/yadimen-pipeline/data/insights.json
yadimen.com/yadimen-pipeline/data/jobs.json
yadimen.com/yadimen-pipeline/data/blog.json
```

---

## 3. TWO TYPES OF CHANGES

### Type 1 — Master Refresh (full site HTML)
**When:** Design changes, new page sections, structural updates, new nav items.
**What changes:** `site/index.html`
**Frequency:** Rarely — only when HTML structure needs updating.

```
Claude edits site/index.html
    ↓ commit to main
GitHub Actions FTPs new index.html to server
    ↓
site refreshes for all visitors
```

**Rule:** `index.html` references all JSON files via `fetch('/data/*.json')`.
Once deployed, content updates never require touching this file.

---

### Type 2 — BAU Content Refresh (JSON only)
**When:** New job, new insight, Compass refresh, blog post, any content update.
**What changes:** One JSON file in `/data/`
**Frequency:** Weekly (jobs), monthly (insights), quarterly (compass), as needed (blog).

```
Claude edits data/[filename].json
    ↓ commit to main
GitHub Actions FTPs updated JSON to server
    ↓
site reads new JSON on next page load — live immediately
```

**No HTML changes. No WordPress. No Elementor. No browser.**

---

## 4. JSON SCHEMAS — CANONICAL STRUCTURE

### compass.json
```json
{
  "meta": {
    "scan_date": "2026-Q1",
    "version": "1.0",
    "domains": ["Regulatory", "Resilience", "Platform", "Payments", "Lending"]
  },
  "roles": [
    {
      "id": "r001",
      "title": "TPRM Programme Manager",
      "domain": "Resilience",
      "sfia": "5-6",
      "band": "NOW",
      "geo": ["NL", "UK", "DE", "FR"],
      "skills": ["DORA", "TPRM", "ISO 27001"],
      "window": "Q1-Q2 2026",
      "signal": "DORA Art.28 enforcement"
    }
  ]
}
```

### insights.json
```json
[
  {
    "id": "c001",
    "title": "DORA Year Two: What Supervisors Are Actually Looking For",
    "domain": "Resilience",
    "date": "2026-03",
    "type": "Enterprise Playbook",
    "pages": "6pp",
    "audience": ["leaders", "ta"],
    "summary": "Post-enforcement analysis of how the DORA mandate is driving role creation...",
    "pdf_url": "https://yadimen.com/wp-content/uploads/2026/03/DORA-Year-Two-Enterprise-Playbook.pdf",
    "active": true
  }
]
```

### jobs.json
```json
[
  {
    "id": "j001",
    "title": "TPRM Programme Manager",
    "type": "Contract",
    "domain": "Resilience",
    "sfia": "5-6",
    "location": "Dublin / Amsterdam",
    "posted": "2026-03-18",
    "active": true,
    "summary": "Leading DORA Art.28 remediation across Tier 1-3 institutions...",
    "apply": "mailto:hello@yadimen.com?subject=TPRM PM Application"
  }
]
```

### blog.json
```json
[
  {
    "id": "b001",
    "title": "DORA Year Two: What the First Inspections Found",
    "slug": "dora-year-two-inspections",
    "date": "2026-03-18",
    "domain": "Resilience",
    "author": "Yadimen Intelligence",
    "summary": "The first wave of ESA inspections is complete. Here is what they found.",
    "body": "Full article text here...",
    "active": true
  }
]
```

---

## 5. BAU OPERATIONS — HOW TO DO EACH TASK

### Post a new job
```
You say: "Post this job: [title], [type], [location], [domain], [SFIA level], [brief description]"
Claude: adds entry to data/jobs.json → commits to main
Result: live on site within 45 seconds
```

### Add a new research report / insight
```
You say: "New insight: [title], [domain], [audience], [summary]" + drop PDF into project
Claude: adds entry to data/insights.json + commits PDF to reports/
Result: new gated card appears on Insights page
```

### Quarterly Compass refresh
```
You say: "Refresh Compass for Q[N] [year]" + provide updated role data
Claude: updates data/compass.json → commits to main
Result: Compass page shows new data within 45 seconds
```

### Publish a blog post
```
You say: "Publish this post" + paste draft text
Claude: formats + adds entry to data/blog.json → commits
Result: post appears on Blog/Insights section
```

### Site design change
```
You say: "Update [section] to [change]"
Claude: edits site/index.html → commits
Result: site updates within 45 seconds
```

### Verify pipeline is healthy
```
Visit: yadimen.com/yadimen-pipeline/data/test.json
Should show: JSON with "pipe": "claude-to-github-to-ftp"
If 404: FTP pipeline broken — check GitHub Actions logs
```

---

## 6. GITHUB ACTIONS — WORKFLOW

File: `.github/workflows/deploy.yml`

```yaml
name: Deploy to Yadimen via FTP
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: SamKirkland/FTP-Deploy-Action@v4.3.5
        with:
          server: ${{ secrets.FTP_SERVER }}
          username: ${{ secrets.FTP_USERNAME }}
          password: ${{ secrets.FTP_PASSWORD }}
          port: 21
          protocol: ftp
          local-dir: ./
          server-dir: /public_html/yadimen-pipeline/
          exclude: |
            **/.git*
            **/.git*/**
            **/node_modules/**
            .github/**
```

**GitHub Secrets required:**
| Secret | Value |
|--------|-------|
| `FTP_SERVER` | `66.96.131.109` |
| `FTP_USERNAME` | `yadimen` |
| `FTP_PASSWORD` | (set in GitHub Secrets — never in chat) |
| `WP_APP_PASSWORD` | (set in GitHub Secrets — never in chat) |
| `WP_BRIDGE_TOKEN` | (set after bridge plugin installed) |

---

## 7. WORDPRESS — WHAT STILL LIVES THERE

WordPress is still needed for:
- Post 2496 — the Elementor page that serves the SPA shell
- Media library — PDFs stored at `yadimen.com/wp-content/uploads/`
- Contact forms (CF7)
- Terms/Privacy pages (6063, 6064)

**WordPress interaction method:** Chrome plugin only.
The container cannot reach yadimen.com (egress proxy blocks it).
Never attempt curl/REST/API from the container directly.

---

## 8. SENSITIVITY PROTOCOL (D1 — CLOSED)

Before every content push, verify:
- [ ] No pool depth data in public JSON
- [ ] No volume estimates
- [ ] No rate trend data
- [ ] No urgency badges
- [ ] No client-identifiable data
- [ ] Scan date current
- [ ] Disclaimer present

See full protocol in `/mnt/project/Compass-Sensitivity-Audit.md`

---

## 9. DECISIONS LOG

| # | Decision | Status |
|---|----------|--------|
| D1 | Sensitivity classification | CLOSED |
| D2 | Design — quarter-arc radar | CLOSED |
| D3 | Workflow — FTP pipeline via GitHub Actions | CLOSED |
| D4 | Zoho gate — post-launch | CLOSED (deferred) |
| D5 | First edition — March 2026 | CLOSED |
| D6 | Team section — no individual photos | CLOSED |
| D7 | Deployment — FTP pipeline, not Chrome plugin | CLOSED — supersedes old D7 |
| D8 | Jobs — JSON file (not WP Job Manager) | CLOSED |
| D9 | Blog — JSON file (not WP posts) | CLOSED |
| D10 | Compass — JSON data file | CLOSED |
| D11 | FTP server — IP 66.96.131.109, user yadimen | CLOSED |

---

## 10. CURRENT STATUS (March 2026)

| Item | Status |
|------|--------|
| Pipeline (Claude → GitHub → FTP → server) | ✅ PROVEN |
| Site HTML v6 | ✅ Built — needs deployment to `site/index.html` |
| compass.json | ✅ In repo at `compass/compass-public.json` — needs moving to `data/` |
| insights.json | ❌ Not yet created |
| jobs.json | ❌ Not yet created |
| blog.json | ❌ Not yet created |
| index.html reads from JSON | ❌ Not yet — v6 has hardcoded data |
| Zoho CRM gate | ❌ Pending |
| Zoho SalesIQ chat | ❌ Pending |
| Bridge plugin | ✅ Built (v2.0) — not yet installed |

---

## 11. NEXT ACTIONS — IN ORDER

```
1. Move compass.json to data/compass.json in repo
2. Create data/insights.json, data/jobs.json, data/blog.json
3. Update site/index.html (v6) to fetch from /data/*.json instead of hardcoded
4. Confirm server-dir path is correct for production (not /yadimen-pipeline/)
5. Deploy v6 + all data files → site live
6. Wire Zoho CRM gate
7. Add Zoho SalesIQ chat
```

---

## 12. SESSION STARTUP CHECKLIST

Every session that touches this repo:
- [ ] Read this file (OPERATIONS.md) first
- [ ] Check current status table (section 10)
- [ ] Confirm what changed since last session
- [ ] Never build from memory — read canonical files first
- [ ] Never share credentials in chat
- [ ] Verify pipeline health: `yadimen.com/yadimen-pipeline/data/test.json`

---

**END OF OPERATIONS.md v1.0**
