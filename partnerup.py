from app import app, db
from app.models import Startup, User, Job
from flask import render_template
from flask_mail import Message
from app import mail
import os
from app import cli
# load pre imports in flask shell
@app.shell_context_processor
def make_shell_context():
    return {
    'app': app,
    'db': db,
    'User': User,
    'Startup': Startup,
    'Job': Job,
    'render_template': render_template,
    'Message': Message,
    'mail': mail,
    'os': os
    }
