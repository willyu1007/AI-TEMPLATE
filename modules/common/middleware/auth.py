"""
基于 JWT 的轻量认证中间件，配合 AI Repo 的 Guardrail 使用。
"""

from __future__ import annotations

import os
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError


@dataclass
class AuthConfig:
    """认证相关配置。"""
    secret_key: str = field(default_factory=lambda: os.environ.get("TEMPLATEAI_AUTH_SECRET", "change-me"))
    algorithm: str = "HS256"
    token_ttl_seconds: int = 3600
    leeway_seconds: int = 30


class AuthError(PermissionError):
    """认证失败时抛出的错误。"""


class AuthMiddleware:
    """
    负责签发/校验 JWT，同时提供权限检查等工具。
    """
    
    def __init__(self, config: Optional[AuthConfig] = None):
        self.config = config or AuthConfig()
        if not self.config.secret_key:
            raise ValueError("Auth secret key cannot be empty")
        self.last_validated: Optional[str] = None
        self.permissions: List[str] = []
        self.token_cache: Dict[str, Dict[str, Any]] = {}
    
    # --- Token helpers -------------------------------------------------
    def issue_token(
        self,
        *,
        user_id: str,
        username: str,
        role: str,
        permissions: Optional[List[str]] = None,
        ttl_seconds: Optional[int] = None,
    ) -> str:
        """签发 JWT，默认带过期时间。"""
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user_id,
            "username": username,
            "role": role,
            "permissions": permissions or [],
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(seconds=ttl_seconds or self.config.token_ttl_seconds)).timestamp()),
            "jti": secrets.token_hex(8),
        }
        token = jwt.encode(payload, self.config.secret_key, algorithm=self.config.algorithm)
        bearer = f"Bearer {token}"
        self.token_cache[bearer] = payload
        return bearer
    
    def _decode_token(self, token: str) -> Dict[str, Any]:
        """内部解码函数，统一处理异常。"""
        if not token.startswith("Bearer "):
            raise AuthError("Authorization header must start with 'Bearer '")
        raw = token.split(" ", 1)[1]
        return jwt.decode(
            raw,
            self.config.secret_key,
            algorithms=[self.config.algorithm],
            options={"require": ["exp", "sub"]},
            leeway=self.config.leeway_seconds,
        )
    
    # --- Public APIs ---------------------------------------------------
    def validate_token(self, token: str) -> bool:
        """只校验是否有效，不返回 payload。"""
        if not token:
            return False
        
        try:
            payload = self._decode_token(token)
        except (ExpiredSignatureError, InvalidTokenError, AuthError):
            return False
        
        self.last_validated = token
        self.token_cache[token] = payload
        return True
    
    def extract_user(self, token: str) -> Optional[Dict[str, Any]]:
        """解析用户信息。"""
        if not token:
            return None
        
        try:
            payload = self._decode_token(token)
        except InvalidTokenError:
            return None
        
        user_id = payload.get("sub") or payload.get("user_id")
        if not user_id:
            return None
        user = {
            "user_id": user_id,
            "username": payload.get("username"),
            "permissions": payload.get("permissions", []),
            "role": payload.get("role"),
        }
        self.token_cache[token] = payload
        return user
    
    def set_permissions(self, permissions: List[str]):
        """设置当前上下文的权限集合。"""
        self.permissions = permissions
    
    def check_permission(self, permission: str) -> bool:
        """权限检查。"""
        return permission in self.permissions
    
    def refresh_token(self, token: str) -> Optional[str]:
        """根据旧 token 的 payload 生成一个新的 token。"""
        payload = self.token_cache.get(token)
        if payload is None:
            payload = self.extract_user(token)
        if payload is None:
            return None
        
        user_id = payload.get("sub") or payload.get("user_id")
        if not user_id:
            return None
        return self.issue_token(
            user_id=user_id,
            username=payload.get("username", ""),
            role=payload.get("role", "user"),
            permissions=payload.get("permissions", []),
        )
    
    def logout(self, token: str):
        """移除缓存中的 token 记录。"""
        self.token_cache.pop(token, None)
        self.last_validated = None
        self.permissions = []


_default_auth = AuthMiddleware()


def get_current_user(token: Optional[str] = None) -> Optional[dict]:
    """
    提供与旧接口兼容的 helper，内部使用默认的 AuthMiddleware。
    """
    if not token:
        return None
    return _default_auth.extract_user(token)


def _resolve_token_from_args(*args, **kwargs) -> Optional[str]:
    token = kwargs.get("token")
    if token:
        return token
    if args:
        candidate = getattr(args[0], "headers", None)
        if candidate:
            return candidate.get("Authorization")
    return None


def require_auth(func: Callable) -> Callable:
    """
    装饰器，确保函数执行前已经通过认证，并将 `current_user` 注入 kwargs。
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = _resolve_token_from_args(*args, **kwargs)
        user = get_current_user(token)
        if user is None:
            raise AuthError("Unauthorized request")
        # 避免把 token 透传到业务函数
        if "token" in kwargs:
            kwargs.pop("token")
        kwargs["current_user"] = user
        return func(*args, **kwargs)
    
    return wrapper
