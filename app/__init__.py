from flask import Flask
from config import Config, base_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
# I'm not sure if this works or not yet, need to git pull
bootstrap = Bootstrap(app)
login.init_app(app)
login.login_view = 'login'
login.session_protection = "strong"

bootstrap = Bootstrap(app)

from app import routes, models
