from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_wtf.html5 import URLField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError, url
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Categorie


class AddCatForm(FlaskForm):
    nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=2, max=32, message="Veuillez respecté les caractères")])
    submit = SubmitField('Ajouter une catégorie')

    def validate_nom(self, nom):
        categorie = Categorie.query.filter_by(nom=nom.data).first()
        if categorie:
            raise ValidationError("Cette catégorie existe déjà")

        


class EditeCatForm(FlaskForm):
    nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=2, max=32, message="Veuillez respecté les caractères")])
    submit = SubmitField('Ajouter une catégorie')

    def validate_nom(self, nom):
        categorie = Categorie.query.filter_by(nom=nom.data).first()
        if categorie:
            raise ValidationError("Cette catégorie existe déjà")
