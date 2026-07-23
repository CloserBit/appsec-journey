import json, base64
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.primitives import serialization

def b64url_to_int(s):
    return int.from_bytes(base64.urlsafe_b64decode(s + "=" * (-len(s) % 4)), "big")

n = b64url_to_int("JWKS_n")
e = b64url_to_int("AQAB")

pub = RSAPublicNumbers(e, n).public_key()
pem = pub.public_bytes(
    serialization.Encoding.PEM,
    serialization.PublicFormat.SubjectPublicKeyInfo,
)
open("public.pem", "wb").write(pem)
print(pem.decode())