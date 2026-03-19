# CLAUDE.md — Current Task Brief
<!-- Updated by claude.ai after each session. Read by Claude Code on startup. -->

## Current Sprint
Sprint 0 — Foundation

## Current Goal
Complete Sprint 0: SDLC bootstrap in GitHub + data JSON files + site reads from JSON.

## Current State (March 2026)
- v9 live at yadimen.com — orbit hero, clean photo, pipeline proven
- inspect.py passing 39/39 in GitHub Actions
- OPERATIONS.md, INSPECTION-REPORT.md, deploy.yml in repo
- MISSING: ENGINEER.md, QA.md, PROJECT-METADATA.md, agent-poll.py
- MISSING: data/compass.json, data/insights.json, data/jobs.json, data/blog.json
- MISSING: GitHub Issue label schema, Sprint 0-7 issues
- site/index.html still has hardcoded data — not reading from JSON yet

## Next Actions (in order)
1. Push ENGINEER.md, QA.md, PROJECT-METADATA.md, agent-poll.py to repo root
2. Create GitHub Issue label schema (9 state + type + priority + sprint labels)
3. Create Sprint 0-7 GitHub Issues with full task briefs
4. Create data/compass.json — Q1 2026, 18 roles, signal status field
5. Create data/insights.json — 8 playbooks with PDF URLs
6. Create data/jobs.json — 3 seed roles, active:true
7. Create data/blog.json — empty array
8. Update site/index.html — wire all fetch() calls to /data/*.json
9. Run inspect.py — confirm 39/39 with zero skips (JSON checks must pass)
10. Push and confirm GitHub Actions green

## Guardrails for This Task
- STOP after 5 attempts on any single item — post report and escalate
- Do NOT modify .htaccess or WordPress files
- Do NOT delete any file with a date before 2025
- STOP before any paid service activation (Zoho)

## Do Not Touch
- WordPress core files
- .htaccess (confirmed working — do not modify)
- data/test.json (pipeline health check — do not delete)

## Verify Success By
1. yadimen.com loads with v9 hero
2. yadimen.com/data/compass.json returns valid JSON
3. yadimen.com/data/test.json returns valid JSON
4. GitHub Actions: inspect.py passes 39/39 zero skips
5. Site renders Compass roles from JSON (not hardcoded)

## Framework Files Status
| File | Status |
|------|--------|
| OPERATIONS.md | ✅ In repo |
| INSPECTION-REPORT.md | ✅ Auto-generated |
| deploy.yml | ✅ In repo |
| inspect.py | ✅ In repo |
| ENGINEER.md | ❌ Missing |
| QA.md | ❌ Missing |
| PROJECT-METADATA.md | ❌ Missing |
| CLAUDE.md | ✅ This file |
| agent-poll.py | ❌ Missing |

## Last Updated
March 2026 — end of SDLC bootstrap session
