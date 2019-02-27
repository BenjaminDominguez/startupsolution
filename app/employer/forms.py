from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
from flask_babel import _, lazy_gettext as _l
from app.special import l18n_tuples

company_types = ['Limited Liability Corporation', 'Limited Partnership', 'S-Corp', 'Corporation (Inc.)', 'Sole Proprietorship', 'Partnership']
jobs = ['iOS Developement', 'Full-Stack Web Dev', 'Front-End Web Dev', 'Backend Web Dev']
job_times = ['1 - 4 weeks', '1 - 2 months', '2 - 6 months', 'Over 6 months']

class EditCompanyForm(FlaskForm):
    description = TextAreaField(_l('Change company description'))
    company_type = SelectField(_l("Revise company type"), choices=l18n_tuples(company_types), validators=[DataRequired()])
    taxID = StringField(_l("Revise Tax ID (if US)"), validators=[DataRequired()])
    logo = FileField(_l("Upload a new company logo/profile pic"), validators=[DataRequired()])
    submit = SubmitField(_l('Submit changes'))

class PostNewJobForm(FlaskForm):
    name = TextAreaField(_l('Enter a job posting title'), validators=[DataRequired()])
    job_description = TextAreaField(_l('Enter a brief job description'), validators=[DataRequired()])
    offer_price = StringField(_l('Enter an initial listing price (in US dollars)'), validators=[DataRequired()])
    job_type = SelectField(_l('What type of work?'), choices=l18n_tuples(jobs), validators=[DataRequired()])
    estimated_developement_time = SelectField(_l('Expected completion time'), choices=l18n_tuples(job_times), validators=[DataRequired()])
    equity_job = BooleanField(_l('Work for equity job (Select if you are willing to offer some form of equity as compensation)'))
    submit = SubmitField(_l('Submit job listing!'))

class EditJobForm(FlaskForm):
    name = TextAreaField(_l('Revise the job title'))
    job_description = TextAreaField(_l('Revise the job description'))
    offer_price = StringField(_l('Revise the initial listing price (in US dollars)'))
    job_type = SelectField(_l('Revise the type of work', choices=l18n_tuples(jobs)))
    estimated_developement_time = SelectField(_l('Revise the expected completion time'), choices=l18n_tuples(job_times))
    equity_job = BooleanField(_l("Work for equity job (Select if you are willing to offer some form of equity as compensation)"))
    submit = SubmitField(_l('Save changes'))

class DeleteJobForm(FlaskForm):
    username = StringField(_l('Enter username'), validators=[DataRequired()])
    password = PasswordField(_l('Enter password'), validators=[DataRequired()])
    submit = SubmitField(_l('Delete job'))
