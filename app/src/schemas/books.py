from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field, ConfigDict, field_validator
from pydantic.alias_generators import to_camel
import uuid

from app.src.entity import enums


class BookResponse(BaseModel):
    book_id: uuid.UUID
    title: str = Field(max_length=250, description="Назва книги")
    author: str = Field(max_length=100, description="Автор книги")
    original_title: Optional[str] = Field(
        max_length=250, description="Оригінальна назва книги"
    )
    genre: enums.GenreEnum = Field(description="Жанр книги")
    categories: List[enums.CategoriesEnum] = Field(
        description="Масив цільових аудиторій книги"
    )
    target_ages: List[enums.TargetAgesEnum] = Field(
        description="Масив цільових вікових груп"
    )
    series: Optional[str] = None
    publisher: Optional[str] = Field(
        max_length=200, description="Видавництво, що випустило книгу"
    )
    publication_year: Optional[int]
    book_type: List[enums.BookTypeEnum] = Field(description="Типи книги в наявності")
    page_count: Optional[int] = Field(description="Кількість сторінок у книзі")
    paper_type: Optional[enums.PaperTypeEnum] = Field(description="Тип паперу")
    language: enums.LanguageEnum = Field(description="Мова перекладу або тексту книги")
    original_language: enums.LanguageEnum = Field(description="Мова оригіналу книги")
    translator: Optional[str] = Field(
        max_length=100, description="Особа, яка перекладала"
    )
    cover_type: Optional[enums.CoverTypeEnum] = Field(
        description="Тип обкладинки книги"
    )
    weight: Optional[float] = Field(description="Вага книги в грамах")
    dimensions: Optional[str] = Field(
        max_length=20,
        description="Розміри книги у форматі 'ширина x висота' в міліметрах",
    )
    isbn: Optional[str] = Field(
        max_length=50, description="Міжнародний стандартний номер книги"
    )
    article_number: Optional[str] = Field(
        max_length=50,
        description="Артикул або внутрішній ідентифікатор книги",
    )
    price: float = Field(ge=0, description="Ціна книги в гривні")
    actual_price: float = Field(
        ge=0, description="Ціна книги в гривні з урахуванням знижки"
    )
    discount: float = Field(
        ge=0, le=1, description="Знижка на книгу (0.0 <= коеф <= 1.0)"
    )
    stock_quantity: int = Field(
        ge=0, description="Кількість книг на складі, доступних для продажу (>= 0)"
    )
    description: Optional[str] = Field(
        max_length=1500, description="Короткий або детальний опис книги"
    )
    images: Optional[List[str]] = Field(
        description="Масив URL-адрес до фотографій книги"
    )
    reviews: Optional[List] = Field(
        description="Масив відгуків юзерів і критиків про книгу"
    )
    is_bestseller: bool = Field(description="Чи є книга бестселером?")
    is_publish: bool = Field(description="Чи доступна книга для продажу?")
    is_gifted: bool = Field(description="Чи подарункове видання?")
    is_available: bool = Field(description="Чи доступна для продажу?")
    # Кількість проданих книг за весь час продажів (необов’язкове)
    total_sales: Optional[int] = None
    # Масив замовлень, де присутня ця книга
    orders: Optional[List[str]] = None
    created_at: datetime = Field(description="Дата створення запису про книгу")
    updated_at: datetime = Field(description="Дата останнього оновлення запису")
    rate: float = Field(ge=0, le=5, description="Середня оцінка відгуків по книзі")

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class BookPaginationResponse(BaseModel):
    total_books: int
    total_pages: int
    current_page: int
    size: int
    books: List[BookResponse]

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class BookFilterParams(BaseModel):
    author: Optional[str] = Field(default=None, description="Фільтр за ім'ям автора")
    title: Optional[str] = Field(default=None, description="Фільтр за назвою книги")
    genre: Optional[str] = Field(default=None, description="Фільтр за жанром книги")
    paper_type: Optional[str] = Field(
        default=None, description="Фільтр за типом паперу"
    )
    language: Optional[str] = Field(
        default=None,
        description="Фільтр за мовою книги",
    )
    cover_type: Optional[str] = Field(
        default=None,
        description="Фільтр типом обкладинки",
    )
    discount_min: Optional[float] = Field(
        None, ge=0, le=1, description="min поріг знижки"
    )
    discount_max: Optional[float] = Field(
        None, ge=0, le=1, description="max поріг знижки"
    )
    actual_price_min: Optional[float] = Field(
        None, ge=0, description="min поріг actual_price"
    )
    actual_price_max: Optional[float] = Field(
        None, ge=0, description="max поріг actual_price"
    )
    created_at_after: Optional[str] = Field(
        None, description="Filter by creation date after"
    )
    created_at_before: Optional[str] = Field(
        None, description="Filter by creation date before"
    )

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )

    @field_validator("created_at_after", "created_at_before", mode="before")
    @classmethod
    def validate_date(cls, value):
        if value is None:
            return value

        if isinstance(value, int) or (
            isinstance(value, str) and value.isdigit() and len(value) == 4
        ):
            return f"{int(value)}-01-01"

        if isinstance(value, str):
            try:
                parsed_date = datetime.strptime(value, "%Y-%m-%d")
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid date format: '{value}'. Use 'YYYY-MM-DD' (e.g., '2024-03-20') or 'YYYY' (e.g., '2000').",
                )

        raise HTTPException(
            status_code=400,
            detail=f"Invalid date type: {type(value).__name__}. Must be string (YYYY-MM-DD) or integer (year).",
        )
