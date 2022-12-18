from app import db


class Appointment(db.Model):
    __tablename__ = 'appointment'
    on_date = db.Column(db.DateTime, nullable=False)
    patient_tc = db.Column(db.String(11), db.ForeignKey('patient.p_tc'), primary_key=True, nullable=False)
    poly_name = db.Column(db.String(25), db.ForeignKey('polyclinic.pol_name'), nullable=False)

    appo_p = db.relationship(
        'Patient',
        back_populates='appos1',
        foreign_keys=[patient_tc],
    )

    appo_poly = db.relationship(
        'Polyclinic',
        back_populates='appos2',
        foreign_keys=[poly_name])


class Treatment(db.Model):
    _tablename_ = 'treatment'
    diagnosis = db.Column(db.String(50))
    treatment = db.Column(db.String(250))

    d_tc = db.Column(db.String(11), db.ForeignKey('doctor.doctor_tc'), primary_key=True)
    treat_d = db.relationship(
        'Doctor',
        back_populates='treats1',
        foreign_keys=[d_tc])

    pa_tc = db.Column(db.String(11), db.ForeignKey('patient.p_tc'), primary_key=True)
    treat_p = db.relationship(
        'Patient',
        back_populates='treats2',
        foreign_keys=[pa_tc])
