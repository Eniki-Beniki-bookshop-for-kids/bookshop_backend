import uuid

from libgravatar import Gravatar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, func, select, desc

from app.src.entity import enums
from app.src.entity.models import User
from app.src.schemas.users import UserModel, GoogleUser


async def get_user_by_email(
    email: str,
    session: AsyncSession,
) -> User:
    query = select(User).where(func.lower(User.email) == func.lower(email))
    result = await session.execute(query)
    return result.scalars().first()


async def get_user_by_phone_number(
    phone_number: str,
    session: AsyncSession,
) -> User:
    query = select(User).where(
        func.lower(User.phone_number) == func.lower(phone_number)
    )
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


async def get_user_by_google_sub(
    google_sub: int,
    session: AsyncSession,
) -> User:
    query = select(User).where(User.google_id == str(google_sub))
    result = await session.execute(query)
    return result.scalars().first()


async def create_user_from_google_info(
    google_user: GoogleUser,
    session: AsyncSession,
) -> User:
    google_id = google_user.sub
    email = google_user.email

    existing_user = await get_user_by_email(email, session)

    if existing_user:
        existing_user.google_id = google_id
        await session.commit()
        return existing_user
    else:
        new_user = User(
            id=uuid.uuid4(),
            email=email,
            username=(
                f"{google_user.given_name}_{google_user.family_name}".lower()
                if google_user.family_name
                else google_user.given_name.lower()
            ),
            first_name=google_user.given_name,
            last_name=google_user.family_name,
            gender=enums.GenderEnum.other_gender,
            avatar=google_user.picture,
            login_method="google",
            password="*",
            is_confirmed=True,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
