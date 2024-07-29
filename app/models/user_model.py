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

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass
