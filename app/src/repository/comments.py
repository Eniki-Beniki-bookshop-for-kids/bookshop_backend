from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, func, select, desc

from app.src.entity.models import Comment, User, Book
from app.src.schemas.comments import CommentModel


async def get_comment_by_id(session: AsyncSession, comment_id: int, user_id: int):
    query = (
        select(Comment)
        .where(Comment.id == comment_id)
        .where(Comment.user_id == user_id)
    )
    result = await session.execute(query)
    return result.scalars().first()


async def get_comments_by_book(session: AsyncSession, book_id: int):
    query = (
        select(
            Comment.id,
            Comment.user_id,
            Comment.book_id,
            Comment.review_text,
            Comment.rate,
            Comment.created_at,
            Comment.updated_at,
        )
        .where(Comment.book_id == book_id)
        .order_by(desc(Comment.updated_at))
    )
    comments = await session.execute(query)
    return comments.mappings().all()


async def post_comment(
    body: CommentModel,
    user: User,
    session: AsyncSession,
) -> Comment:
    book = await session.get(Book, body.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book with this ID does not exist")
    comment = Comment(
        user_id=user.id,
        book_id=body.book_id,
        review_text=body.review_text,
        rate=body.rate,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment


async def update_comment(
    comment_id: int,
    body: CommentModel,
    user: User,
    session: AsyncSession,
) -> Comment:
    comment = await get_comment_by_id(session, comment_id, user.id)
    if comment:
        comment.review_text = body.review_text
        comment.rate = body.rate
        comment.updated_at = datetime.now()
        await session.commit()
        await session.refresh(comment)
    return comment


async def remove_comment(comment_id: int, session: AsyncSession, user: User):
    comment = await get_comment_by_id(session, comment_id, user.id)
    if comment:
        await session.delete(comment)
        await session.commit()
    return comment
