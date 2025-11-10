"""



"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
from dataclasses import dataclass, field, asdict


@dataclass
class BaseModel:
    """
    
    
    
    
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
        
        
        Returns:
            
        """
        return asdict(self)
    
    def to_json(self) -> str:
        """
         JSON 
        
        Returns:
            JSON 
        """
        import json
        return json.dumps(self.to_dict(), default=str, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        
        
        Args:
            data: 
            
        Returns:
            
        """
        return cls(**data)


@dataclass
class TimestampMixin:
    """
    
    
    
    
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
        """ updated_at """
        self.updated_at = datetime.now(timezone.utc)

