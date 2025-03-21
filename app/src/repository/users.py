from libgravatar import Gravatar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, func, select, desc

from app.src.entity.models import User
from app.src.schemas.users import UserModel


async def get_user_by_email(
    email: str,
    session: AsyncSession,
) -> User:
    query = select(User).where(func.lower(User.email) == func.lower(email))
    result = await session.execute(query)
    return result.scalars().first()


async def create_user(
    body: UserModel,
    session: AsyncSession,
) -> User:
    avatar = Gravatar(body.email)
    new_user = User(
        **body.dict(),
        avatar=avatar.get_image(),
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def update_token(
    user: User,
    refresh_token_,
    session: AsyncSession,
) -> None:
    user.refresh_token = refresh_token_
    await session.commit()
