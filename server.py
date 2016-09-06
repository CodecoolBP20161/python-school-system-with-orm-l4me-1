from flask import Flask, request, url_for, render_template, redirect, flash, g
from models import *
from applicant import *
from build import *

SECRET_KEY = 'l4me is cool'
app = Flask('school_system-l4me')
app.config.from_object(__name__)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/apply', methods=['POST'])
def applicant_apply():
    Applicant.create(**request.form.to_dict())
    flash('Succesfully applied to CODECOOL. You will receive an email with further information.')
    return redirect(url_for('homepage'))


@app.route('/apply', methods=['GET'])
def application_form():
    return render_template('application_form.html')


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

with app.app_context():
    connect_to_db()
    build_tables()
    app.run(debug=True)
