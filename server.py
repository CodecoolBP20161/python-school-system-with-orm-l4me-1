from flask import Flask, request, url_for, render_template, redirect
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
    appl = Applicant.get()
    return appl.full_name

with app.app_context():
    app.run(debug=True)
