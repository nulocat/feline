import base64
import hashlib

from cryptography.fernet import Fernet

from feline.context import context


def get_secret_key() -> str:
    return context.config.secret_key


def base64_key_transformer(secret: str) -> bytes:
    hashed_key: bytes = hashlib.sha256(string=secret.encode()).digest()
    return base64.urlsafe_b64encode(s=hashed_key)

def encrypt(data: str, secret: str|None = None) -> str:
    if secret is None:
        secret = get_secret_key()
    hashed_key: bytes = base64_key_transformer(secret=secret)
    return Fernet(key=hashed_key).encrypt(data=data.encode()).decode()


def decrypt(data: str, secret: str|None = None) -> str:
    if secret is None:
        secret = get_secret_key()
    hashed_key: bytes = base64_key_transformer(secret=secret)
    return Fernet(key=hashed_key).decrypt(token=data.encode()).decode()

