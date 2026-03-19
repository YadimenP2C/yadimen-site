# CLAUDE.md — Current Task Brief
<!-- Repo: YadimenP2C/yadimen-site -->
<!-- Local path: C:\Users\BG\OneDrive\Documents\GitHub\yadimen-site -->

---

## ⚠️ EMERGENCY — Two critical issues. Run BOTH in parallel.

---

## TASK 1 — IR-0: Fix SSL certificate (DO FIRST, highest priority)

**Goal:** `https://yadimen.com` loads with valid SSL. No ERR_CERT_AUTHORITY_INVALID.
`curl -I https://yadimen.com` returns HTTP/2 200.

**Root cause:** `.htaccess` we deployed broke SSL chain on Network Solutions WordPress hosting.

**Steps:**
1. Get current `.htaccess` from repo root
2. Replace entire content with:

```
# Force HTTPS — before anything else
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteCond %{REQUEST_URI} !^/\.well-known/
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Never intercept WordPress core paths
RewriteCond %{REQUEST_URI} ^/wp- [NC]
RewriteRule ^ - [L]

# Serve our static site for all other requests
DirectoryIndex index.html index.php

# WordPress fallback
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^ index.php [L]
```

3. Run `python .github/scripts/inspect.py` — must pass
4. Commit: `fix: htaccess SSL preservation — resolves ERR_CERT and FortiGuard block`
5. Push to main
6. Wait 45s for deploy
7. Run: `curl -I https://yadimen.com` — confirm HTTP/2 200
8. Run: `curl -I http://yadimen.com` — confirm 301 redirect to https

**STOP AFTER 2 FAILED ATTEMPTS — report to PO**

---

## TASK 2 — IR-2: Add Infrastructure & Reachability checks to inspect.py

**Goal:** inspect.py checks SSL and HTTPS redirect on every deploy. Blocks deploy if broken.
Run AFTER Task 1 is verified working.

**Steps:**
1. Open `.github/scripts/inspect.py`
2. Add new Category 5 section before the report generation block:

```python
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
    ok("CI-IR1", "HTTPS redirect rule in .htaccess", has_https_redirect)

    # CI-IR2: WordPress paths preserved
    has_wp_preserve = (
        "/wp-" in htaccess and
        "RewriteRule ^ - [L]" in htaccess
    )
    ok("CI-IR2", "WordPress paths preserved in .htaccess", has_wp_preserve)

    # CI-IR3: .well-known path preserved for SSL renewal
    ok("CI-IR3", ".well-known path preserved for SSL renewal",
        ".well-known" in htaccess)
else:
    skip("CI-IR1", "HTTPS redirect in .htaccess", ".htaccess not in repo")
    skip("CI-IR2", "WordPress paths in .htaccess", ".htaccess not in repo")
    skip("CI-IR3", ".well-known path", ".htaccess not in repo")

# CI-IR4: No mixed content in site HTML
mixed = re.findall(r'(?:src|href)=["\']http://(?!localhost)[^"\']+', html)
ok("CI-IR4", "No mixed content (HTTP asset references)",
    not mixed, f"Found: {mixed[:2]}" if mixed else "")
```

3. Run `python .github/scripts/inspect.py` — all new CI-IR checks must pass
4. Commit: `ci: add Category 5 Infrastructure & Reachability checks to inspect.py`
5. Push to main

**STOP AFTER 2 FAILED ATTEMPTS — report to PO**

---

## TASK 3 — UX Pipeline: Build Phase 1 automated baseline

**Goal:** Single command `bash tests/ux-pipeline/run.sh` runs Lighthouse + Pa11y against
`https://yadimen.com` and outputs dated JSON reports to `tests/ux-pipeline/reports/`.
Run AFTER Tasks 1 and 2 are complete.

**Steps:**
1. Create folder structure: `tests/ux-pipeline/`
2. Create `tests/ux-pipeline/package.json`:
```json
{
  "name": "yadimen-ux-pipeline",
  "version": "1.0.0",
  "scripts": {
    "lighthouse": "lighthouse https://yadimen.com --output json --output-path ./reports/lighthouse-$(date +%Y%m%d).json --chrome-flags=\"--headless --no-sandbox\"",
    "pa11y": "pa11y https://yadimen.com --reporter json > ./reports/a11y-$(date +%Y%m%d).json"
  },
  "devDependencies": {
    "lighthouse": "^12.0.0",
    "pa11y": "^8.0.0"
  }
}
```
3. Create `tests/ux-pipeline/run.sh`:
```bash
#!/bin/bash
set -e
DATE=$(date +%Y%m%d)
mkdir -p reports
echo "Running Lighthouse..."
npx lighthouse https://yadimen.com \
  --output json \
  --output-path ./reports/lighthouse-$DATE.json \
  --chrome-flags="--headless --no-sandbox" \
  --quiet
echo "Running Pa11y accessibility audit..."
npx pa11y https://yadimen.com \
  --reporter json > ./reports/a11y-$DATE.json
echo "Done. Reports in ./reports/"
ls -la reports/
```
4. Add `tests/ux-pipeline/reports/` to `.gitignore` (reports are local artifacts)
5. Run: `cd tests/ux-pipeline && npm install && bash run.sh`
6. Confirm both JSON files created in reports/
7. Commit: `test: add UX pipeline Phase 1 — Lighthouse + Pa11y baseline`
8. Push to main

**STOP AFTER 2 FAILED ATTEMPTS — report to PO**

---

## Do NOT touch
- `wp-config.php` or any WordPress core files
- `site/index.html` (no design changes in this task)
- Any file with dates before 2025 on the server

## Verify all three tasks done:
- Task 1: `curl -I https://yadimen.com` → HTTP/2 200
- Task 2: `python .github/scripts/inspect.py` → 43/43 passed (4 new IR checks)
- Task 3: `tests/ux-pipeline/reports/` contains lighthouse + a11y JSON files

## Last Updated
March 2026 — Emergency SSL fix + IR checks + UX pipeline Phase 1
