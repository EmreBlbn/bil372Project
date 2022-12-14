from flask import Blueprint, flash
from flask import render_template, redirect, url_for, request
from users.models import User
from flask_login import login_required, login_user, current_user, logout_user
from users.forms import LoginForm
from app import bc

users = Blueprint('users', __name__)


@users.route('/', methods=['GET', 'POST'])
@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user and user.user_password:
                login_user(user)
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for('dashboard.profile'))
            else:
                flash('Incorrect email or password!')
                return render_template('login.html', form=form)
        else:
            print("No Username Exists")

    return render_template('login.html', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))
