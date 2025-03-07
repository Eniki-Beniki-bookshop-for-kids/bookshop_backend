from fastapi import APIRouter

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_all_books():
    pass


@router.get("/{book_id}")
async def get_book(book_id: int):
    pass


@router.post("/")
async def create_book():
    pass


@router.put("/{book_id}")
async def update_book(book_id: int):
    pass


@router.delete("/{book_id}")
async def delete_book(book_id: int):
    pass
