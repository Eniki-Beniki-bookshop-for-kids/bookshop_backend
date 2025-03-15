from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=20)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str

    class Config:
        from_attributes = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
