from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from sqlalchemy import func, desc, asc, cast, Numeric
from sqlalchemy.orm import Query

from app.src.entity import enums
from app.src.entity.models import Book, BookInfo, Category, TargetAge, BookType
from sqlalchemy.sql import and_


class Filter(ABC):

    @abstractmethod
    def apply(self, query: Query):
        pass


class AuthorFilter(Filter):
    def __init__(self, author):
        self.author = author

    def apply(self, query):
        return query.filter(Book.author.ilike(f"%{self.author}%"))


class TitleFilter(Filter):
    def __init__(self, title):
        self.title = title

    def apply(self, query):
        return query.filter(Book.title.ilike(f"%{self.title}%"))


class GenreFilter(Filter):
    def __init__(self, genre):
        try:
            self.genre = enums.GenreEnum(genre)
        except ValueError:
            self.genre = None

    def apply(self, query):
        if self.genre:
            return query.filter(Book.genre == self.genre)
        return query


class CategoriesFilter(Filter):
    def __init__(self, categories_: Optional[str]):
        self.categories = []
        if categories_:
            for category in categories_.split(","):
                try:
                    self.categories.append(enums.CategoriesEnum(category.strip()))
                except ValueError:
                    pass

    def apply(self, query):
        if self.categories:
            return query.join(Category).filter(Category.category.in_(self.categories))
        return query


class TargetAgesFilter(Filter):
    def __init__(self, target_ages: Optional[str]):
        self.target_ages = []
        if target_ages:
            for target_age in target_ages.split(","):
                try:
                    self.target_ages.append(enums.TargetAgesEnum(target_age.strip()))
                except ValueError:
                    pass

    def apply(self, query):
        if self.target_ages:
            return query.join(TargetAge).filter(
                TargetAge.target_age.in_(self.target_ages)
            )
        return query


#
class BookTypeFilter(Filter):
    def __init__(self, book_types: Optional[str]):
        self.book_types = []
        if book_types:
            for book_type in book_types.split(","):
                try:
                    self.book_types.append(enums.BookTypeEnum(book_type.strip()))
                except ValueError:
                    pass

    def apply(self, query):
        if self.book_types:
            return query.join(BookType).filter(BookType.book_type.in_(self.book_types))
        return query


class PaperTypeFilter(Filter):
    def __init__(self, paper_type):
        try:
            self.paper_type = enums.PaperTypeEnum(paper_type)
        except ValueError:
            self.paper_type = None

    def apply(self, query):
        if self.paper_type:
            return query.join(BookInfo).filter(BookInfo.paper_type == self.paper_type)
        return query


class LanguageFilter(Filter):
    def __init__(self, language):
        try:
            self.language = enums.LanguageEnum(language)
        except ValueError:
            self.language = None

    def apply(self, query):
        if self.language:
            return query.filter(Book.language == self.language)
        return query


class CoverTypeFilter(Filter):
    def __init__(self, cover_type):
        try:
            self.cover_type = enums.CoverTypeEnum(cover_type)
        except ValueError:
            self.cover_type = None

    def apply(self, query):
        if self.cover_type:
            return query.join(BookInfo).filter(BookInfo.cover_type == self.cover_type)
        return query


class DiscountRangeFilter(Filter):
    def __init__(self, discount_min, discount_max):
        self.discount_min = discount_min
        self.discount_max = discount_max

    def apply(self, query):
        return query.filter(
            and_(Book.discount >= self.discount_min, Book.discount <= self.discount_max)
        )


class PriceRangeFilter(Filter):
    def __init__(self, price_min, price_max, actual_price_subquery):
        self.price_min = price_min
        self.price_max = price_max
        self.actual_price_subquery = actual_price_subquery

    def apply(self, query):
        actual_price = self.actual_price_subquery.c.actual_price
        return query.filter(
            and_(
                actual_price >= self.price_min,
                actual_price <= self.price_max,
            )
        )


class CreatedAtRangeFilter(Filter):
    def __init__(self, created_at_after, created_at_before):
        self.created_at_after = created_at_after
        self.created_at_before = created_at_before

    def apply(self, query):
        return query.filter(
            and_(
                Book.created_at >= self.created_at_after,
                Book.created_at <= self.created_at_before,
            )
        )


class SortFilter(Filter):
    def __init__(self, sort_by, sort_order, reviews_subquery, actual_price_subquery):
        self.sort_by = sort_by
        self.sort_order = sort_order.lower()
        self.review_subquery = reviews_subquery
        self.actual_price_subquery = actual_price_subquery

    def apply(self, query):
        sort_mapping = {
            "actual_price": self.actual_price_subquery.c.actual_price,
            "rate": func.coalesce(self.review_subquery.c.rate, 0),
            "price": Book.price,
            "discount": Book.discount,
            "created_at": Book.created_at,
            "title": Book.title,
            "author": Book.author,
            "publication_year": BookInfo.publication_year,
        }

        sort_column = sort_mapping.get(
            self.sort_by, self.actual_price_subquery.c.actual_price
        )
        print(f"--------sort_by----{self.sort_by}")
        print(f"--------sort_column----{sort_column}")
        if self.sort_by == "actual_price":
            sort_column = self.actual_price_subquery.c.actual_price

        sort_order = (
            desc(sort_column) if self.sort_order == "desc" else asc(sort_column)
        )

        return query.order_by(sort_order)


# -------------------------------------------------------------------------------------------------------------
# --------------------------Factories -------------------------------------------------------------------------
class FilterFactory(ABC):
    @abstractmethod
    def create_filter(self) -> Filter:
        pass

    def make_filter(self) -> Filter:
        return self.create_filter()


class AuthorFilterFactory(FilterFactory):
    def __init__(self, author):
        self.author = author

    def create_filter(self) -> Filter:
        return AuthorFilter(self.author)


class TitleFilterFactory(FilterFactory):
    def __init__(self, title):
        self.title = title

    def create_filter(self) -> Filter:
        return TitleFilter(self.title)


class GenreFilterFactory(FilterFactory):
    def __init__(self, genre):
        self.genre = genre

    def create_filter(self) -> Filter:
        return GenreFilter(self.genre)


class CategoriesFilterFactory(FilterFactory):
    def __init__(self, categories):
        self.categories = categories

    def create_filter(self) -> Filter:
        return CategoriesFilter(self.categories)


#
class TargetAgesFilterFactory(FilterFactory):
    def __init__(self, target_ages):
        self.target_ages = target_ages

    def create_filter(self) -> Filter:
        return TargetAgesFilter(self.target_ages)


class BookTypeFilterFactory(FilterFactory):
    def __init__(self, book_types):
        self.book_types = book_types

    def create_filter(self) -> Filter:
        return BookTypeFilter(self.book_types)


class PaperTypeFilterFactory(FilterFactory):
    def __init__(self, paper_type):
        self.paper_type = paper_type

    def create_filter(self) -> Filter:
        return PaperTypeFilter(self.paper_type)


class LanguageFilterFactory(FilterFactory):
    def __init__(self, language):
        self.language = language

    def create_filter(self) -> Filter:
        return LanguageFilter(self.language)


class CoverTypeFilterFactory(FilterFactory):
    def __init__(self, cover_type):
        self.cover_type = cover_type

    def create_filter(self) -> Filter:
        return CoverTypeFilter(self.cover_type)


class DiscountRangeFilterFactory(FilterFactory):
    def __init__(self, discount_min, discount_max):
        self.discount_min = discount_min
        self.discount_max = discount_max

    def create_filter(self) -> Filter:
        return DiscountRangeFilter(self.discount_min, self.discount_max)


class PriceRangeFilterFactory(FilterFactory):
    def __init__(self, price_min, price_max, actual_price_subquery):
        self.price_min = price_min
        self.price_max = price_max
        self.actual_price_subquery = actual_price_subquery

    def create_filter(self) -> Filter:
        return PriceRangeFilter(
            self.price_min, self.price_max, self.actual_price_subquery
        )


class CreatedAtRangeFilterFactory(FilterFactory):
    def __init__(self, created_at_after, created_at_before):
        self.created_at_after = (
            created_at_after
            if isinstance(created_at_after, datetime)
            else datetime(1970, 1, 1)
        )
        self.created_at_before = (
            created_at_before
            if isinstance(created_at_before, datetime)
            else datetime.utcnow()
        )

    def create_filter(self) -> Filter:
        return CreatedAtRangeFilter(self.created_at_after, self.created_at_before)


class SortFilterFactory(FilterFactory):
    def __init__(self, sort_by, sort_order, reviews_subquery, actual_price_subquery):
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.reviews_subquery = reviews_subquery
        self.actual_price_subquery = actual_price_subquery

    def create_filter(self) -> Filter:
        return SortFilter(
            self.sort_by,
            self.sort_order,
            self.reviews_subquery,
            self.actual_price_subquery,
        )


# -----------------------------------------------------------------
# -------------------------DynamicFilterFactory--------------------
class DynamicFilterFactory:
    def __init__(
        self,
        filter_params,
        reviews_subquery,
        actual_price_subquery,
    ):
        self.filter_params = filter_params
        self.reviews_subquery = reviews_subquery
        self.actual_price_subquery = actual_price_subquery
        self.sort_by = filter_params.get("sort_by", "created_at")
        self.sort_order = filter_params.get("sort_order", "desc")

    def create_filters(self):
        filters = []

        filter_mapping = {
            "author": AuthorFilterFactory,
            "title": TitleFilterFactory,
            "genre": GenreFilterFactory,
            "categories": CategoriesFilterFactory,
            "target_ages": TargetAgesFilterFactory,
            "book_type": BookTypeFilterFactory,
            "paper_type": PaperTypeFilterFactory,
            "language": LanguageFilterFactory,
            "cover_type": CoverTypeFilterFactory,
            "discount_min": lambda x: DiscountRangeFilterFactory(
                x,
                (
                    self.filter_params.get("discount_max")
                    if self.filter_params.get("discount_max") is not None
                    else 1.0
                ),
            ),
            "discount_max": lambda x: DiscountRangeFilterFactory(
                (
                    self.filter_params.get("discount_min")
                    if self.filter_params.get("discount_min") is not None
                    else 0.0
                ),
                x,
            ),
            "price_min": lambda x: PriceRangeFilterFactory(
                x,
                (
                    self.filter_params.get("price_max")
                    if self.filter_params.get("price_max") is not None
                    else 999_999
                ),
                self.actual_price_subquery,
            ),
            "price_max": lambda x: PriceRangeFilterFactory(
                (
                    self.filter_params.get("price_min")
                    if self.filter_params.get("price_min") is not None
                    else 0
                ),
                x,
                self.actual_price_subquery,
            ),
            "created_at_after": lambda x: CreatedAtRangeFilterFactory(
                datetime.strptime(x, "%Y-%m-%d") if isinstance(x, str) else x,
                (
                    datetime.strptime(
                        self.filter_params.get(
                            "created_at_before", datetime.utcnow().strftime("%Y-%m-%d")
                        ),
                        "%Y-%m-%d",
                    )
                    if isinstance(self.filter_params.get("created_at_before"), str)
                    else self.filter_params.get("created_at_before", datetime.utcnow())
                ),
            ),
            "created_at_before": lambda x: CreatedAtRangeFilterFactory(
                (
                    datetime.strptime(
                        self.filter_params.get("created_at_after", "1970-01-01"),
                        "%Y-%m-%d",
                    )
                    if isinstance(self.filter_params.get("created_at_after"), str)
                    else self.filter_params.get(
                        "created_at_after", datetime(1970, 1, 1)
                    )
                ),
                datetime.strptime(x, "%Y-%m-%d") if isinstance(x, str) else x,
            ),
        }

        for param, value in self.filter_params.items():
            if param in filter_mapping and value is not None:
                factory_class = filter_mapping[param]
                if callable(factory_class):
                    # Для діапазонів (наприклад, discount_min/discount_max)
                    filters.append(factory_class(value).create_filter())
                else:
                    # Для звичайних фільтрів
                    filters.append(factory_class(value).create_filter())

        return filters

    def create_sort_filter(self):
        return SortFilterFactory(
            self.sort_by,
            self.sort_order,
            self.reviews_subquery,
            self.actual_price_subquery,
        ).create_filter()
