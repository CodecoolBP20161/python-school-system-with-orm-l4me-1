from flask import Flask, request, url_for, render_template, redirect, flash, g, session
from models import *
from applicant import *
from build import *
from functools import wraps
from school import *
from mentor import *
from menulink import *

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


def applicant_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'applicant_logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('applicant_login'))
    return wrap


@app.route('/')
def homepage():
    menulist = [Menulink(text="Apply to CODECOOL", href="applicant_apply", css_class="highlight"),
                Menulink(text="Applicant login", href="applicant_login", css_class="normal"),
                Menulink(text="Mentor login", href="homepage", css_class="normal"),
                Menulink(text="Admin login", href="admin_login", css_class="normal")]
    return render_template('home.html', menu_list=menulist)


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
    menulist = [Menulink(text="Apply to CODECOOL", href="applicant_apply", css_class="highlight"),
                Menulink(text="Applicant login", href="applicant_login", css_class="normal"),
                Menulink(text="Mentor login", href="homepage", css_class="normal"),
                Menulink(text="Admin login", href="admin_login", css_class="normal")]
    return render_template('application_form.html', applicant=applicant, menu_list=menulist)


@app.route('/applicantlogin', methods=['POST', 'GET'])
def applicant_login():
    if request.method == 'POST':
        query = Applicant.select().where(Applicant.application_code == request.form['app_code'], Applicant.real_email == request.form['application_email'])
        if not query:
            flash('Invalid account. Try again')
            return render_template('applicant_login_form.html')
        else:
            session['applicant_logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('applicant_profile'))
    else:
        menulist = [Menulink(text="Apply to CODECOOL", href="applicant_apply", css_class="highlight"),
                    Menulink(text="Applicant login", href="applicant_login", css_class="normal"),
                    Menulink(text="Mentor login", href="homepage", css_class="normal"),
                    Menulink(text="Admin login", href="admin_login", css_class="normal")]
        return redirect(url_for('applicant_profile')) if session.get('applicant_logged_in') else render_template('applicant_login_form.html', menu_list=menulist)


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
        menulist = [Menulink(text="Apply to CODECOOL", href="applicant_apply", css_class="highlight"),
                    Menulink(text="Applicant login", href="applicant_login", css_class="normal"),
                    Menulink(text="Mentor login", href="homepage", css_class="normal"),
                    Menulink(text="Admin login", href="admin_login", css_class="normal")]
        if session.get('logged_in'):
            return redirect(url_for('admin_page'))
        else:
            return render_template('login.html', menu_list=menulist)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('homepage'))


@app.route('/applogout')
@applicant_login_required
def applicant_logout():
    session.pop('applicant_logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('homepage'))


@app.route('/adminpage', methods=['POST'])
@login_required
def admin_filter():
    menulist = [Menulink(text="Filter Applicants", href="admin_page", css_class="normal"),
                Menulink(text="Logout", href="logout", css_class="logout")]
    query = Applicant.select()
    subfilter = ""
    applied_filter = ""
    main_filter = request.form['main_filter']
    if request.form.get(main_filter):
        subfilter = request.form[main_filter]
    elif main_filter == 'time' and request.form['to_date']:
        subfilter = request.form['from_date']
        applied_filter = "{} / {}".format(subfilter, request.form['to_date'])
    if subfilter:
        applied_filter = (applied_filter or (Applicant.STATUSDICT.get(int(subfilter))
                          if subfilter.isdigit() else subfilter))
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
                           last_search=applied_filter or 'ALL RECORDS', menu_list=menulist)


@app.route('/adminpage', methods=['GET'])
@login_required
def admin_page():
    menulist = [Menulink(text="Filter Applicants", href="admin_page", css_class="normal"),
                Menulink(text="Logout", href="logout", css_class="logout")]
    return render_template('admin_filterapplicant.html', records=Applicant.select(), schools=School.select(),
                           mentors=Mentor.select(), last_search='ALL RECORDS', menu_list=menulist)


@app.route('/applicantprofile')
@applicant_login_required
def applicant_profile():
    menulist = [Menulink(text="My profile", href="applicant_profile", css_class="normal"),
                Menulink(text="Logout", href="applicant_logout", css_class="logout")]
    return render_template('applicant_profile.html', menu_list=menulist)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

with app.app_context():
    connect_to_db()
    build_tables()
    app.run(debug=True, host='0.0.0.0')
