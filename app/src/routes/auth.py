from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, HTTPException, Depends, status, Security, Request
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.src.config.config import settings
from app.src.database.db import db
from app.src.entity.models import User
from app.src.repository import users as repository_users
from app.src.schemas.users import (
    UserModel,
    UserResponse,
    TokenModel,
    GoogleUser,
    GoogleResponse,
)
from app.src.services.auth import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

security = HTTPBearer()
oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    client_kwargs={
        "scope": "openid email profile",
    },
)


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
            status_code=status.HTTP_409_CONFLICT,
            detail="Account with this email already exists",
        )
    exist_user = await repository_users.get_user_by_phone_number(
        body.phone_number, session
    )
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This phone number is already used",
        )
    body.password = auth_service.get_password_hash(body.password)
    _ = await repository_users.create_user(body, session)
    new_user = await repository_users.get_user_by_email(body.email, session)
    return UserResponse(user_id=new_user.id, **new_user.__dict__)


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
    if not user:
        user = await repository_users.get_user_by_phone_number(body.username, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or phone number",
            )
    if user.login_method == "google":
        raise HTTPException(
            status_code=403,
            detail="Account registered via Google — use OAuth login",
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
    print(access_token)
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
    refresh_token_ = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token_, session)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token_,
        "token_type": "bearer",
    }


@router.get("/google")
async def login_google(request: Request):
    return await oauth.google.authorize_redirect(request, settings.google_redirect_uri)


@router.get("/google/callback", response_model=GoogleResponse)
async def auth_google(request: Request, session: AsyncSession = Depends(db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user_info = token.get("userinfo")

    google_user = GoogleUser(**user_info)
    try:
        existing_user: User = await repository_users.get_user_by_google_sub(
            google_user.sub, session
        )

        if existing_user:
            user: User = existing_user
        else:
            user: User = await repository_users.create_user_from_google_info(
                google_user, session
            )

        access_token = await auth_service.create_access_token(data={"sub": user.email})
        refresh_token_ = await auth_service.create_refresh_token(
            data={"sub": user.email}
        )

    except Exception as e:
        print(f"OAuth error: {e}")
        raise HTTPException(status_code=500, detail="OAuth callback failed")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token_,
        "token_type": "bearer",
        "user": UserResponse(user_id=user.id, **user.__dict__),
    }
