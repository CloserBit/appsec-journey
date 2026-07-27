# appsec-journey

Мой путь подготовки на позицию **AppSec Engineer**: конспекты, secure-coding,
write-up'ы уязвимостей, автоматизация и практика на живых целях. Репозиторий
растёт по мере прохождения роадмапа.

## Цель
Уверенно находить, эксплуатировать и **чинить** топ-уязвимости веб-приложений и API;
понимать их root cause и место в **Secure SDLC**; встраивать SAST/DAST/SCA в CI/CD;
вести триаж и приоритизацию находок с опорой на OWASP и MITRE CWE.

## Методология (для каждой темы)
root cause → механика эксплуатации → обнаружение (SAST/DAST/SCA) → fix в коде →
защита на уровне SSDLC. Каждой уязвимости присваиваю **CWE-ID**.

## Стек и инструменты
Python · Burp Suite · nmap · Metasploit · OWASP ZAP · Nuclei · Semgrep · Trivy · Postman · Docker

## Стандарты-опоры
OWASP: Top 10 (web 2025 / API 2023) · ASVS · Cheat Sheet Series · WSTG · SAMM
MITRE: CWE (в т.ч. CWE Top 25) · CVE · ATT&CK / CAPEC
BSIMM: модель зрелости (обзорно)

## Структура
- `notes/`      — конспекты по темам (HTTP, JWT, OWASP Top 10, CSRF, auth, десериализация)
- `notes/recon-checklist.md` — методология разведки для CTF/THM/HTB
- `code/`       — secure coding: пары «уязвимый ↔ исправленный» на Python
- `scripts/`    — питон-автоматизации для тестов
- `writeups/`   — разборы уязвимостей (шаги, impact, CWE, fix)
- `labs/`       — трекеры практики (PortSwigger, TryHackMe)

## Сквозные треки (идут через все фазы)
- [x] Secure SDLC — где в цикле рождается и где дешевле всего ловится каждая уязвимость
- [x] CWE-маппинг — у каждой находки проставлен CWE-ID (цель: покрыть CWE Top 25)
- [ ] Secure coding (Python) — vulnerable + fixed на каждую уязвимость
- [ ] Стандарты — ASVS/Cheat Sheets как рабочие справочники, обзор MITRE/BSIMM

## Прогресс по фазам
- [x] Фаза 0 — окружение
- [x] Фаза 1 — фундамент: HTTP, JWT (2 атаки), REST/API, IDOR, OAuth/OIDC
- [~] Фаза 2 — веб-уязвимости (OWASP Top 10):
      ✅ Broken Access Control / IDOR · ✅ SQLi (in-band + blind) ·
      ✅ Command injection · ✅ XSS (reflected/stored/DOM + обход фильтров) ·
      ✅ CSRF (+ CRLF-инъекция) · ✅ Auth failures (enumeration, 2FA, brute-force, reset) ·
      ✅ Insecure deserialization (modify objects, type juggling)
      — осталось: deserialization RCE, misconfiguration, crypto failures
- [ ] Фаза 3 — безопасность API
- [ ] Фаза 4 — инструменты AppSec, SSDLC/DevSecOps, стандарты
- [~] Фаза 5 — практика на живых целях: TryHackMe (Jr Penetration Tester, в процессе)

## Артефакты
- **Write-up'ы:** JWT (signature bypass, sensitive data), SQLi, XSS — с root cause, PoC, CWE, fix
- **Практика:** ~33 лаборатории PortSwigger · 10 комнат TryHackMe
- **Скрипты:** автоматизация IDOR-теста (login → перебор id)