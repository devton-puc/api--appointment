from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")

class StatusResponseSchema(BaseModel, Generic[T]):
    code: int
    message: str
    details: Optional[str] = None
    result: Optional[T] = None  
    
    model_config = ConfigDict(from_attributes=True)


