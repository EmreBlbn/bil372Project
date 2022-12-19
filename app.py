import psycopg2
from flask import Flask, render_template, request
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
import config
import logging

from users.forms import PatientForm

app = Flask(__name__)
app.debug = True
logging.basicConfig(level=logging.DEBUG)

POSTGRES_URL = config.CONFIG['postgresUrl']
POSTGRES_USER = config.CONFIG['postgresUser']
POSTGRES_PASS = config.CONFIG['postgresPass']
POSTGRES_PORT = config.CONFIG['postgresPort']
POSTGRES_DB = config.CONFIG['postgresDb']
DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PASS, url=POSTGRES_URL,
                                                      port=POSTGRES_PORT, db=POSTGRES_DB)
print(DB_URL)
app.config[
    'SECRET_KEY'] = 'mF4k_1tGfeNCxXz7g_mn7_mIfAlPBZ0lwrMCSVqH0BOnQQ75A11jEMrpI6MpmVvcuFG-8OhSnoQV8mH2Yiww4rXf-d5CwlMq'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_RECORD_QUERIES'] = True

db = SQLAlchemy(app)
bc = Bcrypt(app)
ma = Marshmallow(app)

login_manager = LoginManager(app)
login_manager.login_view = 'users.login'

# register dashboard app
from users.routes import users

app.register_blueprint(users)

# registered users app
from dashboard.routes import dashboard

app.register_blueprint(dashboard)


def get_db_connection():
    conn = psycopg2.connect(host=POSTGRES_URL,
                            database=POSTGRES_DB,
                            user=POSTGRES_USER,
                            password=POSTGRES_PASS)
    return conn


@app.route('/patient_info')
def patient_info():
    conn = get_db_connection()
    cur = conn.cursor()
    patient_form = PatientForm()
    if request.method == 'GET':
        return render_template('patient.html', patient_form=patient_form)

    if request.method == 'POST':
        if patient_form.validate_on_submit():
            cur.execute('SELECT * FROM patient WHERE p_tc=$patient_form.TC;')
            deneme = conn.cursor()
            deneme.execute('SELECT * FROM doctor;')
            books = cur.fetchall()
            books2 = deneme.fetchall()
            cur.close()
            deneme.close()
            conn.close()
    return render_template('patient.html', books=books, books2=books2)



