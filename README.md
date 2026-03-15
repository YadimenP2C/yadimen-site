# Yadimen Site

Deployment pipeline for yadimen.com.

## Structure

```
site/
  yadimen-site.html     ← full single-file site (edit this)
compass/
  compass-public.json   ← Compass data (PUBLIC fields only)
.github/
  workflows/
    deploy.yml          ← auto-deploys on push to main
```

## How it works

Push to `main` → GitHub Action fires → curl to WP REST API → live on yadimen.com.

**Site HTML** updates WordPress page ID 2496 (front page).  
**Compass JSON** uploads to WordPress media.

Typical deploy time: ~15 seconds.

## Secrets required

Set these in GitHub → Settings → Secrets → Actions:

| Secret | Value |
|--------|-------|
| `WP_USER` | `admin@yadimen` |
| `WP_APP_PASSWORD` | `waYN qKvV p6fD Q6nk KCWV 0FI3` |

## Local test (optional)

```bash
curl -u "admin@yadimen:waYN qKvV p6fD Q6nk KCWV 0FI3" \
  https://yadimen.com/wp-json/wp/v2/users/me
```
