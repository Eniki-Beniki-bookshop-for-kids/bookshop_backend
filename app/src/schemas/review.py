from datetime import datetime
import uuid

from pydantic import BaseModel, Field, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel


class ReviewModel(BaseModel):
    book_id: uuid.UUID
    review_text: str = Field(min_length=1, max_length=1500)
    rate: float = Field(gt=0, le=5)
    review_date: datetime.utcnow()

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class ReviewResponse(ReviewModel):
    id: uuid.UUID
    user_id: uuid.UUID
    review_name: str
    avatar: str
    created_at: datetime
    updated_at: datetime
