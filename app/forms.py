from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,\
SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, DataRequired, Email,\
EqualTo
from app.models import User

company_types = ['Limited Liability Corporation', 'Limited Partnership', 'S-Corp', 'Corporation (Inc.)', 'Sole Proprietorship', 'Partnership']

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')

class FirstRegistrationForm(FlaskForm):
    username = StringField('Create a username', validators=[DataRequired()])
    email = StringField('Enter your work email', validators=[DataRequired(), Email()])
    password = PasswordField('Select a password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired()\
    , EqualTo('password')])
    """
    IMPORTANT:
    if you have extra fields in your forms that are not in your template,
    your form will not validate on submit.
    """
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username taken. Please select a different one.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Username taken. Please select a different one')


class SecondRegistrationForm(FlaskForm):
    role = SelectField('Are you an employer or freelancer?', choices=[('Employer', 'Employer'), ('Freelancer', 'Freelancer')])
    submit = SubmitField('Submit')
