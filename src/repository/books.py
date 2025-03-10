from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, func, select

from src.entity.models import Book, Comment


async def get_all_books(session: AsyncSession):
    query = (
        select(
            Book.id,
            Book.author,
            Book.title,
            Book.price,
            Book.is_available,
            Book.discount,
            func.coalesce(func.avg(Comment.rate), 0).label("rate"),
            func.count(Comment.id).label("comments_count"),
        )
        .outerjoin(Comment, Comment.book_id == Book.id)
        .group_by(Book.id)
    )
    books = await session.execute(query)
    return books.mappings().all()
