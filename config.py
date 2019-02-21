import os
base_directory = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(base_directory, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/app/static/database_files'
    JOBS_PER_EXPLORE_PAGE = 10
    FREELANCERS_PER_PAGE = 10
    OAUTH_CREDENTIALS = {
    'linkedin': {
        'id': '470154729788964',
        'secret': '010cc08bd4f51e34f3f3e684fbdea8a7'
    },
    'github': {
        'id': '3RzWQclolxWZIMq5LJqzRZPTl',
        'secret': 'm9TEd58DSEtRrZHpz2EjrV9AhsBRxKMo8m3kuIZj3zLwzwIimt'
    }
}
# to grab a key with nested dictionaries
# to get id of facebook
# app.config['OAUTH_CREDENTIALS']['linkedin']['id']
