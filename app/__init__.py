from flask import Flask
from config import Config, base_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'
login.session_protection = "strong"
mail = Mail(app)
bootstrap = Bootstrap(app)

app.debug = True

# if the application is not running in debug mode
if not app.debug:
    # if the mail server is set
    if app.config['MAIL_SERVER']:
        auth = None
        username, password = app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']
        if username or password:
            auth = (username, password)
        # if username and password are set, set the auth equal to those values, else the auth is none
        secure = None
        # if TLS is not set, set secure eaul to an empty value
        #remember mail_use_tls is set to os.environ.get("MAIL_TLS") is not None
        #if it is not None, that would be true
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr='do-not-reply@' + app.config['MAIL_SERVER'],
        toaddrs=app.config['ADMINS'][0], subject='Startup Solution Web App Failure',
        credentials=auth, secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/startupsolution.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Startup Solution startup')


from app import routes, models, errors
