from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from flask_babel import _, lazy_gettext as _l
from wtforms.validators import DataRequired, ValidationError, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.models import User

class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('Tell us about yourself: Employment History, Skills and Languages, Past Projects, etc.'), validators=[Length(min=0, max=1000)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Username already taken. Please use a different one.'))

class UploadProfilePicForm(FlaskForm):
    profile_pic = FileField(_l('Profile Pic'), validators=\
    [FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField(_l('Submit'))

class SendMessageForm(FlaskForm):
    message = TextAreaField(_l("Message"), validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField(_l("Submit"))
