from flask import render_template, redirect, flash, request, current_app, url_for
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, FirstRegistrationForm, SecondRegistrationForm,\
EmployerRegistrationForm, FreelancerForm
from app.models import User, Job, Role, Startup
from datetime import datetime

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    #post request
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash(_('Username does not exist'))
            return redirect(url_for('auth.login'))
        elif user.check_password(str(form.password.data)) is False:
            flash(_("Incorrect password. Try again."))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        flash(_("Login succesful"))
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def start_registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = FirstRegistrationForm()
    if form.validate_on_submit():
        """
        This should not be added first
        """
        user = User(username = form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.registration_date = datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        """
        This doesn't work.. how do we automatically log in a user after they have logged in?
        """
        return redirect(url_for('auth.second_registration', user=user.username))
    return render_template('start_registration.html', form=form)

@bp.route('/regiser/2', methods=['GET', 'POST'])
def second_registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.query.filter_by(username=request.args['user']).first()
    form = SecondRegistrationForm()
    if form.validate_on_submit():
        role = Role.query.filter_by(name=form.role.data).first()
        user.roles.append(role)
        db.session.add(role)
        db.session.commit()
        if user.employer():
            return redirect(url_for('auth.employer_registration', user=user.username))
        elif user.freelancer():
            return redirect(url_for('auth.freelancer_registration', user=user.username))
    return render_template('second_registration.html', title='Which are you?', form=form)

@bp.route('/register/employer', methods=['GET', 'POST'])
def employer_registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    """
    This passing of variables through the url needs to be fixed.
    Security concerns, maybe using a session variable?

    """
    user = User.query.filter_by(username=request.args['user']).first()
    form = EmployerRegistrationForm()
    if form.validate_on_submit():
        try:
            file = request.files['logo']
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        except KeyError:
            file_path = None
        startup_kwargs = {
        'company_name': form.company_name.data,
        'email': user.email,
        'state_of_incorporation': form.state_of_incorporation.data,
        'company_type': form.company_type.data,
        'taxID': form.taxID.data,
        'logo_data': file_path,
        'description': form.description.data
        }
        startup = Startup(**startup_kwargs)
        db.session.add(startup)
        user.create_startup(startup)
        db.session.commit()
        login_user(user)
        flash(_("Successfully registered your company %(company_name)s!", company_name=startup.company_name))
        return redirect(url_for('auth.login'))
    return render_template('employer_registration.html', title='Register your company!', form=form)

@bp.route('/register/freelancer', methods=['GET', 'POST'])
def freelancer_registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.query.filter_by(username=request.args['user']).first()
    form = FreelancerForm()
    if form.validate_on_submit():
        user.first, user.last, user.occupation, user.about_me, user.hours_a_week = form.first.data, \
        form.last.data, form.occupation.data, form.about_me.data, form.hours_a_week.data
        db.session.commit()
        login_user(user)
        flash(_("Successfully created profile!"))
        return redirect(url_for('auth.login'))
    return render_template('freelancer_registration.html', title='Register!', form=form)

@bp.route('/github')
def login_with_github():
    return "pass"

@bp.route('/linkedin')
def login_with_linkedin():
    return "pass"
