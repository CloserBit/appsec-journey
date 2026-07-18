# Прогресс обучения — appsec-journey

Дневник занятий. Обновляется в конце каждого дня: что закрыл / где затык / что перенёс.
Крупные вехи дублируются в README.md.

**Легенда:** ✅ закрыто · 🔄 в процессе · ⏭ перенесено

---

## Текущая позиция
**Фаза 2 · Неделя 6 — XSS вглубь.** Закрыты: Недели 3 (BAC), 4 (SQLi), 5 (cmd injection + intro XSS: 3 типа руками). Дальше: XSS вглубь → mock-интервью → резюме.

---

## Журнал

### Фаза 0 — Окружение
- ✅ Kali VM, Docker, Juice Shop, аккаунты (PortSwigger/THM/HTB)
- ✅ Репозиторий `appsec-journey`, структура папок
- ✅ Burp перехватывает трафик (урок: заходить по IP, не localhost; HTTP-прокси, не SOCKS)
- ✅ Чек-поинт: перехват + повтор запроса через Repeater

### Фаза 1 · Неделя 1 — HTTP-механика
- ✅ Запрос/ответ, методы, статус-коды, заголовки
- ✅ Cookie vs токены, жизненный цикл JWT снаружи (выдача → `Authorization: Bearer`)
- ✅ Конспект `notes/01-http.md`

### Фаза 1 · Неделя 2 — JWT (в процессе)
- ✅ Анатомия JWT: header.payload.signature, Base64 ≠ шифрование
- ✅ Подпись и секрет: один серверный секрет, сервер не хранит токены (сверяет на лету)
- ✅ SAST vs DAST: зоны видимости и слепые пятна
- ✅ Рамка Secure SDLC + shift-left, конспект `notes/00-secure-sdlc.md`
- ✅ 🚩 Находка: password + totpSecret в payload (CWE-522 / CWE-200) → write-up TODO
- ✅ Атака `alg:none` через jwt_tool + Repeater
- ✅ Атака RS256→HS256 confusion — эксплуатирована на Juice Shop end-to-end (JWKS → JWK→PEM → jwt_tool -X k → data.role:admin → 200 /rest/admin/application-configuration)
- ✅ Root cause обеих атак: сервер доверяет alg → фикс allowlist algorithms=["RS256"]
- ✅ Цепочка верификации JWT (6 шагов) → notes/02-JWT.md
- ✅ Write-up по обеим атакам (jwt-alg-none.md → расширить до signature-bypass)
- ✅ REST-механика: REST/ресурсы/методы, IDOR (root: авторизация на уровне объекта), идемпотентность (POST replay → idempotency-key), версионирование (забытая v1) → notes/03-rest-api.md
- ✅ OAuth2/OIDC: делегированный доступ, access vs ID token (aud);
      атаки: redirect_uri (→allowlist exact match), нет state (→login CSRF), путаница токенов → notes/04-oauth-oidc.md
- ✅ Сквозной вывод: JWT alg / IDOR id / redirect_uri — один корень (доверие вводу) → одна защита (allowlist/серверная сверка)
- ✅ Мини-проект: scripts/idor_baskets.py — login → перебор basket/{id}.
      Подтверждён IDOR на Juice Shop (чужие корзины доступны).
      Урок триажа: скрипт даёт кандидатов (200+тело), верификацию «своё/чужое» делает человек.

### Фаза 1 · Экзамен
- ✅ Экзамен Фазы 1 сдан (15 вопросов + разбор кода). Оценка 4/5.
- ✅ Добиты пробелы: HTTP-коды (401/403/404/400), cookie(stateful) vs JWT(stateless),
      терминология подпись/проверка/кодирование, state в OAuth.
- ✅ Ключевой узел confusion закрыт: stateless → нет памяти о токене → доверие к alg.

### Фаза 2 · Неделя 3 — Broken Access Control / IDOR / SSRF
- ✅ BAC как категория: 4 подтипа (объектный/функциональный/параметр/обход метода), корень — сломанная авторизация, deny by default
- ✅ IDOR углублённо (чтение vs запись, объектная vs ролевая проверка)
- ✅ Эскалация привилегий: горизонтальная / вертикальная
- ✅ SSRF: механика (сервер как прокси в периметр), метаданные 169.254.169.254, защита (allowlist по финальному IP, не по строке URL), blind SSRF, detection
- ✅ PortSwigger #1: Unprotected admin functionality (robots.txt recon) — solved
- ✅ PortSwigger #2: Unprotected admin functionality, unpredictable URL (JS recon) — solved
- ✅ PortSwigger #3: User role controlled by request parameter (роль admin=true, вертикаль) — solved
- ✅ PortSwigger #4: User ID controlled by request parameter (IDOR id=wiener→carlos, горизонталь) — solved
- ✅ Различие руками: IDOR (принадлежность объекта, горизонталь) vs role-подмена (роль, вертикаль)
- ✅ PortSwigger #5: Basic SSRF against local server (stockApi → http://localhost/admin/delete) — solved
- ✅ PortSwigger SQLi: WHERE hidden data, login bypass (administrator'--), determine columns (UNION SELECT NULL×3) — solved
- ✅ PortSwigger SQLi UNION: finding column with text (3 столбца, текстовый — 2-й) — solved
- ✅ PortSwigger SQLi UNION: retrieving data from other tables (вытащил administrator creds, вход) — solved. Первая кража данных через SQLi.
- ✅ PortSwigger SQLi: Blind boolean (conditional responses) — пароль admin через Intruder Cluster bomb. Освоен Intruder (payload positions, sets, Grep Match).
- ✅ PortSwigger SQLi: Blind time-based (time delays + retrieval) — пароль 20 симв. через pg_sleep + Cluster bomb по колонке времени. Solved.
- ✅ Write-up по SQLi → writeups/sqli.md (виды, PoC, защита слоями, detection через data-flow). Третий write-up портфеля.
- ✅ PortSwigger: OS command injection simple case (;whoami в storeId/productId → RCE) — solved
- ✅ PortSwigger: Reflected XSS into HTML context, nothing encoded (<script>alert(1)</script>) — solved. Первый XSS.
- ✅ PortSwigger: Stored XSS into HTML context, nothing encoded — solved. Разница с reflected: массовость + не нужно действие жертвы.
- ✅ PortSwigger: DOM XSS in document.write via location.search ("><script>alert(1)</script>) — solved. Три типа XSS руками.