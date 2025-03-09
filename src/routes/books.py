from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import db
from src.repository import books as repository_books
from src.schemas.books import BookShortResponse

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[BookShortResponse])
async def get_all_books(session: AsyncSession = Depends(db)):
    books_repository = await repository_books.get_all_books(session)
    return books_repository


@router.get("/{book_id}")
async def get_book(book_id: int):
    pass


#
#
# @router.post("/")
# async def create_book():
#     pass
#
#
# @router.put("/{book_id}")
# async def update_book(book_id: int):
#     pass
#
#
# @router.delete("/{book_id}")
# async def delete_book(book_id: int):
#     pass
