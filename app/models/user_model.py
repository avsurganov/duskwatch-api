from datetime import datetime

from pydantic import BaseModel, EmailStr, SecretStr


class LoginRequest(BaseModel):
    email: str
    password: SecretStr


class AuthUser(BaseModel):
    user_id: str
    access_token: str


class RegisterUserRequest(BaseModel):
    email: str
    password: SecretStr


class UserBase(BaseModel):
    email: EmailStr


class UserUpdate(UserBase):
    password: str | None = None


class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass
