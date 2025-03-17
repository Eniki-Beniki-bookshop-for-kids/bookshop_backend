from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
import uuid

from app.src.entity import enums


class BookResponse(BaseModel):
    book_id: uuid.UUID
    title: str = Field(max_length=250, description="Назва книги")
    author: str = Field(max_length=100, description="Автор книги")
    original_title: str = Field(max_length=250, description="Оригінальна назва книги")
    genre: enums.Genre = Field(description="Жанр книги")
    categories: List[enums.Categories] = Field(
        description="Масив цільових аудиторій книги"
    )
    target_ages: List[enums.TargetAges] = Field(
        description="Масив цільових вікових груп"
    )
    series: Optional[str] = None
    publisher: str = Field(
        max_length=200, description="Видавництво, що випустило книгу"
    )
    publication_year: datetime
    book_type: List[enums.BookType] = Field(description="Типи книги в наявності")
    page_count: int = Field(description="Кількість сторінок у книзі")
    paper_type: enums.PaperType = Field(description="Тип паперу")
    language: enums.Language = Field(description="Мова перекладу або тексту книги")
    original_language: enums.Language = Field(description="Мова оригіналу книги")
    translator: str = Field(max_length=100, description="Особа, яка перекладала")
    cover_type: enums.CoverType = Field(description="Тип обкладинки книги")
    weight: float = Field(description="Вага книги в грамах")
    dimensions: str = Field(
        max_length=20,
        description="Розміри книги у форматі 'ширина x висота' в міліметрах",
    )
    isbn: str = Field(max_length=50, description="Міжнародний стандартний номер книги")
    article_number: str = Field(
        max_length=50,
        description="Артикул або внутрішній ідентифікатор книги",
    )
    price: float = Field(gt=0, description="Ціна книги в гривні")
    discount: float = Field(
        gt=0, le=1, description="Знижка на книгу (0.0 <= коеф <= 1.0)"
    )
    stock_quantity: int = Field(
        gt=0, description="Кількість книг на складі, доступних для продажу (>= 0)"
    )
    description: str = Field(
        max_length=1500, description="Короткий або детальний опис книги"
    )
    images: List[str] = Field(description="Масив URL-адрес до фотографій книги")
    reviews: List[str] = Field(description="Масив відгуків юзерів і критиків про книгу")
    is_bestseller: bool = Field(description="Чи є книга бестселером?")
    is_publish: bool = Field(description="Чи доступна книга для продажу?")
    is_gifted: bool = Field(description="Чи подарункове видання?")
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
    )

    class Config:
        from_attributes = True
