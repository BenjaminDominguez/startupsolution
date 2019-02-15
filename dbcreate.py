from app import db
from app.models import Startup, User, Job
"""
Database model for use in template
"""
db.create_all()

u = User(username='bendominguez011', role='Freelancer')
u.set_password('password')
u1 = User(username='partnerupcreator', role='Employer')
u1.set_password('password')
s = Startup(company_name='partnerup')
j = Job(name='Test job')

db.session.add_all([u, u1, s, j])

u.add_job_to_job_list(j)
u1.create_startup(s)
s.create_job(j)

db.session.commit()
