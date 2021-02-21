from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


teachers_goals = db.Table('teachers_goals',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
    db.Column('goal_id', db.String(11), db.ForeignKey('goals.id'))
)


class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.String(11), nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(1), nullable=False)
    teachers = db.relationship("Teacher", secondary=teachers_goals, back_populates="goals")
    requests = db.relationship('Request', back_populates='goals')


class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    about = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    free = db.Column(db.String, nullable=False)
    goals = db.relationship("Goal", secondary=teachers_goals, back_populates="teachers")
    bookings = db.relationship('Booking', back_populates='teachers')


class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    teachers = db.relationship('Teacher', back_populates='bookings')
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    weekday = db.Column(db.String(3), nullable=False)
    time = db.Column(db.String(5), nullable=False)


class Request(db.Model):
    __tablename__ = "requests"
    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.String(11), db.ForeignKey('goals.id'), nullable=False)
    goals = db.relationship('Goal', back_populates='requests')
    time = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)