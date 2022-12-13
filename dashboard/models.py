from app import db


class Appointment(db.Model):
    __tablename__ = 'appointment'
    appo_id = db.Column(db.Integer, primary_key=True)
    on = db.Column(db.DateTime, nullable=False)
    patient_tc = db.Column(db.String, nullable=False)


class Treatment(db.Model):
    _tablename_ = 'treatment'
    diagnosis = db.Column(db.Integer, primary_key=True)
    treatment = db.Column(db.String(250))



