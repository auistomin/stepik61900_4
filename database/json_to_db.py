from flask import Flask
from json import load as json_load, dumps as json_dumps
from os import path, remove as remove_file
from models import db, migrate, Goal, Teacher
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.app_context().push()
migrate.init_app(app, db)


def seed(data_json):
    for key, value in data_json.get('goals').items():
        goal = Goal(
            id=key,
            name=value['title'],
            symbol=value['pic']
        )
        db.session.add(goal)
        db.session.flush()
    for json_teacher in data_json.get('teachers'):
        teacher = Teacher(
            name=json_teacher['name'],
            about=json_teacher['about'],
            rating=json_teacher['rating'],
            picture=json_teacher['picture'],
            price=json_teacher['price'],
            free=json_dumps(json_teacher["free"])
        )
        db.session.add(teacher)
        for json_goal in json_teacher["goals"]:
            goal = Goal.query.filter(Goal.id == json_goal).first()
            teacher.goals.append(goal)
    db.session.commit()


def main():
    filename = path.dirname(path.realpath(__file__)) + '\\base.db'
    if path.exists(filename):
        remove_file(filename)
    db.create_all()
    with open('data.json', 'r', encoding="utf-8") as file:
        data_json = json_load(file)
    seed(data_json)


if __name__ == '__main__':
    main()