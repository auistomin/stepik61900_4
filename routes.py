from json import loads as json_loads

from flask import render_template, request, abort
from numpy import random

from config import week_days, week_times
from forms import BookingForm, RequestForm, SortingForm
from models import Goal, Teacher, Booking, Request
from app import app, db


@app.route('/')
def render_index():

    goals = Goal.query.all()
    teachers = Teacher.query.all()
    random.shuffle(teachers)

    return render_template("index.html", goals=goals, teachers=teachers[0:6])


@app.route('/all/', methods=["POST", "GET"])
def render_all():

    form = SortingForm()
    goals = Goal.query.all()

    teachers = []
    if request.method == "POST":
        if form.validate_on_submit():
            sorting = form.sorting.data
            if sorting == "1":
                teachers = Teacher.query.all()
                random.shuffle(teachers)
            elif sorting == "2":
                teachers = Teacher.query.order_by(Teacher.rating.desc()).all()
            elif sorting == "3":
                teachers = Teacher.query.order_by(Teacher.price.desc()).all()
            elif sorting == "4":
                teachers = Teacher.query.order_by(Teacher.price).all()
    if not teachers:
        teachers = Teacher.query.all()
        random.shuffle(teachers)

    return render_template("all.html", form=form, goals=goals, teachers=teachers, n_teachers=len(teachers))


@app.route('/goal/<goal>/')
def render_goal(goal):

    goals = Goal.query.all()
    teachers = Teacher.query.filter(Teacher.goals.any(Goal.id == goal)).order_by(Teacher.rating.desc()).all()
    active_goal = Goal.query.filter(Goal.id == goal).first_or_404()

    return render_template("goal.html", goals=goals, teachers=teachers, goal=active_goal)


@app.route('/profile/<int:teacher_id>/')
def render_profile(teacher_id):

    goals = Goal.query.all()
    teacher = Teacher.query.get_or_404(teacher_id)
    teacher_free = json_loads(teacher.free)
    teacher_goals = Goal.query.filter(Goal.teachers.any(Teacher.id == teacher_id)).all()

    return render_template("profile.html", goals=goals, teacher=teacher, teacher_free=teacher_free, teacher_goals=teacher_goals, week_days=week_days)


@app.route('/booking/<int:teacher_id>/<weekday>/<time>/', methods=['GET', 'POST'])
def render_booking(teacher_id, weekday, time):

    form = BookingForm()
    if request.method == "POST":
        teacher_id = form.teacher.data
        weekday = form.weekday.data
        time = form.time.data

    goals = Goal.query.all()
    teacher = Teacher.query.get_or_404(teacher_id)
    teacher_free = json_loads(teacher.free)

    fulltime = time + ":00"
    if not weekday in teacher_free:
        abort(404)
    elif not fulltime in teacher_free[weekday]:
        abort(404)
    elif not teacher_free[weekday][fulltime]:
        abort(404)

    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            phone = form.phone.data
            booking = Booking(teacher_id=teacher_id, name=name, phone=phone, weekday=weekday, time=fulltime)
            db.session.add(booking)
            db.session.commit()
            return render_template("booking_done.html", goals=goals, name=name, phone=phone, weekday=week_days[weekday], time=time)

    return render_template("booking.html", form=form, goals=goals, teacher=teacher, week_days=week_days, weekday=weekday, time=time)


@app.route('/request/', methods=["POST", "GET"])
def render_request():

    goals = Goal.query.all()

    form = RequestForm()
    if request.method == "POST":
        if form.validate_on_submit():
            goal_id = form.goal.data
            goal = Goal.query.get_or_404(goal_id)
            time = form.time.data
            name = form.name.data
            phone = form.phone.data
            request_obj = Request(goal_id=goal_id, time=time, name=name, phone=phone)
            db.session.add(request_obj)
            db.session.commit()
            return render_template("request_done.html", goal=goal.name, time=week_times[time], name=name, phone=phone)

    return render_template("request.html", form=form, goals=goals)


@app.route('/302/')
def render_302():
    return render_template('302.html')


@app.errorhandler(404)
def render_404(error):
    return render_template('404.html')