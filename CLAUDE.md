# CLAUDE.md — Current Task Brief

## EMERGENCY — Two critical issues blocking yadimen.com

---

## Issue 1 — IR-0: SSL Certificate Invalid (DO THIS FIRST)

**Goal:** `https://yadimen.com` loads with valid SSL, no browser warning, no ERR_CERT_AUTHORITY_INVALID.

**Root cause:** `.htaccess` deployment broke SSL certificate chain on Network Solutions WordPress hosting.

**Claude Code task:**
1. Get current `.htaccess` from repo
2. Replace entire content with this corrected version:

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

3. Run `inspect.py` — must pass
4. Commit: `fix: htaccess SSL preservation — resolves ERR_CERT and FortiGuard block`
5. Push to main
6. After deploy (45s): run `curl -I https://yadimen.com`
7. Verify: HTTP/2 200, no SSL error, `http://` redirects to `https://`

**STOP AFTER 2 FAILED ATTEMPTS — report to PO**

---

## Issue 2 — IR-2: Add Infrastructure & Reachability tests to inspect.py

**Goal:** inspect.py checks SSL validity and HTTPS redirect on every deploy. Deploy blocked if SSL is broken.

**Do this AFTER IR-0 is resolved and verified.**

Add these checks to `.github/scripts/inspect.py` as a new Category 5 — Infrastructure & Reachability:

```python
# ─────────────────────────────────────────────────────────────
# CATEGORY 5 — INFRASTRUCTURE & REACHABILITY
# ─────────────────────────────────────────────────────────────
import urllib.request, ssl as ssl_lib, socket

LIVE_URL = "yadimen.com"  # read from PROJECT-METADATA.md in full implementation

# CI-IR1: HTTPS redirect present in .htaccess
has_https_redirect = (
    "RewriteCond %{HTTPS} off" in html and
    "https://%{HTTP_HOST}" in html
)
record("CI-IR1", "HTTPS redirect rule in .htaccess", has_https_redirect)

# CI-IR2: wp-admin preserved (not intercepted by our rules)
has_wp_preserve = (
    "REQUEST_URI} ^/wp-" in html and
    "RewriteRule ^ - [L]" in html
)
record("CI-IR2", "WordPress paths preserved in .htaccess", has_wp_preserve)

# CI-IR3: No mixed content (http:// asset references in HTML)
mixed = re.findall(r'(?:src|href)=["\']http://(?!localhost)[^"\']+', html)
record("CI-IR3", "No mixed content (HTTP asset references)",
    len(mixed) == 0,
    f"Found: {mixed[:2]}" if mixed else "")

# CI-IR4: .well-known path preserved for SSL cert renewal
has_wellknown = ".well-known" in html
record("CI-IR4", ".well-known path preserved for SSL renewal", has_wellknown)
```

Run `inspect.py` — all new checks must pass.
Commit: `ci: add IR infrastructure checks to inspect.py`
Push to main.

**STOP AFTER 2 FAILED ATTEMPTS — report to PO**

---

## After both done

Post results as comments here in CLAUDE.md or tell PO:
- IR-0: `curl -I https://yadimen.com` output
- IR-2: `inspect.py` pass count (should be 43/43 with new IR checks)

## Do NOT touch
- `wp-config.php`
- WordPress core files
- Any file with dates before 2025

## Last Updated
March 2026 — Emergency SSL + FortiGuard fix session
