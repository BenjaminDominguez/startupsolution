from app import app, db
import os
from app.models import Startup, Job, User
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, FirstRegistrationForm, SecondRegistrationForm,\
EmployerRegistrationForm, FreelancerForm, EditProfileForm, UploadProfilePic
from werkzeug.urls import url_parse
from werkzeug import secure_filename
from datetime import datetime

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
            flash('Username does not exist')
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
    return render_template('registration/start_registration.html', form=form)

@app.route('/regiser/2', methods=['GET', 'POST'])
def second_registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.query.filter_by(username=request.args['user']).first()
    form = SecondRegistrationForm()
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.commit()
        if form.role.data == "Employer":
            return redirect(url_for('employer_registration', user=user.username))
        elif form.role.data == "Freelancer":
            return redirect(url_for('freelancer_registration', user=user.username))
    return render_template('registration/second_registration.html', title='Which are you?', form=form)

@app.route('/register/employer', methods=['GET', 'POST'])
def employer_registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    """
    This passing of variables through the url needs to be fixed.
    Security concerns, maybe using a session variable?

    """
    user = User.query.filter_by(username=request.args['user']).first()
    form = EmployerRegistrationForm()
    if form.validate_on_submit():
        startup_kwargs = {
        'company_name': form.company_name.data,
        'state_of_incorporation': form.state_of_incorporation.data,
        'company_type': form.company_type.data,
        'taxID': form.taxID.data
        }
        startup = Startup(**startup_kwargs)
        db.session.add(startup)
        user.create_startup(startup)
        db.session.commit()
        login_user(user)
        flash("Successfully registered {0} with company {1}".format(user.username, startup.company_name))
        return redirect(url_for('login'))
    return render_template('registration/employer_registration.html', title='Register your company!', form=form)

@app.route('/register/freelancer', methods=['GET', 'POST'])
def freelancer_registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.query.filter_by(username=request.args['user']).first()
    form = FreelancerForm()
    if form.validate_on_submit():
        user.first, user.last, user.occupation, user.about_me = form.first.data, \
        form.last.data, form.occupation.data, form.about_me.data
        db.session.commit()
        login_user(user)
        flash("Successfully created user profile {0}, with first {1} and last {2}".format(user.username, user.first, user.last))
        return redirect(url_for('login'))
    return render_template('registration/freelancer_registration.html', title='Register!', form=form)

@app.route('/freelancers/available')
def freelancers_available():
    return render_template("dashboards/freelancers_available.html", u=User)

@app.route('/employers/jobs')
def jobs_available():
    return render_template("dashboards/jobs_available.html", title='Jobs available', j=Job)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    jobs = [job for job in user.jobs]
    no_profile_pic = bool(user.avatar_data is None)
    avatar_url=None
    if not no_profile_pic:
        url = user.avatar_data.split('/')
        avatar_url = "/{0}/{1}".format(url[-2], url[-1])
    return render_template('/user/user.html', user=user, jobs=jobs, no_jobs=bool(len(jobs) == 0), no_profile_pic=no_profile_pic, avatar_url=avatar_url)
"""
The before request decorator allows me to
run this function before any other view function.
This function simply checks if the current user is logged in
and if they are, set the last seen to utcnow()
"""
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        #check if username already exists
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved!")
        return redirect(url_for('edit_profile'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('user/edit_profile.html', title='Edit Profile', form=form)

@app.route('/upload_profile_pic', methods=['GET', 'POST'])
@login_required
def upload_profile_pic():
    form = UploadProfilePic()
    if form.validate_on_submit():
        file = request.files['profile_pic']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        current_user.avatar_data = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        flash("Succesfully submitted profile pic!")
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))
    return render_template('user/upload_profile_pic.html', title='Upload Profile Pic', form=form)

@app.route('/github')
def login_with_github():
    return "pass"

@app.route('/linkedin')
def login_with_linkedin():
    return "pass"
