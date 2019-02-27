from flask import Flask, request
from config import Config, base_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
from flask_mail import Mail
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l("Please log in to access this page")
mail = Mail()
bootstrap = Bootstrap()
babel = Babel()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.debug = True
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    babel.init_app(app)

    from app.errors import bp as errors_bp
    from app.auth import bp as auth_bp
    from app.freelancer import bp as freelancer_bp
    from app.main import bp as main_bp
    from app.admin import bp as admin_bp
    from app.employer import bp as employer_bp

    app.register_blueprint(errors_bp, url_prefix='/error')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(freelancer_bp, url_prefix='/freelancer')
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(employer_bp, url_prefix='/employer')

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(app.config['LANGUAGES'])

# if the application is not running in debug mode
    if not app.debug and not app.testing:
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
    return app


from app import models
