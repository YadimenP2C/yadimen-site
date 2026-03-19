# Yadimen UX/CX Pressure Test Pipeline

Four-phase testing pipeline for yadimen.com.
Run after every significant design iteration.

## Phases

| Phase | Tool | Runtime | Trigger |
|-------|------|---------|--------|
| 1 — Automated Baseline | Lighthouse + Pa11y | ~5 min | Every deploy |
| 2 — Journey Simulation | Playwright | ~10 min | Per sprint |
| 3 — Persona Intelligence | Claude API | ~3 min | Per sprint |
| 4 — Competitive Benchmark | Phases 1+3 on comparators | ~15 min | Quarterly |

## Phase 1 — Quick Start

```bash
cd tests/ux-pipeline
npm install
bash run.sh
```

Outputs to `reports/YYYYMMDD-lighthouse.json` and `reports/YYYYMMDD-a11y.json`.

## Targets

| Metric | Target |
|--------|--------|
| Performance score | >80 |
| Accessibility score | >90 |
| First Contentful Paint | <2.5s |
| Time to Interactive | <5s |
| Largest Contentful Paint | <4s |
| Cumulative Layout Shift | <0.1 |

## SSL Gate — MUST PASS BEFORE ANY UX TEST

```bash
curl -vI https://yadimen.com 2>&1 | grep -E 'SSL|certificate|expire|issuer'
# Must show valid cert — no ERR_CERT errors
```

If SSL fails: stop. All UX findings are meaningless until the site is reachable.

## Personas (Phase 2 + 3)

- CRO / Head of Transformation — 90 seconds, evaluating vs 2 SIs
- Head of TA — open TPRM role, 6 weeks unfilled, needs domain depth in 60s
- PSL Evaluator — formal supplier assessment, 3-5 minutes
- Senior FS Specialist SFIA 5-6 — assessing firm credibility vs generalist agency

## Priority Fix Queue

### P0 — Blocks everything
0. SSL certificate valid (ERR_CERT_AUTHORITY_INVALID = site unreachable)
1. Hero leads with outcome not brand line
2. CTA hierarchy — one dominant path per persona
3. Trust anchor — one specificity signal in first 3 sections

### P1 — High impact
4. Proof surfacing — Compass and vetting chain in first 3 sections
5. Mobile table audit — cards/accordions for table-heavy content
6. Scroll pacing — section breaks as micro-commitment moments

### P2 — Polish
7. Visual authority calibration — design must match content credibility
8. Mobile interaction test — Compass widget, persona selector, PDF downloads
9. Load performance — fix any >3s LCP

## Canonical reference
See `tests/ux-pipeline/yadimen-ux-pressure-test-v1.1.md` for full spec.
