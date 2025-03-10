from pydantic import BaseModel, Field


class BookShortResponse(BaseModel):
    id: int = Field(
        gt=0,
        description="The ID of the book",
    )
    author: str = Field(
        min_length=1,
        max_length=100,
    )
    title: str = Field(
        min_length=1,
        max_length=100,
        description="The title of the book",
    )
    # image_url: str = Field(
    #     description="The image url of the book",
    # )
    # stock_quantity: int = Field(
    #     ge=0,
    #     description="The stock quantity of the book",
    # )
    price: float = Field(
        gt=0,
        description="The price of the book",
    )
    is_available: bool = Field(
        description="The availability of the book",
    )
    discount: float = Field(
        description="The discount of the book",
    )
    rate: float = Field(
        ge=0,
        le=5,
        description="The rate of the book",
    )
    comments_count: int = Field(
        ge=0,
        description="The number of comments of the book",
    )

    class Config:
        from_attributes = True
