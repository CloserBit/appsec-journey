# TryHackMe — трекер комнат

Прогресс по практике на живых целях (recon-методология, инструменты).
Цель: навык поиска уязвимостей на НЕназванных целях (то, что не дают лабы).

**Легенда:** ✅ пройдено · 🔄 в процессе · ⬜ впереди

---

## Путь: Jr Penetration Tester (в процессе)

### Инструменты и recon
- ✅ Nmap — сканирование портов/сервисов (`-sV` версии, `-sC` скрипты, `-p` порты)
- ✅ Metasploit: Introduction — фреймворк эксплуатации
- ✅ Search Skills — поиск эксплойтов/CVE/документации

### Web-фундамент
- ✅ HTTP in Detail — протокол HTTP (запрос/ответ, методы, коды)
- ✅ Web Application Basics — URL, методы, коды, заголовки

### Контекст / основы
- ✅ Inside a Computer System — компоненты системы
- ✅ Defensive Security Intro — оборонительная сторона
- ✅ Offensive Security Intro — наступательная сторона
- ✅ Careers in Cyber — направления в ИБ

### Практика: recon → компрометация
- ✅ Guided Pentest: Web — цепочка recon → уязвимости → компрометация
      (урок: chaining — связка мелких уязвимостей в critical)

## Самостоятельные машины (без walkthrough)
- ✅ **Pickle Rick** — первая машина. Цикл: recon (nmap/gobuster) → креды из
      HTML+robots.txt → RCE (Command Panel) → обход фильтров команд → recon ФС →
      privesc (sudo -l) → 3 ингредиента.
      Уроки: rabbit hole (ловушка), пробелы в путях (кавычки), sudo для privesc.
- ✅ **Basic Pentesting** — вторая машина. Цепочка: nmap → gobuster (/development/) →
      SMB enum (enum4linux → Anonymous share → staff.txt → username jan/kay) →
      SSH брутфорс jan (Hydra) → читаемый id_rsa kay → ssh2john+john (passphrase) →
      вход kay. Освоено: SMB, Hydra, John the Ripper, SSH-ключи.

## Впереди
- ⬜ Web-focused комнаты (применение SQLi/XSS/IDOR на неназванных целях)
- ⬜ OWASP Top 10 room (сверка знаний на практике)
- ⬜ Третья машина (закрепление recon)
- ⬜ Web path (после Jr Pentester)

---

**Итого пройдено: 12 комнат, 2 самостоятельные машины**

## Освоенные инструменты
nmap · gobuster/ffuf · enum4linux · smbclient · Hydra · John the Ripper ·
Metasploit · Burp Suite

## Ключевые уроки практики
- На реальной цели тип уязвимости НЕ назван — recon-методология решает
- Chaining: критичность из связки мелких уязвимостей, не одной большой
- Первый шаг — nmap (порты/версии → CVE); дальше gobuster (скрытые файлы, с `-x`)
- Уже внутри машины → путь дальше ИЗНУТРИ (recon ФС, ключи, privesc), не внешний брутфорс
- Держать recon-checklist под рукой