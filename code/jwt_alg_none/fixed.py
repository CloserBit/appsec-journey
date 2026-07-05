# ИСПРАВЛЕННАЯ ВЕРСИЯ
import jwt

def verify_token(token: str, public_key: str):
    # FIX: сервер САМ жёстко задаёт разрешённый алгоритм (allowlist).
    # alg из токена вообще не учитывается; none невозможен.
    return jwt.decode(token, public_key, algorithms=["RS256"])