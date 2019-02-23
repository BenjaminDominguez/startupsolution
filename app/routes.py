from app import app, db
import os
from app.models import Startup, Job, User
from flask import render_template, flash, redirect, url_for, request, abort, session
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, FirstRegistrationForm, SecondRegistrationForm,\
EmployerRegistrationForm, FreelancerForm, EditProfileForm, UploadProfilePic, EditCompanyForm,\
PostNewJobForm, DeleteJobForm, EditJobForm
from werkzeug.urls import url_parse
from werkzeug import secure_filename
from datetime import datetime

# The before request decorator allows me to
# run this function before any other view function.
# This function simply checks if the current user is logged in
# and if they are, set the last seen to utcnow()

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

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
        flash("Login succesful")
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
        file = request.files['logo']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        startup_kwargs = {
        'company_name': form.company_name.data,
        'email': user.email,
        'state_of_incorporation': form.state_of_incorporation.data,
        'company_type': form.company_type.data,
        'taxID': form.taxID.data,
        'logo_data': os.path.join(app.config['UPLOAD_FOLDER'], filename),
        'description': description
        }
        startup = Startup(**startup_kwargs)
        db.session.add(startup)
        user.create_startup(startup)
        db.session.commit()
        login_user(user)
        flash("Successfully registered your company {1}!".format(startup.company_name))
        return redirect(url_for('login'))
    return render_template('registration/employer_registration.html', title='Register your company!', form=form)

@app.route('/register/freelancer', methods=['GET', 'POST'])
def freelancer_registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.query.filter_by(username=request.args['user']).first()
    form = FreelancerForm()
    if form.validate_on_submit():
        user.first, user.last, user.occupation, user.about_me, user.hours_a_week = form.first.data, \
        form.last.data, form.occupation.data, form.about_me.data, form.hours_a_week.data
        db.session.commit()
        login_user(user)
        flash("Successfully created profile!")
        return redirect(url_for('login'))
    return render_template('registration/freelancer_registration.html', title='Register!', form=form)

@app.route('/freelancers_available')
def freelancers_available():
    page = request.args.get('page', 1, type=int)
    most_recently_active = User.query.filter_by(role="Freelancer").\
    order_by(User.last_seen.desc()).paginate(page,\
    app.config['FREELANCERS_PER_PAGE'], False)
    next_url = (url_for('freelancers_available', page=most_recently_active.next_num)\
    if most_recently_active.has_next else None)
    prev_url = (url_for('freelancers_available', page=most_recently_active.prev_num)\
    if most_recently_active.has_prev else None)
    return render_template("dashboards/freelancers_available.html",\
    freelancers = most_recently_active.items,\
    next_url=next_url, prev_url=prev_url)

@app.route('/jobs')
def jobs_available():
    page = request.args.get('page', 1, type=int)
    jobs = Job.query.order_by(Job.posted_on.desc()).paginate(
    page, app.config['JOBS_PER_EXPLORE_PAGE'], False
    )
    next_url = (url_for('jobs_available', page=jobs.next_num) if jobs.has_next else None)
    prev_url = (url_for('jobs_available', page=jobs.prev_num) if jobs.has_prev else None)
    return render_template("dashboards/jobs_available.html", title='Jobs available',\
    jobs=jobs.items, next_url=next_url, prev_url=prev_url)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    jobs = [job for job in user.jobs]
    #set outside of the conditional because need to use profile_pic as a variable later
    profile_pic = user.avatar_data is not None
    if profile_pic:
        url = user.avatar_data.split('/')
        avatar_url = "/{0}/{1}".format(url[-2], url[-1])
        session['avatar_url'] = avatar_url
        session['profile_pic'] = True
    else:
        avatar_url = None
    return render_template('user/user_profile.html', user=user, jobs=jobs, no_jobs=bool(len(jobs) == 0),\
    profile_pic=profile_pic, avatar_url=avatar_url, home_active=True)

@app.route('/user/<username>/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EditProfileForm(username)
    if form.validate_on_submit():
        #check if username already exists
        current_user.username = form.username.data
        username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved!")
        return redirect(url_for('edit_profile', username=username))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('user/edit_profile.html', title='Edit Profile', form=form, user=user, avatar_url=session.get('avatar_url'), edit_active=True,\
    profile_pic=session.get('profile_pic'))

@app.route('/user/<username>/current_jobs')
@login_required
def current_jobs(username):
    user = User.query.filter_by(username=username).first_or_404()
    jobs = [job for job in user.jobs]
    return render_template('user/current_jobs.html', username=username, profile_pic=session.get('profile_pic'),\
    current_jobs_active=True, user=user, avatar_url=session.get('avatar_url'), jobs=jobs)

@app.route('/company/<company_name>', methods=['GET', 'POST'])
@login_required
def company(company_name):
    company = Startup.query.filter_by(company_name=company_name).first_or_404()
    # for now, but I have to see how competitors treat this
    form = PostNewJobForm()
    is_admin = (current_user.startup.first() == company)
    if is_admin:
        jobs = company.jobs
        no_jobs = (len([job for job in jobs]) == 0)
    else:
        jobs, no_jobs = None, True
    logo_pic = company.logo_data is not None
    if logo_pic:
        url = company.logo_data.split('/')
        logo_url = "/{0}/{1}".format(url[-2], url[-1])
    if form.validate_on_submit():
        kwargs = {
        'name': form.name.data,
        'job_description': form.job_description.data,
        'offer_price': form.offer_price.data,
        'job_type': form.job_type.data,
        'estimated_developement_time': form.estimated_developement_time.data,
        'equity_job': form.equity_job.data
        }
        job = Job(**kwargs)
        job.post_job_time()
        db.session.add(job)
        company.create_job(job)
        db.session.commit()
        flash('Successfully created new job')
        return redirect(url_for('company', company_name=company_name))
    kwargs= {
    'title': company_name,
    'company_name': company_name,
    'company': company,
    'is_admin': is_admin,
    'jobs': jobs,
    'no_jobs': no_jobs,
    'logo_url': logo_url,
    'form': form
    }
    return render_template('company/company.html', **kwargs)

@app.route('/company/<company_name>/edit_profile', methods=['GET', 'POST'])
@login_required
def company_edit_profile(company_name):
    company = Startup.query.filter_by(company_name = company_name).first_or_404()
    if current_user.startup.first() != company:
        abort(404)
    form = EditCompanyForm()
    if form.validate_on_submit():
        company.description = form.description.data
        db.session.commit()
        flash('Succesfully made changes')
    if request.method == 'GET':
        form.description.data = company.description
    return render_template('company/edit_company_profile.html', title='Edit your profile', form = form)

@app.route('/company/<company_name>/new_job_posting', methods=['GET', 'POST'])
def new_job_posting(company_name):
    company = Startup.query.filter_by(company_name=company_name).first_or_404()
    is_admin = (current_user.startup.first() == company)
    if not current_user.is_authenticated or not is_admin:
        abort(404)
    form = PostNewJobForm()
    if form.validate_on_submit():
        kwargs = {
        'name': form.name.data,
        'job_description': form.job_description.data,
        'offer_price': form.offer_price.data,
        'job_type': form.job_type.data,
        'estimated_developement_time': form.estimated_developement_time.data,
        'equity_job': form.equity_job.data
        }
        job = Job(**kwargs)
        job.post_job_time()
        db.session.add(job)
        company.create_job(job)
        db.session.commit()
        flash('Successfully created new job')
        return redirect(url_for('company', company_name=company_name))
    return render_template('company/new_job_listing.html', title='Create new job listing', form=form)

"""

This is not working right now
"""
@app.route('/company/<company_name>/<job_name>/delete_job')
@login_required
def delete_job(company_name, job_name):
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('company', company_name=company_name))

@app.route('/company/<company_name>/<job_name>/edit_job', methods=['GET', 'POST'])
@login_required
def edit_job_details(company_name, job_name):
    deleteform = DeleteJobForm()
    editform = EditJobForm()
    job = Job.query.filter_by(name = job_name).first_or_404()
    admin = Startup.query.filter_by(company_name=company_name).first_or_404().admin
    if admin.username is not current_user.username:
        abort(404)
    if deleteform.validate_on_submit():
        if (deleteform.username.data == admin.username)\
         and (admin.check_password(deleteform.password.data)):
            db.session.delete(job)
            db.session.commit()
            flash("Job '{0}' deleted".format(job.name))
            return redirect(url_for('company', company_name=company_name))
        else:
            flash('Password or username incorrect.')
            return redirect(url_for('edit_job_details', company_name=company_name, job_name=job_name))
    if editform.validate_on_submit():
        job.name = editform.name.data
        job.job_description = editform.job_description.data
        job.offer_price = editform.offer_price.data
        job.job_type = editform.job_type.data
        job.estimated_developement_time = editform.estimated_developement_time.data
        job.equity_job = editform.equity_job.data
        db.session.commit()
        flash("Changes saved.")
        return redirect(url_for('edit_job_details', company_name=company_name, job_name=job_name))
    if request.method == 'GET':
        editform.name.data = job.name
        editform.job_description.data = job.job_description
        editform.offer_price.data = job.offer_price
        editform.job_type.data = job.job_type
        editform.estimated_developement_time.data = job.estimated_developement_time
        editform.equity_job.data = job.equity_job
    return render_template('company/edit_job_form.html', title='Edit Job Details', editform=editform, deleteform=deleteform)


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

@app.route('/aboutus')
def about_us():
    return render_template('about_us.html')

@app.route('/post_job', methods=['GET', 'POST'])
@login_required
def post_job():
    return "pass"

@app.route('/github')
def login_with_github():
    return "pass"

@app.route('/linkedin')
def login_with_linkedin():
    return "pass"
