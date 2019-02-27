from flask import Blueprint

bp = Blueprint('freelancer', __name__, template_folder='templates')

from app.freelancer import routes
