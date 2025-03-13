import contextlib

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

from app.src.config.config import settings


URI = settings.db_url


class DataBaseSessionManager:

    def __init__(self, url):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker | None = async_sessionmaker(
            autoflush=False, autocommit=False, bind=self._engine, expire_on_commit=False
        )

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Session maker is not initialized")
        session: AsyncSession = self._session_maker()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


session_manager = DataBaseSessionManager(URI)
