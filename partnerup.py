from app import app, db
from app.models import Startupcreator, Startup, Developer, Job

#load pre imports in flask shell
# @app.shell_context_processor
# def make_shell_context():
#     return {
#     'sc': StartupCreator(username='bendominguez011'),
#     'd': Developer(username='ben', first='ben', last='ben'),
#     's': Startup(name='PartnerUP'),
#     'j': Job(name='job_1'),
#     'SC': StartupCreator.query.all(),
#     'D': Developer.query.all(),
#     'S': StartUp.query.all(),
#     'J': Job.query.all()
#     }
