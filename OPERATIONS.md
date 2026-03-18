# Yadimen Site — Canonical Operations Reference

<!--
FILE: OPERATIONS.md
VERSION: 1.1
DATE: March 2026
STATUS: CANONICAL — load this at the start of every session
PURPOSE: Single master reference for all yadimen.com site operations.
  Defines repo structure, deploy pipeline, content refresh workflow, BAU operations.
SUPERSEDES:
  - yadimen-web-portal-context-v2.md §5 (Chrome deploy protocol)
  - yadimen-build-plan-v1.md Sprint 0 deploy steps
  - yadimen-build-plan-v1.md Sprint 3 (WP Job Manager)
  - yadimen-build-plan-v1.md Sprint 5 (Insights CPT)
  - Decisions D7/D8/D9/D10 in build plan
LOADS ALONGSIDE:
  - yadimen-web-portal-context-v2.md (site structure, WP post IDs, sensitivity)
  - yadimen-portal-theme-v1.md (design tokens, typography, colour palette)
  - yadimen-site-spec-v1.md (page specifications, persona map)
  - Compass-Sensitivity-Audit.md (sensitivity classification)
-->

---

## ⚠️ HARD RULES — READ FIRST, EVERY SESSION

```
RULE 1 — NEVER deploy via Chrome browser injection.
  No injecting HTML into Elementor via JavaScript.
  No pasting content into Elementor widgets via Chrome.
  No using the Chrome extension to push site content.
  REASON: Not scalable, not repeatable, not auditable.
           The GitHub → FTP pipeline exists precisely to replace this.

RULE 2 — ALL site changes go through GitHub.
  Every change to site HTML, JSON data, or PDFs must be committed to
  github.com/YadimenP2C/yadimen-site and deployed via GitHub Actions FTP.
  This is the only approved deploy method.

RULE 3 — Never share credentials in chat.
  FTP credentials, WordPress passwords, API tokens — all go into
  GitHub Secrets directly. Never typed into any conversation.

RULE 4 — Never build from memory.
  Read OPERATIONS.md and check current status before every session.
```

---

## 1. THE PIPELINE — HOW IT WORKS

```
Claude (this project)
    ↓  edits files via GitHub MCP
GitHub repo: github.com/YadimenP2C/yadimen-site
    ↓  every push to main triggers GitHub Actions automatically
FTP → Network Solutions server
      IP: 66.96.131.109 | User: yadimen
    ↓  files land at /public_html/yadimen-pipeline/
yadimen.com serves them live
```

**The site HTML (`site/index.html`) fetches JSON data files at runtime.**
Content updates = edit one JSON file. No HTML changes needed.
Pipeline proven: March 18, 2026.

**Why this model:**
- Scalable — one process handles all content types forever
- Secure — credentials in GitHub Secrets, never in chat or code
- Repeatable — every deploy is identical, logged, reversible
- Auditable — full git history of every change ever made

---

## 2. REPO STRUCTURE — CANONICAL

```
yadimen-site/
│
├── site/
│   └── index.html              ← Full site SPA (master HTML)
│                                  Edit only for design/structural changes
│
├── data/
│   ├── compass.json            ← Compass roles, signals, bands (quarterly)
│   ├── insights.json           ← Research report cards + PDF URLs (monthly)
│   ├── jobs.json               ← Live job postings (weekly)
│   ├── blog.json               ← Blog post cards (as needed)
│   └── test.json               ← Pipeline health check (do not delete)
│
├── reports/
│   └── *.pdf                   ← Research PDFs (binary FTP)
│
├── .github/
│   └── workflows/
│       └── deploy.yml          ← GitHub Actions FTP workflow (do not edit)
│
└── OPERATIONS.md               ← THIS FILE — load every session
```

**Server path mapping:**

| Repo path | Server path | Live URL |
|-----------|------------|----------|
| `site/index.html` | `/public_html/yadimen-pipeline/site/index.html` | `yadimen.com/yadimen-pipeline/site/` |
| `data/compass.json` | `/public_html/yadimen-pipeline/data/compass.json` | `yadimen.com/yadimen-pipeline/data/compass.json` |
| `data/insights.json` | `/public_html/yadimen-pipeline/data/insights.json` | `yadimen.com/yadimen-pipeline/data/insights.json` |
| `data/jobs.json` | `/public_html/yadimen-pipeline/data/jobs.json` | `yadimen.com/yadimen-pipeline/data/jobs.json` |
| `data/blog.json` | `/public_html/yadimen-pipeline/data/blog.json` | `yadimen.com/yadimen-pipeline/data/blog.json` |
| `reports/*.pdf` | `/public_html/yadimen-pipeline/reports/` | `yadimen.com/yadimen-pipeline/reports/` |

> **Note:** `/yadimen-pipeline/` is the current test path. Once confirmed stable,
> update `server-dir` in `deploy.yml` to `/public_html/` for production root.

---

## 3. TWO TYPES OF CHANGES — FOREVER

### Type 1 — Master HTML Refresh

**When:** Design changes, new page sections, navigation updates, structural changes.
**What changes:** `site/index.html` only.
**Frequency:** Rare — once per design cycle.

```
Claude edits site/index.html in GitHub
    ↓ GitHub Actions triggers on commit to main
FTP deploys new index.html to server
    ↓
Site refreshes for all visitors — live in ~45 seconds
```

**Rule:** `index.html` references all content via `fetch('/data/*.json')`.
Once deployed, content changes NEVER require touching this file.

### Type 2 — BAU Content Refresh

**When:** New job posting, new research report, Compass quarterly refresh, blog post.
**What changes:** One JSON file in `data/`.
**Frequency:** Weekly (jobs) / Monthly (insights) / Quarterly (compass) / As needed (blog).

```
Claude edits data/[filename].json in GitHub
    ↓ GitHub Actions triggers on commit to main
FTP deploys updated JSON to server
    ↓
Site reads new JSON on next page load — live in ~45 seconds
```

**No HTML changes. No WordPress admin. No Elementor. No browser. No Chrome injection.**

---

## 4. HOW EVERY DEPLOY WORKS — STEP BY STEP

Every single change, regardless of size, follows this exact flow:

```
Step 1: You describe the change in this Claude project
Step 2: Claude edits the appropriate file(s) via GitHub MCP
Step 3: GitHub commit triggers automatically
Step 4: GitHub Actions runs FTP deploy (~45 seconds)
Step 5: Change is live — verify at the relevant URL
```

**There are no other steps. There is no Step 0 involving a browser.**

---

## 5. JSON SCHEMAS — CANONICAL STRUCTURE

### compass.json
```json
{
  "meta": {
    "scan_date": "2026-Q1",
    "version": "1.0",
    "next_refresh": "2026-Q2",
    "domains": ["Regulatory", "Resilience", "Platform", "Payments", "Lending"]
  },
  "roles": [{
    "id": "r001",
    "title": "TPRM Programme Manager",
    "domain": "Resilience",
    "sfia": "5-6",
    "band": "NOW",
    "geo": ["NL", "UK", "DE", "FR"],
    "skills": ["DORA", "TPRM", "ISO 27001"],
    "window": "Q1-Q2 2026",
    "signal": "DORA Art.28 enforcement"
  }]
}
```

### insights.json
```json
[{
  "id": "c001",
  "title": "DORA Year Two: What Supervisors Are Actually Looking For",
  "domain": "Resilience",
  "date": "2026-03",
  "type": "Enterprise Playbook",
  "pages": "6pp",
  "audience": ["leaders", "ta"],
  "summary": "Post-enforcement analysis...",
  "pdf_url": "https://yadimen.com/wp-content/uploads/2026/03/DORA-Year-Two-Enterprise-Playbook.pdf",
  "active": true
}]
```

### jobs.json
```json
[{
  "id": "j001",
  "title": "TPRM Programme Manager",
  "type": "Contract",
  "domain": "Resilience",
  "sfia": "5-6",
  "location": "Dublin / Amsterdam",
  "posted": "2026-03-18",
  "active": true,
  "summary": "Leading DORA Art.28 remediation...",
  "apply": "mailto:hello@yadimen.com?subject=TPRM PM Application"
}]
```

### blog.json
```json
[{
  "id": "b001",
  "title": "DORA Year Two: What the First Inspections Found",
  "slug": "dora-year-two-inspections",
  "date": "2026-03-18",
  "domain": "Resilience",
  "author": "Yadimen Intelligence",
  "summary": "The first wave of ESA inspections is complete.",
  "body": "Full article text here as plain text or light HTML.",
  "active": true
}]
```

---

## 6. BAU OPERATIONS — HOW TO DO EACH TASK

| Task | What you say | File changed | Deploy time |
|------|-------------|-------------|-------------|
| Post a new job | "Post this job: [title, type, location, domain, brief]" | `data/jobs.json` | ~45s |
| Close a job | "Close job [id or title]" | `data/jobs.json` — sets `active: false` | ~45s |
| New research report | "New insight: [title, domain, audience, summary, PDF]" | `data/insights.json` | ~45s |
| Quarterly Compass refresh | "Refresh Compass for Q[N] [year]" + data | `data/compass.json` | ~45s |
| New blog post | "Publish this post" + paste text | `data/blog.json` | ~45s |
| Site design change | "Update [section] to [change]" | `site/index.html` | ~45s |
| Verify pipeline | — | Visit `yadimen.com/yadimen-pipeline/data/test.json` | instant |

---

## 7. GITHUB ACTIONS WORKFLOW

File: `.github/workflows/deploy.yml` — **do not edit manually.**

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
            .github/**
```

### GitHub Secrets — Required

Location: `github.com/YadimenP2C/yadimen-site/settings/secrets/actions`

| Secret name | What it is | Status |
|-------------|-----------|--------|
| `FTP_SERVER` | `66.96.131.109` | ✅ Set |
| `FTP_USERNAME` | `yadimen` | ✅ Set |
| `FTP_PASSWORD` | FTP account password | ✅ Set |
| `WP_APP_PASSWORD` | WordPress Application Password | ✅ Set |
| `WP_BRIDGE_TOKEN` | Bridge plugin token | ⏳ After plugin install |

**Never share secret values in chat. Always update directly in GitHub Secrets.**

---

## 8. WORDPRESS — LIMITED ROLE

WordPress is still needed for a small set of things only:

| Asset | WP Post ID | Purpose |
|-------|-----------|---------|
| Main site SPA shell | 2496 | Elementor Canvas page — serves via FTP now |
| Insights hub | 4969 | Separate WP page |
| Terms of Use | 6064 | Legal |
| Privacy Policy | 6063 | Legal |
| Header template | 5097 | Must exclude post 2496 |
| Media library | — | PDFs at `yadimen.com/wp-content/uploads/` |
| Contact forms | — | CF7 plugin |

**WordPress admin access: for media uploads and plugin management only.**
**Never for site content deployment — that is the pipeline's job.**

---

## 9. WHAT CHROME / BROWSER IS USED FOR

Chrome (via Claude in Chrome extension) has one remaining legitimate use:

| Task | Allowed? |
|------|---------|
| Upload media (PDFs, images) to WordPress media library | ✅ Yes |
| Install/configure WordPress plugins | ✅ Yes |
| Check live site visually after a deploy | ✅ Yes |
| Inject HTML into Elementor widgets | ❌ Never |
| Paste site content into WordPress editor | ❌ Never |
| Deploy any site file via browser | ❌ Never |

---

## 10. DECISIONS LOG

| # | Decision | Outcome | Status |
|---|----------|---------|--------|
| D1 | Sensitivity classification | Three-tier: PUBLIC / GATED / INTERNAL | CLOSED |
| D2 | Design — Compass | Quarter-arc radar, light/warm theme | CLOSED |
| D3 | Workflow | FTP pipeline via GitHub Actions | CLOSED |
| D4 | Zoho gate | Deferred to post-launch | DEFERRED |
| D5 | First edition timing | March 2026 | CLOSED |
| D6 | Team section | No individual photos — team photo + AI agent cards | CLOSED |
| D7 | Deploy method | GitHub → FTP pipeline ONLY. Chrome injection permanently prohibited. | CLOSED |
| D8 | Jobs content | `data/jobs.json` — not WP Job Manager | CLOSED |
| D9 | Insights content | `data/insights.json` — not WP CPT | CLOSED |
| D10 | Blog content | `data/blog.json` — not WP posts | CLOSED |
| D11 | FTP server | IP: `66.96.131.109` · User: `yadimen` · Proven March 18, 2026 | CLOSED |
| D12 | Chrome injection | Permanently prohibited — pipeline only for all site deploys | CLOSED |

---

## 11. CONFLICTS WITH OLDER CONTEXT FILES

These items in existing project files are superseded by this document:

| File | Section | Old approach | Superseded by |
|------|---------|-------------|---------------|
| `yadimen-web-portal-context-v2.md` | §5 Deploy Protocol (Steps A–E) | Chrome plugin paste into Elementor | FTP pipeline — Type 1 or 2 above |
| `yadimen-web-portal-context-v2.md` | §8 Quarterly Workflow step 5 | "Deploy via Chrome plugin" | "Commit to GitHub → FTP auto-deploys" |
| `yadimen-build-plan-v1.md` | Sprint 0 steps 0.3–0.6 | Paste HTML into Elementor via Chrome | Push `site/index.html` to repo |
| `yadimen-build-plan-v1.md` | Sprint 3 (Jobs) | WP Job Manager plugin | `data/jobs.json` |
| `yadimen-build-plan-v1.md` | Sprint 5 (Content pipeline) | WP CPT / Insights plugin | `data/insights.json` |
| `yadimen-build-plan-v1.md` | Decisions D7/D8/D9/D10 | Open decisions | All closed — see section 10 above |

---

## 12. CURRENT STATUS — March 18, 2026

| Item | Status | Next action |
|------|--------|------------|
| Pipeline (Claude→GitHub→FTP→server) | ✅ PROVEN | — |
| Site HTML v7 | ✅ Built | Push `site/index.html` via GitHub MCP |
| v7 reads from JSON (not hardcoded) | ❌ Not yet | Update `site/index.html` after deploy confirmed |
| `data/compass.json` | ⏳ At `compass/compass-public.json` | Move to `data/compass.json` |
| `data/insights.json` | ❌ Not created | Create with 8 playbook entries |
| `data/jobs.json` | ❌ Not created | Create with seed roles |
| `data/blog.json` | ❌ Not created | Create empty, populate on first post |
| Team photo `Yadimen_Final_team.png` | ✅ Uploaded to WP | Referenced in v7 HTML |
| Production `server-dir` path | ⏳ Confirm | Change `/yadimen-pipeline/` → `/public_html/` |
| Zoho CRM gate wired | ❌ Pending | Sprint 1 |
| Zoho SalesIQ chat | ❌ Pending | Sprint 2 |
| Bridge plugin v2.0 | ✅ Built in repo | Install in WordPress when needed |

---

## 13. SESSION STARTUP CHECKLIST

Every session — no exceptions:

- [ ] Read `OPERATIONS.md` first — check section 12 for current status
- [ ] Check what changed since last session — ask if unclear
- [ ] Never build from memory — read canonical files first
- [ ] Never share credentials in chat
- [ ] Never attempt Chrome/browser injection for site deploys
- [ ] Verify pipeline health: `yadimen.com/yadimen-pipeline/data/test.json`
- [ ] All deploys go through GitHub → FTP pipeline only

---

*YADIMEN OPERATIONS v1.1 · March 2026 · Canonical · Load every session*
