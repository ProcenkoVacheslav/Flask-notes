import sqlite3
import datetime
from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from settings import main_menu
from models import Login, Registrate, ElseInfo, AddNote
from users import UserLogin

DEBUG = True
SECRET_KEY = 'asdsa34543fjkb@h33k566786as@cavsx345acv34sc'

app = Flask(__name__)
app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message = 'Вы не авторизованы, пожалуйста авторизуйтесь.'
login_manager.login_message_category = 'light_error'


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().from_db(user_id, Users)


class Users(db.Model):
    __tablename__ = 'users'

    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500), nullable=False)

    relationship = db.relationship('Profile', backref='users', uselist=False)
    second_relationship = db.relationship('Notes', backref='users', uselist=False)

    def __repr__(self):
        return f'User: {self.id_}'


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('users.id_'))
    city = db.Column(db.String(20))
    age = db.Column(db.Integer)
    sure_name = db.Column(db.String(20))
    about_yourself = db.Column(db.String(100))
    gender = db.Column(db.String(20))

    def __repr__(self):
        return f'User: {self.id}'


class Notes(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('users.id_'))
    title = db.Column(db.String(20), nullable=False)
    task = db.Column(db.String(150), nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'User: {self.id}'


@app.route('/')
def index():
    return render_template('index.html', title='главная', menu=main_menu)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Вы уже зарегестрированны, выйдите из профиля, чтобы войти снова.', 'light_error')
        return redirect(url_for('index'))

    form = Login()

    if form.validate_on_submit():
        user = UserLogin().get_user_by_email(form.email.data, Users)

        if user and check_password_hash(user.password, form.password.data) \
                and user.name == form.name.data and user.email == form.email.data:
            session['email'] = form.email.data
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            flash('Вы успешно вошли', 'success')
            return redirect(url_for('index'))
        else:
            flash('Что-то пошло не так', 'error')
    return render_template('login.html', title='войти', menu=main_menu, form=form)


@app.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    form = AddNote()
    user = UserLogin().get_user_by_email(session['email'], Users)
    all_notes = Notes.query.filter_by(note_id=user.id_).all()

    if form.validate_on_submit():

        user_datas = {
            'title': form.title.data,
            'task': form.task.data,
            'note_id': user.id_,
        }

        try:
            note = Notes(**user_datas)
            db.session.add(note)
            db.session.commit()
            flash('Заметка успешно добавлена', 'success')
            return redirect(url_for('notes'))

        except Exception as error:
            flash('Что-то пошло не так', 'error')
            db.session.rollback()
            print(f'Error in notes {error}')

    return render_template('notes.html', title='заметки', menu=main_menu, form=form, notes=all_notes)


@app.route('/complite/<name>', methods=['GET', 'POST'])
def complite(name):

    if request.method == 'POST':
        try:
            note = Notes.query.filter_by(id=name).first()
            db.session.delete(note)
            db.session.commit()
            flash('Заметка успешно удалена', 'success')
        except Exception as error:
            flash('Что-то пошло не так', 'error')
            print(f'Ошибка в complite {error}')
            db.session.rollback()

    return redirect(url_for('notes'))


@app.route('/profile')
@login_required
def profile():
    user = UserLogin().get_user_by_email(session['email'], Users)
    else_datas = Profile.query.filter_by(id=user.id_).first()

    if else_datas:
        user_data = {
            'Имя: ': user.name,
            'Фамилия:': else_datas.sure_name,
            'Возраст:': else_datas.age,
            'Город:': else_datas.city,
            'Пол:': else_datas.gender,
            'Email: ': user.email,
            'О себе:': else_datas.about_yourself,
        }
    else:
        user_data = {
            'Имя: ': user.name,
            'Email: ': user.email,
        }

    return render_template('profile.html', title='профиль', menu=main_menu, datas=user_data)


@app.route('/new_datas', methods=['GET', 'POST'])
@login_required
def new_datas():
    form = ElseInfo()
    user = UserLogin().get_user_by_email(session['email'], Users)

    if form.validate_on_submit():
        user_datas = {
            'sure_name': form.sure_name.data,
            'age': form.age.data,
            'city': form.city.data,
            'gender': form.gender.data,
            'about_yourself': form.about_yourself.data,
            'profile_id': user.id_,
        }

        user_profile = Profile.query.filter_by(id=user.id_).first()
        if user_profile:
            try:
                user_profile.update(user_profile)
                db.session.commit()
                flash('Данные успешно обнавлены', 'success')
                return redirect(url_for('profile'))
            except Exception as error:
                flash('Что-то пошло не так', 'error')
                print(f'Error in new_datas {error}')

        try:
            user_profile = Profile(**user_datas)
            db.session.add(user_profile)
            db.session.commit()
            flash('Данные успешно добавлены', 'success')
            return redirect(url_for('profile'))

        except sqlite3.Error as error:
            flash('Что-то пошло не так', 'error')
            db.session.rollback()
            print(f'Произошла ошибка в new_data {error}')

    return render_template('new_datas.html', title='о себе', menu=main_menu, form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из акаунта', 'success')

    return redirect(url_for('index'))


@app.route('/registrate', methods=['GET', 'POST'])
def registrate():
    form = Registrate()

    if form.validate_on_submit():
        password_hash = generate_password_hash(form.second_password.data)

        user_datas = {
            'name': form.name.data,
            'email': form.email.data,
            'password': password_hash,
        }

        try:
            user = Users(**user_datas)
            db.session.add(user)
            db.session.commit()
            flash('Регистрация прошла успешно', 'success')
            return redirect(url_for('login'))
        except sqlite3.Error:
            db.session.rollback()
            flash('Что-то пошло не так', 'error')
            print('Произошла ошибка при добавлении пользователя /registrate')

    return render_template('registrate.html', title='регистрация', menu=main_menu, form=form)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
