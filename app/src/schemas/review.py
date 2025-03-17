from datetime import datetime
import uuid

from pydantic import BaseModel, Field, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel


class ReviewModel(BaseModel):
    book_id: uuid.UUID
    review_text: str = Field(min_length=1, max_length=2000, description="Текст відгуку")
    rate: float = Field(gt=0, le=5, description="Оцінка відгуку")
    review_date: datetime.utcnow() = Field(description="Дата публікації відгуку")

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class ReviewResponse(ReviewModel):
    id: uuid.UUID
    user_id: uuid.UUID
    review_name: str = Field(description="Ім'я користувача")
    avatar: str = Field(description="Посилання на аватар")
    created_at: datetime = Field(description="Дата створення")
    updated_at: datetime = Field(description="Дата оновлення")
