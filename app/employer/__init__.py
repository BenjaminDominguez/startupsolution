from flask import Blueprint

bp = Blueprint('employer', __name__, template_folder='templates')

from app.employer import routes
