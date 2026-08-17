# Прогресс обучения — appsec-journey

Дневник занятий. Обновляется в конце каждого дня: что закрыл / где затык / что перенёс.
Крупные вехи дублируются в README.md.

**Легенда:** ✅ закрыто · 🔄 в процессе · ⏭ перенесено

---

## Текущая позиция
**Активная практика на живых целях (THM) + подготовка к трудоустройству.**
Трек: AppSec-вход → пентест (пентест-навыки коплю параллельно).
Закрыто: костяк веб-уязвимостей (Фаза 2), Linux privilege escalation (10 векторов),
8+ машин самостоятельно (включая многоступенчатый pivoting).
🔄 Сейчас: TryHackMe Jr Penetration Tester path (Nmap, Metasploit) + упаковка портфеля.
Отклики на AppSec-стажировки отправлены (Астра, hh.ru), резюме под AppSec готово + 2 write-up машин.
Осталось хвостами: deserialization RCE (gadget chains), Неделя 8 (misconfig/crypto/STRIDE),
экзамен Фазы 2, Фаза 3 (API), Фаза 4 (SAST/DAST-инструменты).

---

## Вехи (быстрый обзор)
- ✅ Экзамен Фазы 1 — 4/5
- ✅ Костяк веб-уязвимостей руками: BAC, SQLi, cmd injection, XSS, CSRF, auth, десериализация
- ✅ ~29 лабораторных PortSwigger
- ✅ 4 write-up (JWT×2, SQLi, XSS) + IDOR-скрипт на Python
- ✅ Mock-интервью пройден -> вердикт «подавать»
- ✅ 3 резюме (МТС-стажёр / DevSecOps / AppSec Engineer) + сопроводительное
- ✅ Старт практики на живых целях: TryHackMe (12 комнат, 2 самостоятельные машины)
- ✅ recon-чеклист + трекеры лаб (labs/)
- ✅ Linux privilege escalation — полная карта (10 векторов), конспект notes/16-linux-privesc.md
- ✅ 8+ машин самостоятельно (Beach Bar, Ponzi, Infinity Pool, SSTI, Zip Slip и др.)
- ✅ Навыки: reverse shell, pivoting (chisel), SSTI, business logic / race condition, YAML RCE
- ✅ 2 write-up машин (Infinity Pool, Beach Bar) — цепочки с CWE и защитой
- ✅ Резюме под AppSec + сопроводительное + hh-профиль, отклики отправлены

---

## Журнал

### Фаза 0 — Окружение
- ✅ Kali VM, Docker, Juice Shop, аккаунты (PortSwigger/THM/HTB)
- ✅ Репозиторий appsec-journey, структура папок
- ✅ Burp перехватывает трафик (урок: заходить по IP, не localhost; HTTP-прокси, не SOCKS)
- ✅ Чек-поинт: перехват + повтор запроса через Repeater

### Фаза 1 · Неделя 1 — HTTP-механика
- ✅ Запрос/ответ, методы, статус-коды, заголовки
- ✅ Cookie vs токены, жизненный цикл JWT снаружи (выдача -> Authorization: Bearer)
- ✅ Конспект notes/01-http.md

### Фаза 1 · Неделя 2 — JWT
- ✅ Анатомия JWT: header.payload.signature, Base64 != шифрование
- ✅ Подпись и секрет: один серверный секрет, сервер не хранит токены (сверяет на лету)
- ✅ SAST vs DAST: зоны видимости и слепые пятна
- ✅ Рамка Secure SDLC + shift-left, конспект notes/00-secure-sdlc.md
- ✅ Находка: password + totpSecret в payload (CWE-522 / CWE-200)
- ✅ Атака alg:none через jwt_tool + Repeater
- ✅ Атака RS256->HS256 confusion — эксплуатирована на Juice Shop end-to-end
- ✅ Root cause обеих атак: сервер доверяет alg -> фикс allowlist algorithms=["RS256"]
- ✅ Цепочка верификации JWT (6 шагов) -> notes/02-JWT.md
- ✅ Write-up по обеим атакам (jwt-signature-bypass.md, jwt-sensitive-data.md)
- ✅ REST-механика: IDOR, идемпотентность, версионирование -> notes/03-rest-api.md
- ✅ OAuth2/OIDC: делегированный доступ, access vs ID token; атаки redirect_uri, нет state -> notes/04-oauth-oidc.md
- ✅ Сквозной вывод: JWT alg / IDOR id / redirect_uri — один корень (доверие вводу)
- ✅ Мини-проект scripts/idor_baskets.py — подтверждён IDOR на Juice Shop. Урок триажа: скрипт даёт кандидатов, верификацию делает человек.

### Фаза 1 · Экзамен
- ✅ Экзамен Фазы 1 сдан (15 вопросов + разбор кода). Оценка 4/5.
- ✅ Добиты пробелы: HTTP-коды (401/403/404/400), cookie(stateful) vs JWT(stateless), терминология, state в OAuth.
- ✅ Ключевой узел confusion: stateless -> нет памяти о токене -> доверие к alg.

### Фаза 2 · Неделя 3 — Broken Access Control / IDOR / SSRF
- ✅ BAC как категория: 4 подтипа, корень — сломанная авторизация, deny by default
- ✅ IDOR углублённо (чтение vs запись, объектная vs ролевая проверка)
- ✅ Эскалация привилегий: горизонтальная / вертикальная
- ✅ SSRF: механика, метаданные 169.254.169.254, защита (allowlist по финальному IP), blind SSRF
- ✅ PortSwigger #1: Unprotected admin functionality (robots.txt) — solved
- ✅ PortSwigger #2: Unprotected admin, unpredictable URL (JS recon) — solved
- ✅ PortSwigger #3: User role controlled by request parameter (вертикаль) — solved
- ✅ PortSwigger #4: User ID controlled by request parameter (IDOR, горизонталь) — solved
- ✅ Различие руками: IDOR (объект, горизонталь) vs role-подмена (роль, вертикаль)
- ✅ PortSwigger #5: Basic SSRF against local server — solved

### Фаза 2 · Неделя 4 — SQL Injection
- ✅ WHERE hidden data, login bypass (administrator'--), determine columns — solved
- ✅ UNION: finding column with text (3 столбца, текстовый — 2-й) — solved
- ✅ UNION: retrieving data from other tables (creds administrator) — solved. Первая кража данных.
- ✅ Blind boolean (conditional responses) — Intruder Cluster bomb. Освоен Intruder.
- ✅ Blind time-based (pg_sleep + Cluster bomb по времени) — solved.
- ✅ Защита вглубь: параметризация + нюанс структурных частей (ORDER BY -> allowlist), ORM/raw, least privilege
- ✅ Write-up SQLi -> writeups/sqli.md (detection через data-flow source->sink). Третий write-up.
- ✅ Пробелы: CWE-иерархия (CWE-89 не CWE-74), data-flow (где SAST слепнет)

### Фаза 2 · Неделя 5 — Command Injection + intro XSS
- ✅ Command Injection: корень (ввод -> команда ОС), разделители (; | && $()), blind (sleep/OOB)
- ✅ Защита: не звать shell / subprocess массив + shell=False (аналог параметризации), least power
- ✅ OS command injection simple case (;whoami) — solved. Первый RCE.
- ✅ Разбор: куда летит инъекция (код определяет: БД->SQLi, shell->cmd)
- ✅ XSS-парадигма: инъекция в браузер ДРУГОГО юзера, три типа, экранирование по контексту
- ✅ Reflected XSS into HTML, nothing encoded — solved. Первый XSS.
- ✅ Stored XSS into HTML, nothing encoded — solved. Массовость + не нужно действие жертвы.
- ✅ DOM XSS via location.search — solved. Три типа руками.

### Фаза 2 · Неделя 6 — XSS вглубь
- ✅ Impact: кража cookie, действия от имени жертвы; HttpOnly (блокирует ЧТЕНИЕ, не использование)
- ✅ Обход фильтров: blocklist дырявый, event handlers вместо <script>, обфускация
- ✅ CSP: script-src 'self', блок inline; unsafe-inline убивает; nonce/hash — замена
- ✅ Экранирование по контексту: HTML-сущности vs JS (\"); вложенные контексты (</script>)
- ✅ Парсинг: сервер собирает текст -> браузер (HTML-парсер ПЕРВЫМ, потом JS-движок)
- ✅ Валидация (принять/отклонить) vs санитизация (очистить, DOMPurify)
- ✅ Reflected XSS most tags/attributes blocked — solved. Цепочка: Intruder -> body+onresize -> iframe. Сложная.
- ✅ Reflected XSS with SVG markup (animatetransform onbegin) — solved
- ✅ Reflected XSS into JS string (</script> вырыв) — solved
- ✅ Reflected XSS into attribute (вырыв из атрибута) — solved
- ✅ Защита XSS целиком: экранирование по контексту + CSP + HttpOnly + валидация/санитизация
- ✅ Write-up XSS -> writeups/xss.md. Четвёртый write-up.

### Фаза 2 · Неделя 7 — Auth/сессии + CSRF + десериализация
- ✅ CSRF: механика (браузер сам прикладывает cookie), SOP (отправить можно, прочитать ответ нельзя -> слепой)
- ✅ Защита CSRF: токен (случайный, привязан к сессии) vs токен в localStorage+заголовок; связь с OAuth state
- ✅ CRLF-инъекция: \r\n (%0d%0a) разбивает заголовки, внедрение Set-Cookie
- ✅ Разбор сессий: server-side (cookie=ID) vs JWT (данные в токене, подпись != шифрование); браузер — курьер
- ✅ CSRF no defenses (форма + автосабмит) — solved
- ✅ CSRF token depends on method (POST->GET) — solved
- ✅ CSRF token duplicated in cookie (навязал csrf через CRLF + форму) — solved
- ✅ CSRF token tied to csrfKey (CRLF-цепочка: навязать свою валидную пару) — solved. Самая сложная CSRF.
- ✅ CSRF token not tied to session (свой свежий токен) — solved. Токены обновляемые.
- ✅ Username enumeration via different responses — solved
- ✅ Timing-enumeration: логин по времени (хеширование bcrypt/argon2 медленное)
- ✅ 2FA simple bypass (переход минуя ввод кода) — solved
- ✅ 2FA broken logic (подмена username + брутфорс кода) — solved. Логика + брутфорс.
- ✅ Broken brute-force protection IP block (Pitchfork + 1 concurrent) — solved. Порядок-зависимые -> 1 поток.
- ✅ Password reset broken logic (подмена username) — solved. Корень = доверие подконтрольному вводу.
- ✅ Десериализация: сериализация <-> объект, языко-специфичные форматы опасны, восстановление = выполнение кода
- ✅ Modifying serialized objects (b:0->b:1 admin) — solved. Первая десериализация.
- ✅ Modifying serialized data types (i:0 + type juggling обход ==) — solved. PHP == vs ===.
- ⬜ Осталось: deserialization RCE (gadget chains, phpggc)

### Веха — подготовка к трудоустройству
- ✅ Mock-интервью: 6 блоков. Итог 3.3 -> 4.0/5 после закрытия 5 пробелов (SCA, 401, cookie/JWT, fix'ы, FP-триаж). Вердикт: ПОДАВАТЬ.
- ✅ 3 резюме: МТС-стажёр, AppSec/DevSecOps, AppSec Engineer (честные, инфраструктура помечена «в процессе»)
- ✅ Сопроводительное письмо (шаблон + под вакансию)
- ✅ Отклики отправлены (МТС и др.)
- ✅ Урок фильтрации вакансий: цель — стажёр/junior + ядро «веб-уязвимости»; пропускать «опыт 1-2 года», инфраструктуру, не-технические

### Фаза 5 (старт раньше плана) — практика на живых целях (THM)
- ✅ Осознание: лабы дают «названные» уязвимости, реальность — recon-навык (с чего начать)
- ✅ recon-чеклист (notes/recon-checklist.md): mapping -> исходники -> fingerprint -> fuzzing -> классы -> privesc
- ✅ TryHackMe Jr Penetration Tester (в процессе): Nmap, Metasploit, Search Skills, HTTP, Web Basics + intro (12 комнат)
- ✅ Guided Pentest: Web — chaining (связка мелких уязвимостей в critical)
- ✅ МАШИНА Pickle Rick — первая. recon -> креды (HTML+robots) -> RCE -> обход фильтров -> recon ФС -> privesc (sudo -l) -> 3 ингредиента
- ✅ МАШИНА Basic Pentesting — вторая. nmap -> gobuster -> SMB (enum4linux -> staff.txt -> jan/kay) -> Hydra (jan) -> id_rsa kay -> ssh2john+john -> вход kay
- ✅ Инструменты: nmap, gobuster/ffuf, enum4linux, smbclient, Hydra, John the Ripper, Metasploit
- ✅ Сдвиг: уже внутри машины -> путь ИЗНУТРИ (recon ФС, ключи, privesc), не внешний брутфорс

### Фаза 5 (продолжение) — Hacker Holidays + privesc
- ✅ Linux PrivEsc + Arena: полная карта векторов (SUID, writable passwd, sudo escaping,
     cron, PATH hijacking, kernel/DirtyCow, stored passwords, shadow cracking, .so injection, NFS)
- ✅ МАШИНА Beach Bar — YAML deserialization RCE → reverse shell (base64) → пароль в ps aux → root
- ✅ МАШИНА Ponzi Portfolio — business logic, race condition (single-packet) → накрутка баланса
- ✅ МАШИНА Infinity Pool — pivoting: command injection → chisel → watchtower → FreePBX → automation RCE от root
- ✅ МАШИНА SSTI — Node.js template injection → RCE → disk-группа privesc (debugfs)
- ✅ МАШИНА Zip Slip — path traversal через имя файла в архиве
- ✅ Инструменты добавлены: chisel (pivoting), LinEnum/LinPEAS, revshells.com, base64-обёртка
- ✅ Write-up'ы: writeups/infinity-pool.md, writeups/beach-bar.md
- 🔄 THM: поддержание стрика + продвижение по лигам (соревновательный драйвер)

### Трекеры и артефакты
- ✅ labs/portswigger.md — ~29 лаб по темам
- ✅ labs/tryhackme.md — 12 комнат, 2 машины, инструменты
- ✅ notes/recon-checklist.md — методология разведки

---

## Что дальше
Под AppSec-вход (вакансии, куда откликнулся):
- ⬜ Фаза 4 — SAST (Semgrep на своём коде) + ZAP: превратить «готов осваивать» в «начал»
- ⬜ Фаза 3 — безопасность API (BOLA, mass assignment) — релевантно вакансиям
- ⬜ Хвосты Фазы 2: deserialization RCE, Неделя 8 (misconfig/crypto/STRIDE), экзамен Фазы 2

Под пентест-трек (параллельно, драйвер — стрик/лиги THM):
- 🔄 THM Jr Penetration Tester path: Nmap, Metasploit (углубить recon + фреймворк)
- 🔄 Поддержание стрика THM + продвижение по лигам (соревновательная мотивация)
- ⬜ Windows + Active Directory (пробел, обязателен для пентеста): Blue, Windows PrivEsc
- ⬜ eJPT (среднесрочно) — входной пентест-сертификат

Упаковка (поддерживать актуальным):
- 🔄 Write-up'ы по пройденным машинам (2 готовы, добить TakeOver/Ponzi/SSTI)
- ⬜ Конспекты: pivoting/chisel, business logic, разбить 17-ssti (вынести disk/reverse shell)
- ⬜ Опционально: пары vulnerable/fixed кода