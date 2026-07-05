# НАМЕРЕННО УЯЗВИМЫЙ УЧЕБНЫЙ ПРИМЕР — не использовать в проде
import jwt  # PyJWT

def verify_token(token: str, public_key: str):
    # УЯЗВИМОСТЬ: алгоритм берётся из САМОГО токена (header),
    # т.е. атакующий диктует, как проверять его же токен.
    header = jwt.get_unverified_header(token)
    alg = header["alg"]                      # ← доверие недоверенному вводу
    if alg == "none":                        # ← blocklist, пропустит "NONE"
        return jwt.decode(token, options={"verify_signature": False})
    return jwt.decode(token, public_key, algorithms=[alg])