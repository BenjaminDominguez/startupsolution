def create():
    from faker import Faker
    from app import db
    from app.models import Startup, Job, User, Role
    from random import randint as number
    import random
    import string
    db.create_all()
    fake = Faker()
    count = 100
    employer_role = Role(name='Employer')
    freelancer_role = Role(name='Freelancer')
    db.session.add_all([employer_role, freelancer_role])
    while count > 0:
        try:
            first, last = fake.name().lower().split()
            num = str(number(0, 9)) + str(number(0, 9)) + str(number(0, 9))
            username = first[0] + last[0] + num
            email = username + '@gmail.com'
            user = User(username=username, first=first, last=last, email=email)
            user.roles.append(freelancer_role)
            db.session.add(user)
            user.set_password('password')
            db.session.commit()
            random_word = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
            startup = Startup(company_name='{0}'.format(random_word), website='{0}'.format(random_word + '.com'), access_to_financials=True, previously_funded=True)
            random_word = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
            job = Job(name='{0}'.format(random_word))
            db.session.add_all([startup, job])
            startup.create_job(job)
            user.add_job_to_job_list(job)
            db.session.commit()
            count = count - 1
        except ValueError:
            pass
