from flask import Flask, request, url_for, render_template, redirect, flash, g, session
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
    session["applicant"] = ""
    if not Applicant.select().where(Applicant.real_email == request.form["real_email"]):
        Applicant.create(**request.form.to_dict())
        flash('Succesfully applied to CODECOOL. You will receive an email with further information.')
        return redirect(url_for('homepage'))
    else:
        session["applicant"] = request.form.to_dict()
        flash('Email address already exists in our records')
        return redirect(url_for('application_form'))


@app.route('/apply', methods=['GET'])
def application_form():
    return render_template('application_form.html', applicant=session.get("applicant"))


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

with app.app_context():
    connect_to_db()
    build_tables()
    app.run(host="0.0.0.0", debug=True)
