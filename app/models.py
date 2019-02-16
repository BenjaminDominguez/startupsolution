from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
genhash, checkhash = generate_password_hash, check_password_hash
from flask_login import UserMixin

"""
Using Jinja2 to integrate database references within HTML
------------------------------------------------------------------
s = Startupcreator(username='user', first='ben', last='dominguez')
#creating an instance of a class Startupcreator

#to access the atrributes of an instance of the class for use in a html file with Jinja2:
                    <p>{{ s.username }}</p>

                        is equivalent to:

                    <p>      user       </p>
So as long as you know the column names for the database, you can name the "instance" anything you like
and I'll pass it in through the backend as a variable.

all_devs = Developers.query.all()
This returns a list of all the developers in the database.
to iterate through the list of developers in html (For example, if you needed to return all developers available on a certain page)
    {% for dev in all_devs %}
    <div>
        <p> dev.username: dev.first dev.last </p>
    </div>
    {% endfor %}

    would be equivalent to:
    <div>
        <p>user1: ben dominguez</p>
    </div>
    <div>
        <p>user2: carlos nunez</p>
    </div>

    and on and on until we've gone through the entire query.

You can create for loops like this and as long as the queries are reasonable, I can integrate it through the back end
and pass in the appropriate list to iterate through for all_devs


Jinja2 documentation
--------------------
http://jinja.pocoo.org/docs/2.10/
"""

# MANY devs have MANY jobs database relationship table.
jobs_users = db.Table('jobs_users',
    db.Column('job_id', db.Integer, db.ForeignKey('job.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')))

class BooleanError(Exception):
    pass

"""
UserMixin provides the methods that Flask-Login needs to
operate. Startup is inheriting those methods and attributes
These include:
Attribute is_authenticated
Attribute is_active
Attribute is_anonymous
Method get_id()
"""

""""
Users have one startup, if they are an employer
Users have many jobs, if they are a freelancer
One job has one freelancer
User to jobs is a one to many relationship!!!!
One startup has many jobs.

"""

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(64))
    role = db.Column(db.String(64)) # must be either "Employer" or "Freelancer"
    first = db.Column(db.String(64), index=True)
    last = db.Column(db.String(64), index=True)
    registration_date = db.Column(db.DateTime, index=True)
    email = db.Column(db.String(64), index=True)
    occupation = db.Column(db.String(64), index=True, default='Developer')
    # one to one relationship between user and startup
    startup = db.relationship('Startup', backref='admin', lazy='dynamic')
    # one to many relationship between user and jobs
    jobs = db.relationship('Job', backref='freelancer', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = genhash(password)

    def check_password(self, password):
        return checkhash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def set_registration_date(self):
        self.registration_date = datetime.now()

    def create_startup(self, startup):
        if self.role == 'Employer':
            self.startup.append(startup)
        else:
            print("Not an employer")

    def get_username(self):
        return self.username

    def add_job_to_job_list(self, job):
        if not self.is_on_job_list(job) and self.role == 'Freelancer':
            self.jobs.append(job)

    def remove_job_from_job_list(self, job):
        if self.is_on_job_list(job) and self.role == 'Freelancer':
            self.jobs.remove(job)

    def is_on_job_list(self, job):
        return self.jobs.filter(jobs_users.c.job_id \
        == job.id).count() != 0

    def delete_startup(self, startup):
        pass # not sure if I should add this functionality yet, does not make sense.

    def info(self):
        if self.role == 'Employer':
            return '<Employer {0}>'.format(self.username)
        elif self.role == 'Freelancer':
            return '<Freelancer {0} {1}>'.format(self.first, self.last)
        else:
            return '<ROLE NOT ASSIGNED FOR {0}>'.format(self.username)

    __repr__ = info


class Startup(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64), index=True, unique=True)
    founded_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    website = db.Column(db.String(64), unique=True, index=True)
    #one to one relationship
    """
    information that should be available to developers who
    are considering taking equity in the firm
    """
    access_to_financials = db.Column(db.Boolean) # this can be marked with a check mark
    previously_funded = db.Column(db.Boolean) # this can be marked with a check
    certificate_of_incorporation = db.Column(db.Boolean, default=True)
    state_of_incorporation = db.Column(db.String(64), default='Delaware')
    company_type = db.Column(db.String(64), default='C-Corp')
    taxID = db.Column(db.String(64), default='00-0000000')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
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

    def info(self):
        return "<Startup {0}>".format(self.company_name)

    __repr__ = info

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    is_complete = db.Column(db.Boolean)
    startup_id = db.Column(db.Integer, db.ForeignKey('startup.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def info(self):
        return '<Job {0}>'.format(self.name)

    __repr__ = info
