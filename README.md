# appsec-journey

Мой путь подготовки на позицию **AppSec Engineer**: конспекты, secure-coding,
write-up'ы уязвимостей и автоматизация. Репозиторий растёт по мере прохождения
роадмапа (~4 месяца).

## Цель
Уверенно находить, эксплуатировать и **чинить** топ-уязвимости веб-приложений и API;
понимать их root cause и место в **Secure SDLC**; встраивать SAST/DAST/SCA в CI/CD;
вести триаж и приоритизацию находок с опорой на OWASP и MITRE CWE.

## Методология (для каждой темы)
root cause → механика эксплуатации → обнаружение (SAST/DAST/SCA) → fix в коде →
защита на уровне SSDLC. Каждой уязвимости присваиваю **CWE-ID** и пишу
**vulnerable + fixed** версию на Python.

## Стек и инструменты
Python · Burp Suite · OWASP ZAP · Nuclei · Semgrep · Trivy · Postman · Docker

## Стандарты-опоры
OWASP: Top 10 (web 2025 / API 2023) · ASVS · Cheat Sheet Series · WSTG · SAMM
MITRE: CWE (в т.ч. CWE Top 25) · CVE · ATT&CK / CAPEC
BSIMM: модель зрелости (обзорно)

## Структура
- `notes/`      — конспекты по темам (HTTP, OWASP Top 10, API Security и т.д.)
- `notes/standards/` — разбор OWASP / MITRE / BSIMM
- `code/`       — secure coding: пары «уязвимый ↔ исправленный» на Python
- `scripts/`    — питон-автоматизации для тестов
- `writeups/`   — разборы уязвимостей (шаги, impact, CWE, fix)
- `labs/`       — заметки по лабам (PortSwigger, THM, HTB)

## Сквозные треки (идут через все фазы)
- [ ] Secure SDLC — где в цикле рождается и где дешевле всего ловится каждая уязвимость
- [ ] CWE-маппинг — у каждой находки проставлен CWE-ID (цель: покрыть CWE Top 25)
- [ ] Secure coding (Python) — vulnerable + fixed на каждую уязвимость
- [ ] Стандарты — ASVS/Cheat Sheets как рабочие справочники, обзор MITRE/BSIMM

## Прогресс по фазам
- [x] Фаза 0 — окружение
- [ ] Фаза 1 — фундамент: web + HTTP + API/auth  *(HTTP-часть закрыта)*
- [ ] Фаза 2 — веб-уязвимости (OWASP Top 10 + CWE) + secure coding
- [ ] Фаза 3 — безопасность API
- [ ] Фаза 4 — инструменты AppSec, SSDLC/DevSecOps, стандарты (OWASP/MITRE/BSIMM)
- [ ] Фаза 5 — пентест-практика и портфель