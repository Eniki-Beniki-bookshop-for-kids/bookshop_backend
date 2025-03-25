import uuid
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, func, select, desc

from app.src.entity.models import Review, User, Book
from app.src.schemas.review import ReviewModel


async def get_review_by_id(session: AsyncSession, review_id: uuid.UUID, user_id: int):
    query = (
        select(
            Review,
        )
        .where(Review.id == review_id)
        .where(Review.user_id == user_id)
    )
    result = await session.execute(query)
    return result.scalars().first()


async def get_reviews_by_user(session: AsyncSession, user: User):
    query = (
        select(
            Review.id,
            Review.user_id,
            Review.book_id,
            Review.review_text,
            Review.rate,
            Review.created_at,
            Review.updated_at,
        )
        .where(Review.user_id == user.id)
        .order_by(desc(Review.updated_at))
    )
    reviews = await session.execute(query)
    return reviews.mappings().all()


async def post_review(
    body: ReviewModel,
    user: User,
    session: AsyncSession,
) -> Review:
    book = await session.get(Book, body.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book with this ID does not exist")
    review = Review(
        user_id=user.id,
        book_id=body.book_id,
        review_text=body.review_text,
        rate=body.rate,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    session.add(review)
    await session.commit()
    await session.refresh(review)
    return review


async def update_review(
    review_id: uuid.UUID,
    body: ReviewModel,
    user: User,
    session: AsyncSession,
) -> Review:
    review = await get_review_by_id(session, review_id, user.id)
    if review:
        review.review_text = body.review_text
        review.rate = body.rate
        review.updated_at = datetime.now()
        await session.commit()
        await session.refresh(review)
    return review


async def remove_review(review_id: uuid.UUID, session: AsyncSession, user: User):
    review = await get_review_by_id(session, review_id, user.id)
    if review:
        await session.delete(review)
        await session.commit()
    return review
