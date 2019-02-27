import unittest
from datetime import datetime
from app import create_app, db
from app.models import Startupcreator, Startup, Job, Developer
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class StartupTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_startup_methods(self):
        s = Startup(name='partnerup')
        j = Job(name='test_job')
        db.session.add_all([s, j])
        db.session.commit()
        self.assertIsNone(s.access_to_financials)

        s.mark_access_to_financials(T_or_F= True)
        s.mark_previously_funded(T_or_F= False)

        self.assertTrue(s.access_to_financials)
        self.assertFalse(s.previously_funded)

        s.create_job(j)
        self.assertTrue(s.is_job_in_bin(j))
        s.delete_job(j)
        self.assertFalse(s.is_job_in_bin(j))

    def test_startupcreator_methods(self):
        s = Startup(name='partnerup')
        sc = Startupcreator(username='ben')
        db.session.add_all([s, sc])

        sc.create_startup(s)
        self.assertTrue(sc.is_startup_in_bin(s))
        self.assertEqual(sc.startups[0], s)

        sc.delete_startup(s)
        self.assertFalse(sc.is_startup_in_bin(s))


    def test_job_developer_relationship(self):
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2) # adjust the verbosity from 0 to 2 for more or less detail on tests
