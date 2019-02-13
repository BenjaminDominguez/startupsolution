from app import app, db
from app.models import Startupcreator, Startup, Job, Developer
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from app.forms import LoginForm

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

@app.route('/userprofile')
def user_profile():
    return render_template('user_profile.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {0}, remember_me={1}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
