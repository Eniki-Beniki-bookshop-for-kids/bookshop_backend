import enum


class Genre(enum.Enum):
    classics: str = "Класика"
    fantasy: str = "Фантастика"
    science_fiction: str = "Наука-фантастика"
    mystery: str = "Детектив"
    romance: str = "Романтика"
    non_fiction: str = "Нехудожня-література"
    coloring: str = "Розмальовки"
    fairy_tales: str = "Казки"
    biography: str = "Біографія"
    history: str = "Історія"
    poetry: str = "Поезія"
    self_help: str = "Саморозвиток"
    business: str = "Бізнес"
    travel: str = "Подорожі"
    cooking: str = "Кулінарія"
    other_genre: str = "Інше"


class Language(enum.Enum):
    ukrainian: str = "Українська"
    english: str = "Англійська"
    russian: str = "Російська"
    german: str = "Німецька"
    french: str = "Французька"
    spanish: str = "Іспанська"
    italian: str = "Італійська"
    polish: str = "Польська"
    chinese: str = "Китайська"
    japanese: str = "Японська"
    arabic: str = "Арабська"
    turkish: str = "Турецька"
    portuguese: str = "Португальська"
    dutch: str = "Голландська"
    swedish: str = "Шведська"
    latin: str = "Латинська"
    greek: str = "Грецька"
    hebrew: str = "Іврит"
    other_language: str = "Інша мова"


class BookType(enum.Enum):
    paperback: str = "Паперова книга"
    Ebook: str = "Електронна книга"
    audiobook: str = "Аудіокнига"


class CoverType(enum.Enum):
    hard: str = "Тверда"
    soft: str = "М’яка"
    spiral: str = "Спиральна"


class PaperType(enum.Enum):
    offset: str = "Офсетний папір"
    newsprint: str = "Газетний папір"
    writing: str = "Письмовий папір"
    coated: str = "Крейдований папір"
    vellum: str = "Веленевий папір"
    cardboard: str = "Картон"


class UserRole(enum.Enum):
    admin: str = "Admin"
    superadmin: str = "SuperAdmin"
    user: str = "User"


class Categories(enum.Enum):
    children_literature: str = "Дитяча література"
    young_adult: str = "Для підлітків"
    adult_literature: str = "Для дорослих"
    parents: str = "Для батьків"
    other_category: str = "Інша категорія"


class TargetAges(enum.Enum):
    age_1_3: str = "1-3"
    age_3_5: str = "3-5"
    age_5_8: str = "5-8"
    age_8_12: str = "8-12"
    teenager: str = "Підліткам"
    adult: str = "Дорослим"
    other_target: str = "Інше"


#
# genre_enum = sa.Enum(
#     "classics",
#     "fantasy",
#     "science_fiction",
#     "mystery",
#     "romance",
#     "non_fiction",
#     "coloring",
#     "fairy_tales",
#     "biography",
#     "history",
#     "poetry",
#     "self_help",
#     "business",
#     "travel",
#     "cooking",
#     "other_genre",
#     name="genre_enum",
# )
# language_enum = sa.Enum(
#     "ukrainian",
#     "english",
#     "russian",
#     "german",
#     "french",
#     "spanish",
#     "italian",
#     "polish",
#     "chinese",
#     "japanese",
#     "arabic",
#     "turkish",
#     "portuguese",
#     "dutch",
#     "swedish",
#     "latin",
#     "greek",
#     "hebrew",
#     "other_language",
#     name="language_enum",
# )
# paper_type_enum = sa.Enum(
#     "offset",
#     "newsprint",
#     "writing",
#     "coated",
#     "vellum",
#     "cardboard",
#     name="paper_type_enum",
# )
# cover_type_enum = sa.Enum("hard", "soft", "spiral", name="cover_type_enum")
# user_role_enum = sa.Enum("admin", "superadmin", "user", name="user_role_enum")
# categories_enum = sa.Enum(
#     "children_literature",
#     "young_adult",
#     "adult_literature",
#     "parents",
#     "other_category",
#     name="categories_enum",
# )
# target_ages_enum = sa.Enum(
#     "age_1_3",
#     "age_3_5",
#     "age_5_8",
#     "age_8_12",
#     "teenager",
#     "adult",
#     "other_target",
#     name="target_ages_enum",
# )
#
# booktype_enum = sa.Enum("paperback", "Ebook", "audiobook", name="booktype_enum")
#
# # drop enums
# categories_enum.drop(op.get_bind(), checkfirst=True)
# cover_type_enum.drop(op.get_bind(), checkfirst=True)
# language_enum.drop(op.get_bind(), checkfirst=True)
# genre_enum.drop(op.get_bind(), checkfirst=True)
# paper_type_enum.drop(op.get_bind(), checkfirst=True)
# target_ages_enum.drop(op.get_bind(), checkfirst=True)
# user_role_enum.drop(op.get_bind(), checkfirst=True)
# booktype_enum.drop(op.get_bind(), checkfirst=True)
