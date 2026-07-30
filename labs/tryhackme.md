# TryHackMe — трекер комнат

Прогресс по практике на живых целях (recon-методология, инструменты).
Цель: навык поиска уязвимостей на НЕназванных целях (то, что не дают лабы).

**Легенда:** ✅ пройдено · 🔄 в процессе · ⬜ впереди

---

## Обучающие комнаты (инструменты, фундамент, методология)

### Инструменты и recon
- ✅ Nmap — сканирование портов/сервисов (`-sV` версии, `-sC` скрипты, `-p` порты)
- ✅ Metasploit: Introduction — фреймворк эксплуатации
- ✅ Search Skills — поиск эксплойтов/CVE/документации

### Web-фундамент
- ✅ HTTP in Detail — протокол HTTP (запрос/ответ, методы, коды)
- ✅ Web Application Basics — URL, методы, коды, заголовки

### Контекст / основы / методология
- ✅ Inside a Computer System — компоненты системы
- ✅ Cyber Kill Chain — фазы атаки (recon → weaponization → delivery → exploitation → installation → C2 → actions)
- ✅ Defensive Security Intro — оборонительная сторона
- ✅ Offensive Security Intro — наступательная сторона
- ✅ Careers in Cyber — направления в ИБ
- ✅ Guided Pentest: Web — цепочка recon → уязвимости → компрометация
      (урок: chaining — связка мелких уязвимостей в critical)

---

## Самостоятельные машины и челленджи (без walkthrough)

### Web + privesc
- ✅ **Pickle Rick** — первая машина. Цикл: recon (nmap/gobuster) → креды из
      HTML+robots.txt → RCE (Command Panel) → обход фильтров команд → recon ФС →
      privesc (sudo -l) → 3 ингредиента.
      Уроки: rabbit hole (ловушка), пробелы в путях (кавычки), sudo для privesc.
- ✅ **Basic Pentesting** — вторая машина. Цепочка: nmap → gobuster (/development/) →
      SMB enum (enum4linux → Anonymous share → staff.txt → username jan/kay) →
      SSH брутфорс jan (Hydra) → читаемый id_rsa kay → ssh2john+john (passphrase) →
      вход kay. Освоено: SMB, Hydra, John the Ripper, SSH-ключи.

### IDOR / логика
- ✅ **Corridor** — IDOR через MD5-хеши id страниц. john расшифровал видимые хеши (числа 1-13),
      понял систему (MD5 от числа), сгенерировал MD5 скрытых (echo -n "N" | md5sum) → страница 0 → флаг.
      Урок: захешированный id = ложная защита (хеш предсказуем).
- ✅ **The Concierge Knows Too Much** — prompt injection

### Cloud (AWS)
- ✅ **Room 404** — cloud эксплуатация. .git на сервере (git-dumper) → исходник с открытым
      Cognito Identity Pool ID + DynamoDB table → анонимные AWS guest-креды (cognito-identity
      get-id → get-credentials) → dynamodb scan → дамп чужих профилей → флаг.
      Освоено: git-dumper, AWS CLI (Cognito/DynamoDB), cloud misconfiguration (широкие права guest-роли).
- ✅ **Complimentary** — cloud read-only keys (приложение раздаёт всем одинаковые cloud-ключи,
      read-only, но доступ к контактам всех гостей).

### DNS / сертификаты / OSINT
- ✅ **TakeOver** — subdomain enumeration через сертификаты. Серт support.futurevera.thm →
      SAN раскрыл скрытый secrethelpdesk934752.support.futurevera.thm (не в словарях) →
      /etc/hosts → curl https → флаг в пути ответа.
      Уроки: серт раскрывает скрытые поддомены (SAN); .thm только через /etc/hosts (не публичный DNS);
      vhost-фаззинг (gobuster vhost / ffuf -H "Host:"), не dns
- ✅ **The Brochure** — OSINT: AI-fingerprint на фото → отслеживание аккаунта

---

## Впереди
- ⬜ Web-focused комнаты (применение SQLi/XSS/IDOR на неназванных целях)
- ⬜ OWASP Top 10 room (сверка знаний на практике)
- ⬜ Следующие машины (закрепление recon, разные типы)
- ⬜ Web path / углубление после Jr Pentester

---

**Итого пройдено: ~19 комнат, из них 8 самостоятельных машин/челленджей**
(web, network, cloud, DNS/сертификаты, OSINT)

## Освоенные инструменты
nmap · gobuster/ffuf · enum4linux · smbclient · Hydra · John the Ripper (+ ssh2john) ·
Metasploit · git-dumper · AWS CLI (Cognito/DynamoDB) · openssl (серты) · dig/host · Burp Suite

## Ключевые уроки практики
- На реальной цели тип уязвимости НЕ назван — recon-методология решает
- Читать НАЗВАНИЕ и цель лабы — они направляют (TakeOver → серты/поддомены, не директории)
- Chaining: критичность из связки мелких уязвимостей, не одной большой
- Первый шаг — nmap (порты/версии → CVE); дальше gobuster (скрытые файлы, с `-x`)
- Уже внутри машины → путь ИЗНУТРИ (recon ФС, ключи, privesc), не внешний брутфорс
- .git на сервере = утечка истории кода (git-dumper → git log --all)
- Сертификаты раскрывают скрытые поддомены (SAN), .thm через /etc/hosts, DNS машины (@IP)
- Cloud: открытые ключи/пулы в клиентском коде → анонимный доступ к облачным данным
- Застрял → смотри writeup на конкретный шаг (учиться на разборе — нормально)
- Держать recon-checklist под рукой