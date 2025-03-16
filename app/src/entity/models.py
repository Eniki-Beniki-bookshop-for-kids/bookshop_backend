import uuid
import enum
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

from app.src.entity.enums import UserRole

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    author = Column(String, index=True, nullable=False, default="Unknown")
    title = Column(String, index=True, nullable=False)
    price = Column(Numeric, index=True, nullable=False, default=0.0)
    is_available = Column(Boolean, index=True, nullable=False, default=1)
    stock_quantity = Column(Integer, nullable=False, default=1)
    discount = Column(Numeric(5, 2), index=True, nullable=False, default=0.0)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    age_category = Column(Integer, index=True, nullable=False, default=0)
    description = Column(String(300), nullable=True)

    comments = relationship(
        "Comment", back_populates="book", cascade="all, delete-orphan"
    )

    @validates("price")
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError("Price must be greater than 0")
        return value

    @validates("discount")
    def validate_discount(self, key, value):
        if value < 0 or value > 100:
            raise ValueError("Discount must be between 0 and 100")
        return value

    @validates("age_category")
    def validate_age_category(self, key, value):
        if value < 0:
            raise ValueError("Age category must be greater than 0")
        return value


class Review(Base):
    __tablename__ = "reviews"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    review_text = Column(String, nullable=True)
    rate = Column(Numeric(3, 1), index=True, nullable=False, default=5.0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
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
    address = Column(String(250))
    city = Column(String(200))
    postal_code = Column(String(50))
    country = Column(String(50))
    role = Column(Enum(UserRole), nullable=False, default=UserRole.user)
    google_id = Column(String(255), unique=True, nullable=True)
    google_access_token = Column(String(512), nullable=True)
    avatar = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    password = Column(String(50), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)

    favorite = relationship("Favorite", back_populates="user")
    reviews = relationship("Review", back_populates="user")
