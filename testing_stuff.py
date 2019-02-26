
"""
Writing an:
@employer_required
@freelancer_required

function
"""

def employer_required(view):
    @wraps(view)
    def check_if_employer():
        if current_user.employer():
            pass
        else:
            flash('Not authorized to view this page. Must be an employer.')
            return redirect(url_for('index'))
