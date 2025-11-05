"""
基础模型类

提供所有数据模型的基础功能和通用字段。
"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
from dataclasses import dataclass, field, asdict


@dataclass
class BaseModel:
    """
    基础模型类
    
    所有数据模型应继承此类，提供通用的序列化和验证功能。
    
    Examples:
        >>> class User(BaseModel):
        ...     id: str
        ...     name: str
        >>> user = User(id="123", name="John")
        >>> user.to_dict()
        {'id': '123', 'name': 'John'}
    """
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        
        Returns:
            包含所有字段的字典
        """
        return asdict(self)
    
    def to_json(self) -> str:
        """
        转换为 JSON 字符串
        
        Returns:
            JSON 格式的字符串
        """
        import json
        return json.dumps(self.to_dict(), default=str, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        从字典创建实例
        
        Args:
            data: 字典数据
            
        Returns:
            模型实例
        """
        return cls(**data)


@dataclass
class TimestampMixin:
    """
    时间戳混入类
    
    提供创建时间和更新时间字段。
    
    Examples:
        >>> @dataclass
        ... class User(BaseModel, TimestampMixin):
        ...     id: str
        ...     name: str
        >>> user = User(id="123", name="John")
        >>> user.created_at is not None
        True
    """
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    
    def touch(self):
        """更新 updated_at 字段为当前时间"""
        self.updated_at = datetime.now(timezone.utc)

