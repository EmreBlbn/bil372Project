from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.fields import DateField, TimeField
from wtforms.validators import DataRequired


class DoctorForm(FlaskForm):
    name = StringField('Ad:', validators=[DataRequired()])
    last_name = StringField('Soyad:', validators=[DataRequired()])
    gender = RadioField('Cinsiyet:', choices=['M', 'F'])
    phone = StringField('Telefon:', validators=[DataRequired()])
    doctor_tc = StringField('TC No:', validators=[DataRequired()])
    major = StringField('Brans:')
    bdate = DateField('Dogum Tarihi:')
    submit_button = SubmitField('Hasta Kaydet')


class PatientCreationForm(FlaskForm):
    p_name = StringField('Ad:', validators=[DataRequired()])
    p_last_name = StringField('Soyad:', validators=[DataRequired()])
    p_phone = StringField('Telefon:', validators=[DataRequired()])
    p_tc = StringField('TC No:', validators=[DataRequired()])
    p_address = StringField('Adres:')
    p_bdate = DateField('Dogum Tarihi:')
    # username = StringField('Kullanici Adi:', validators=[DataRequired()])
    # user_password = StringField('Sifre:', validators=[DataRequired()])
    submit_button = SubmitField('Hasta Kaydet')


class AppointmentCreationForm(FlaskForm):
    on = DateField('Tarih:')
    hour = TimeField('Saat:')
    patient_tc = StringField('Hasta:', validators=[DataRequired()])
    submit_button = SubmitField('Yarat')


class TreatmentCreationForm(FlaskForm):
    diagnosis = StringField('Tani:')
    treatment = StringField('Tedavi: ')
    submit_button = SubmitField('Yarat')
