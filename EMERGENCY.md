# Emergency Issues — March 2026

Two critical infrastructure failures blocking all corporate access to yadimen.com.
Both must be resolved before any sprint work continues.

## IR-0 — SSL Certificate Invalid (ERR_CERT_AUTHORITY_INVALID)
**Status:** OPEN — blocks all browser access
**Root cause:** .htaccess deployment broke SSL certificate chain on Network Solutions hosting
**Fix:** You — renew/re-issue SSL in Network Solutions panel OR install Really Simple SSL plugin
**Fix:** Claude Code — update .htaccess with SSL preservation rules

## IR-1 — FortiGuard Malicious Website Classification
**Status:** OPEN — blocks all corporate firewall access
**Root cause:** Invalid SSL triggered FortiGuard malicious site detection
**Fix:** Resolve IR-0 first, then submit reclassification at fortiguard.com/webfilter
**Affects:** Every FS buyer, TA lead, and procurement evaluator behind corporate firewall

## IR-2 — Test Pack Gap: Infrastructure & Reachability
**Status:** OPEN — tests must be added to inspect.py and QA matrix
**Gap:** 700+ tests assumed site was reachable — none tested SSL, blacklists, or firewall classification
**Fix:** Claude Code — add IR test category to inspect.py
