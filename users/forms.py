from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Kullanici Adi', validators=[DataRequired()])
    password = PasswordField('Parola', validators=[DataRequired()])
    submit_button = SubmitField('Giris')


class PatientForm(FlaskForm):
    TC = StringField('TC Kimlik No:', validators=[DataRequired()])
    submit_button = SubmitField('Giris')


class AppForm(FlaskForm):
    name = StringField('Isim:')
    surname = StringField('Soy Isim:')
    password = PasswordField('Parola', validators=[DataRequired()])
    tckn = StringField('TC Kimlik Numarasi:')
    phone_number = StringField('Telefon Numarasi: ')
    submit_button = SubmitField('Giris')
