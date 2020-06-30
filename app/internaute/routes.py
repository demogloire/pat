from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User
#from app.user.forms import AddUserForm
# from app.authentification.function import avatar
#from flask_login import login_user, current_user, login_required


from . import internaute

@internaute.route('/', methods=['GET', 'POST'])
def index():
   title='Bienvenu'


   return render_template('internaute/index.html', title=title )

@internaute.route('/internaute/categorie', methods=['GET', 'POST'])
def internaute_categorie():
   title='Categorie'
   
   return render_template('internaute/categorie.html', title=title )

@internaute.route('/internaute/detail-produit/<int:id>', methods=['GET', 'POST'])
def internaute_detail_produit(id):
   title='Detail Produit'
   
   return render_template('internaute/detail-produit.html', title=title)