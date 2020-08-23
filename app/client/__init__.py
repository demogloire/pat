from flask import Blueprint

client = Blueprint('client', __name__,url_prefix='/c')

from . import routes