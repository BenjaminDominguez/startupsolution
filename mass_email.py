from app import app
from flask import render_template
from flask_mail import Message
from app import mail
from app.models import User
import os

class MassEmail(object):
    os.environ['MAIL_SERVER'] = 'fakeserver.com'
    os.environ['MAIL_PORT'] = '587'
    os.environ['MAIL_USE_TLS'] = '1'
    os.environ['MAIL_USERNAME'] = 'bendominguez011'
    os.environ['MAIL_PASSWORD'] = 'mjnoppQ12'

    def __init__(self):
        self.sender = app.config['SEND_ADMINS'][0]

    def change_default_variables(self, **var_tuple):
        for key, value in var_tuple.items():
            if (str(key) is 'sender'):
                if value in app.config['SEND_ADMINS']:
                    self.sender = str(value)
                else:
                    raise KeyError(
                    "No sender found in SEND_ADMINS in app.config. \
                    Try checking your spelling or add admin to Config.py")
            if str(key) is not 'sender':
                os.environ[str(key)] = value

    def send_mass_email(self, subject, template_name, recipients):
        msg = Message(subject, sender = self.sender, recipients=recipients)
        msg.html = render_template('/emails/{0}'.format(template_name))
        mail.send(msg)

    def mass_email_employers(self, subject, template_name):
        employers = User.query.filter_by(role='employer').all()
        email_list = [employer.email for employer in employers]
        with app.app_context():
            self.send_mass_email(subject=subject, template_name=template_name)

    def mass_email_freelancers(self, subject, template_name):
        freelancers = User.query.filter_by(role='freelancer').all()
        email_list = [freelancer.email for freelancer in freelancers]
        with app.app_context():
            self.send_mass_email(subject=subject, template_name=template_name)

m = MassEmail()
m.change_default_variables(MAIL_SERVER='smtp.googleemail.com')
