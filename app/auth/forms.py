from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField,\
SubmitField, SelectField, DateTimeField, TextAreaField
from wtforms.fields import RadioField
from wtforms.validators import ValidationError, DataRequired, DataRequired, Email,\
EqualTo, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_babel import lazy_gettext as _l
from flask_babel import _
from app.models import User, Startup
from app.special import l18n_tuples

company_types = ['Limited Liability Corporation', 'Limited Partnership', 'S-Corp', 'Corporation (Inc.)', 'Sole Proprietorship', 'Partnership']

job_types = ['iOS Developement', 'Static website', 'Web application', 'Design', 'Marketing']

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

hours_a_week = ['Less than 10 hours a week', '10 to 20 hours a week', '20 to 30 hours a week', '30 to 40 hours a week', 'Over 40 hours a ']
ef = ['Employer', 'Freelancer']

class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    submit = SubmitField(_l('Sign in'))

class FreelancerRegistrationForm(FlaskForm):
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    repeat_password = PasswordField(_l("Repeat password"), validators=[DataRequired()\
    , EqualTo('password')], render_kw={'placeholder': _l("Repeat your password")})
    first = StringField(_l("First name", validators=[DataRequired()]))
    last = StringField(_l("Last name", validators=[DataRequired()]))
    city = StringField(_l("Enter your city", validators=[DataRequired()]))
    state = SelectField(_l("Enter your state", choices=l18n_tuples(states), validators=[DataRequired()]))
    occupation = SelectField(_l("What job do you do?"), choices=l18n_tuples(job_types), validators=[DataRequired()])
    hours_a_week = SelectField(_l("How many hours a week are you available?"), choices=l18n_tuples(hours_a_week), validators=[DataRequired()])
    about_me = TextAreaField(_l('Tell us about yourself: Employment History, Skills and Languages, Past Projects, etc.'), validators=[Length(min=0, max=1000)])
    submit = SubmitField(_l("Finish Registration for now!"))
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Username taken. Please select a different one.'))

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError(_('Email taken. Please select a different one'))



class EmployerRegistrationForm(FlaskForm):
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    repeat_password = PasswordField(_l("Repeat password"), validators=[DataRequired()\
    , EqualTo('password')], render_kw={'placeholder': _l("Repeat your password")})
    first = StringField(_l("First name", validators=[DataRequired()]))
    last = StringField(_l("Last name", validators=[DataRequired()]))
    company_name = StringField(_l("Company Name"), validators=[DataRequired()])
    state_of_incorporation = SelectField(_l("What's your state of incorporation?"), choices=l18n_tuples(states), validators=[DataRequired()])
    company_type = SelectField(_l("What type of company are you?"), choices=l18n_tuples(company_types), validators=[DataRequired()])
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
