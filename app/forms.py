from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,\
SubmitField, SelectField, DateTimeField, TextAreaField, RadioField
from wtforms.validators import ValidationError, DataRequired, DataRequired, Email,\
EqualTo, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import User, Startup

company_types = ['Limited Liability Corporation', 'Limited Partnership', 'S-Corp', 'Corporation (Inc.)', 'Sole Proprietorship', 'Partnership']

job_types = ['iOS Developement', 'Static website', 'Web application', 'Design', 'Marketing']

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

jobs = ['iOS Developement', 'Full-Stack Web Dev', 'Front-End Web Dev', 'Backend Web Dev']
job_times = ['1 - 4 weeks', '1 - 2 months', '2 - 6 months', 'Over 6 months']
hours_a_week = ['Less than 10 hours a week', '10 to 20 hours a week', '20 to 30 hours a week', '30 to 40 hours a week', 'Over 40 hours a ']

states_tup = tuple(zip(states, states))
company_types_tup = tuple(zip(company_types, company_types))
jobs_tup = tuple(zip(jobs, jobs))
job_types_tup = tuple(zip(job_types, job_types))
job_times_tup = tuple(zip(job_times, job_times))
hours_a_week_tup = tuple(zip(hours_a_week, hours_a_week))

class LoginForm(FlaskForm):
    username = StringField('Username or email', validators=[DataRequired()], render_kw={"placeholder": "Enter your username or email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'Enter your password'})
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

class EmployerRegistrationForm(FlaskForm):
    company_name = StringField("Company Name", validators=[DataRequired()])
    state_of_incorporation = SelectField("What's your state of incorporation?", choices=states_tup, validators=[DataRequired()])
    company_type = SelectField("What type of company are you?", choices=company_types_tup, validators=[DataRequired()])
    #Im taking out date of incorporation for now
    # date_of_incorporation = DateTimeField("Date of incorporation?", validators=[DataRequired()]) #matches with founded date, need to update models
    taxID = StringField("Tax ID (if US)", validators=[DataRequired()])
    description = TextAreaField("Tell us about your company!", validators=[DataRequired()])
    #data is required for now..
    logo = FileField("Upload a company logo/profile pic", validators=[DataRequired()])
    submit = SubmitField('Finish registration for now!')

    def validate_company_name(self, company_name):
        name = Startup.query.filter_by(company_name=company_name.data).first()
        if name is not None:
            raise ValidationError("Company name already taken. Try again?")

class FreelancerForm(FlaskForm):
    first = StringField("First name", validators=[DataRequired()])
    last = StringField("Last name", validators=[DataRequired()])
    occupation = SelectField("What job do you do?", choices=jobs_tup, validators=[DataRequired()])
    hours_a_week = SelectField("How many hours a week are you available?", choices=hours_a_week_tup, validators=[DataRequired()])
    about_me = TextAreaField('Tell us about yourself: Employment History, Skills and Languages, Past Projects, etc.', validators=[Length(min=0, max=1000)])
    submit = SubmitField("Finish Registration for now!")

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('Tell us about yourself: Employment History, Skills and Languages, Past Projects, etc.', validators=[Length(min=0, max=1000)])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None and user.username != username.data:
            raise ValidationError('Username taken. Please select a different one.')

class UploadProfilePic(FlaskForm):
    profile_pic = FileField('Profile Pic', validators=\
    [FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Submit')

class EditCompanyForm(FlaskForm):
    description = TextAreaField('Change company description')
    company_type = SelectField("Revise company type", choices=company_types_tup, validators=[DataRequired()])
    taxID = StringField("Revise Tax ID (if US)", validators=[DataRequired()])
    logo = FileField("Upload a new company logo/profile pic", validators=[DataRequired()])
    submit = SubmitField('Submit changes')

class PostNewJobForm(FlaskForm):
    name = TextAreaField('Enter a job posting title', validators=[DataRequired()])
    job_description = TextAreaField('Enter a brief job description', validators=[DataRequired()])
    offer_price = StringField('Enter an initial listing price (in US dollars)', validators=[DataRequired()])
    job_type = SelectField('What type of work?', choices=job_types_tup, validators=[DataRequired()])
    estimated_developement_time = SelectField('Expected completion time', choices=job_times_tup, validators=[DataRequired()])
    equity_job = BooleanField('Work for equity job (Select if you are willing to offer some form of equity as compensation)')
    submit = SubmitField('Submit job listing!')

class EditJobForm(FlaskForm):
    name = TextAreaField('Revise the job title')
    job_description = TextAreaField('Revise the job description')
    offer_price = StringField('Revise the initial listing price (in US dollars)')
    job_type = SelectField('Revise the type of work', choices=job_types_tup)
    estimated_developement_time = SelectField('Revise the expected completion time', choices=job_times_tup)
    equity_job = BooleanField("Work for equity job (Select if you are willing to offer some form of equity as compensation)")
    submit = SubmitField('Save changes')

class DeleteJobForm(FlaskForm):
    username = StringField('Enter username', validators=[DataRequired()])
    password = PasswordField('Enter password', validators=[DataRequired()])
    submit = SubmitField('Delete job')
