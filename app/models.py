from app import db, login_manager
from datetime import datetime, date
from sqlalchemy.orm import backref
from flask_login import UserMixin, current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(120))
    cout_production=db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    cout_vente_detaille=db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    cout_vente_engros=db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    avatar = db.Column(db.String(120), default='avatar.jpg' )
    description=db.Column(db.Text)
    statut=db.Column(db.Boolean, default=True)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'), nullable=False)
    ventes = db.relationship('Vente', backref='vente_produit', lazy='dynamic')
    fichiers = db.relationship('Fichier', backref='produit_fichier', lazy='dynamic')
    paniers = db.relationship('Panier', backref='produit_panier', lazy='dynamic')
    

class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(120))
    priorite=db.Column(db.Boolean, default=False)
    statut=db.Column(db.Boolean, default=True)
    produits = db.relationship('Produit', backref='categorie_produit', lazy='dynamic')
    relation_produit=db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(120))
    post_nom = db.Column(db.String(120))
    prenom = db.Column(db.String(120))
    telephone=db.Column(db.String(120))
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    adresse_u = db.Column(db.String(120))
    adresse_d = db.Column(db.String(120))
    pays= db.Column(db.String(120))
    type_user = db.Column(db.String(120))
    statut = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String(120), default='default.png' )
    categories = db.relationship('Categorie', backref='user_categorie', lazy='dynamic')
    paniers = db.relationship('Panier', backref='user_panier', lazy='dynamic')
    depenses = db.relationship('Depense', backref='user_depense', lazy='dynamic')
    commandes = db.relationship('Commande', backref='user_commande', lazy='dynamic')

class Panier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantite = db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    prix = db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    montant = db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)

class Commande(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code= db.Column(db.String(120))
    montantGenerale = db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    date_commande = db.Column(db.Date, default=datetime.utcnow)
    livraison = db.Column(db.Boolean)
    date_livraison = db.Column(db.Date, default=datetime.utcnow)
    statut = db.Column(db.Boolean)
    lieu_de_livraison=db.Column(db.String(120))
    telphone=db.Column(db.String(20))
    montant_echellon = db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    ventes = db.relationship('Vente', backref='commande_vente', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    payements = db.relationship('Payement', backref='commande_payement', lazy='dynamic')

class Payement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_payement=db.Column(db.String(120))
    somme = db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    commande_id = db.Column(db.Integer, db.ForeignKey('commande.id'), nullable=False)
    
class Vente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantite = db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    prix = db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    montant = db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    commande_id = db.Column(db.Integer, db.ForeignKey('commande.id'), nullable=False)

class Fichier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    urlProduit = db.Column(db.String(120))
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)

class Compte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(120))
    statut = db.Column(db.Boolean)
    depenses = db.relationship('Depense', backref='compte_depense', lazy='dynamic')

class Depense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    DateDepense = db.Column(db.Date, default=date.today())
    montant = db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    compte_id = db.Column(db.Integer, db.ForeignKey('compte.id'), nullable=False)