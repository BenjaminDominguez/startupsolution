from app import app, db
from app.models import Startup, User, Job

# load pre imports in flask shell
@app.shell_context_processor
def make_shell_context():
    return {
    'u': User.query.get(1),
    'u1': User.query.get(2),
    's': Startup.query.get(1),
    'j': Job.query.get(1),
    'db': db
    }
