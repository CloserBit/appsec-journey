# Прогресс обучения — appsec-journey

Дневник занятий. Обновляется в конце каждого дня: что закрыл / где затык / что перенёс.
Крупные вехи дублируются в README.md.

**Легенда:** ✅ закрыто · 🔄 в процессе · ⏭ перенесено

---

## Текущая позиция
**Фаза 1** (фундамент) · **Неделя 2** теория закрыта (JWT+API+OAuth), остался мини-проект → потом экзамен Фазы 1.

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
- ⬜ Мини-проект: скрипт login → перебор id (заготовка под IDOR)