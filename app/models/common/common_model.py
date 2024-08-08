from typing import TypeVar, Generic, Dict, Any, Optional

from pydantic import BaseModel

T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    status: str = 'success'
    data: T


class OperationResult(BaseModel):
    success: bool


class ErrorResponse(BaseModel):
    status: str
    description: str
    data: Optional[Dict[str, Any]] = None
