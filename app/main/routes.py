from app.main import bp
from flask_login import current_user, login_required
from flask import request, url_for, redirect, render_template, current_app
from datetime import datetime
from app.special import roles_required
from app import db
from app.models import User, Job, Startup

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/freelancers')
def freelancers_available():
    page = request.args.get('page', 1, type=int)
    most_recently_active = User.query.filter(User.roles.any(name="Freelancer")).\
    order_by(User.last_seen.desc()).paginate(page,\
    current_app.config['FREELANCERS_PER_PAGE'], False)
    next_url = (url_for('main.freelancers_available', page=most_recently_active.next_num)\
    if most_recently_active.has_next else None)
    prev_url = (url_for('main.freelancers_available', page=most_recently_active.prev_num)\
    if most_recently_active.has_prev else None)
    return render_template("freelancers_available.html",\
    freelancers = most_recently_active.items,\
    next_url=next_url, prev_url=prev_url)

@bp.route('/freelancers/ranked')
def freelancers_ranked():
    ranked_freelancers = [u.calculate_score() for u in User.query.all()].sort(reverse=True)
    return "pass"

@bp.route('/jobs')
@login_required
def jobs_available():
    page = request.args.get('page', 1, type=int)
    jobs = Job.query.order_by(Job.posted_on.desc()).paginate(
    page, current_app.config['JOBS_PER_EXPLORE_PAGE'], False
    )
    next_url = (url_for('main.jobs_available', page=jobs.next_num) if jobs.has_next else None)
    prev_url = (url_for('main.jobs_available', page=jobs.prev_num) if jobs.has_prev else None)
    return render_template("jobs_available.html", title='Jobs available',\
    jobs=jobs.items, next_url=next_url, prev_url=prev_url)

@bp.route('/aboutus')
def about_us():
    return render_template('about_us.html')
