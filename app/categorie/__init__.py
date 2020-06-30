from flask import Blueprint

categorie = Blueprint('categorie', __name__, url_prefix='/categories')

from . import routes