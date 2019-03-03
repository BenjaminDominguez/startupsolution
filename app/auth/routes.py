from flask import render_template, redirect, flash, request, current_app, url_for
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, FreelancerRegistrationForm,\
EmployerRegistrationForm
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
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash(_('Email not currently registed with freeline'))
            return redirect(url_for('auth.login'))
        elif user.check_password(str(form.password.data)) is False:
            flash(_("Incorrect password. Try again."))
            return redirect(url_for('auth.login'))
        #have to add back remember me functionality later
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        flash(_("Login succesful"))
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def start_registration():
    return render_template('start_registration.html')

@bp.route('/regiser/2', methods=['GET', 'POST'])
def freelancer_registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = FreelancerRegistrationForm()
    if form.validate_on_submit():
        pass
    return render_template('freelancer_registration.html', form=form)

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

@bp.route('/github')
def login_with_github():
    return "pass"

@bp.route('/linkedin')
def login_with_linkedin():
    return "pass"
