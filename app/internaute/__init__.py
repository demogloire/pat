from flask import Blueprint

internaute = Blueprint('internaute', __name__)

from . import routes