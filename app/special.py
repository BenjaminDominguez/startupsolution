from flask_login import current_user
from functools import wraps
from flask import render_template
from flask_babel import lazy_gettext as _l
from app.models import User


"""
roles_required decorator restricts access to certain views (web pages)
based off the users role
@login_required should always come before roles_required
"""
def roles_required(roles):
    def real_decorator(view):
        @wraps(view)
        def decorated_view(*args, **kwargs):
            if 'Employer' in roles and current_user.employer():
                return view(*args, **kwargs)
            elif 'Admin' in roles and current_user.admin():
                return view(*args, **kwargs)
            elif 'Freelancer' in roles and current_user.freelancer():
                return view(*args, **kwargs)
            else:
                return render_template('errors/404.html'), 404
        return decorated_view
    return real_decorator

"""
l18n_tuples helps create l18n tuples from a list
of values, (_l(x), _l(x)), (_l(y), _l(y)), (_l(z), _l(z)) for input [x, y, z]
"""

def l18n_tuples(list):
    list = [_l(i) for i in list]
    return tuple(zip(list, list))

"""
Ranks freelancers by score
"""
def rank_freelancers():
    return [u.calculate_score() for u in User.query.all()].sort(reverse=True)

"""

Checks if the user is an admin of the company

"""

def company_admin_required(view):
    @wraps(view)
    def decorated_view():
        pass
