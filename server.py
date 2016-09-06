from flask import Flask, request, url_for, render_template, redirect, flash
from models import *
from applicant import *

app = Flask('school_system-l4me')


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/apply', methods=['POST'])
def applicant_apply():
    Applicant.create(**request.form.to_dict())
    flash('Succesfully applied to CODECOOL. You will receive an email with further information.')
    return redirect(url_for('homepage'))


@app.route('/apply', methods=['GET'])
def applicant_apply():
    return render_template('application_form.html')


with app.app_context():
    app.run(debug=True)
