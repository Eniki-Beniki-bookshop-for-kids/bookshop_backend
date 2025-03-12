from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class CommentModel(BaseModel):
    id: int = Field(gt=0)
    # user_id: int = Field(gt=0)
    book_id: int = Field(gt=0)
    review_text: str = Field(min_length=1, max_length=1000)
    rate: float = Field(gt=0, le=5)
    published_at: datetime

    @field_validator("published_at", mode="before")
    @classmethod
    def validate_published_at(cls, value: datetime) -> datetime:
        if isinstance(value, str):
            value = datetime.fromisoformat(value)
        return value.replace(tzinfo=None) if value.tzinfo else value


class CommentResponse(CommentModel):
    pass
