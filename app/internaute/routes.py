from flask import render_template, flash, url_for, redirect, request, session, g
from .. import db, bcrypt
from ..models import User, Produit, Panier
#from app.user.forms import AddUserForm
from app.internaute.function import menu_principale, liste_produit, caroussel_produit, ligne, sumulaire_pro, connexion_client
import flask_sijax
from flask_login import login_user, current_user, login_required


from . import internaute

@flask_sijax.route(internaute, '/',methods=['GET', 'POST'])
def index():
   title='Bienvenu'
   
   def ajouter_panier(obj_response, arg1):
      ver_client=connexion_client()
      if ver_client !=None:
         if arg1 is not None:
            produit_req=Produit.query.filter_by(id=arg1).first_or_404()
            #Vérification du panier
            panier_ver=Panier.query.filter_by(produit_id=produit_req.id, user_id=ver_client ).first()
            if panier_ver is None:
               produit_en=Panier(quantite=1, prix=produit_req.cout_vente_detaille, montant=produit_req.cout_vente_detaille, produit_id=produit_req.id, user_panier=current_user )
               db.session.add(produit_en)
               db.session.commit()
               #Mise à jour du panier
               panier_c=[]  
               panier_contenu=Panier.query.filter_by(user_id=ver_client).all()
               for i in panier_contenu:
                  panier_c.append(i.montant)
               data_panier=render_template('elements/internaute/jquery_page/panier.html',panier_glob=sum(panier_c), panier_contenu=panier_contenu, nbr_panier=len(panier_c) )
               obj_response.html('#panier',data_panier)
            else:
               obj_response.alert("Déjà dans le panier")
      else:
         return redirect(url_for('auth.client_login'))
         
      
   def supp_panier(obj_response, arg1):
      ver_client=connexion_client()
      if ver_client != None:  
         if arg1 is not None:
            #Vérification du panier
            Panier.query.filter_by(id=arg1).first_or_404()
            Panier.query.filter_by(id=arg1).delete()
            db.session.commit()
            panier_c=[]  
            panier_contenu=Panier.query.filter_by(user_id=ver_client).all()
            for i in panier_contenu:
               panier_c.append(i.montant)
            data_panier=render_template('elements/internaute/jquery_page/panier.html',panier_glob=sum(panier_c), panier_contenu=panier_contenu, nbr_panier=len(panier_c) )
            obj_response.html('#panier',data_panier)
      else:
         pass       
       
         
   if g.sijax.is_sijax_request:
      g.sijax.register_callback('ajouter_panier',ajouter_panier)
      g.sijax.register_callback('supp_panier',supp_panier)
      return g.sijax.process_request()
   else:  
      ver_client=connexion_client()
      #La menu de la page
      menu_primaire, menu_secondaire=menu_principale()
      #Liste des produit
      produits=liste_produit()
      #Caroussel
      caroussel=caroussel_produit()  
      #Panier du client 
      panier_c=[]  
      panier_contenu=Panier.query.filter_by(user_id=ver_client).all()
      for i in panier_contenu:
         panier_c.append(i.montant)
         
         
      return render_template('internaute/index.html', panier_glob=sum(panier_c), caroussel=caroussel, panier_contenu=panier_contenu, nbr_panier=len(panier_c), title=title, menu_primaire=menu_primaire, menu_secondaire=menu_secondaire, produits=produits)






@internaute.route('/internaute/categorie', methods=['GET', 'POST'])
def internaute_categorie():
   title='Categorie'
   
   menu_primaire, menu_secondaire=menu_principale()
   
   return render_template('internaute/categorie.html', title=title, menu_primaire=menu_primaire, menu_secondaire=menu_secondaire)




@flask_sijax.route(internaute, '/detail-produit/<int:id>',methods=['GET', 'POST'])
def internaute_detail_produit(id):
   title='Detail produit'
   
   def ajouter_panier(obj_response, arg1):
      ver_client=connexion_client()
      if ver_client !=None:
         if arg1 is not None:
            produit_req=Produit.query.filter_by(id=arg1).first_or_404()
            #Vérification du panier
            panier_ver=Panier.query.filter_by(produit_id=produit_req.id, user_id=ver_client ).first()
            if panier_ver is None:
               produit_en=Panier(quantite=1, prix=produit_req.cout_vente_detaille, montant=produit_req.cout_vente_detaille, produit_id=produit_req.id, user_panier=current_user )
               db.session.add(produit_en)
               db.session.commit()
               #Mise à jour du panier
               panier_c=[]  
               panier_contenu=Panier.query.filter_by(user_id=ver_client).all()
               for i in panier_contenu:
                  panier_c.append(i.montant)
               data_panier=render_template('elements/internaute/jquery_page/panier.html',panier_glob=sum(panier_c), panier_contenu=panier_contenu, nbr_panier=len(panier_c) )
               obj_response.html('#panier',data_panier)
            else:
               obj_response.alert("Déjà dans le panier")
      else:
         return redirect(url_for('auth.client_login'))

   
      
   def supp_panier(obj_response, arg1):
      ver_client=connexion_client()
      if ver_client != None:  
         if arg1 is not None:
            #Vérification du panier
            Panier.query.filter_by(id=arg1).first_or_404()
            Panier.query.filter_by(id=arg1).delete()
            db.session.commit()
            panier_c=[]  
            panier_contenu=Panier.query.filter_by(user_id=ver_client).all()
            for i in panier_contenu:
               panier_c.append(i.montant)
            data_panier=render_template('elements/internaute/jquery_page/panier.html',panier_glob=sum(panier_c), panier_contenu=panier_contenu, nbr_panier=len(panier_c) )
            obj_response.html('#panier',data_panier)
      else:
         pass       
       
         
   if g.sijax.is_sijax_request:
      g.sijax.register_callback('ajouter_panier',ajouter_panier)
      g.sijax.register_callback('supp_panier',supp_panier)
      return g.sijax.process_request()
   else:  
      ver_client=connexion_client()
      #La menu de la page
      menu_primaire, menu_secondaire=menu_principale()
      #Liste des produit
      produits=liste_produit()
      #Caroussel
      caroussel=caroussel_produit()  
      #Panier du client 
      panier_c=[]  
      panier_contenu=Panier.query.filter_by(user_id=ver_client).all()
      for i in panier_contenu:
         panier_c.append(i.montant)
      
      # les informations du produit
      produit_detail=Produit.query.filter_by(id=id, statut=True).first_or_404()
      #Les produits sumulaires
      sum_pro_cat=sumulaire_pro(id,produit_detail.categorie_id)
   

      return render_template('internaute/detail-produit.html', panier_glob=sum(panier_c), panier_contenu=panier_contenu, nbr_panier=len(panier_c), title=title, menu_primaire=menu_primaire, menu_secondaire=menu_secondaire,  produit=produit_detail, sumalire=sum_pro_cat)

   
   
 