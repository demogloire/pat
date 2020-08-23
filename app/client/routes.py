from flask import render_template, flash, url_for, redirect, request, session, g
from .. import db, bcrypt
from ..models import User, Produit, Panier, Commande, Vente
from app.client.forms import QuantiteForm, PremierPayementForm
from app.client.function import  produit_panier, autorisation_client, numero_commande
from flask_login import login_user, current_user, login_required
import flask_sijax


from . import client

@client.route('/dash', methods=['GET', 'POST'])
@login_required
@autorisation_client
def index():
   title='Dashboard'
   milieu=produit_panier() 
   return render_template('client/index.html', milieu=milieu)



@client.route('/<int:id>', methods=['GET', 'POST'])
@login_required
@autorisation_client
def voir_panier_val(id):
   title='Dashboard'
   #Formulaire
   form=QuantiteForm()
   
   if form.validate_on_submit():
      ver_produit=Panier.query.filter_by(produit_id=id, user_id=current_user.id).first_or_404()
      valueur=float(form.quant.data)*float(ver_produit.prix)
      ver_produit.quantite=form.quant.data
      ver_produit.prix=ver_produit.prix    
      ver_produit.montant=valueur
      db.session.commit()
      return redirect(url_for('client.voir_panier'))
   else:
      return redirect(url_for('client.voir_panier'))



@flask_sijax.route(client,'/voir/panier',methods=['GET', 'POST'])
@login_required
@autorisation_client
def voir_panier():
   title='Dashboard'
   #Produit
   def supp_panier(obj_response, arg1): 
      form=QuantiteForm()
      if arg1 is not None:
         #Vérification du panier
         Panier.query.filter_by(id=arg1, user_id=current_user.id).first_or_404()
         Panier.query.filter_by(id=arg1, user_id=current_user.id).delete()
         db.session.commit()
         milieu=produit_panier() 
         sum_panier=[]
         for i in milieu:
            sum_panier.insert(0,i.montant)
         valeur_total=sum(sum_panier)
         data_panier=render_template('elements/internaute/jquery_page/client_panier.html', milieu=milieu, valeur_total=valeur_total, form=form )
         obj_response.html('#panier',data_panier)
   
   if g.sijax.is_sijax_request:
      g.sijax.register_callback('supp_panier',supp_panier)
      return g.sijax.process_request()
   else:  
      milieu=produit_panier() 
      sum_panier=[]
      for i in milieu:
         sum_panier.insert(0,i.montant)
      valeur_total=sum(sum_panier)
      form=QuantiteForm()
      return render_template('client/voirpanier.html', milieu=milieu, valeur_total=valeur_total, form=form)



@client.route('/commander', methods=['GET', 'POST'])
@login_required
@autorisation_client
def commander():
   title='Commande'
   #Selection pannier
   panier_ensmebre=Panier.query.filter_by(user_id=current_user.id).all()   
   if panier_ensmebre==[]:
      return redirect(url_for('internaute.index'))
   else:
      liste_panier_somme=[]
      
      #Enregistrement des produits pour vente
      commande=Commande(code=numero_commande(current_user), user_id=current_user.id)
      db.session.add(commande)
      db.session.commit()
      #Enregistrement du produit pour commande
      for produit in panier_ensmebre:
         liste_panier_somme.append(produit.montant)
         produit=Vente(quantite=produit.quantite, prix=produit.prix, montant=produit.montant, produit_id=produit.produit_id,
                       commande_vente=commande)
         db.session.add(produit)
         db.session.commit()
      #Supression du panier
      for produit in panier_ensmebre:
         Panier.query.filter_by(id=produit.id).delete()
         db.session.commit()
      #Mie à jour de la facture du commande
      mise_a_jour=Commande.query.filter_by(id=commande.id).first()
      mise_a_jour.montantGenerale=sum(liste_panier_somme)
      db.session.commit()
      #Envoie en session des élèment de la session
      session['id_commande']=commande.id
      flash("Information livraison et paiement","success")
      return redirect(url_for('client.premier_payement'))

@client.route('/premier/payement', methods=['GET', 'POST'])
@login_required
@autorisation_client
def premier_payement():
   title='Payement'
   #Formulaire
   form=PremierPayementForm()
   return render_template('client/effectuer_payement.html', title=title, form=form)
      
         
         
         
         
      
      
      
      





