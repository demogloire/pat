from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_wtf.html5 import URLField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError, url
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Produit, Categorie



def categorie_select():
    return Categorie.query.filter_by(statut=True).all()

class AddProduitForm(FlaskForm):
    nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=2, max=32, message="Veuillez respecté les caractères")])
    cout_production= DecimalField('Cout production', validators=[DataRequired("Completer le cout de production")])
    cout_vente_detaille= DecimalField('Cout vente detail', validators=[DataRequired("Completer prenom")])
    cout_vente_engros = DecimalField('Cout vente en gros', validators=[DataRequired("Completer numéro téléphone")])
    description= TextAreaField('Description', validators=[DataRequired('Veuillez completer la description')])
    avatar= FileField("Image",validators=[FileAllowed(['jpg','png'],'Seul jpg et png sont autorisés')])
    categorie_produit=QuerySelectField(query_factory=categorie_select, get_label='nom', allow_blank=False, blank_text='Choisir la catagorie')
    submit = SubmitField('Ajouter Produit')


    def validate_produit(self, nom):
        produit = Produit.query.filter_by(nom=nom.data).first()
        if produit:
            raise ValidationError("Ce produit existe déjà")


class EditerProduitForm(FlaskForm):
    nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=2, max=32, message="Veuillez respecté les caractères")])
    cout_production= DecimalField('Cout production', validators=[DataRequired("Completer le cout de production")])
    cout_vente_detaille= DecimalField('Cout vente detail', validators=[DataRequired("Completer prenom")])
    cout_vente_engros = DecimalField('Cout vente en gros', validators=[DataRequired("Completer numéro téléphone")])
    description= TextAreaField('Description', validators=[DataRequired('Veuillez completer la description')])
    #avatar= FileField("Image",validators=[DataRequired("L'image du produit svp"), FileAllowed(['jpg','png'],'Seul jpg et png sont autorisés')])
    categorie_produit=QuerySelectField(query_factory=categorie_select, get_label='nom', allow_blank=False, blank_text='Choisir la catagorie')
    submit = SubmitField('Ajouter Produit')
    


class ImageProduitForm(FlaskForm):
    image_produit= FileField("Image",validators=[DataRequired("Uploqd l'image"), FileAllowed(['jpg','png'],'Seul jpg et png sont autorisés')])
    submit = SubmitField('Ajouter Image')


