from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class CommentModel(BaseModel):
    book_id: int = Field(gt=0)
    review_text: str = Field(min_length=1, max_length=1000)
    rate: float = Field(gt=0, le=5)


class CommentResponse(CommentModel):
    id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    created_at: datetime
    updated_at: datetime
