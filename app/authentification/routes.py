from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User
from app.authentification.forms import AddUserSuperForm, LoginForm
from app.authentification.function import avatar
from flask_login import login_user, current_user, logout_user


from . import auth

@auth.route('/super-admin/register', methods=['GET', 'POST'])
def super_ad_register():

   title='Super administrateur'
   #Initilisation formaulaire
   form=AddUserSuperForm()

   if form.validate_on_submit():
      password_hash=bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
      avatarv=None
      if form.avatar.data:
         avatarv=avatar(form.avatar.data)  
      else:
         avatarv=None
      ajouter_utilisateur=User(nom=form.nom.data.upper(), post_nom=form.post_nom.data.upper(), prenom=form.prenom.data.capitalize(), 
                                 telephone=form.telephone.data, username=form.username.data, password=password_hash,
                                 adresse_u=form.adresse_u.data, adresse_d=form.adresse_d.data, pays=form.pays.data.title(),
                                 type_user='Super admin', statut=True, avatar=avatarv)
      db.session.add(ajouter_utilisateur)
      db.session.commit()
      flash('Ajout super admin avec succès','success')
      return redirect(url_for('auth.login'))

   return render_template('authentification/register.html', title=title, form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
   title='Connexion'


    #Verification de l'authentification de l'utilisateur
   if current_user.is_authenticated:
      return redirect(url_for('main.dashboard'))
   
   form=LoginForm()
   # requete de verfification
   ver_user= User.query.filter(User.type_user=='Super admin').first()
   # Verification de l'existence de l'utilisateur
   if ver_user:
      pass
   else:
      return redirect(url_for('auth.super_ad_register'))
   

   if form.validate_on_submit():
      user=User.query.filter_by(username=form.username.data).first()
      if user and bcrypt.check_password_hash(user.password, form.password.data):
         if user.statut==False:
            flash("Vous êtres bloqué sur la plateforme",'danger')
         else:
            login_user(user, remember=form.remember.data)
            next_page= request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.main'))
      else:
         flash("Mot de passe incorrect",'danger')  

   return render_template('authentification/login.html', title=title, form=form)



#Déconnexion sur la plateforme
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))