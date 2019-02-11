from app import db
from app.models import Startup, Startupcreator, Developer, Job
"""
Database model for use in template
"""
db.session.remove()
db.drop_all()

db.create_all()
d = Developer(username='bendom', first='ben', last='dom')
s1 = Startup(name='PartnerUp', website='partnerup.io')
s2 = Startup(name='Inreview', website='inreview.io')
for s in [s1, s2]:
    s.mark_previously_funded(True)
    s.mark_access_to_financials(True)
    s.set_founded_date(2014, 10, 2)

sc1 = Startupcreator(username='bendominguez011', first='ben', last='dominguez')
sc2 = Startupcreator(username='johndoe', first='john', last='doe')
j1 = Job(name='Job 1')
j2 = Job(name='Job 2')

db.session.add_all([s1, s2, sc1, sc2, j1, j2, d])

sc1.create_startup(s1)
s1.create_job(j1)
s2.create_job(j2)

d.add_job_to_job_list(j1)
d.add_job_to_job_list(j2)
db.session.commit()
