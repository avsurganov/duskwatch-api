from typing import TypeVar, Generic, Dict, Any

from pydantic import BaseModel

T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    status: str = 'success'
    data: T


class ErrorResponse(BaseModel):
    status: str
    description: str
    data: Dict[str, Any]
