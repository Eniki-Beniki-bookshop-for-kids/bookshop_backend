from typing import List, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, over, cast, Numeric

from app.src.entity import enums
from app.src.entity.models import (
    Book,
    Review,
    BookInfo,
    Category,
    TargetAge,
    BookType,
    Image,
    User,
)
from app.src.repository.books_filter import DynamicFilterFactory
from app.src.schemas.books import BookResponse


#
async def get_all_books(
    session: AsyncSession, limit, offset, filter_params
) -> Tuple[int, List[BookResponse]]:
    reviews_subquery = (
        select(
            Review.book_id,
            func.jsonb_agg(
                func.distinct(
                    func.jsonb_build_object(
                        "id",
                        Review.id,
                        "book_id",
                        Review.book_id,
                        "review_text",
                        Review.review_text,
                        "rate",
                        Review.rate,
                        "review_date",
                        Review.review_date,
                        "user_id",
                        Review.user_id,
                        "review_name",
                        User.first_name,
                        "avatar",
                        User.last_name,
                        "created_at",
                        Review.created_at,
                        "updated_at",
                        Review.updated_at,
                    )
                )
            ).label("reviews"),
            func.coalesce(func.avg(func.coalesce(Review.rate, 0)), 0).label("rate"),
        )
        .join(User, User.id == Review.user_id)
        .group_by(Review.book_id)
        .subquery()
    )

    categories_subquery = (
        select(
            Category.book_id,
            func.array_agg(func.distinct(Category.category)).label("categories"),
        )
        .group_by(Category.book_id)
        .subquery()
    )

    target_ages_subquery = (
        select(
            TargetAge.book_id,
            func.array_agg(func.distinct(TargetAge.target_age)).label("target_ages"),
        )
        .group_by(TargetAge.book_id)
        .subquery()
    )

    book_type_subquery = (
        select(
            BookType.book_id,
            func.array_agg(func.distinct(BookType.book_type)).label("book_type"),
        )
        .group_by(BookType.book_id)
        .subquery()
    )

    row_number_subquery = (
        select(
            Book.id,
            over(func.row_number(), order_by=Book.created_at).label("row_num"),
        )
        .group_by(Book.id)
        .subquery()
    )

    # 1. Створюємо базовий запит для книг без ліміту та офсету
    base_query = select(Book.id).group_by(Book.id)

    actual_price_subquery = select(
        Book.id,
        cast(func.round(Book.price * (1.0 - Book.discount), 0), Numeric).label(
            "actual_price"
        ),
    ).subquery()

    # 2. Додаємо фільтрацію до `base_query`
    dynamic_factory = DynamicFilterFactory(
        filter_params, reviews_subquery, actual_price_subquery
    )
    filters = dynamic_factory.create_filters()

    for filter_ in filters:
        base_query = filter_.apply(base_query)

    # 3. Підраховуємо `total_books` після фільтрації (ОКРЕМО від `LIMIT` та `OFFSET`)
    total_books_subquery = (
        select(func.count()).select_from(base_query.subquery()).scalar_subquery()
    )

    filtered_books_subquery = base_query.subquery()

    query = (
        select(
            total_books_subquery.label("total_books"),
            Book.id,
            Book.author,
            Book.title,
            BookInfo.original_title,
            Book.genre,
            categories_subquery.c.categories,
            target_ages_subquery.c.target_ages,
            BookInfo.series,
            BookInfo.publisher,
            BookInfo.publication_year,
            book_type_subquery.c.book_type,
            BookInfo.page_count,
            BookInfo.paper_type,
            Book.language,
            Book.original_language,
            BookInfo.translator,
            BookInfo.cover_type,
            BookInfo.weight,
            BookInfo.dimensions,
            BookInfo.isbn,
            BookInfo.article_number,
            Book.price,
            actual_price_subquery.c.actual_price,
            Book.discount,
            Book.stock_quantity,
            BookInfo.description,
            func.array_agg(Image.image_url).label("images"),
            reviews_subquery.c.reviews,
            Book.is_bestseller,
            Book.is_publish,
            Book.is_gifted,
            Book.is_available,
            Book.created_at,
            Book.updated_at,
            func.coalesce(reviews_subquery.c.rate, 0).label("rate"),
        )
        .join(filtered_books_subquery, filtered_books_subquery.c.id == Book.id)
        .join(row_number_subquery, row_number_subquery.c.id == Book.id)
        .join(actual_price_subquery, actual_price_subquery.c.id == Book.id)
        .outerjoin(BookInfo, BookInfo.book_id == Book.id)
        .outerjoin(reviews_subquery, reviews_subquery.c.book_id == Book.id)
        .outerjoin(categories_subquery, categories_subquery.c.book_id == Book.id)
        .outerjoin(target_ages_subquery, target_ages_subquery.c.book_id == Book.id)
        .outerjoin(book_type_subquery, book_type_subquery.c.book_id == Book.id)
        .outerjoin(Image, Image.book_id == Book.id)
        .group_by(
            Book.id,
            BookInfo.id,
            BookInfo.original_title,
            actual_price_subquery.c.actual_price,
            BookInfo.series,
            BookInfo.publisher,
            BookInfo.publication_year,
            BookInfo.page_count,
            BookInfo.paper_type,
            BookInfo.translator,
            BookInfo.cover_type,
            BookInfo.weight,
            BookInfo.dimensions,
            BookInfo.isbn,
            BookInfo.article_number,
            BookInfo.description,
            reviews_subquery.c.reviews,
            reviews_subquery.c.rate,
            categories_subquery.c.categories,
            target_ages_subquery.c.target_ages,
            book_type_subquery.c.book_type,
        )
        .limit(limit)
        .offset(offset)
    )

    sort_filter = dynamic_factory.create_sort_filter()
    query = sort_filter.apply(query)

    books_result = await session.execute(query)
    books = [dict(book) for book in books_result.mappings().all()]

    # Отримуємо загальну кількість книг з першого запису (оскільки воно однакове для всіх)
    total_books = books[0]["total_books"] if books and "total_books" in books[0] else 0

    categories_mapping = {item.name: item.value for item in enums.CategoriesEnum}
    target_ages_mapping = {item.name: item.value for item in enums.TargetAgesEnum}
    book_type_mapping = {item.name: item.value for item in enums.BookTypeEnum}

    for book in books:
        book["categories"] = [
            categories_mapping.get(cat, enums.CategoriesEnum.other_category.value)
            for cat in book["categories"]
        ]
        book["target_ages"] = [
            target_ages_mapping.get(age, enums.TargetAgesEnum.other_target.value)
            for age in book["target_ages"]
        ]
        book["book_type"] = [
            book_type_mapping.get(bt, enums.BookTypeEnum.paperback.value)
            for bt in book["book_type"]
        ]

    book_responses = [
        BookResponse(
            book_id=book["id"],
            title=book["title"],
            author=book["author"],
            original_title=book["original_title"],
            genre=book["genre"],
            categories=[c for c in book["categories"] if c is not None],
            target_ages=[t for t in book["target_ages"] if t is not None],
            series=book["series"],
            publisher=book["publisher"],
            publication_year=book["publication_year"],
            book_type=[b for b in book["book_type"] if b is not None],
            page_count=book["page_count"],
            paper_type=book["paper_type"],
            language=book["language"],
            original_language=book["original_language"],
            translator=book["translator"],
            cover_type=book["cover_type"],
            weight=book["weight"],
            dimensions=book["dimensions"],
            isbn=book["isbn"],
            article_number=book["article_number"],
            price=book["price"],
            actual_price=book["actual_price"],
            discount=book["discount"],
            stock_quantity=book["stock_quantity"],
            description=book["description"],
            images=[i for i in book["images"] if i is not None],
            reviews=(
                [r for r in book["reviews"] if r is not None] if book["reviews"] else []
            ),
            is_bestseller=book["is_bestseller"],
            is_publish=book["is_publish"],
            is_gifted=book["is_gifted"],
            is_available=book["is_available"],
            total_sales=None,  # Якщо потрібно, можна отримати окремим запитом
            orders=None,
            created_at=book["created_at"],
            updated_at=book["updated_at"],
            rate=book["rate"],
        )
        for book in books
    ]

    return total_books, book_responses
