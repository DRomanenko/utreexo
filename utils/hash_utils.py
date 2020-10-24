import base64
from hashlib import sha256


def base64_decode(s: str) -> bytes:
    return base64.standard_b64decode(s)


def base64_encode(s: bytes) -> str:
    return base64.standard_b64encode(s).decode()


def sha256_encode(b: bytes) -> bytes:
    return sha256(b).digest()
