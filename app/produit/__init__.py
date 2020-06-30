from flask import Blueprint

produit = Blueprint('produit', __name__, url_prefix='/produits')

from . import routes