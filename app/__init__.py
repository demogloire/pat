import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_login import LoginManager
import flask_sijax


from config import app_config


path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')

db = SQLAlchemy()
login_manager= LoginManager()
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    db.init_app(app)

    migrate = Migrate(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    #Sijax
    app.config['SIJAX_STATIC_PATH'] = path
    app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
    flask_sijax.Sijax(app)
    
    
    
    #Login manager use
    login_manager.login_message = "Veuillez vous connecté"
    login_manager.login_view = "auth.user_login"
    login_manager.login_message_category ='danger'


    from app import models

    #Authentification
    from .authentification import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    #User
    from.user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    #User
    from.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    #Categorie
    from.categorie import categorie as categorie_blueprint
    app.register_blueprint(categorie_blueprint)

     #Produit
    from.produit import produit as produit_blueprint
    app.register_blueprint(produit_blueprint)
    
    #Internaute
    from.internaute import internaute as internaute_blueprint
    app.register_blueprint(internaute_blueprint)
    
     #Client
    from.client import client as client_blueprint
    app.register_blueprint(client_blueprint)



    return app



