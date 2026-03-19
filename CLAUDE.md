# CLAUDE.md — Current Task Brief
<!-- Repo: YadimenP2C/yadimen-site -->
<!-- Local path: C:\Users\BG\OneDrive\Documents\GitHub\yadimen-site -->

---

## STATUS

| Task | Status |
|------|--------|
| S0-1 to S0-5: JSON data files + wire site | 🔄 Active |
| UX-1: Aria labels | ⏳ After S0 |
| UX-2: Colour contrast | ⏳ After S0 |
| UX-3: LCP performance | ⏳ After S0 |

---

## ACTIVE — Sprint 0 remaining

Create the four missing data files and wire the site to read from them.
inspect.py must go from 35/35 with 4 SKIPS to 39/39 with 0 SKIPS.

### Step 1 — Create data/compass.json
Use compass-public.json in repo as schema reference.
Populate with Q1 2026 structure. Include signal_status per role:
  emerging / accelerating / peaking / stabilising / dying
Min 5 roles covering: TPRM, DORA, ISO 20022, ServiceNow IRM, AxiomSL.

### Step 2 — Create data/insights.json
8 playbook entries.
Fields: id, title, domain, date, type, pdf_url, supersedes, active
pdf_url format: /wp-content/uploads/2026/03/[slug].pdf
All active:true, supersedes:null

### Step 3 — Create data/jobs.json
3 active seed roles:
  - TPRM Programme Manager (Contract, Resilience, NL/UK/DE/FR)
  - ServiceNow IRM Consultant (Contract, Resilience, NL/DE/FR/IE)
  - AxiomSL ControllerView TF (Contract, Platform, NL/UK/DE)
Fields: id, title, type, domain, location, posted, active, apply
apply format: mailto:hello@yadimen.com?subject=[role-name]

### Step 4 — Create data/blog.json
Empty array: []

### Step 5 — Check site/index.html
Identify hardcoded content that duplicates JSON data.
Wire fetch() calls to load from data/*.json on page load.
Graceful fallback if fetch fails (show static content).

### Step 6 — Verify
Run: python .github/scripts/inspect.py
Must show: 39/39 PASS, 0 SKIP, 0 FAIL

### Step 7 — Commit and push
Commit: "feat(sprint-0): add data JSON files, wire site to JSON — Sprint 0 complete"
Push to main.

**STOP AFTER 2 failed attempts per step — report to PO**

---

## QUEUED — UX Audit Fixes (pick up after Sprint 0)

Three GitHub Issues will be created by PO with full specs.
Do NOT start these until Sprint 0 is verified complete.
Issue titles to look for:
  UX-1: [EMERGENCY] Accessibility — missing aria-labels
  UX-2: [EMERGENCY] Accessibility — colour contrast WCAG AA
  UX-3: [P1] Performance — LCP 13.4s

---

## Do NOT touch
- wp-config.php or WordPress core files
- .github/workflows/ (pipeline is correct)
- Any server files predating 2025

## Last Updated
2026-03-19 — Sprint 0 active, UX fixes queued as GitHub Issues
