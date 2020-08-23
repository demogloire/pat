from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User, Categorie
from app.categorie.forms import AddCatForm, EditeCatForm
from app.categorie.function import autorisation_super_admin
# from app.authentification.function import avatar
from flask_login import login_user, current_user, login_required


from . import categorie



@categorie.route('/', methods=['GET', 'POST'])
@login_required
@autorisation_super_admin
def index():
   title="Catégorie"
   form=AddCatForm()

   if form.validate_on_submit():
      categorie=Categorie(nom=form.nom.data.capitalize(),statut=True, user_categorie=current_user)
      db.session.add(categorie)
      db.session.commit()
      flash("Succès", 'success')
      return redirect(url_for('categorie.index'))

   categorie=Categorie.query.all()

   return render_template('categorie/addcat.html', title=title, form=form, categorie=categorie)



@categorie.route('/status/<int:id>', methods=['GET', 'POST'])
@login_required
@autorisation_super_admin
def acivation_categorie(id):
   #Vérfifcation ID
   if id is None:
      abort(404)
   #Categorie
   categories=Categorie.query.filter_by(id=id).first_or_404()

   message=None
   type_message=None

   if categories.statut==None or categories.statut==False:
      categories.statut=True
      message=f"Vous activé la catégorie {categories.nom}"
      type_message=True
   else:
      categories.statut = False
      message=f"Vous désactivé la catégorie {categories.nom}"
      type_message=False
   
   db.session.commit()
   if type_message==True:
      flash(f"{message}", "success")
      return redirect(url_for("categorie.index"))
   else:
      flash(f"{message}", "danger")
      return redirect(url_for("categorie.index"))




@categorie.route('/priorite/<int:id>', methods=['GET', 'POST'])
@login_required
@autorisation_super_admin
def priorite_categorie(id):
   #Vérfifcation ID
   if id is None:
      abort(404)
      
      
   liste_de_priorite=[]
   
   #Categorie
   categories=Categorie.query.filter_by(id=id).first_or_404()
   #Priorité
   priorite=Categorie.query.filter_by(priorite=True).all()
   for prio in priorite:
      i=prio.id
      liste_de_priorite.insert(0,i)
   nombre_de_cat_prio=len(liste_de_priorite)
   #Message et type de notification
   message=None
   type_message=None
   #Changement de la priorité de catégorie
   if categories.priorite==None or categories.priorite==False:
      if nombre_de_cat_prio == 4:
         #Recuperation de la dernière categorie
         liste_de_priorite.sort(reverse=True)
         liste_derniere_cat=liste_de_priorite[0]
         derniere_cat=Categorie.query.filter_by(id=liste_derniere_cat).first()
         print(derniere_cat,'-----------------------dsqsd--------------')
         
         #desactivation en priorité de l derniere categorie
         derniere_cat.priorite=False
         categories.priorite=True
      else:
         categories.priorite=True
      #Message de notification
      message=f"Vous priorisez la catégorie {categories.nom.lower()}"
      type_message=True
              
   else:
      categories.statut = False
      message=f"Vous dépriorisez la catégorie {categories.nom.lower()}"
      type_message=False
   db.session.commit()
   
   if type_message==True:
      flash(f"{message}", "primary")
      return redirect(url_for("categorie.index"))
   else:
      flash(f"{message}", "warning")
      return redirect(url_for("categorie.index"))


#Modification catégorie
@categorie.route('/<int:id>', methods=['GET', 'POST'])
@login_required
@autorisation_super_admin
def modification_categorie(id):
   title="Lise à jour"
   categories=Categorie.query.filter_by(id=id).first_or_404()
   form=EditeCatForm()
   #Mise à jour avec succes
   if form.validate_on_submit():
      categories.nom=form.nom.data.capitalize()
      db.session.commit()
      flash('Modification avec succès', "success")
      return redirect(url_for('categorie.index'))

   if request.method=='GET':
      form.nom.data=categories.nom

   return render_template('categorie/editcat.html', title=title, cat=categories.nom, form=form)
   

      
