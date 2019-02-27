from app.employer import bp
from flask import redirect, url_for, abort, render_template, request
from app.models import User, Job, Startup, Role
from flask_login import login_required, current_user
from app.special import roles_required
from app import db
from flask_babel import _, lazy_gettext as _l
from app.employer.forms import EditCompanyForm, PostNewJobForm, EditJobForm, DeleteJobForm

@bp.route('/<company_name>', methods=['GET', 'POST'])
@login_required
@roles_required(['Employer'])
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
    logo_url = None
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
    return render_template('company.html', **kwargs)

@bp.route('/<company_name>/edit_profile', methods=['GET', 'POST'])
@login_required
@roles_required(['Employer'])
def company_edit_profile(company_name):
    company = Startup.query.filter_by(company_name = company_name).first_or_404()
    if current_user.startup.first() != company:
        abort(404)
    form = EditCompanyForm()
    if form.validate_on_submit():
        company.description = form.description.data
        db.session.commit()
        flash(_('Succesfully made changes'))
    if request.method == 'GET':
        form.description.data = company.description
    return render_template('edit_company_profile.html', title='Edit your profile', form = form)

@bp.route('/<company_name>/new_job_posting', methods=['GET', 'POST'])
@login_required
@roles_required(['Employer'])
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
        flash(_('Successfully created new job'))
        return redirect(url_for('employer.company', company_name=company_name))
    return render_template('new_job_listing.html', title='Create new job listing', form=form)

@bp.route('/<company_name>/<job_name>/delete_job')
@login_required
@roles_required(['Employer'])
def delete_job(company_name, job_name):
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('company', company_name=company_name))

@bp.route('/<company_name>/<job_name>/edit_job', methods=['GET', 'POST'])
@login_required
@roles_required(['Employer'])
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
            flash(_('Password or username incorrect.'))
            return redirect(url_for('edit_job_details', company_name=company_name, job_name=job_name))
    if editform.validate_on_submit():
        job.name = editform.name.data
        job.job_description = editform.job_description.data
        job.offer_price = editform.offer_price.data
        job.job_type = editform.job_type.data
        job.estimated_developement_time = editform.estimated_developement_time.data
        job.equity_job = editform.equity_job.data
        db.session.commit()
        flash(_("Changes saved."))
        return redirect(url_for('edit_job_details', company_name=company_name, job_name=job_name))
    if request.method == 'GET':
        editform.name.data = job.name
        editform.job_description.data = job.job_description
        editform.offer_price.data = job.offer_price
        editform.job_type.data = job.job_type
        editform.estimated_developement_time.data = job.estimated_developement_time
        editform.equity_job.data = job.equity_job
    return render_template('company/edit_job_form.html', title='Edit Job Details', editform=editform, deleteform=deleteform)

@bp.route('/post_job', methods=['GET', 'POST'])
@login_required
def post_job():
    return "pass"
