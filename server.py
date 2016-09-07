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
    if not Applicant.select().where(Applicant.real_email == request.form["real_email"]):
        Applicant.create(**request.form.to_dict())
        flash('Succesfully applied to CODECOOL. You will receive an email with further information.')
        return (url_for('homepage'))
    else:
        flash('Email address already exists in our records')
        return application_form(request.form.to_dict())


@app.route('/apply', methods=['GET'])
def application_form(applicant=""):
    return render_template('application_form.html', applicant=applicant)


@app.route('/adminlogin', methods=['POST', 'GET'])
def admin_login():
    query = User.get()
    if request.method == 'POST':
        if request.form['user_name'] != query.user_name or request.form['password'] != query.password:
            flash('Invalid account. Try again')
            return render_template('login.html')
        else:
            return redirect(url_for('admin_page'))
    else:
        return render_template('login.html')


@app.route('/adminpage')
def admin_page():
    return render_template('admin_filterapplicant.html')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

with app.app_context():
    connect_to_db()
    build_tables()
    app.run(debug=True)
