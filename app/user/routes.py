from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User
from app.user.forms import AddUserForm, EditeUserForm
from app.user.function import autorisation_super_admin
# from app.authentification.function import avatar
from flask_login import login_user, current_user, login_required


from . import user

@user.route('/', methods=['GET', 'POST'])
@login_required
@autorisation_super_admin
def index():
   #Title
   title='Nouvel utilisateur'
   #Initialisation du formalaire
   form=AddUserForm()
   #Tableaux de comptages des supers admin
   super_admin=[]

   if form.validate_on_submit():
      #Vérifications des administrateurs
      user_super_admin=User.query.filter_by(type_user='Super admin').all()
      for i in user_super_admin:
         super_admin.insert(0,i.id)
      compte=len(super_admin)
      print()
      if compte > 0 and compte < 3:
         pass
      else:
         flash("Vous avez atteint le maximum des supers admins", "danger")
         return redirect(url_for('user.index'))

      #Enregistrement des utilisateurs
      password=bcrypt.generate_password_hash(form.password.data)
      ajout_ut=User(nom=form.nom.data.upper(), post_nom=form.post_nom.data.upper(), type_user=form.role.data, prenom=form.prenom.data.capitalize(), username=form.username.data, password=password)
      db.session.add(ajout_ut)
      db.session.commit()
      flash('Success', 'success')
      return redirect(url_for('user.index'))
   users=User.query.order_by(User.type_user.desc()).all()
   
   return render_template('user/adduser.html', title=title, form=form, users=users )




@user.route('/status/<int:id>', methods=['GET', 'POST'])
@login_required
@autorisation_super_admin
def acivation_user(id):
   #Verfication de l'ID dans l'URL
   if id is None:
      abort(404)
   #Verification d'identifiant
   user=User.query.filter_by(id=id).first_or_404()
   #Mise à jour statut
   message=None
   bol=None


   #Ineterdiction super admin
   if user.type_user=='Super admin':
      flash("Il a les autorisation de Super admin", "danger")
      return redirect(url_for('user.index'))
   if user.statut==True:
      user.statut=False
      message=f"Vous avez désactivé {user.prenom}"
      bol=False
   else:
      user.statut=True
      message=f"Vous avez activé {user.prenom}"
      bol=True
      print('-----------------2-------------------------------------------', user.statut)

   db.session.commit()

   if bol==True:
      flash(f"{message}","success")
   else:
      flash(f"{message}","danger")

   return redirect(url_for('user.index'))




@user.route('/<int:id>', methods=['GET', 'POST'])
@login_required
@autorisation_super_admin
def edit(id):
   #Title
   title='Mise à jour'
   #Initialisation du formalaire
   form=EditeUserForm()
   #Tableaux de comptages des supers admin
   super_admin=[]
   #Verfication de l'ID dans l'URL
   if id is None:
      abort(404)
   #Verification d'identifiant
   user=User.query.filter_by(id=id).first_or_404()


   compte=0
   if form.validate_on_submit():
      #Vérifications des administrateurs
      if form.role.data=='Super admin':
         user_super_admin=User.query.filter_by(type_user='Super admin').all()
         for i in user_super_admin:
            super_admin.insert(0,i.id)
         compte=len(super_admin)

      if compte > 3:
            flash("Vous avez atteint le maximum des supers admins", "danger")
            return redirect(url_for('user.index'))
      
      if form.username.data== user.username:
         user.prenom=form.prenom.data.capitalize()
         user.nom=form.nom.data.upper()
         user.post_nom=form.post_nom.data.upper()
         user.type_user=form.role.data
      else:
         ver_username=User.query.filter_by(username=form.username.data).first()
         if ver_username:
            flash("L'utilisateur existe déjà", "danger")
            return redirect(url_for('user.edit'))

         user.prenom=form.prenom.data.capitalize()
         user.nom=form.nom.data.upper()
         user.post_nom=form.post_nom.data.upper()
         user.type_user=form.role.data
         user.username = form.username.data
      #Enregistrement des données
      db.session.commit()
      flash("Modification réussie", 'success')
      return redirect(url_for("user.index"))
      
   if request.method=='GET':
      form.prenom.data=user.prenom
      form.nom.data=user.nom
      form.post_nom.data=user.post_nom
      form.username.data=user.username
      form.role.data=user.type_user
        
   
   return render_template('user/edituser.html', title=title, form=form, prenom=user.prenom)

