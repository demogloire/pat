from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_wtf.html5 import URLField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError, url
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import User


class AddUserForm(FlaskForm):
    nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=2, max=32, message="Veuillez respecté les caractères")])
    post_nom= StringField('Post-nom', validators=[DataRequired("Completer post nom"),  Length(min=2, max=32, message="Veuillez respecté les caractères")])
    prenom= StringField('Prenom', validators=[DataRequired("Completer prenom"),  Length(min=2, max=32, message="Veuillez respecté les caractères")])
    username= StringField('Email', validators=[DataRequired('Veuillez completer votre email'), Email('Votre email est incorrect')])
    password= PasswordField('Mot de passe', validators=[DataRequired('Veuillez completer votre mot de passe'), EqualTo('confirm','Le mot de passe ne pas le même')])
    confirm=PasswordField('Répeter le mot de passe')
    role= SelectField('Rôle',choices=[('Super admin', 'Super admin'), ('Admin', 'Admin')], default="Choisir le rôle")
    submit = SubmitField('Ajouter user')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Cet utilisateur existe déjà")


class EditeUserForm(FlaskForm):
    nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=2, max=32, message="Veuillez respecté les caractères")])
    post_nom= StringField('Post-nom', validators=[DataRequired("Completer post nom"),  Length(min=2, max=32, message="Veuillez respecté les caractères")])
    prenom= StringField('Prenom', validators=[DataRequired("Completer prenom"),  Length(min=2, max=32, message="Veuillez respecté les caractères")])
    username= StringField('Email', validators=[DataRequired('Veuillez completer votre email'), Email('Votre email est incorrect')])
    role= SelectField('Rôle',choices=[('Super admin', 'Super admin'), ('Admin', 'Admin')], default="Choisir le rôle")
    submit = SubmitField('Ajouter user')