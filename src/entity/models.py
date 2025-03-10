from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Numeric,
    Boolean,
    DateTime,
    func,
)
from sqlalchemy.orm import declarative_base, validates, relationship

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    author = Column(String, index=True, nullable=False, default="Unknown")
    title = Column(String, index=True, nullable=False)
    price = Column(Numeric, index=True, nullable=False, default=0.0)
    is_available = Column(Boolean, index=True, nullable=False, default=1)
    stock_quantity = Column(Integer, nullable=True, default=1)
    discount = Column(Numeric(5, 2), index=True, nullable=False, default=0.0)
    created_at = Column(DateTime, default=func.now())
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


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    review_text = Column(String, nullable=True)
    rate = Column(Numeric(3, 1), index=True, nullable=False, default=5.0)
    published_at = Column(DateTime, default=func.now())
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)

    book = relationship("Book", back_populates="comments")

    @validates("rate")
    def validate_rate(self, key, value):
        if value < 0 or value > 5:
            raise ValueError("Rate must be between 0 and 5")
        return value
