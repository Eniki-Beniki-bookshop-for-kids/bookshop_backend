from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import db
from src.repository import comments as repository_comments
from src.schemas.comments import CommentModel, CommentResponse

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


@router.post("/", response_model=CommentModel, status_code=status.HTTP_201_CREATED)
async def create_comment(
    body: CommentModel,
    session: AsyncSession = Depends(db),
):
    comment = await repository_comments.post_comment(body, session)
    return comment


@router.put("/{comment_id}")
async def update_comment(
    session: AsyncSession = Depends(db),
    comment_id: int = Path(ge=1),
):
    pass


@router.delete("/{comment_id}")
async def delete_comment(
    session: AsyncSession = Depends(db),
    comment_id: int = Path(ge=1),
):
    pass
