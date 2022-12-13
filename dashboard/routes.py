from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user

from flask_sqlalchemy import get_debug_queries

from dashboard.forms import AppointmentCreationForm, TreatmentCreationForm, PatientForm, DoctorForm, PatientCreationForm
from dashboard.models import Appointment, Treatment
from datetime import datetime

from app import db
from users.models import Patient

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
            patient = Patient.query.filter_by(tc=form.patient_tc.data).first()
            new_appointment = Appointment(
                patient_tc=patient.p_tc,
                on=datetime.combine(form.on.data, form.hour.data),
            )
            current_user.appos.append(new_appointment)

            patient.appointments.append(new_appointment)

            db.session.add(new_appointment)
            db.session.commit()
            flash('Randevu basariyla kaydedildi.')

    return render_template('appointment.html', form=form)


@dashboard.route('/create_patient', methods=['GET', 'POST'])
@login_required
def create_patient():  # TODO bos is, kullanim yok
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
            )
            db.session.add(new_patient)
            db.session.commit()
            flash('Hasta bilgileri olusturuldu.')
    return None


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


@dashboard.route('/delete_patient', methods=['GET'])
@login_required
def delete_patient():
    p_id = request.args['button-delete']
    temp_patient = Patient.query.filter_by(p_id=p_id)
    Patient.query.filter_by(patiet_id=p_id).delete()
    db.session.commit()
    return jsonify({'msg': "{} silindi.".format(temp_patient.p_name)})


@dashboard.route('/display_registers', methods=['GET', 'POST'])
@login_required
def display_registers():
    appointments = current_user.appos
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
    patients = Patient.query.filter(Patient.name.like("%" + request.form['text'] + "%")).all()
    results = [p.to_dict() for p in patients]
    return jsonify({'query': results})


@dashboard.route('/delete_appointment', methods=['GET'])
@login_required
def delete_appointment():
    appo_id = request.args['button-delete']
    temp_appo = Appointment.query.filter_by(appo_id=appo_id)
    Appointment.query.filter_by(appo_id=appo_id).delete()
    db.session.commit()
    return jsonify({'msg': "{} silindi.".format(temp_appo.appo_id)})

# @dashboard.route('/profile', methods=['GET', 'POST'])
# @login_required
# def profile2():
#     doctor = DoctorForm()
#     user = current_user.query.filter_by().first()
#     return render_template('profile.html', user=user, doctor=doctor)
