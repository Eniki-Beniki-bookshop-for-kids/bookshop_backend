import enum


class GenreEnum(enum.Enum):
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


class LanguageEnum(enum.Enum):
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


class BookTypeEnum(enum.Enum):
    paperback: str = "Паперова книга"
    Ebook: str = "Електронна книга"
    audiobook: str = "Аудіокнига"


class CoverTypeEnum(enum.Enum):
    hard: str = "Тверда"
    soft: str = "М’яка"
    spiral: str = "Спиральна"


class PaperTypeEnum(enum.Enum):
    offset: str = "Офсетний папір"
    newsprint: str = "Газетний папір"
    writing: str = "Письмовий папір"
    coated: str = "Крейдований папір"
    vellum: str = "Веленевий папір"
    cardboard: str = "Картон"


class UserRoleEnum(enum.Enum):
    admin: str = "Admin"
    superadmin: str = "SuperAdmin"
    user: str = "User"


class CategoriesEnum(enum.Enum):
    children_literature: str = "Дитяча література"
    young_adult: str = "Для підлітків"
    adult_literature: str = "Для дорослих"
    parents: str = "Для батьків"
    other_category: str = "Інша категорія"


class TargetAgesEnum(enum.Enum):
    age_1_3: str = "1-3"
    age_3_5: str = "3-5"
    age_5_8: str = "5-8"
    age_8_12: str = "8-12"
    teenager: str = "Підліткам"
    adult: str = "Дорослим"
    other_target: str = "Інше"
