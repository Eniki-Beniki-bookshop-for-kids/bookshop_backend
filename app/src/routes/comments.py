from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.database.db import db
from app.src.entity.models import User
from app.src.repository import comments as repository_comments
from app.src.schemas.comments import CommentModel, CommentResponse
from app.src.services.auth import auth_service

router = APIRouter(
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{book_id}", response_model=List[CommentResponse])
async def get_comments_by_book(
    session: AsyncSession = Depends(db),
    book_id: int = Path(ge=1),
):
    comments = await repository_comments.get_comments_by_book(session, book_id)
    if not comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return [CommentResponse(**book) for book in comments]


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    body: CommentModel,
    session: AsyncSession = Depends(db),
    current_user: User = Depends(auth_service.get_current_user),
):
    comment = await repository_comments.post_comment(body, current_user, session)
    return comment


@router.put(
    "/{comment_id}", response_model=CommentResponse, status_code=status.HTTP_201_CREATED
)
async def update_comment(
    body: CommentModel,
    session: AsyncSession = Depends(db),
    comment_id: int = Path(ge=1),
    current_user: User = Depends(auth_service.get_current_user),
):

    comment = await repository_comments.update_comment(
        comment_id,
        body,
        current_user,
        session,
    )
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    session: AsyncSession = Depends(db),
    comment_id: int = Path(ge=1),
    current_user: User = Depends(auth_service.get_current_user),
):
    comment = await repository_comments.remove_comment(
        comment_id, session, current_user
    )
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return comment
