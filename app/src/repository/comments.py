from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, func, select, desc

from src.entity.models import Book, Comment
from src.schemas.comments import CommentModel


async def get_comments_by_book(session: AsyncSession, book_id: int):
    query = (
        select(
            Comment.id,
            Comment.book_id,
            Comment.review_text,
            Comment.rate,
            Comment.published_at,
        )
        .where(Comment.book_id == book_id)
        .order_by(desc(Comment.published_at))
    )
    comments = await session.execute(query)
    return comments.mappings().all()


async def post_comment(body: CommentModel, session: AsyncSession):
    comment = Comment(
        review_text=body.review_text,
        rate=body.rate,
        published_at=body.published_at,
        book_id=body.book_id,
    )
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment
