"""
Utility functions related to security
Providing password hashing and symmetric encryption/decryption capabilities
Default implementation is based on PBKDF2 (for password hashing) and Fernet (AES-128 GCM)
"""

from __future__ import annotations

import base64
import os
import secrets
import hashlib
from dataclasses import dataclass
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken

# PBKDF2 默认配置
PBKDF2_ALGORITHM = "sha256"
PBKDF2_ITERATIONS = 600_000
PBKDF2_SALT_BYTES = 16


def _encode_bytes(data: bytes) -> str:
    """将字节序列做 url-safe 的 base64 编码。"""
    return base64.urlsafe_b64encode(data).decode("utf-8")


def _decode_bytes(data: str) -> bytes:
    """与 `_encode_bytes` 相反的动作。"""
    return base64.urlsafe_b64decode(data.encode("utf-8"))


def hash_password(password: str, *, salt: Optional[bytes] = None, iterations: int = PBKDF2_ITERATIONS) -> str:
    """
    使用 PBKDF2-SHA256 为密码生成强哈希，返回格式:
    `pbkdf2_sha256$<iterations>$<salt>$<hash>`
    """
    if not isinstance(password, str) or not password:
        raise ValueError("Password must be a non-empty string")
    
    if salt is None:
        salt = secrets.token_bytes(PBKDF2_SALT_BYTES)
    elif isinstance(salt, str):
        salt = _decode_bytes(salt)
    
    dk = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM,
        password.encode("utf-8"),
        salt,
        iterations,
    )
    return f"pbkdf2_sha256${iterations}${_encode_bytes(salt)}${_encode_bytes(dk)}"


def verify_password(password: str, hashed_password: str) -> bool:
    """验证密码是否与 PBKDF2 哈希匹配。"""
    if not hashed_password:
        return False
    
    try:
        scheme, iterations, salt, digest = hashed_password.split("$")
        if scheme != "pbkdf2_sha256":
            raise ValueError("Unsupported scheme")
        recalculated = hash_password(password, salt=salt, iterations=int(iterations))
        return secrets.compare_digest(recalculated, hashed_password)
    except (ValueError, TypeError):
        return False


@dataclass
class EncryptionContext:
    """包装 Fernet key 的 helper，避免重复推导。"""
    key: bytes

    @classmethod
    def from_secret(cls, secret: Optional[str] = None) -> "EncryptionContext":
        # 尝试从环境变量读取
        secret = secret or os.environ.get("TEMPLATEAI_ENCRYPTION_KEY")
        if secret is None:
            raise ValueError("Missing encryption key. Set TEMPLATEAI_ENCRYPTION_KEY or pass `secret`.")
        
        try:
            key_bytes = _decode_bytes(secret)
        except Exception:
            # 兼容直接传入明文，使用 sha256 归一化后转成 Fernet key
            key_bytes = hashlib.sha256(secret.encode("utf-8")).digest()
            key_bytes = base64.urlsafe_b64encode(key_bytes)
        return cls(key=key_bytes)

    def cipher(self) -> Fernet:
        return Fernet(self.key)


def encrypt_data(data: str, *, secret: Optional[str] = None) -> str:
    """
    使用 Fernet 进行加密。secret 可以是 32 bytes 的 base64 key，或任意字符串。
    """
    if not isinstance(data, str):
        raise ValueError("data must be a string")
    
    ctx = EncryptionContext.from_secret(secret)
    token = ctx.cipher().encrypt(data.encode("utf-8"))
    return token.decode("utf-8")


def decrypt_data(encrypted_data: str, *, secret: Optional[str] = None, default: str = "") -> str:
    """
    解密数据，失败时返回 default。
    """
    if not encrypted_data:
        return default
    
    try:
        ctx = EncryptionContext.from_secret(secret)
        decrypted = ctx.cipher().decrypt(encrypted_data.encode("utf-8"))
        return decrypted.decode("utf-8")
    except (InvalidToken, ValueError):
        return default


