import uuid
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
    tags=["reviews"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[ReviewResponse])
async def get_reviews_by_user(
    session: AsyncSession = Depends(db),
    current_user: User = Depends(auth_service.get_current_user),
):
    reviews = await repository_reviews.get_reviews_by_user(session, current_user)
    print(f"reviews {reviews}")
    if not reviews:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return [
        ReviewResponse(
            review_name=current_user.first_name,
            avatar=current_user.avatar,
            **dict(review),
        )
        for review in reviews
    ]


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    body: ReviewModel,
    session: AsyncSession = Depends(db),
    current_user: User = Depends(auth_service.get_current_user),
):
    review = await repository_reviews.post_review(body, current_user, session)
    return ReviewResponse(
        review_name=current_user.first_name,
        avatar=current_user.avatar,
        **review.__dict__,
    )


@router.put(
    "/{review_id}", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED
)
async def update_review(
    body: ReviewModel,
    session: AsyncSession = Depends(db),
    review_id: uuid.UUID = Path(),
    current_user: User = Depends(auth_service.get_current_user),
):

    review = await repository_reviews.update_review(
        review_id,
        body,
        current_user,
        session,
    )
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    print(f"current_user.first_name {current_user.first_name}")
    return ReviewResponse(
        review_name=current_user.first_name,
        avatar=current_user.avatar,
        **review.__dict__,
    )


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    session: AsyncSession = Depends(db),
    review_id: uuid.UUID = Path(),
    current_user: User = Depends(auth_service.get_current_user),
):
    review = await repository_reviews.remove_review(review_id, session, current_user)
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return review
