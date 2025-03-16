import enum


class Genre(enum.Enum):
    classics = "Classics"
    fantasy = "Fantasy"
    science_fiction = "ScienceFiction"
    mystery = "Mystery"
    romance = "Romance"
    non_fiction = "NonFiction"
    coloring = "Coloring"
    fairy_tales = "fairyTales"
    biography = "Biography"
    history = "History"
    poetry = "Poetry"
    self_help = "SelfHelp"
    business = "Business"
    travel = "Travel"
    cooking = "Cooking"
    other = "Other"


class BookType(enum.Enum):
    paperback = "Паперова книга"
    Ebook = ("Електронна книга",)
    Audiobook = ("Аудіокнига",)


class UserRole(enum.Enum):
    admin: str = "Admin"
    super_admin: str = "SuperAdmin"
    user: str = "User"


class TargetAges(enum.Enum):
    one_three = "1-3"
    three_five = "3-5"
    five_eight = "5-8"
    eight_twelve = "8-12"
    teenager = "Teenager"
    adult = "AdultLiterature"
    other = "Other"
