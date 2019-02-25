from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,\
SubmitField, SelectField, DateTimeField, TextAreaField, RadioField
from wtforms.validators import ValidationError, DataRequired, DataRequired, Email,\
EqualTo, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_babel import lazy_gettext as _l
from flask_babel import _
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

"""
Need to write a function that makes a list of tuples with every list above and wraps it with _l() for translation
"""
lists = [company_types, job_types, jobs, states, job_times, hours_a_week]
def create_translated_tuples(lists):
    return [tuple(zip(list, list)) for list in [[_l(i) for i in list] for list in lists]]
tups = create_translated_tuples(lists)
company_types_tup = tups[0]
job_types_tup = tups[1]
jobs_tup = tups[2]
states_tup = tups[3]
job_times_tup = tups[4]
hours_a_week_tup = tups[5]

class LoginForm(FlaskForm):
    username = StringField(_l('Username or email'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign in'))

class FirstRegistrationForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired()])
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    repeat_password = PasswordField(_l("Repeat password"), validators=[DataRequired()\
    , EqualTo('password')], render_kw={'placeholder': _l("Repeat your password")})
    """
    IMPORTANT:
    if you have extra fields in your forms that are not in your template,
    your form will not validate on submit.
    """
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Username taken. Please select a different one.'))

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError(_('Username taken. Please select a different one'))


class SecondRegistrationForm(FlaskForm):
    role = SelectField(_l('Are you an employer or freelancer?'), choices=[('Employer', 'Employer'), ('Freelancer', 'Freelancer')])
    submit = SubmitField(_l('Submit'))

class EmployerRegistrationForm(FlaskForm):
    company_name = StringField(_l("Company Name"), validators=[DataRequired()])
    state_of_incorporation = SelectField(_l("What's your state of incorporation?"), choices=states_tup, validators=[DataRequired()])
    company_type = SelectField(_l("What type of company are you?"), choices=company_types_tup, validators=[DataRequired()])
    #Im taking out date of incorporation for now
    # date_of_incorporation = DateTimeField("Date of incorporation?", validators=[DataRequired()]) #matches with founded date, need to update models
    taxID = StringField(_l("Tax ID # (if US)"), validators=[DataRequired()], render_kw={'placeholder': 'XX-XXXXXXX'})
    description = TextAreaField(_l("Tell us about your company!"), validators=[DataRequired()])
    #data is required for now..
    logo = FileField(_l("Upload a company logo/profile pic"))
    submit = SubmitField(_l('Finish registration for now!'))

    def validate_company_name(self, company_name):
        name = Startup.query.filter_by(company_name=company_name.data).first()
        if name is not None:
            raise ValidationError(_("Company name already taken. Try again?"))

class FreelancerForm(FlaskForm):
    first = StringField(_l("First name"), validators=[DataRequired()])
    last = StringField(_l("Last name"), validators=[DataRequired()])
    occupation = SelectField(_l("What job do you do?"), choices=jobs_tup, validators=[DataRequired()])
    hours_a_week = SelectField(_l("How many hours a week are you available?"), choices=hours_a_week_tup, validators=[DataRequired()])
    about_me = TextAreaField(_l('Tell us about yourself: Employment History, Skills and Languages, Past Projects, etc.'), validators=[Length(min=0, max=1000)])
    submit = SubmitField(_l("Finish Registration for now!"))

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

class UploadProfilePic(FlaskForm):
    profile_pic = FileField(_l('Profile Pic'), validators=\
    [FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField(_l('Submit'))

class EditCompanyForm(FlaskForm):
    description = TextAreaField(_l('Change company description'))
    company_type = SelectField(_l("Revise company type"), choices=company_types_tup, validators=[DataRequired()])
    taxID = StringField(_l("Revise Tax ID (if US)"), validators=[DataRequired()])
    logo = FileField(_l("Upload a new company logo/profile pic"), validators=[DataRequired()])
    submit = SubmitField(_l('Submit changes'))

class PostNewJobForm(FlaskForm):
    name = TextAreaField(_l('Enter a job posting title'), validators=[DataRequired()])
    job_description = TextAreaField(_l('Enter a brief job description'), validators=[DataRequired()])
    offer_price = StringField(_l('Enter an initial listing price (in US dollars)'), validators=[DataRequired()])
    job_type = SelectField(_l('What type of work?'), choices=job_types_tup, validators=[DataRequired()])
    estimated_developement_time = SelectField(_l('Expected completion time'), choices=job_times_tup, validators=[DataRequired()])
    equity_job = BooleanField(_l('Work for equity job (Select if you are willing to offer some form of equity as compensation)'))
    submit = SubmitField(_l('Submit job listing!'))

class EditJobForm(FlaskForm):
    name = TextAreaField(_l('Revise the job title'))
    job_description = TextAreaField(_l('Revise the job description'))
    offer_price = StringField(_l('Revise the initial listing price (in US dollars)'))
    job_type = SelectField(_l('Revise the type of work', choices=job_types_tup))
    estimated_developement_time = SelectField(_l('Revise the expected completion time'), choices=job_times_tup)
    equity_job = BooleanField(_l("Work for equity job (Select if you are willing to offer some form of equity as compensation)"))
    submit = SubmitField(_l('Save changes'))

class DeleteJobForm(FlaskForm):
    username = StringField(_l('Enter username'), validators=[DataRequired()])
    password = PasswordField(_l('Enter password'), validators=[DataRequired()])
    submit = SubmitField(_l('Delete job'))

class SendMessage(FlaskForm):
    message = TextAreaField(_l("Message"), validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField(_l("Submit"))
