from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel
import uuid

from app.src.entity.enums import UserRole


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=255)


class UserResponse(BaseModel):
    user_id: uuid.UUID
    email: EmailStr = Field(max_length=250)
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(max_length=100)
    phone_number: str = Field(max_length=50)
    date_of_birth: datetime
    address: str = Field(max_length=250)
    city: str = Field(max_length=200)
    postal_code: str = Field(max_length=50)
    country: str = Field(max_length=50)
    role: UserRole
    google_id: Optional[str] = None
    google_access_token: Optional[str] = None
    avatar: str = Field(max_length=255)
    is_active: bool
    # is_confirmed: bool
    favorite_books: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
