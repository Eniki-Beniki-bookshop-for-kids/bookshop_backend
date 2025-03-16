from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.database.db import db
from app.src.entity.models import User
from app.src.repository import review as repository_reviews
from app.src.schemas.review import ReviewModel, ReviewResponse
from app.src.services.auth import auth_service

router = APIRouter(
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{book_id}", response_model=List[ReviewResponse])
async def get_reviews_by_book(
    session: AsyncSession = Depends(db),
    book_id: int = Path(ge=1),
):
    reviews = await repository_reviews.get_comments_by_book(session, book_id)
    if not reviews:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return [ReviewResponse(**review) for review in reviews]


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    body: ReviewModel,
    session: AsyncSession = Depends(db),
    current_user: User = Depends(auth_service.get_current_user),
):
    comment = await repository_reviews.post_comment(body, current_user, session)
    return comment


@router.put(
    "/{review_id}", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED
)
async def update_review(
    body: ReviewModel,
    session: AsyncSession = Depends(db),
    review_id: int = Path(ge=1),
    current_user: User = Depends(auth_service.get_current_user),
):

    review = await repository_reviews.update_comment(
        review_id,
        body,
        current_user,
        session,
    )
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    session: AsyncSession = Depends(db),
    review_id: int = Path(ge=1),
    current_user: User = Depends(auth_service.get_current_user),
):
    review = await repository_reviews.remove_comment(review_id, session, current_user)
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return review
