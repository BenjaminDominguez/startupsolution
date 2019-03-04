import unittest
from datetime import datetime
from app import create_app, db
from app.models import User, Startup, Job, Cat, Sub
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class JobCatTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_subcat_cat(self):
        cat = Cat(name='Web Developement')
        sub = Sub(name='Frontend')
        job = Job(name='A')
        db.session.add_all([cat, sub, job])
        db.session.commit()
        job.add_cat(cat)
        cat.assign_sub_cat(sub)
        db.session.commit()
        job.add_sub_cat(sub)
        db.session.commit()
        check = (sub in job.subs)
        self.assertTrue(check)


    # def test_special_cat_method(self):
    #     cats = ['Web Developement', 'iOS Developement', 'UI/UX Developement', 'Marketing', 'Administrative']
    #     for cat in cats:
    #         j = JobCat(name='{0}'.format(cat))
    #         db.session.add(j)
    #         db.session.commit()
    #     #Web developement sub cats
    #     subcats = {
    #     'Web Developement': ['Frontend Developement', 'HTML/CSS', 'Javascript', 'Backend Developement'],
    #     'iOS Developement': ['Design', 'Swift', 'Objective-C', 'Games'],
    #     'UI/UX Developement': ['Website Design', 'iOS App Design', 'Android App Design', 'Email Templates'],
    #     'Marketing': ['Email Marketing', 'Product Marketing', 'SEO', 'Promotion/Advertising'],
    #     'Administrative': ['Tax Work', 'Legal Work', 'Filing Work', 'Audit Work']
    #     }
    #     for category, subcats in subcats.items():
    #         for s in subcats:
    #             sc = JobSubCat(name='{0}'.format(s))
    #             db.session.add(sc)
    #             db.session.commit()
    #             c = JobCat.query.filter_by(name=category).first()
    #             c.assign_sub_cat(sc)
    #             db.session.add(c)
    #             db.session.commit()
    #     # create Job(name='Job 1'), Job(name='Job 2').... Job(name='Job 12')
    #     count = 1
    #     while count < 13:
    #         j = Job(name='Job {0}'.format(count))
    #         db.session.add(j)
    #         db.session.commit()
    #         count += 1






if __name__ == '__main__':
    unittest.main(verbosity=2) # adjust the verbosity from 0 to 2 for more or less detail on tests
