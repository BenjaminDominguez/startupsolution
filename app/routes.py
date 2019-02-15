from app import app, db
from app.models import Startup, Job, User
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, FirstRegistrationForm, SecondRegistrationForm
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
    kwargs = {
    'jobs': [job for job in User.query.get(1).jobs],
    'month': 10,
    'day': 2,
    'year': 2014
    }
    return render_template('index.html', **kwargs)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Successfully logged in as a startup/freelancer!')
        return redirect(url_for('index'))
    form = LoginForm()
    #post request
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('No such user found')
            return redirect(url_for('login'))
        elif user.check_password(str(form.password.data)) is False:
            flash("Incorrect password. Try again.")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        """

        This needs to be reviewed at a later time

        """
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash("Login requested for Startup {0}, remember_me {1}"\
        .format(user.username, form.remember_me.data))
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def start_registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = FirstRegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        """
        This doesn't work.. how do we automatically log in a user after they have logged in?
        """
        return redirect(url_for('second_registration', user=user.username))
    return render_template('start_registration.html', form=form)

@app.route('/register2', methods=['GET', 'POST'])
def second_registration():
    user = User.query.filter_by(username=request.args['user']).first()
    form = SecondRegistrationForm()
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.commit()
        if form.role.data == "Employer":
            return redirect(url_for('employer_registration', user=user.username))
        elif form.role.data == "Freelancer":
            return redirect(url_for('freelancer_registration', user=user.username))
    return render_template('second_registration.html', title='Which are you?', form=form)

@app.route('/employer_registration')
def employer_registration():
    user = User.query.filter_by(username=request.args['user']).first()
    return "Employer registration {0}, {1}".format(user.username, user.role)

@app.route('/freelancer_registration')
def freelancer_registration():
    user = User.query.filter_by(username=request.args['user']).first()
    return "Freelancer registration {0}, {1}".format(user.username, user.role)
