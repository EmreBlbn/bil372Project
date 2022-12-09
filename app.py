import os
import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='hproje',
                            user='sammy',
                            password='password')
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM hasta;')
    books = cur.fetchall()
    cur.close()
    conn.close()
    print("hastalar")
    print("Boom" * 10)
    return render_template('index.html', books=books)