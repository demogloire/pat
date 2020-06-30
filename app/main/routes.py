from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User
#from app.user.forms import AddUserForm
# from app.authentification.function import avatar
from flask_login import login_user, current_user, login_required


from . import main

@main.route('/', methods=['GET', 'POST'])
@login_required
def main():

   title='Panneau de control'


   return render_template('main/dash.html', title=title )
