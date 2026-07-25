# ROADMAP — appsec-journey

Полный план подготовки на AppSec Engineer (~4 месяца, 15 ч/нед).
Карта целиком; ежедневные детали — в [PROGRESS.md](./PROGRESS.md).

**Легенда:** ✅ закрыто · 🔄 в процессе · ⬜ впереди

---

## Фаза 0 — Окружение
- ✅ Kali VM, Docker, Juice Shop, аккаунты PortSwigger/THM/HTB
- ✅ Репозиторий и структура
- ✅ Burp: перехват + Repeater

## Фаза 1 — Фундамент: web + HTTP + API/auth
### Неделя 1 — HTTP-механика
- ✅ Запрос/ответ, методы, статус-коды, заголовки
- ✅ Cookie vs токены, CORS
- ✅ Python `requests` как инструмент
### Неделя 2 — API + аутентификация/сессии (JWT — приоритет)
- ✅ Анатомия JWT, Base64 ≠ шифрование
- ✅ Подпись и секрет, сервер не хранит токены
- ✅ SAST vs DAST, рамка Secure SDLC + shift-left
- ✅ Атаки на JWT: `alg:none`, RS256→HS256 confusion
- ✅ REST, идемпотентность, версионирование; базово OAuth2/OIDC
- ✅ Мини-проект: скрипт login → перебор `id` (заготовка под IDOR)
- ✅ 🎫 Экзамен Фазы 1 (4/5)

## Фаза 2 — Веб-уязвимости (OWASP Top 10 + CWE) + secure coding
- ✅ Неделя 3 — Broken Access Control / IDOR / SSRF (A01)
- ✅ Неделя 4 — SQL Injection (A05)
- ✅ Неделя 5 — Command injection + прочие + intro XSS
- ✅ Неделя 6 — XSS: reflected/stored/DOM + CSP
- ✅ Неделя 7 — Атаки на auth/сессии (A07) + CSRF + десериализация
- ⬜ Неделя 8 — Security Misconfiguration (A02) + Crypto Failures (A04) + Insecure Design + intro threat modeling (STRIDE)
- ⬜ 🎫 Экзамен Фазы 2
- ⬜ Сквозное: на каждую уязвимость — CWE-ID + vulnerable/fixed код

## Фаза 3 — Безопасность API
- ⬜ Неделя 9 — OWASP API Top 10: BOLA/BFLA/BOPLA/mass assignment
- ⬜ Неделя 10 — Postman/Insomnia вглубь, OpenAPI как карта атаки, лаба crAPI/vAPI
- ⬜ Мини-проект: security-проверка API + отчёт
- ⬜ 🎫 Экзамен Фазы 3

## Фаза 4 — Инструменты AppSec + SSDLC/DevSecOps + стандарты
- ⬜ Неделя 11 — SAST: Semgrep, свои правила, true/false positive
- ⬜ Неделя 12 — DAST: ZAP + Nuclei; SCA: Trivy/Grype, SBOM (A03)
- ⬜ Неделя 13 — Процессы: SSDLC/STLC глубоко, триаж и приоритизация; стандарты OWASP/MITRE/BSIMM
- ⬜ Мини-проект (ключевой): уязвимое приложение + CI-пайплайн SAST+DAST+SCA
- ⬜ 🎫 Экзамен Фазы 4

## Фаза 5 — Пентест-практика и портфель
- ⬜ Неделя 14 — TryHackMe (web-путь), добить PortSwigger advanced
- ⬜ Неделя 15 — HackTheBox web-модули/машины
- ⬜ Неделя 16 — Чтение фреймворков (FastAPI/Flask, React/Vue DOM XSS); финальный портфель
- ⬜ 🎫 Финал: mock-интервью

---

## Сквозные треки
- 🔄 Secure SDLC (рамка задана, применяется на каждой теме)
- 🔄 CWE-маппинг (цель: покрыть CWE Top 25)
- ⬜ Secure coding Python (vulnerable + fixed)
- ⬜ Стандарты (ASVS/Cheat Sheets в работе, обзор MITRE/BSIMM)