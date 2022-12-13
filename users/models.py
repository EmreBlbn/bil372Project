from app import db, login_manager, app, bc
from flask import url_for, redirect, flash, render_template
from flask_login import UserMixin, current_user
from flask_admin import Admin as Administrator, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import inspect
from dashboard import models as dmodels


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


# Union with
class User(db.Model, UserMixin):
    __tablename__ = 'appuser'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    user_password = db.Column(db.String(15), nullable=False)
    user_type = db.Column(db.String(10))
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": user_type
    }

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return "USER_ID: {} , USERNAME: {} , PASSWORD: {} , TYPE: {} ".format(
            self.user_id, self.username, self.user_password, self.user_type)

    def to_dict(self):
        return dict({'id': self.user_id,
                     'username': self.username,
                     'password': self.user_password,
                     'type': self.user_type})

    def change_password(self, password):
        self.password = bc.generate_password_hash(password).decode('utf-8')

    @classmethod
    def create_user(cls, username, password):
        hashed_pw = bc.generate_password_hash(password).decode('utf-8')
        new_user = cls(username=username, password=hashed_pw)

        db.session.add(new_user)
        db.session.commit()

    def user_dashboard(self, user):
        pass


class Admin(User):
    __tablename__ = 'admin'
    user_id = db.Column(db.Integer, db.ForeignKey('appuser.user_id'), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }

    def __repr__(self):
        return super().__repr__()

    @classmethod
    def create_user(cls, username, password):
        super().create_user(username, password)

    def user_dashboard(self):
        return redirect('/admin')


class Doctor(User):
    __tablename__ = 'doctor'
    doctor_id = db.Column(db.Integer, db.ForeignKey('appuser.user_id'))
    doctor_tc = db.Column(db.String(11), primary_key=True)
    doctor_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    phone = db.Column(db.String(11))
    gender = db.Column(db.String(1))
    bdate = db.Column(db.DateTime)
    major = db.Column(db.String(25))

    # supervisor_tc = db.Column(db.String(11))
    #
    # supervisor = db.relationship(
    #     'doctor',
    #     back_populates='supervisee',
    #     foreign_keys=[supervisor_tc])

    def user_dashboard(self):
        return render_template("doctor_dashboard.html", user=self)

    __mapper_args__ = {
        "polymorphic_identity": "doctor",
    }

    def __repr__(self):
        return super().__repr__()

    @classmethod
    def create_user(cls, username, password):
        hashed_pw = bc.generate_password_hash(password).decode('utf-8')
        new_user = cls(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()


class Patient(User):
    __tablename__ = 'patient'
    p_id = db.Column(db.Integer, db.ForeignKey('appuser.user_id'))
    p_tc = db.Column(db.String(11), primary_key=True)
    p_name = db.Column(db.String(11), nullable=False)
    p_last_name = db.Column(db.String(11), nullable=False)
    p_phone = db.Column(db.String(11))
    p_address = db.Column(db.String(50))
    p_bdate = db.Column(db.DateTime)

    def user_dashboard(self):
        return render_template("patient_dashboard.html", user=self)

    __mapper_args__ = {
        "polymorphic_identity": "patient",
    }

    def __repr__(self):
        return super().__repr__()

    @classmethod
    def create_user(cls, username, password):
        hashed_pw = bc.generate_password_hash(password).decode('utf-8')
        new_user = cls(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()


class Polyclinic(User):
    __tablename__ = 'polyclinic'
    pol_id = db.Column(db.Integer, db.ForeignKey('appuser.user_id'))
    pol_name = db.Column(db.String(25), nullable=False, primary_key=True)
    pol_no = db.Column(db.String(1), nullable=False, primary_key=True)
    pol_location = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "polyclinic",
    }

    def __repr__(self):
        return super().__repr__()

    def user_dashboard(self):
        return render_template("polyclinic_dashboard.html", user=self)

    @classmethod
    def create_user(cls, username, password, field=None):
        hashed_pw = bc.generate_password_hash(password).decode('utf-8')
        new_user = cls(username=username, password=hashed_pw, field=field)
        db.session.add(new_user)
        db.session.commit()


class Laboratory(User):
    __tablename__ = 'laboratory'
    # lab_id = db.Column(db.Integer, db.ForeignKey('appuser.user_id'))
    # doc_tc = db.Column(db.String(11), nullable=False, db.ForeignKey('doctor.doctor_id'))
    # pat_tc = db.Column(db.String(11), nullable=False, db.ForeignKey('doctor.doctor_id'))
    # test_no = db.Column(db.String(10), nullable=False, primary_key=True)
    # lab_result = db.Column(db.String(100), nullable=False)
    #
    # __mapper_args__ = {
    #     "polymorphic_identity": "laboratory",
    # }
    #
    # def __repr__(self):
    #     return super().__repr__()
    #
    # @classmethod
    # def create_user(cls, username, password):
    #     super().create_user(username=username, password=password)
    #
    # def user_dashboard(self):
    #     return render_template("laboratory_dashboard.html", user=self)


class AdminView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.user_type == 'admin':
            return True
        return False

    def inaccessible_callback(self, **kwargs):
        flash('You are not allowed to enter admin section', 'error')
        return redirect(url_for('dashboard.profile'))


class UserView(ModelView):
    column_display_pk = True
    column_searchable_list = ['username']

    export_types = ['csv', 'json']
    column_exclude_list = ['password']
    form_edit_rules = ['user_id', 'username', 'user_type']
    form_excluded_columns = ['user_type']

    def create_model(self, form):
        form.password.data = bc.generate_password_hash(form.password.data)
        super().create_model(form)


class DoctorView(UserView):
    column_exclude_list = UserView.column_exclude_list[:].append('user_type')


class PatientView(UserView):
    column_exclude_list = UserView.column_exclude_list[:].append('user_type')


class PolyclinicView(UserView):
    column_exclude_list = UserView.column_exclude_list[:].append('user_type')


class LaboratoryView(UserView):
    column_exclude_list = UserView.column_exclude_list[:].append('user_type')


admin = Administrator(app, index_view=AdminView())
admin.add_view(UserView(User, db.session))
admin.add_view(DoctorView(Doctor, db.session))
admin.add_view(PatientView(Patient, db.session))
admin.add_view(PatientView(Polyclinic, db.session))
admin.add_view(LaboratoryView(Laboratory, db.session))

for name, obj in inspect.getmembers(dmodels, inspect.isclass):
    if name != 'datetime':
        admin.add_view(ModelView(obj, db.session))
