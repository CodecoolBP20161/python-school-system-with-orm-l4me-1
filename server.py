from flask import Flask, request, url_for, render_template, redirect, flash, g, session
from models import *
from applicant import *
from build import *
from functools import wraps
from school import *
from mentor import *

SECRET_KEY = 'l4me is cool'
app = Flask('school_system-l4me')
app.config.from_object(__name__)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('admin_login'))
    return wrap


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/apply', methods=['POST'])
def applicant_apply():
    if not Applicant.select().where(Applicant.real_email == request.form["real_email"]):
        Applicant.create(**request.form.to_dict())
        flash('Succesfully applied to CODECOOL. You will receive an email with further information.')
        return redirect(url_for('homepage'))
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
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('admin_page'))
    else:
        return redirect(url_for('admin_page')) if session.get('logged_in') else render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('homepage'))


@app.route('/adminpage', methods=['GET', 'POST'])
@login_required
def admin_page():
    query = Applicant.select()
    subfilter = ""
    applied_filter = ""
    if request.method == 'POST':
        if request.form.get('main_filter'):
            main_filter = request.form['main_filter']
            if request.form.get(main_filter):
                subfilter = request.form[main_filter]
            elif main_filter == 'time' and request.form['to_date']:
                subfilter = request.form['from_date']
                applied_filter = "{} / {}".format(subfilter, request.form['to_date'])
            if subfilter:
                applied_filter = (applied_filter or Applicant.STATUSDICT.get(int(subfilter))
                                  if subfilter.isdigit() else subfilter)
                if main_filter == 'mentor':
                    mentor = Mentor.get(Mentor.id == subfilter)
                    query = InterviewSlot.filter_applicant_by_mentor(mentor=mentor)
                    applied_filter = mentor.full_name
                else:
                    if main_filter == 'school':
                        applied_filter = School.get(School.id == subfilter).location
                    query = Applicant.filter_applicant(filter_by=main_filter, value=subfilter,
                                                       value_2=request.form['to_date'])
            else:
                flash('Please fill the subfilter')
    return render_template('admin_filterapplicant.html', records=query,
                           schools=School.select(), mentors=Mentor.select(),
                           last_search=applied_filter or 'ALL RECORDS')


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

with app.app_context():
    connect_to_db()
    build_tables()
    app.run(debug=True, host='0.0.0.0')
