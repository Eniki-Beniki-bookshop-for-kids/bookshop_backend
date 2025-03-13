from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.src.database.connect import session_manager


async def db() -> AsyncGenerator[AsyncSession, None]:
    async with session_manager.session() as session:
        yield session
