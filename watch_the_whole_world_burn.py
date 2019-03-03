from app import db
from flask import current_app
import shutil, os

with current_app._get_current_object().app_context():
    db.session.remove()
    db.drop_all()
    shutil.rmtree('migrations')
    os.remove('app.db')
