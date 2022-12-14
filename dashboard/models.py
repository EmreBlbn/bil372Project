from app import db


class Appointment(db.Model):
    __tablename__ = 'appointment'
    appo_no = db.Column(db.Integer, primary_key=True)
    on = db.Column(db.DateTime, nullable=False)
    pati_tc = db.Column(db.String(11), nullable=False)
    poly_name = db.Column(db.String(25), nullable=False)

    tc_pat = db.Column(db.Integer, db.ForeignKey('patient.p_tc'))
    appo_p = db.relationship(
        'Patient',
        back_populates='appos1',
        foreign_keys=[tc_pat])

    name_poly = db.Column(db.Integer, db.ForeignKey('polyclinic.pol_name'))
    appo_poly = db.relationship(
        'Polyclinic',
        back_populates='appos2',
        foreign_keys=[name_poly])


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
