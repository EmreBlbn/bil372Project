from datetime import datetime

import psycopg2
from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
#from flask_sqlalchemy import or_

from app import db, POSTGRES_PASS, POSTGRES_USER, POSTGRES_DB, POSTGRES_URL
from dashboard.forms import AppointmentCreationForm, TreatmentCreationForm, PatientCreationForm, DoctorForm
from dashboard.models import Appointment, Treatment
from users.models import Patient, Polyclinic

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/')
@dashboard.route('/dashboard')
@login_required
def profile():
    return current_user.user_dashboard()


@dashboard.route('/make_appointment', methods=['GET', 'POST'])
@login_required
def create_appointment():
    form = AppointmentCreationForm()
    if request.method == 'GET':
        return render_template('appointment.html', form=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            patient = Patient.query.filter_by(p_tc=form.patient_tc.data).first()
            polyclinic = Polyclinic.query.filter_by(pol_name=form.polyclinic_name.data).first()
            new_appointment = Appointment(
                patient_tc=patient.p_tc,
                poly_name=polyclinic.pol_name,
                on_date=datetime.combine(form.on.data, form.hour.data),
            )
            if current_user.user_type == 'Patient':
                current_user.appos1.append(new_appointment)

            if current_user.user_type == 'Polyclinic':
                current_user.appos2.append(new_appointment)

            db.session.add(new_appointment)
            db.session.commit()
            flash('Randevu basariyla kaydedildi.')

    return render_template('appointment.html', form=form)


@dashboard.route('/create_new_patient', methods=['GET', 'POST'])
@login_required
def create_patient():
    conn = get_db_connection()
    usr_id_s = conn.cursor()
    usr_id_s.execute('SELECT user_id FROM appuser;')
    user_ids = usr_id_s.fetchall()
    patient_usrnames = conn.cursor()
    patient_usrnames.execute('SELECT p_name FROM patient, appuser where p_id=user_id;')
    # remove edildiginde appuser database'inden silinmeyip, patient database'inden silindigi icin
    # kullanici adi auto gen. icin yapildi.
    patient_usernames = patient_usrnames.fetchall()
    pat_tcs = conn.cursor()
    pat_tcs.execute('SELECT p_tc FROM patient;')
    patient_tc = pat_tcs.fetchall()

    patient_creation_form = PatientCreationForm()
    if request.method == 'GET':
        return render_template('create_patient.html', patient_creation_form=patient_creation_form)

    if request.method == 'POST':
        if patient_creation_form.validate_on_submit():
            new_patient = Patient(
                p_name=patient_creation_form.p_name.data,
                p_last_name=patient_creation_form.p_last_name.data,
                p_tc=patient_creation_form.p_tc.data,
                p_bdate=patient_creation_form.p_bdate.data,
                p_phone=patient_creation_form.p_phone.data,
                p_address=patient_creation_form.p_address.data,
                user_id=len(user_ids) + 1,
                username='pat' + str(len(patient_usernames) + 1),
                user_password='123456',
                user_type='Patient'
            )

            sameTCFlag = False
            for tc in patient_tc:
                print('length Ptc = ' + str(len(patient_tc)))
                if new_patient.p_tc == tc[0]:
                    flash('Hata Olustu : Insan mi klonluyoruz???.', 'error')
                    sameTCFlag = True

            if not sameTCFlag:
                db.session.add(new_patient)
                # ustteki komut:
                # INSERT INTO appuser (username, user_password, user_type) VALUES (%(username)s, %(user_password)s, %(user_type)s);
                db.session.commit()
                flash('Bilgi : Hasta bilgileri olusturuldu.', 'message')

    return render_template('create_patient.html', user=current_user,
                           patient_creation_form=patient_creation_form)


@dashboard.route('/register_new_treatment', methods=['GET', 'POST'])
@login_required
def register_new_treatment():
    treatment_creation_form = TreatmentCreationForm()
    if request.method == 'GET':
        return render_template('register_new_treatment.html', treatment_creation_form=treatment_creation_form)

    if request.method == 'POST':
        if treatment_creation_form.validate_on_submit():
            add_list = []
            new_treatment = Treatment(
                patient_tckn=treatment_creation_form.patient_tckn.data,
                diagnosis=treatment_creation_form.diagnosis.data,
                treatment=treatment_creation_form.treatment.data,
            )
            add_list.append(new_treatment)
            db.session.commit()
            flash('Tedavi olusturuldu.')

    return render_template('register_new_treatment.html', user=current_user,
                           treatment_creation_form=treatment_creation_form)


@dashboard.route('/list_patient', methods=['GET', 'POST'])
@login_required
def list_patient():
    patients = Patient.query.all()
    print(get_debug_queries())
    if request.method == "POST":
        id = request.form['button-delete']
        Patient.query.filter_by(p_id=id).delete()
        db.session.commit()
        patients = Patient.query.all()
        return render_template('list_patient.html', patients=patients)
    return render_template('list_patient.html', patients=patients)


@dashboard.route('/list_treatments', methods=['GET', 'POST'])
@login_required
def list_treatments():
    treatments = Treatment.query.all()
    print(get_debug_queries())
    if request.method == "POST":
        id = request.form['button-delete']
        Treatment.query.filter_by(patient_tc=id).delete()
        db.session.commit()
        treatments = Treatment.query.all()
        return render_template('list_treatments.html', treatments=treatments)
    return render_template('list_treatments.html', treatments=treatments)

@dashboard.route('/delete_patient', methods=['GET'])
@login_required
def delete_patient():
    p_id = request.args['button-delete']
    temp_patient = Patient.query.filter_by(p_id=p_id)
    Patient.query.filter_by(patient_id=p_id).delete()
    db.session.commit()
    return jsonify({'msg': "{} silindi.".format(temp_patient.p_name)})


@dashboard.route('/display_registers', methods=['GET', 'POST'])
@login_required
def display_registers():
    if current_user.user_type == 'Patient':
        appointments = current_user.appos1

    if current_user.user_type == 'Polyclinic':
        appointments = current_user.appos2

    if request.method == "POST":
        id = request.form['button-delete']
        Appointment.query.filter_by(appo_id=id).delete()
        db.session.commit()
        appointments = Appointment.query.all()
        return render_template('display_registers.html', appointments=appointments)

    return render_template('display_registers.html', appointments=appointments)




@dashboard.route('/search_patient', methods=['POST'])
@login_required
def search_patient():
    if request.form['text'] == "":
        return jsonify({})
    patients = Patient.query.filter(

            Patient.p_tc.ilike("%" + request.form['text'] + "%") |
            Patient.p_name.ilike("%" + request.form['text'] + "%")

    ).all()
    results = [p.to_dict() for p in patients]
    print(patients)
    return jsonify({'query': results})


@dashboard.route('/delete_appointment', methods=['GET'])
@login_required
def delete_appointment():
    appo_id = request.args['button-delete']
    temp_appo = Appointment.query.filter_by(appo_id=appo_id)
    Appointment.query.filter_by(appo_id=appo_id).delete()
    db.session.commit()
    return jsonify({'msg': "{} silindi.".format(temp_appo.appo_id)})


@dashboard.route('/profile', methods=['GET', 'POST'])
@login_required
def profile2():
    doctor = DoctorForm()
    user = current_user.query.filter_by().first()
    return render_template('profile.html', user=user, doctor=doctor)


def get_db_connection():
    conn = psycopg2.connect(host=POSTGRES_URL,
                            database=POSTGRES_DB,
                            user=POSTGRES_USER,
                            password=POSTGRES_PASS)
    return conn


def layout():
    conn = get_db_connection()
    usr_id_s = conn.cursor()
    usr_id_s.execute('SELECT user_id FROM appuser where user_type=\'Patient\';')
    not_patient = True
    pat_id_s = usr_id_s.fetchall()
    usr = current_user.current_user.query.filter_by().first().user_id
    for id in pat_id_s:
        if id == current_user.current_user.query.filter_by().first().user_id:
            not_patient = False
    usr_id_s.close()
    conn.close()
    return render_template('layout.html', not_patient=not_patient, usr=usr)
