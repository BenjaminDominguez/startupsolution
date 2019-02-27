from app.freelancer import bp
from app.freelancer.forms import EditProfileForm
from app.models import User, Job
from app.special import roles_required
from flask_login import login_required, current_user
from app.freelancer.forms import EditProfileForm, UploadProfilePicForm, SendMessageForm

@bp.route('/<username>')
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
    return render_template('user_profile.html', user=user, jobs=jobs, no_jobs=bool(len(jobs) == 0),\
    profile_pic=profile_pic, avatar_url=avatar_url, home_active=True)

@bp.route('/<username>/edit_profile', methods=['GET', 'POST'])
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
    return render_template('edit_profile.html', title='Edit Profile', form=form, user=user, avatar_url=session.get('avatar_url'), edit_active=True,\
    profile_pic=session.get('profile_pic'))

@bp.route('/<username>/current_jobs')
@login_required
def current_jobs(username):
    user = User.query.filter_by(username=username).first_or_404()
    jobs = [job for job in user.jobs]
    return render_template('current_jobs.html', username=username, profile_pic=session.get('profile_pic'),\
    current_jobs_active=True, user=user, avatar_url=session.get('avatar_url'), jobs=jobs)

@bp.route('/upload_profile_pic', methods=['GET', 'POST'])
@login_required
def upload_profile_pic():
    form = UploadProfilePicForm()
    if form.validate_on_submit():
        file = request.files['profile_pic']
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        current_user.avatar_data = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        flash(_("Succesfully submitted profile pic!"))
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))
    return render_template('user/upload_profile_pic.html', title='Upload Profile Pic', form=form)
