from datetime import datetime
from typing import Optional, List

from pyasn1.compat.octets import null
from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator
from pydantic.alias_generators import to_camel
import uuid

from app.src.entity import enums


class UserModel(BaseModel):
    username: str = Field(
        min_length=5,
        max_length=100,
        description="Username: Обов'язкове поле",
        example="username",
    )
    email: EmailStr = Field(
        max_length=250,
        description="email: Обов'язкове поле, має бути унікальним",
        example="email@example.com",
    )
    password: str = Field(
        min_length=6,
        max_length=255,
        description="password: Обов'язкове поле",
        example="some_password",
    )
    first_name: str = Field(
        min_length=2,
        max_length=100,
        description="first_name: Обов'язкове поле",
        example="first_name",
    )
    gender: enums.GenderEnum = Field(
        description="gender: Обов'язкове поле",
        example="чоловіча",
    )
    last_name: Optional[str] = Field(
        max_length=100,
        description="last_name: Не обов'язкове поле",
        example="",
        default=None,
    )
    phone_number: Optional[str] = Field(
        max_length=50,
        description="phone_number: Не обов'язкове поле, має бути унікальним",
        example="",
        default=None,
    )
    date_of_birth: Optional[datetime] = Field(
        description="date_of_birth: Обов'язкове поле",
        example=datetime.now().isoformat(),
    )

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )

    @field_validator("last_name", "phone_number")
    @classmethod
    def validate_null(cls, value):
        if not value:
            return None
        return value


class UserResponse(BaseModel):
    user_id: uuid.UUID
    email: EmailStr = Field(max_length=250)
    first_name: str = Field(min_length=2, max_length=100)
    last_name: Optional[str] = Field(max_length=100)
    phone_number: Optional[str] = Field(max_length=50)
    date_of_birth: Optional[datetime]
    gender: enums.GenderEnum
    address: Optional[str] = Field(max_length=250)
    city: Optional[str] = Field(max_length=200)
    postal_code: Optional[str] = Field(max_length=50)
    country: Optional[str] = Field(max_length=50)
    role: enums.UserRoleEnum
    google_id: Optional[str] = None
    # google_access_token: Optional[str] = None
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

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class GoogleUser(BaseModel):
    sub: int
    email: str
    given_name: str
    family_name: str
    picture: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class GoogleResponse(TokenModel):
    user: UserResponse

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )
