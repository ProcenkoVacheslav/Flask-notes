from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length, Email, NumberRange, Optional


class Login(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=3, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Length(min=3, max=50), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Войти')


class Registrate(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=3, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Length(min=3, max=50), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6, max=20)])
    second_password = PasswordField('Повтор пароля', validators=[EqualTo('password')])
    submit = SubmitField('Зарегестрироваться')


class ElseInfo(FlaskForm):
    city = StringField('Город', validators=[Length(min=3, max=20), Optional()])
    age = IntegerField('Возраст', validators=[NumberRange(), Optional()])
    sure_name = StringField('Фамилия', validators=[Length(min=3, max=20), Optional()])
    about_yourself = StringField('О себе', validators=[Length(min=3, max=100), Optional()])
    gender = StringField('Пол', validators=[Length(min=3, max=20), Optional()])
    submit = SubmitField('Отправить')


class AddNote(FlaskForm):
    title = StringField('Название', validators=[Length(min=1, max=20), DataRequired()])
    task = StringField('Задача', validators=[Length(min=10, max=150), DataRequired()])
    submit = SubmitField('Добавить')
