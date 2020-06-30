from flask import Blueprint

user = Blueprint('user', __name__, url_prefix='/users')

from . import routes