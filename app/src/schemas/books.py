from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
import uuid


class BookResponse(BaseModel):
    book_id: uuid.UUID
    title: str
    author: str
    original_title: str
    genre: str
    categories: List[str]
    target_ages: List[str]
    series: Optional[str] = None
    publisher: str
    publication_year: datetime
    book_type: List[str]
    page_count: int
    paper_type: Optional[str] = None
    language: str
    original_language: str
    translator: Optional[str] = None
    cover_type: str
    weight: int
    dimensions: str
    isbn: str
    article_number: str
    price: float = Field(
        gt=0,
    )
    discount: float
    stock_quantity: int
    description: Optional[str] = None
    images: List[str]
    reviews: Optional[List[str]] = None
    is_bestseller: bool
    is_publish: bool
    is_gifted: bool
    total_sales: Optional[int] = None
    orders: List[str]
    created_at: str
    updated_at: str
    rate: float = Field(ge=0, le=5)

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    class Config:
        from_attributes = True
