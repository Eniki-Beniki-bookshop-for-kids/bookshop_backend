from fastapi import APIRouter, HTTPException, Depends, status, Security
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.database.db import db
from app.src.repository import users as repository_users
from app.src.schemas.users import UserModel, UserResponse, TokenModel
from app.src.services.auth import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)
security = HTTPBearer()


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    body: UserModel,
    session: AsyncSession = Depends(db),
):
    exist_user = await repository_users.get_user_by_email(body.email, session)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, session)
    return new_user


@router.post(
    "/login",
    response_model=TokenModel,
    status_code=status.HTTP_200_OK,
)
async def login(
    body: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db),
):
    user = await repository_users.get_user_by_email(body.username, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )
    # if not user.confirmed:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed"
    #     )
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token_ = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token_, session)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token_,
        "token_type": "bearer",
    }


@router.get(
    "/refresh_token",
    response_model=TokenModel,
)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: AsyncSession = Depends(db),
):
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, session)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, session)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, session)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
