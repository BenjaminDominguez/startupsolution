from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
genhash, checkhash = generate_password_hash, check_password_hash
from flask_login import UserMixin
import os
import base64
import onetimepass
from hashlib import md5
from app import moment
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



class User(db.Model, UserMixin):

    __searchable__ = ['city', 'hours_a_week', 'occupation']

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    first = db.Column(db.String(64), index=True)
    last = db.Column(db.String(64), index=True)
    registration_date = db.Column(db.DateTime, index=True)
    email = db.Column(db.String(64), index=True)
    hours_a_week = db.Column(db.String(64))
    occupation = db.Column(db.String(64), index=True, default='Developer')
    social_id = db.Column(db.String(64), nullable=True) #nullable?
    about_me = db.Column(db.String(1000))
    avatar_data = db.Column(db.String(400))
    city = db.Column(db.String(100))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # one to one relationship between user and startup
    startup = db.relationship('Startup', backref='admin', lazy='dynamic')
    # one to many relationship between user and jobs
    jobs = db.relationship('Job', backref='freelancer', lazy='dynamic')
    #one to many relationship between user and pastemployments
    resume = db.relationship('PastEmployments', backref='freelancer', lazy='dynamic')
    #one to many relationship between user and reviews
    reviews = db.relationship('Reviews', backref='freelancer', lazy='dynamic')
    #one to many relationship between user and skills
    # oh boy, messages
    messages_sent = db.relationship('Message',
    foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    messages_recieved = db.relationship('Message',
    foreign_keys='Message.recipient_id', backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)
    roles = db.relationship('Role', secondary='user_roles')
    ranking = db.Column(db.Integer, index=True)

    def avatar(self, size):
        """
        convert email to all lower case because this is what is required by
        Gravatar, and encode the string to bytes before passing it to
        the hash function.
        """
        if self.email is not None:
            digest = md5(self.email.lower().encode('utf-8')).hexdigest()
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
                digest, size)
        else:
            return None

    def make_avatar_url(self):
        if self.avatar_data:
            url = self.avatar_data.split('/')
            avatar_url = "/{0}/{1}".format(url[-2], url[-1])
        return avatar_url

    def set_password(self, password):
        self.password = genhash(password)

    def check_password(self, password):
        return checkhash(self.password, password)

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def set_registration_date(self):
        self.registration_date = datetime.now()

    def create_startup(self, startup):
        if self.employer():
            self.startup.append(startup)
        else:
            print("Not an employer")

    def get_username(self):
        return self.username

    def add_job_to_job_list(self, job):
        if not self.is_on_job_list(job) and self.freelancer():
            self.jobs.append(job)

    def remove_job_from_job_list(self, job):
        if self.is_on_job_list(job) and self.freelancer():
            self.jobs.remove(job)

    def employer(self):
        return ('Employer' in [role.name for role in self.roles])

    def freelancer(self):
        return ('Freelancer' in [role.name for role in self.roles])

    def admin(self):
        return ('Admin' in [role.name for role in self.roles])

    def is_on_job_list(self, job):
        return self.jobs.filter(jobs_users.c.job_id \
        == job.id).count() != 0

    def delete_startup(self, startup):
        pass # not sure if I should add this functionality yet, does not make sense.

    def add_to_my_resume(self, past_employment):
        self.resume.append(past_employment)

    def remove_off_my_resume(self, past_employment):
        self.resume.remove(past_employment)

    def last_seen_formatted(self):
        delta = datetime.utcnow() - self.last_seen
        if delta.seconds < 86400: #24 hours
            if delta.seconds < 3600: # 1 hour
                if delta.seconds < 60:
                    return 'online'
                return ('minutes', int(round(delta.seconds/60)))
            return ('hours', int(round(delta.seconds/3600)))
        return ('days', delta.days)

    def last_seen_string(self):
        x = self.last_seen_formatted()
        if x[0] is 'online':
            return "Online"
        else:
            return 'Last seen {0} {1} ago'.format(x[1], x[0])

    def is_admin_for_the_company(self, company_name):
        bool = (Startup.query.filter_by(Startup.admin.any(username=self.username)).first())
        return bool


    def info(self):
        if self.employer():
            return '<Employer {0}>'.format(self.username)
        elif self.freelancer():
            return '<Freelancer {0} {1}>'.format(self.first, self.last)
        else:
            return '<ROLE NOT ASSIGNED FOR {0}>'.format(self.username)

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
        Message.timestamp > last_read_time).count()

    def calculate_score(self):
        score = 0
        score_weights = {
        1: -5,
        2: -4,
        3: -1,
        4: 1,
        5: 2
        }
        for review.stars in self.reviews:
            score += score_weights[review.stars]
        return score



    __repr__ = info

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return "<Role {0}>".format(self.name)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))

class Startup(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64), index=True, unique=True)
    founded_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    website = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
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
    description = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    logo_data = db.Column(db.String(400))
    #one to many relationship between startups and jobs
    jobs = db.relationship('Job', backref='company', lazy='dynamic')
    #one to many relationship between startups and reviews
    reviews = db.relationship('Reviews', backref='company', lazy='dynamic')

    def logo(self, size):
        """
        convert email to all lower case because this is what is required by
        Gravatar, and encode the string to bytes before passing it to
        the hash function.
        """
        if self.email:
            digest = md5(self.email.lower().encode('utf-8')).hexdigest()
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
                digest, size)
        else:
            return None

    def make_logo_url(self):
        if self.logo_data:
            url = self.logo_data.split('/')
            logo_url = "/{0}/{1}".format(url[-2], url[-1])
        return logo_url

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

    def write_review(self, review):
        self.reviews.append(review)

    def __repr__(self):
        return "<Startup {0}>".format(self.company_name)

class Job(db.Model):

    __searchable__ = ['name', 'equity_job', 'job_description', 'offer_price', 'job_type', 'estimated_developement_time']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    job_description = db.Column(db.String(1000))
    offer_price = db.Column(db.Integer, index=True)
    job_type = db.Column(db.String(200), index=True)
    equity_job = db.Column(db.Boolean)
    posted_on = db.Column(db.DateTime)
    estimated_developement_time = db.Column(db.String(40), index=True)
    is_complete = db.Column(db.Boolean)
    startup_id = db.Column(db.Integer, db.ForeignKey('startup.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def post_job_time(self):
        now = datetime.utcnow()
        self.posted_on = now

    def time_elapsed(self):
        pass

    def __repr__(self):
        return '<Job {0}>'.format(self.name)


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer, index=True)
    description = db.Column(db.String(1000))
    time_written = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    startup_id = db.Column(db.Integer, db.ForeignKey('startup.id'))

    def info(self):
        return 'Review by {0} for {1}, {2} stars'.format(
        'company', 'freelancer', self.stars
        )

    __repr__ = info

class PastEmployments(db.Model):
    #table name is past_employments
    id = db.Column(db.Integer, primary_key=True)
    job_description = db.Column(db.String(100))
    company_worked_for = db.Column(db.String(64), index=True)
    timeframe = db.Column(db.DateTime)
    location = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Past employment working for {0}'.format(
        'company_worked_for'
        )

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)
