from flask import render_template, current_app
from flask_mail import Message
from app import mail
from app.models import User
import os

class MassEmail(object):
    os.environ['MAIL_SERVER'] = 'smtp.googlemail.com'
    os.environ['MAIL_PORT'] = '587'
    os.environ['MAIL_USE_TLS'] = '1'
    os.environ['MAIL_USERNAME'] = 'bendominguez011'
    os.environ['MAIL_PASSWORD'] = 'mjnoppQ12'

    def __init__(self):
        self.sender = app.config['SEND_ADMINS'][0]
        self.freelancers = User.query.filter_by(role="freelancer").all()
        self.employers = User.query.filter_by(role="employers").all()

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

    def send_mass_email(self, subject, template_name, recipients, **template_kwargs):
        with current_app._get_current_object().app_context():
            msg = Message(subject, sender = self.sender, recipients=recipients)
            msg.html = render_template('/emails/{0}'.format(template_name), **template_kwargs)
            mail.send(msg)

    def mass_email_employers_no_ref(self, subject, template_name):
        emails= [employer.email for employer in self.employers if employer.email]
        with current_app._get_current_object().app_context():
            self.send_mass_email(subject=subject, recipients=emails, template_name=template_name)

    def mass_email_freelancers_no_ref(self, subject, template_name):
        emails = [freelancer.email for freelancer in self.freelancers if freelancer.email]
        with current_app._get_current_object().app_context():
            self.send_mass_email(subject=subject, recipients=emails, template_name=template_name)

    def mass_email_employers_ref(self, subject, template_name):
        for employer in self.employers:
            user, email = employer, employer.email
            with current_app._get_current_object().app_context():
                self.send_mass_email(subject=subject, template_name=template_name, recipients=email, user=user)

    def mass_email_freelancers_ref(self, subject, template_name):
        for freelancer in self.freelancers:
            user, email = freelancer, freelancer.email
            with current_app._get_current_object().app_context():
                self.send_mass_email(subject=subject, template_name=template_name, recipients=email, user=user)

    def __repr__(self):
        info = {
        'MAIL_SERVER': os.environ.get('MAIL_SERVER'),
        'MAIL_PORT': os.environ.get('MAIL_PORT'),
        'MAIL_USE_TLS': os.environ.get('MAIL_USE_TLS'),
        'MAIL_USERNAME': os.environ.get('MAIL_USERNAME'),
        'MAIL_PASSORD': os.environ.get('MAIL_PASSWORD'),
        'SENDER': self.sender
        }
        return str(info)

"""

Write code below to actually send the email and run the script

"""


m = MassEmail()
user = User.query.filter_by(username='bendominguez011').first()
m.send_mass_email(subject='Welcome', template_name='welcome.html', recipients=[user.email], template_kwargs={'user': user})
