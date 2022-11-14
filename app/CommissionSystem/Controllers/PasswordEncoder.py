import hashlib
import os
from . import Env


class PasswordEncoder:

    @classmethod
    def generate_salt(cls) -> bytes:
        return os.urandom(32)

    @classmethod
    def encode(cls, plain_password: str, salt: bytes):
        return hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000)

    @classmethod
    def verify(cls, plain_password: str, encoded_password: bytes, salt: bytes):
        encoded_attempt: bytes = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000)
        return encoded_attempt == encoded_password
