from app import app, db
from app.models import Startupcreator, Startup, Job, Developer
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    kwargs = {
    'user': Developer.query.get(1),
    'jobs': [job for job in Developer.query.get(1).jobs],
    'month': 10,
    'day': 2,
    'year': 2014
    }
    return render_template('index.html', **kwargs)
