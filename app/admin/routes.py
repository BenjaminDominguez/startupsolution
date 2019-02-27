from app.special import roles_required
from flask_login import login_required
from flask import request, redirect, render_template, url_for, current_app
from app.models import User
from app.admin import bp

@bp.route('/admin/freelancer_info')
@login_required
@roles_required(['Admin'])
def freelancer_info():
    return render_template('freelancer_info.html', title='Freelancer info')

@bp.route('/admin/company_info')
@login_required
@roles_required(['Admin'])
def company_info():
    page = request.args.get('page', 1, type=int)
    employers = User.query.filter(User.roles.any(name="Employer")).order_by(User.last_seen.desc()).paginate(page, current_app.config['COMPANIES_PER_PAGE_ADMIN'], False)
    next_url = (url_for('company_info', page=employers.next_num) if employers.has_next else None)
    prev_url = (url_for('company_info', page=employers.prev_num) if employers.has_prev else None)
    return render_template("company_info.html",employers = employers.items,next_url=next_url, prev_url=prev_url)
