PortSwigger Web Security Academy — трекер лаб

Прогресс по решённым лабораториям. Обновляется по мере прохождения. Формат: тема → лаба → ключевой приём.

Легенда: ✅ решено · 🔄 в процессе · ⬜ впереди

Access Control / IDOR (4)
✅ Unprotected admin functionality — доступ через /robots.txt
✅ Unprotected admin, unpredictable URL — recon через JS
✅ User role controlled by request parameter — подмена роли в параметре
✅ User ID controlled by request parameter — IDOR (подмена id)
SQL Injection (5)
✅ WHERE clause — retrieval of hidden data (' OR 1=1 --)
✅ Login bypass (administrator'--)
✅ UNION — determine number of columns (ORDER BY / UNION SELECT NULL)
✅ UNION — find column with text + retrieve data (UNION SELECT username,password)
✅ Blind — conditional responses (boolean, Intruder Cluster bomb)
✅ Blind — time delays (pg_sleep, CASE WHEN)
OS Command Injection (1)
✅ Simple case (;whoami)
Cross-Site Scripting / XSS (7)
✅ Reflected into HTML context — nothing encoded (<script>alert(1)</script>)
✅ Stored into HTML context — nothing encoded
✅ DOM — document.write / location.search ("><script>)
✅ Reflected into attribute — angle brackets encoded (вырыв из атрибута)
✅ Reflected into JS string — quote/backslash escaped (</script> вырыв)
✅ Most tags/attributes blocked (Intruder перебор → body+onresize+iframe)
✅ SVG markup allowed (animatetransform onbegin)
CSRF (5)
✅ No defenses (форма + автосабмит)
✅ Token validation depends on request method (POST→GET)
✅ Token duplicated in cookie (CRLF-инъекция для установки cookie)
✅ Token tied to non-session cookie / csrfKey (CRLF-цепочка, навязать свою пару)
✅ Token not tied to session (свой валидный свежий токен)
Authentication (5)
✅ Username enumeration via different responses (Intruder, разница ответов)
✅ 2FA simple bypass (переход на пост-2FA страницу минуя код)
✅ 2FA broken logic (подмена username + брутфорс кода)
✅ Broken brute-force protection, IP block (Pitchfork чередование, 1 concurrent)
✅ Password reset broken logic (подмена username в финальном запросе)
Insecure Deserialization (2)
✅ Modifying serialized objects (PHP object в cookie, b:0→b:1)
✅ Modifying serialized data types (type juggling, i:0 обход ==)

Итого решено: ~29 лаб

Впереди (по плану)
⬜ Deserialization — RCE via gadget chains (phpggc)
⬜ API security (BOLA, mass assignment) — Фаза 3
⬜ SSRF, path traversal, file upload
⬜ Advanced: OAuth-атаки, prototype pollution, web cache poisoning