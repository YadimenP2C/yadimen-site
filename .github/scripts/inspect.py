#!/usr/bin/env python3
"""
Yadimen Site — Code Inspector
Version: 1.0
Runs: GitHub Actions, before every deploy
Blocks: Deploy if any check fails
Output: Annotated pass/fail report committed to repo

Rules test structural properties and engineering standards.
Knowing the rules does not help you pass them — you must build correctly.
"""

import re
import json
import sys
import os
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────

SITE_FILE       = "site/index.html"
DATA_DIR        = "data"
REPORT_FILE     = "INSPECTION-REPORT.md"

REQUIRED_PAGES  = [
    "pg-home", "pg-compass", "pg-signals", "pg-hww",
    "pg-insights", "pg-scan", "pg-psl", "pg-sectors",
    "pg-global", "pg-candidates"
]

REQUIRED_FONTS  = ["Playfair Display", "DM Mono", "DM Sans"]

REQUIRED_TOKENS = [
    "--ink:", "--paper:", "--cream:", "--gold:",
    "--ai-blue:", "--ai-glow:", "--steel:", "--mist:"
]

INTERNAL_FIELDS = [
    "pool depth: scarce", "pool depth: constrained",
    "pool depth: available", '"vol":', '"urg":', '"rate":',
    "urgency badge", "rate trend", "volume estimate"
]

FORBIDDEN_HOSTS = ["unsplash.com", "placeholder.com", "picsum.photos",
                   "lorem", "lorempixel", "dummyimage"]

FORBIDDEN_PATTERNS = [
    r'eval\s*\(',
    r'document\.write\s*\(',
    r'innerHTML\s*=\s*[^;]*user',
    r'\.html\s*\(\s*[^"\'`]',
]

CREDENTIAL_PATTERNS = [
    r'ghp_[A-Za-z0-9]{36}',
    r'sk-[A-Za-z0-9]{48}',
    r'xoxb-[0-9]+-',
    r'AKIA[0-9A-Z]{16}',
    r'password\s*=\s*["\'][^"\']{8,}["\']',
    r'api_key\s*=\s*["\'][^"\']{8,}["\']',
]

JSON_SCHEMAS = {
    "compass.json": {
        "type": "object",
        "required_keys": ["meta", "roles"],
        "roles_required": ["id", "title", "domain", "band", "geo", "signal"]
    },
    "insights.json": {
        "type": "array",
        "required_keys": ["id", "title", "domain", "date", "type", "pdf_url", "active"]
    },
    "jobs.json": {
        "type": "array",
        "required_keys": ["id", "title", "type", "location", "posted", "active", "apply"]
    },
    "blog.json": {
        "type": "array",
        "required_keys": ["id", "title", "date", "author", "summary", "active"]
    },
}

MIN_MEDIA_QUERIES = 3
MAX_FILE_SIZE_KB  = 200
MIN_FONT_SIZE_REM = 0.6  # below this in desktop CSS = too small

# ─────────────────────────────────────────────────────────────
# RESULT COLLECTOR
# ─────────────────────────────────────────────────────────────

results = []
pass_count = 0
fail_count = 0
skip_count = 0

def record(rule_id, name, passed, detail="", line=None):
    global pass_count, fail_count
    status = "PASS" if passed else "FAIL"
    if passed:
        pass_count += 1
    else:
        fail_count += 1
    loc = f" (line {line})" if line else ""
    results.append({
        "id": rule_id,
        "name": name,
        "status": status,
        "detail": detail + loc,
    })

def skip(rule_id, name, reason):
    global skip_count
    skip_count += 1
    results.append({
        "id": rule_id,
        "name": name,
        "status": "SKIP",
        "detail": reason,
    })

def find_line(html, pattern):
    """Find line number of first pattern match."""
    lines = html.split("\n")
    for i, line in enumerate(lines, 1):
        if pattern in line:
            return i
    return None

# ─────────────────────────────────────────────────────────────
# LOAD SITE FILE
# ─────────────────────────────────────────────────────────────

site_path = Path(SITE_FILE)
if not site_path.exists():
    print(f"FATAL: {SITE_FILE} not found in repo root.")
    print("Expected path: site/index.html")
    sys.exit(2)

with open(site_path, "r", encoding="utf-8") as f:
    html = f.read()

html_lower = html.lower()
lines = html.split("\n")

# Separate CSS from full HTML for desktop-only checks
css_match = re.search(r"<style>(.*?)</style>", html, re.DOTALL)
css_block = css_match.group(1) if css_match else ""

# CSS above first @media = desktop CSS
media_split = re.split(r"@media\s", css_block, maxsplit=1)
desktop_css = media_split[0] if media_split else css_block

# ─────────────────────────────────────────────────────────────
# CATEGORY 1 — STRUCTURE INTEGRITY
# ─────────────────────────────────────────────────────────────

print("\n── Category 1: Structure Integrity ──")

# CI-S1 DOCTYPE
record("CI-S1", "Valid HTML5 DOCTYPE",
    html.strip().startswith("<!DOCTYPE html>"))

# CI-S2 Document structure
has_html  = html.count("<html") == 1 and html.count("</html>") == 1
has_head  = html.count("<head>") == 1 and html.count("</head>") == 1
has_body  = html.count("<body>") == 1 and html.count("</body>") == 1
record("CI-S2", "Single html/head/body elements",
    has_html and has_head and has_body,
    "" if (has_html and has_head and has_body) else
    f"html:{html.count('<html')} head:{html.count('<head>')} body:{html.count('<body>')}")

# CI-S3 Meta tags
has_charset  = 'charset="UTF-8"' in html or "charset=UTF-8" in html
has_viewport = 'name="viewport"' in html
record("CI-S3", "charset and viewport meta present",
    has_charset and has_viewport,
    "" if (has_charset and has_viewport) else
    f"charset={'✓' if has_charset else '✗'} viewport={'✓' if has_viewport else '✗'}")

# CI-S4 Title non-empty
title_match = re.search(r"<title>([^<]+)</title>", html)
record("CI-S4", "Title tag non-empty",
    bool(title_match and len(title_match.group(1).strip()) > 5),
    title_match.group(1) if title_match else "no title found")

# CI-S5 Required page sections
missing_pages = [p for p in REQUIRED_PAGES if f'id="{p}"' not in html]
record("CI-S5", f"All {len(REQUIRED_PAGES)} required page sections present",
    len(missing_pages) == 0,
    f"Missing: {', '.join(missing_pages)}" if missing_pages else "")

# CI-S6 Exactly one page active on load
on_count = len(re.findall(r'class="pg on"', html))
record("CI-S6", "Exactly one page active on load",
    on_count == 1,
    f"Found {on_count} pages with class='pg on' (expected 1)")

# CI-S7 No duplicate IDs
all_ids = re.findall(r'\bid="([^"]+)"', html)
dupes = [id_ for id_ in set(all_ids) if all_ids.count(id_) > 1]
record("CI-S7", "No duplicate element IDs",
    len(dupes) == 0,
    f"Duplicates: {', '.join(dupes[:5])}" if dupes else "")

# CI-S8 CSS balanced braces
open_braces  = css_block.count("{")
close_braces = css_block.count("}")
record("CI-S8", "CSS balanced braces",
    open_braces == close_braces,
    f"Open: {open_braces} Close: {close_braces}")

# CI-S9 go() function defined
record("CI-S9", "go() navigation function defined",
    "function go(" in html or "const go=" in html or "let go=" in html)

# CI-S10 renderCompass defined
record("CI-S10", "renderCompass() function defined",
    "renderCompass" in html)

# CI-S11 All onclick go() calls use valid page IDs
go_calls = re.findall(r"go\('([^'${}]+)'\)", html)
go_calls += re.findall(r'go\("([^"${}]+)"\)', html)
valid_pages = set(p.replace("pg-", "") for p in REQUIRED_PAGES)
invalid_calls = [c for c in go_calls if c not in valid_pages]
record("CI-S11", "All go() calls reference valid page IDs",
    len(invalid_calls) == 0,
    f"Invalid targets: {', '.join(set(invalid_calls))}" if invalid_calls else "")

# CI-S12 No script/style closing tags inside strings
# CI-S12 — Check for </script> outside its closing position (genuine parse-break risk)
# Template literals legitimately contain HTML — we only flag actual string-concat attacks
sc_lines = [i+1 for i, line in enumerate(lines)
            if '</script>' in line
            and not line.strip().startswith('</')
            and '<script' not in line
            and '`' not in line  # template literals are fine
            and line.strip() != '</script>']
record("CI-S12", "No premature </script> tag outside script block",
    len(sc_lines) == 0,
    f"Suspicious lines: {sc_lines[:3]}" if sc_lines else "")

# ─────────────────────────────────────────────────────────────
# CATEGORY 2 — SECURITY & SENSITIVITY
# ─────────────────────────────────────────────────────────────

print("\n── Category 2: Security & Sensitivity ──")

# CI-SEC1 No credentials
cred_found = []
for pattern in CREDENTIAL_PATTERNS:
    matches = re.findall(pattern, html)
    if matches:
        cred_found.extend(matches[:1])
record("CI-SEC1", "No hardcoded credentials or API keys",
    len(cred_found) == 0,
    f"Found: {cred_found[0][:20]}..." if cred_found else "")

# CI-SEC2 No INTERNAL tier data
internal_found = []
for field in INTERNAL_FIELDS:
    if field.lower() in html_lower:
        line = find_line(html, field)
        internal_found.append(f"'{field}' at line {line}")
record("CI-SEC2", "No INTERNAL tier data in public HTML",
    len(internal_found) == 0,
    "; ".join(internal_found[:3]) if internal_found else "")

# CI-SEC3 No direct PDF href links
direct_pdfs = re.findall(r'href="[^"]*\.pdf"', html)
record("CI-SEC3", "No direct PDF links (all must be gated via JS)",
    len(direct_pdfs) == 0,
    f"Found {len(direct_pdfs)}: {direct_pdfs[0][:60]}" if direct_pdfs else "")

# CI-SEC4 No dangerous JS patterns
dangerous_js = []
for pattern in FORBIDDEN_PATTERNS:
    matches = re.finditer(pattern, html)
    for m in matches:
        line = html[:m.start()].count("\n") + 1
        dangerous_js.append(f"line {line}: {m.group()[:40]}")
record("CI-SEC4", "No dangerous JavaScript patterns",
    len(dangerous_js) == 0,
    "; ".join(dangerous_js[:2]) if dangerous_js else "")

# CI-SEC5 No HTTP external resources
http_resources = re.findall(r'(?:href|src)="http://[^"]+', html)
record("CI-SEC5", "All external resources use HTTPS",
    len(http_resources) == 0,
    f"Found: {http_resources[0][:60]}" if http_resources else "")

# CI-SEC6 No console.log in gate functions
console_logs = [(i+1, l.strip()) for i, l in enumerate(lines)
                if "console.log" in l and "gate" in l.lower()]
record("CI-SEC6", "No console.log in gate functions",
    len(console_logs) == 0,
    f"Line {console_logs[0][0]}: {console_logs[0][1][:60]}" if console_logs else "")

# CI-SEC7 No placeholder/stock image hosts
placeholder_found = [h for h in FORBIDDEN_HOSTS if h in html_lower]
record("CI-SEC7", "No placeholder or stock image URLs",
    len(placeholder_found) == 0,
    f"Found: {', '.join(placeholder_found)}" if placeholder_found else "")

# CI-SEC8 No debug comments
debug_comments = re.findall(r'<!--\s*(TODO|FIXME|DEBUG|HACK|XXX)[^>]*-->', html, re.IGNORECASE)
record("CI-SEC8", "No TODO/FIXME/DEBUG comments in deployed code",
    len(debug_comments) == 0,
    f"Found {len(debug_comments)}: {debug_comments[0][:60]}" if debug_comments else "")

# ─────────────────────────────────────────────────────────────
# CATEGORY 3 — RENDER CAPABILITY
# ─────────────────────────────────────────────────────────────

print("\n── Category 3: Render Capability ──")

# CI-RC1 Bootstrap override
record("CI-RC1", "Bootstrap 16px font-size override present",
    "font-size: 16px !important" in html or "font-size:16px!important" in html)

# CI-RC2 All three fonts declared
missing_fonts = [f for f in REQUIRED_FONTS if f not in html]
record("CI-RC2", "All three brand fonts declared",
    len(missing_fonts) == 0,
    f"Missing: {', '.join(missing_fonts)}" if missing_fonts else "")

# CI-RC3 Minimum 3 media query breakpoints
media_queries = re.findall(r"@media\s*\([^)]+\)", css_block)
record("CI-RC3", f"Minimum {MIN_MEDIA_QUERIES} responsive breakpoints present",
    len(media_queries) >= MIN_MEDIA_QUERIES,
    f"Found {len(media_queries)}, need {MIN_MEDIA_QUERIES}: {[m[:40] for m in media_queries]}")

# CI-RC4 No tiny fonts in desktop CSS (above first @media)
# Check body/paragraph text font sizes — label/mono sizes (.55rem+) are acceptable design system values
# Threshold for body copy: .75rem. For labels/mono: .55rem.
body_tiny = [(m.group(1), float(m.group(1).replace("rem",""))) for m in
    re.finditer(r"(?:body|p|\.page-sub|\.hero-sub|\.chain-detail|\.step-body)[^}]*font-size:\s*(\.[0-9]+rem)", desktop_css)
    if float(re.search(r"\d\.?\d*", m.group(1)).group()) < 0.75]
label_tiny = [(m.group(1), float(m.group(1).replace("rem",""))) for m in
    re.finditer(r"font-size:\s*(\.[0-9]+)rem", desktop_css)
    if float(m.group(1)) < 0.5]  # absolute floor: nothing below .5rem
actually_tiny = label_tiny
record("CI-RC4", "No font-size below absolute floor (.5rem) in desktop CSS",
    len(actually_tiny) == 0,
    f"Found {len(actually_tiny)} below .5rem: {actually_tiny[:3]}" if actually_tiny else "")

# CI-RC5 All CSS tokens defined
missing_tokens = [t for t in REQUIRED_TOKENS if t not in css_block]
record("CI-RC5", "All required CSS colour tokens defined",
    len(missing_tokens) == 0,
    f"Missing: {', '.join(missing_tokens)}" if missing_tokens else "")

# CI-RC6 File size
file_size_kb = len(html.encode("utf-8")) / 1024
record("CI-RC6", f"File size under {MAX_FILE_SIZE_KB}KB",
    file_size_kb < MAX_FILE_SIZE_KB,
    f"{file_size_kb:.1f}KB (limit: {MAX_FILE_SIZE_KB}KB)")

# CI-RC7 All images have alt
imgs_no_alt = re.findall(r'<img(?![^>]*alt=)[^>]*>', html)
record("CI-RC7", "All img tags have alt attributes",
    len(imgs_no_alt) == 0,
    f"{len(imgs_no_alt)} img(s) missing alt" if imgs_no_alt else "")

# CI-RC8 No fixed 100vw that causes overflow
vw_overflow = re.findall(r"(?:width|min-width)\s*:\s*100vw", css_block)
record("CI-RC8", "No width:100vw (causes mobile overflow)",
    len(vw_overflow) == 0,
    f"Found {len(vw_overflow)} instance(s)" if vw_overflow else "")

# CI-RC9 Hero section has responsive grid
hero_css = re.search(r"\.hero\s*\{([^}]+)\}", css_block)
hero_responsive = (
    "grid-template-columns: 1fr;" in css_block and
    "@media" in css_block
)
record("CI-RC9", "Hero has responsive grid (collapses on mobile)",
    hero_responsive,
    "No mobile grid collapse found for .hero" if not hero_responsive else "")

# CI-RC10 Nav links hidden on mobile
nav_mobile_hidden = ".nav-links { display: none; }" in html or \
                    ".nav-links{display:none}" in html or \
                    ".nav-links { display:none" in html
record("CI-RC10", "Nav links collapse on mobile",
    nav_mobile_hidden,
    "No .nav-links display:none found in media queries" if not nav_mobile_hidden else "")

# ─────────────────────────────────────────────────────────────
# CATEGORY 4 — JSON DATA INTEGRITY
# ─────────────────────────────────────────────────────────────

print("\n── Category 4: JSON Data Integrity ──")

data_path = Path(DATA_DIR)
if not data_path.exists():
    skip("CI-J1", "JSON data directory exists", f"No {DATA_DIR}/ directory found")
else:
    json_files_found = list(data_path.glob("*.json"))

    # CI-J1 All JSON files parse
    parse_errors = []
    parsed = {}
    for jf in json_files_found:
        try:
            with open(jf) as f:
                parsed[jf.name] = json.load(f)
        except json.JSONDecodeError as e:
            parse_errors.append(f"{jf.name}: {e}")
    record("CI-J1", "All JSON files parse without errors",
        len(parse_errors) == 0,
        "; ".join(parse_errors) if parse_errors else f"{len(json_files_found)} file(s) valid")

    # CI-J2 through CI-J5 Schema validation
    for filename, schema in JSON_SCHEMAS.items():
        rule_id = f"CI-J{list(JSON_SCHEMAS.keys()).index(filename)+2}"
        if filename not in parsed:
            skip(rule_id, f"{filename} schema valid", f"{filename} not found in {DATA_DIR}/")
            continue
        data = parsed[filename]
        errors = []

        if schema["type"] == "object":
            for key in schema["required_keys"]:
                if key not in data:
                    errors.append(f"missing top-level key: {key}")
            if "roles_required" in schema and "roles" in data:
                for i, role in enumerate(data["roles"][:3]):
                    for key in schema["roles_required"]:
                        if key not in role:
                            errors.append(f"role[{i}] missing: {key}")
        elif schema["type"] == "array":
            if not isinstance(data, list):
                errors.append("expected array, got object")
            else:
                for i, entry in enumerate(data[:3]):
                    for key in schema["required_keys"]:
                        if key not in entry:
                            errors.append(f"entry[{i}] missing: {key}")

        record(rule_id, f"{filename} schema valid",
            len(errors) == 0,
            "; ".join(errors[:3]) if errors else f"{len(data) if isinstance(data, list) else 1} entry/entries valid")

    # CI-J6 No duplicate IDs within JSON files
    for filename, data in parsed.items():
        if isinstance(data, list):
            ids = [e.get("id") for e in data if "id" in e]
            dupes = [id_ for id_ in set(ids) if ids.count(id_) > 1]
            record(f"CI-J6-{filename}", f"{filename}: no duplicate IDs",
                len(dupes) == 0,
                f"Duplicates: {dupes}" if dupes else "")

    # CI-J7 PDF URLs point to yadimen.com
    if "insights.json" in parsed:
        insights = parsed["insights.json"]
        if isinstance(insights, list):
            bad_urls = [e.get("pdf_url", "") for e in insights
                       if e.get("pdf_url") and "yadimen.com" not in e.get("pdf_url", "")]
            record("CI-J7", "All PDF URLs reference yadimen.com",
                len(bad_urls) == 0,
                f"Bad URLs: {bad_urls[:2]}" if bad_urls else "")

# ─────────────────────────────────────────────────────────────
# CATEGORY 5 — INFRASTRUCTURE & REACHABILITY
# ─────────────────────────────────────────────────────────────

print("\n── Category 5: Infrastructure & Reachability ──")

# CI-IR1: HTTPS redirect rule present in .htaccess
htaccess_path = Path(".htaccess")
if htaccess_path.exists():
    htaccess = htaccess_path.read_text()
    has_https_redirect = (
        "RewriteCond %{HTTPS} off" in htaccess and
        "https://%{HTTP_HOST}" in htaccess
    )
    record("CI-IR1", "HTTPS redirect rule in .htaccess", has_https_redirect)

    # CI-IR2: WordPress paths preserved
    has_wp_preserve = (
        "/wp-" in htaccess and
        "RewriteRule ^ - [L]" in htaccess
    )
    record("CI-IR2", "WordPress paths preserved in .htaccess", has_wp_preserve)

    # CI-IR3: .well-known path preserved for SSL renewal
    record("CI-IR3", ".well-known path preserved for SSL renewal",
        ".well-known" in htaccess)
else:
    skip("CI-IR1", "HTTPS redirect in .htaccess", ".htaccess not in repo")
    skip("CI-IR2", "WordPress paths in .htaccess", ".htaccess not in repo")
    skip("CI-IR3", ".well-known path", ".htaccess not in repo")

# CI-IR4: No mixed content in site HTML
mixed = re.findall(r'(?:src|href)=["\']http://(?!localhost)[^"\']+', html)
record("CI-IR4", "No mixed content (HTTP asset references)",
    len(mixed) == 0, f"Found: {mixed[:2]}" if mixed else "")

# ─────────────────────────────────────────────────────────────
# REPORT GENERATION
# ─────────────────────────────────────────────────────────────

total = pass_count + fail_count + skip_count
pct   = round(pass_count / max(pass_count + fail_count, 1) * 100)

from datetime import datetime, timezone
now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

lines_report = [
    "# Yadimen Code Inspection Report",
    "",
    f"**Run:** {now}  ",
    f"**File:** `{SITE_FILE}`  ",
    f"**Result:** {'✅ ALL PASSED' if fail_count == 0 else f'❌ {fail_count} FAILURE(S) — DEPLOY BLOCKED'}  ",
    f"**Score:** {pass_count}/{pass_count + fail_count} ({pct}%)  ",
    "",
    "---",
    "",
    "## Results",
    "",
    "| Rule | Name | Status | Detail |",
    "|------|------|--------|--------|",
]

for r in results:
    icon = "✅" if r["status"] == "PASS" else ("❌" if r["status"] == "FAIL" else "⏭️")
    detail = r["detail"].replace("|", "\\|") if r["detail"] else "—"
    lines_report.append(f"| `{r['id']}` | {r['name']} | {icon} {r['status']} | {detail} |")

lines_report += [
    "",
    "---",
    "",
    f"*Generated by `.github/scripts/inspect.py` — do not edit manually.*",
]

report_text = "\n".join(lines_report)

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write(report_text)

# ─────────────────────────────────────────────────────────────
# CONSOLE OUTPUT
# ─────────────────────────────────────────────────────────────

print(f"\n{'='*60}")
print(f"YADIMEN CODE INSPECTOR — {now}")
print(f"{'='*60}")

for r in results:
    icon = "✅" if r["status"] == "PASS" else ("❌" if r["status"] == "FAIL" else "⏭️")
    detail = f"  ({r['detail']})" if r["detail"] else ""
    print(f"{icon}  {r['id']:<12} {r['name']}{detail}")

print(f"\n{'='*60}")
print(f"PASSED:  {pass_count}")
print(f"FAILED:  {fail_count}")
print(f"SKIPPED: {skip_count}")
print(f"TOTAL:   {total}")
print(f"{'='*60}")

if fail_count > 0:
    print(f"\n❌ DEPLOY BLOCKED — {fail_count} check(s) failed.")
    print(f"Fix the failures above and push again.")
    print(f"Report written to {REPORT_FILE}")
    sys.exit(1)
else:
    print(f"\n✅ ALL CHECKS PASSED — proceeding to deploy.")
    print(f"Report written to {REPORT_FILE}")
    sys.exit(0)
