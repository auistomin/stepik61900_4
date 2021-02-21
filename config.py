from os import environ, path


DATABASE_URL = environ.get("DATABASE_URL")
if DATABASE_URL is None:
    current_path = path.dirname(path.realpath(__file__))
    DATABASE_URL = 'sqlite:///' + current_path + '\\database\\base.db'


class Config:
    DEBUG = True
    SECRET_KEY = "e36424c7deb8c33b7391e7851bf24267"
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False


week_days = {
    "mon": "Понедельник",
    "tue": "Вторник",
    "wed": "Среда",
    "thu": "Четверг",
    "fri": "Пятница",
    "sat": "Суббота",
    "sun": "Воскресенье"
}

week_times = {
    "time12": "1-2 часа в неделю",
    "time35": "3-5 часов в неделю",
    "time57": "5-7 часов в неделю",
    "time710": "7-10 часов в неделю"
}

sorting_options = {
    1: "В случайном порядке",
    2: "Сначала лучшие по рейтингу",
    3: "Сначала дорогие",
    4: "Сначала недорогие"
}