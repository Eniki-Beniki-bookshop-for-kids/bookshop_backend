import re

from fastapi import APIRouter, Query
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.database.db import db
from app.src.repository import books as repository_books
from app.src.schemas.books import BookPaginationResponse, BookFilterParams


router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)


def camel_to_snake(name: str) -> str:
    return re.sub(r"([a-z])([A-Z])", r"\1_\2", name).lower()


@router.get("/", response_model=BookPaginationResponse)
async def get_all_books(
    session: AsyncSession = Depends(db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort_by: str = Query(
        "actualPrice",
        alias="sortBy",
        description="Sort field: actualPrice, rate, price, discount, createdAt, title, author, publicationYear",
    ),
    sort_order: str = Query(
        "asc",
        alias="sortOrder",
        description="Sort order: asc or desc",
    ),
    filter_params: BookFilterParams = Depends(),
    categories: str = Query(
        None,
        alias="categories",
        description="Фільтр за категоріями (Дитяча література, Для підлітків, Для дорослих, Для батьків, "
        "Інша категорія)(рядок, розділений комами)",
    ),
    target_ages: str = Query(
        None,
        alias="targetAges",
        description="Фільтр за масивом цільових вікових груп (1-3, 3-5, 5-8, 8-12, Підліткам, Дорослим, Інше) (рядок, "
        "розділений комами)",
    ),
    book_type: str = Query(
        None,
        alias="bookType",
        description="Фільтр за типом книги (Електронна книга, Аудіокнига, Паперова книга)(рядок, розділений комами)",
    ),
):
    filter_params_dict = filter_params.dict()
    filter_params_dict["sort_by"] = camel_to_snake(sort_by)
    filter_params_dict["sort_order"] = sort_order
    filter_params_dict["categories"] = categories
    filter_params_dict["target_ages"] = target_ages
    filter_params_dict["book_type"] = book_type

    total_books, books_repository = await repository_books.get_all_books(
        session, limit, offset, filter_params_dict
    )
    if total_books == 0:
        raise HTTPException(status_code=404, detail="Not found any book")
    total_pages = (total_books + limit - 1) // limit
    return BookPaginationResponse(
        total_books=total_books,
        total_pages=total_pages,
        current_page=(offset // limit) + 1,
        limit=limit,
        offset=offset,
        books=books_repository,
    )
