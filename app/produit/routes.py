from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User, Produit, Fichier
from app.produit.forms import AddProduitForm, ImageProduitForm, EditerProduitForm
from app.produit.function import avatar_produit, session_id, ver_session
from flask_login import login_user, current_user, logout_user


from . import produit


@produit.route('/upload_image', methods=['GET', 'POST'])
@session_id
def upload_picture():

   title='Image produit'
   id_produit=ver_session()
   #Initilisation formaulaire
   form=ImageProduitForm()
   
   if form.validate_on_submit():
      file=avatar_produit(form.image_produit.data)
      image=Fichier(urlProduit=file, produit_id=id_produit)
      db.session.add(image)
      db.session.commit()
      
      flash("Ajouter une autre image","success")
      return redirect(url_for('produit.upload_picture'))

   return render_template('produit/upload_image.html', title=title, form=form)


@produit.route('/terminer_upload', methods=['GET', 'POST'])
@session_id
def terminer_upload():
   session.pop('produit_encours',None)
   return redirect(url_for('produit.index'))


@produit.route('/', methods=['GET', 'POST'])
def index():
   title="Liste des produits"
   #Les produits
   produits=Produit.query.all()
   
   
   return render_template('produit/index.html', title=title, produits=produits)
   
@produit.route('/produit/edit/<int:id>', methods=['GET', 'POST'])
def produit_edit(id):
   
   title="Modification du Produit"
   #initiation du produit
   form=EditerProduitForm()
   #Verfication de l'ID dans l'URL
   if id is None:
      abort(404)
      
   #Verification d'identifiant
   modif_prod=Produit.query.filter_by(id=id).first_or_404()
   
   if form.validate_on_submit():
      
      ver_produit_categorie=Produit.query.filter_by(nom=form.nom.data.capitalize(), 
                                                    categorie_id=form.categorie_produit.data.id).first()
      
      if ver_produit_categorie is not None:
         modif_prod.cout_production=form.cout_production.data
         modif_prod.cout_vente_detaille=form.cout_vente_detaille.data
         modif_prod.cout_vente_engros=form.cout_vente_engros.data
         modif_prod.description=form.description.data
      else:
         modif_prod.nom=form.nom.data.capitalize()
         modif_prod.cout_production=form.cout_production.data
         modif_prod.cout_vente_detaille=form.cout_vente_detaille.data
         modif_prod.cout_vente_engros=form.cout_vente_engros.data
         modif_prod.description=form.description.data
         modif_prod.categorie_id=form.categorie_produit.data.id
      
      #Enregistrement des données
      db.session.commit()
      flash("Modification réussie", 'success')
      return redirect(url_for("produit.index"))
   
   
   if request.method=='GET':
      form.nom.data=modif_prod.nom
      form.cout_production.data = modif_prod.cout_production
      form.cout_vente_detaille.data = modif_prod.cout_vente_detaille
      form.cout_vente_engros.data = modif_prod.cout_vente_engros
      form.description.data = modif_prod.description
      form.categorie_produit.data=modif_prod.categorie_produit
      
      
   
   
   
   return render_template('produit/editerProduit.html', title=title, form=form, avatar=modif_prod.avatar)

@produit.route('produit/<int:id>', methods=['GET', 'POST'])
def produit_statut(id):
   if id is None:
      abort(404)
   #Produit statut
   produit_statut=Produit.query.filter_by(id=id).first_or_404()
   noti=None
   if produit_statut.statut==True:
      produit_statut.statut=False
      message="Vous avez desactivé le produit"
      noti=False
   else:
      produit_statut.statut=True
      message="Vous avez activé le produit"
      noti=True
   
   db.session.commit()
   if noti==True:
      flash(f"{message}", "success")
   else:
      flash(f"{message}", "warning")
      
   return redirect(url_for('produit.index'))
      
   
@produit.route('produit/image/<int:id>', methods=['GET', 'POST'])
def produit_images(id):
   title="edit produit image"
   form=ImageProduitForm()
   #Produit
   produit_ima_ava=Produit.query.filter_by(id=id).first_or_404()
   
   if form.validate_on_submit():
      file=avatar_produit(form.image_produit.data)
      produit_ima_ava.avatar=file
      db.session.commit()
      flash("Avatar mise à jour avec succès", "success")
      return redirect(url_for('produit.produit_images', id=id))
      
   return render_template('produit/upload_image_edit.html', title=title, produit_autres_images=produit_ima_ava, form=form, avatar=produit_ima_ava.avatar, produit_nom=produit_ima_ava.nom)


@produit.route('produit/image/<int:id_produit>/<int:id>', methods=['GET', 'POST'])
def produit_image_sec(id, id_produit):
   
   form=ImageProduitForm()
   #Produit
   if id_produit is None or id is None:
      abort(404)
   produit_ima_ava=Produit.query.filter_by(id=id_produit).first_or_404()
   fichiers_autres=Fichier.query.filter_by(id=id).first_or_404()
   
   if form.validate_on_submit():
      file=avatar_produit(form.image_produit.data)
      fichiers_autres.urlProduit=file
      db.session.commit()
      flash("Modification avec succès de l'image", "success")
      return redirect(url_for('produit.produit_images', id=id_produit))

@produit.route('produit/image/sup/<int:id_produit>/<int:id>', methods=['GET', 'POST'])
def produit_image_sup(id, id_produit):
   #Produit
   if id_produit is None or id is None:
      abort(404)
   produit_ima_ava=Produit.query.filter_by(id=id_produit).first_or_404()
   fichiers_autres=Fichier.query.filter_by(id=id).first_or_404()
   Fichier.query.filter_by(id=id).delete()
   db.session.commit()
   flash("Suppression avec succès", "warning")
   return redirect(url_for('produit.produit_images', id=id_produit))


@produit.route('produit/terminer/op', methods=['GET', 'POST'])
def produit_image_terminer():
   #Produit
   return redirect(url_for('produit.index'))


@produit.route('/add', methods=['GET', 'POST'])
def produit():

   title='produit'
   #Initilisation formaulaire
   form=AddProduitForm()
   session.pop('produit_encours',None)
   
   if form.validate_on_submit():
      file_produit=avatar_produit(form.avatar.data)
      
      produit_enreg=Produit(nom=form.nom.data.capitalize(), 
      cout_production=form.cout_production.data,
      cout_vente_detaille=form.cout_vente_detaille.data,
      cout_vente_engros=form.cout_vente_engros.data,
      description=form.description.data,
      categorie_id=form.categorie_produit.data.id,
      avatar=file_produit)
      #Enregistrement
      db.session.add(produit_enreg)
      db.session.commit()
      session['produit_encours']=produit_enreg.id

      flash("Ajouter autres images", "primary")
      return redirect(url_for('produit.upload_picture'))
      
   return render_template('produit/addProuit.html', title=title, form=form)


