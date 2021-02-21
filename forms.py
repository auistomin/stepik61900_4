from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, RadioField, SelectField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp
from wtforms.fields.html5 import TelField
from config import week_times, sorting_options
from models import Goal


class BookingForm(FlaskForm):
    weekday = HiddenField()
    time = HiddenField()
    teacher = HiddenField()
    name = StringField("Вас зовут", validators=[InputRequired("Введите ваше имя"), Length(min=2, max=100, message="Имя должно быть не менее 2 символов и не более 100 символов")])
    phone = TelField("Ваш телефон", validators=[InputRequired("Введите ваш номер телефона"), Regexp("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", message="Номер телефона имеет некорректный формат")])
    submit = SubmitField("Записаться на пробный урок")


class RequestForm(FlaskForm):
    choices = [(goal.id, goal.name) for goal in Goal.query.all()]
    goal = RadioField('Какая цель занятий?', choices=choices, default="travel")
    choices = [(key, value) for key, value in week_times.items()]
    time = RadioField('Сколько времени есть?', choices=choices, default="time12")
    name = StringField("Вас зовут", validators=[InputRequired("Введите ваше имя"), Length(min=2, message="Имя должно быть не менее 2 символов")])
    phone = TelField("Ваш телефон", validators=[InputRequired("Введите ваш номер телефона"), Regexp("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", message="Номер телефона имеет некорректный формат")])
    submit = SubmitField("Найдите мне преподавателя")


class SortingForm(FlaskForm):
    choices = [(key, value) for key, value in sorting_options.items()]
    sorting = SelectField("Сортировка", choices=choices)