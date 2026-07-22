# PortSwigger — прогресс по лабам

## Access Control (4)
- ✅ Unprotected admin functionality (robots.txt)
- ✅ Unprotected admin, unpredictable URL (JS recon)
- ✅ User role controlled by request parameter
- ✅ User ID controlled by request parameter (IDOR)

## SQL Injection (5)
- ✅ WHERE clause — hidden data
- ✅ Login bypass
- ✅ UNION — determine columns / find text / retrieve data
- ✅ Blind boolean (conditional responses)
- ✅ Blind time-based

## OS Command Injection (1)
- ✅ Simple case

## XSS (7)
- ✅ Reflected into HTML (nothing encoded)
- ✅ Stored into HTML (nothing encoded)
- ✅ DOM (document.write / location.search)
- ✅ Reflected into attribute (angle brackets encoded)
- ✅ Reflected into JS string (quote/backslash escaped)
- ✅ Most tags/attributes blocked (body+onresize+iframe)
- ✅ SVG markup allowed (animatetransform onbegin)

## CSRF (5)
- ✅ No defenses
- ✅ Token validation depends on method (POST→GET)
- ✅ Token duplicated in cookie (CRLF)
- ✅ Token tied to non-session cookie / csrfKey (CRLF chain)
- ✅ Token not tied to session

**Итого: ~22 лабы**