import uuid
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Numeric,
    Boolean,
    DateTime,
    func,
    Enum,
)
from sqlalchemy.orm import declarative_base, validates, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.src.entity import enums

Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    category = Column(Enum(enums.CategoriesEnum), nullable=False, index=True)
    book = relationship("Book", back_populates="categories")


class TargetAge(Base):
    __tablename__ = "target_ages"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    target_age = Column(Enum(enums.TargetAgesEnum), nullable=False, index=True)
    book = relationship("Book", back_populates="target_ages")


class BookType(Base):
    __tablename__ = "book_types"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    book_type = Column(Enum(enums.BookTypeEnum), nullable=False, index=True)
    book = relationship("Book", back_populates="book_types")


class Image(Base):
    __tablename__ = "images"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    image_url = Column(String(100), nullable=False, index=True)
    book = relationship("Book", back_populates="book_images")


class Book(Base):
    __tablename__ = "books"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    title = Column(String(250), index=True, nullable=False)
    author = Column(String(100), index=True, nullable=False)
    genre = Column(Enum(enums.GenreEnum), nullable=False, server_default="other_genre")
    categories = relationship(
        "Category", back_populates="book", cascade="all, delete-orphan"
    )
    target_ages = relationship(
        "TargetAge", back_populates="book", cascade="all, delete-orphan"
    )
    book_types = relationship(
        "BookType", back_populates="book", cascade="all, delete-orphan"
    )
    language = Column(Enum(enums.LanguageEnum), nullable=False, index=True)
    original_language = Column(Enum(enums.LanguageEnum), nullable=False, index=True)
    price = Column(Numeric, index=True, nullable=False, default=0.0)
    discount = Column(Numeric(4, 2), index=True, nullable=False, default=0.0)
    stock_quantity = Column(Integer, nullable=False, default=1)
    book_images = relationship(
        "Image", back_populates="book", cascade="all, delete-orphan"
    )
    reviews = relationship(
        "Review", back_populates="book", cascade="all, delete-orphan"
    )
    is_bestseller = Column(Boolean, index=True, nullable=False, default=0)
    is_publish = Column(Boolean, index=True, nullable=False, default=1)
    is_gifted = Column(Boolean, index=True, nullable=False, default=1)

    is_available = Column(Boolean, index=True, nullable=False, default=1)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    book_info = relationship(
        "BookInfo", back_populates="book", uselist=False, cascade="all, delete"
    )

    @validates("price")
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError("Price must be greater than 0")
        return value

    @validates("discount")
    def validate_discount(self, key, value):
        if value < 0 or value > 1:
            raise ValueError("Discount must be between 0 and 1")
        return value


class BookInfo(Base):
    __tablename__ = "books_info"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    original_title = Column(String(250), index=True, nullable=True)
    series = Column(String(200), nullable=True)
    publisher = Column(String(200), nullable=True, index=True)
    publication_year = Column(Integer, nullable=True)
    page_count = Column(Integer, nullable=True)
    paper_type = Column(Enum(enums.PaperTypeEnum), nullable=True, index=True)
    translator = Column(String(100), index=True, nullable=True)
    cover_type = Column(Enum(enums.CoverTypeEnum), nullable=True, index=True)
    weight = Column(Numeric(5, 2), nullable=True)
    dimensions = Column(String(20), nullable=True)
    isbn = Column(String(50), nullable=True, unique=True)
    article_number = Column(String(50), nullable=True)
    description = Column(String(1500), nullable=True)
    book_id = Column(
        UUID(as_uuid=True),
        ForeignKey("books.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    book = relationship("Book", back_populates="book_info")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    review_text = Column(String(2000), nullable=True)
    rate = Column(Numeric(3, 1), index=True, nullable=False, default=5.0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    review_date = Column(DateTime, default=func.now())
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    @validates("rate")
    def validate_rate(self, key, value):
        if value < 0 or value > 5:
            raise ValueError("Rate must be between 0 and 5")
        return value


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    email = Column(String(250), unique=True, index=True, nullable=True)
    username = Column(String(100), index=True, nullable=False)
    first_name = Column(String(100), index=True, nullable=False)
    last_name = Column(String(100), nullable=True)
    phone_number = Column(String(50), unique=True, index=True, nullable=True)
    date_of_birth = Column(DateTime, default=func.now())
    gender = Column(Enum(enums.GenderEnum), nullable=False, server_default="інша")
    address = Column(String(250))
    city = Column(String(200))
    postal_code = Column(String(50))
    country = Column(String(50))
    role = Column(Enum(enums.UserRoleEnum), nullable=False, server_default="user")
    google_id = Column(String(255), unique=True, nullable=True)
    google_access_token = Column(String(512), nullable=True)
    login_method = Column(
        String(20), nullable=False, default="local", server_default="local"
    )
    avatar = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    is_confirmed = Column(Boolean, default=False)

    # favorite = relationship("Favorite", back_populates="user")
    reviews = relationship("Review", back_populates="user")
