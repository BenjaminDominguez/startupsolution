from app import create_app, db, cli
from app.models import Startup, User, Job, Cat, Sub
from flask import render_template
from flask_mail import Message
from app import mail
import os
# load pre imports in flask shell

app = create_app()
cli.register(app)

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
    'os': os,
    'Cat': Cat,
    'Sub': Sub
    }
