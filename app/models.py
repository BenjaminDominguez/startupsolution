from app import db
from datetime import datetime
# from types import BooleanType doesnt exist anymore
"""
StartUpCreators have Startups
One StartupCreator has many Startups (Possibly, but not likely)
Startups have Jobs (One Startup has many (individual) Jobs)
Many Developers have many jobs
"""

# aforementioned, many devs may have many startups
jobs_developers = db.Table('jobs_developers',
    db.Column('job_id', db.Integer, db.ForeignKey('job.id')),
    db.Column('developer_id', db.Integer, db.ForeignKey('developer.id')))

class BooleanError(Exception):
    pass

class Startupcreator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(65), index=True, unique=True)
    first = db.Column(db.String(65), index=True)
    last = db.Column(db.String(65), index=True)
    """
    one startup creator may have many different startups
    """
    startups = db.relationship('Startup', backref='creator', lazy='dynamic')

    def create_startup(self, startup):
        if not self.is_startup_in_bin(startup):
            self.startups.append(startup)

    def delete_startup(self, startup):
        if self.is_startup_in_bin(startup):
            self.startups.remove(startup)

    def is_startup_in_bin(self, startup):
        return (startup in self.startups)

    def __repr__(self):
        return "Startupcreator('{0}')".format(self.username)

class Startup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    founded_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    website = db.Column(db.String(64), unique=True, index=True)
    """
    information that should be available to developers who
    are considering taking equity in the firm
    """
    access_to_financials = db.Column(db.Boolean) # this can be marked with a check mark
    previously_funded = db.Column(db.Boolean) # this can be marked with a check
    creator_id = db.Column(db.Integer, db.ForeignKey('startupcreator.id'))
    jobs = db.relationship('Job', backref='company', lazy='dynamic')

    def mark_complete(self):
        self.is_complete = True

    def mark_access_to_financials(self, T_or_F):
        try:
            if repr(type(T_or_F)) == "<class 'bool'>":
                self.access_to_financials = T_or_F
            else:
                raise BooleanError
        except BooleanError:
            print("Enter a boolean, dumbass.")

    def mark_previously_funded(self, T_or_F):
        try:
            if repr(type(T_or_F)) == "<class 'bool'>":
                self.previously_funded = T_or_F
            else:
                raise BooleanError
        except BooleanError:
            print("Enter a boolean, idiot.")

    def create_job(self, job):
        if not self.is_job_in_bin(job):
            self.jobs.append(job)

    def delete_job(self, job):
        if self.is_job_in_bin(job):
            self.jobs.remove(job)

    def is_job_in_bin(self, job):
        return (job in self.jobs)

    def set_founded_date(self, year, month, day):
        self.founded_date = datetime(year, month, day)

    def __repr__(self):
        return "Startup('{0}')".format(self.name)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    is_complete = db.Column(db.Boolean)
    startup_id = db.Column(db.Integer, db.ForeignKey('startup.id'))
    developers = db.relationship(
    'Developer',
    secondary=jobs_developers,
    back_populates='jobs',
    lazy='dynamic'
    )

    def __repr__(self):
        return "Job('{0}')".format(self.name)


class Developer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(65), index=True, unique=True)
    first = db.Column(db.String(64))
    last = db.Column(db.String(64))
    jobs = db.relationship(
    'Job',
    secondary=jobs_developers,
    back_populates='developers',
    lazy='dynamic'
    )

    def add_job_to_job_list(self, job):
        if not self.is_on_job_list(job):
            self.jobs.append(job)

    def remove_job_from_job_list(self, job):
        if self.is_on_job_list(job):
            self.jobs.remove(job)

    def is_on_job_list(self, job):
        return self.jobs.filter(jobs_developers.c.job_id \
        == job.id).count() != 0

    def __repr__(self):
        return "Developer('{0}')".format(self.username)
