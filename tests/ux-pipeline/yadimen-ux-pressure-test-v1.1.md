# Yadimen.com — UX/CX Pressure Test Pipeline
**Version 1.1 · March 2026 · Canonical reference**

Full spec including all four phases, persona prompts, Nielsen heuristics scoring template,
priority fix queue, and Claude Code build order.

This is the source of truth for UX testing methodology on yadimen.com.
Load at the start of any UX sprint session.

---

## SSL Gate — P0 Pre-Render Check

Before running any UX test:

```bash
curl -vI https://yadimen.com 2>&1 | grep -E 'SSL|certificate|expire|issuer|subject'
# OR
echo | openssl s_client -connect yadimen.com:443 -servername yadimen.com 2>/dev/null \
  | openssl x509 -noout -dates -issuer -subject
```

If SSL fails: output PIPELINE BLOCKED: SSL FAILURE and halt.
No UX finding is meaningful until the site is reachable without a security warning.

In Playwright — NEVER use ignoreHTTPSErrors: true in production tests.
SSL failures must surface as hard test failures.

---

## Phase 1 — Automated Baseline

Tools: Lighthouse CLI, Pa11y
Runtime: ~5 minutes
Trigger: After every deploy

```bash
lighthouse https://www.yadimen.com \
  --output json \
  --output-path ./reports/lighthouse-$(date +%Y%m%d).json \
  --chrome-flags="--headless"

pa11y https://www.yadimen.com \
  --reporter json \
  > ./reports/a11y-$(date +%Y%m%d).json
```

Targets: Performance >80, Accessibility >90, FCP <2.5s, TTI <5s, LCP <4s, CLS <0.1

---

## Phase 2 — Journey Simulation

Tool: Playwright
Runtime: ~10 minutes
Trigger: After structural changes, per sprint

Personas tested:
- buyer-desktop (1440x900)
- buyer-mobile (390x844)
- psl-evaluator (1280x800)

Checkpoints: landing, hero-fold, first-cta-visible, proof-section,
compass-widget, intelligence-section, bottom-cta

Measure: time to first CTA, scroll depth to proof mechanisms,
mobile table rendering, CTA visibility per checkpoint

---

## Phase 3 — Persona Intelligence Layer

Tool: Claude API (Sonnet)
Runtime: ~3 minutes
Trigger: After content or flow changes, per sprint

Four personas:
1. CRO/Head of Transformation — Tier 2 EU bank, DORA programme, 90 seconds, vs 2 SIs
2. Head of TA — US bank Dublin entity, TPRM PM role open 6 weeks, needs domain depth 60s
3. PSL Evaluator — formal supplier assessment, 3-5 minutes on site
4. Senior FS Specialist SFIA 5-6 — assessing credibility vs generalist agency

Evaluation structure per persona:
- First impression (0-10 seconds)
- Primary question answered? How quickly?
- Trust signals — what builds / undermines credibility
- Friction points — ranked, specific
- Conversion decision — yes/no/which CTA/why not
- One change for this persona

Cadence: Compare verdicts across versions to track friction point resolution.

---

## Phase 4 — Competitive Benchmark (Quarterly)

Run Phase 1 + Phase 3 against:
- Bruin Financial or Broadgate Search (niche FS staffing)
- Infosys or Wipro FS talent page (SI comparator)
- Well-regarded boutique consultancy with similar positioning

Benchmark: Lighthouse scores, persona verdicts, time to proof

---

## Nielsen Heuristics Scoring

| # | Heuristic | CRO/Buyer | TA Lead | PSL Evaluator | Candidate |
|---|-----------|-----------|---------|---------------|-----------|
| 1 | Visibility of system status | | | | |
| 2 | Match between system and real world | | | | |
| 3 | User control and freedom | | | | |
| 4 | Consistency and standards | | | | |
| 5 | Error prevention | | | | |
| 6 | Recognition rather than recall | | | | |
| 7 | Flexibility and efficiency of use | | | | |
| 8 | Aesthetic and minimalist design | | | | |
| 9 | Help recover from errors | | | | |
| 10 | Help and documentation | | | | |

Weighting for B2B FS buyers: heuristics 2, 6, 8 carry highest weight.

---

## Diagnosis Summary — March 2026

| Finding | Severity | Sprint action |
|---------|----------|---------------|
| SSL invalid — ERR_CERT_AUTHORITY_INVALID | P0 | Fix immediately — blocks all UX work |
| Hero is positioning not converting | High | Lead with outcome, make persona selector dominant |
| No progressive commitment architecture | High (buyers) | Restructure around trust escalation model |
| Social proof structurally absent | High (PSL/enterprise) | Add one specificity anchor in first 3 sections |
| CTA proliferation — no dominant path | High | One primary CTA per persona, suppress others |
| Mobile table-heavy content degraded | High (mobile) | Cards/accordions for mobile |
| Visual design below content authority | Medium-High | Typography, spacing, white space audit |

---

## Claude Code Build Order

1. `tests/ux-pipeline/run.sh` — Phase 1 master runner
2. `tests/ux-pipeline/lighthouse-runner.sh` — Lighthouse wrapper
3. `tests/ux-pipeline/playwright-journey.js` — Phase 2 journey simulation
4. `tests/ux-pipeline/persona-eval.js` — Phase 3 Claude API persona layer
5. `tests/ux-pipeline/report-assembler.js` — combine + diff vs previous run

Single command: `bash tests/ux-pipeline/run.sh`
Output: `tests/ux-pipeline/reports/YYYY-MM-DD/` with all artefacts
