import os
import secrets
from flask import render_template, flash, url_for, redirect, request, session
from flask_login import login_user, current_user, login_required
from PIL import Image
from .. import create_app
from .. import db
from functools import wraps


config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

def avatar_produit(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/produit', picture_fn)
    output_sz = (600,500)
    i= Image.open(form_picture)
    i.thumbnail(output_sz)
    i.save(picture_path)
    return picture_fn

#Vérification ID du produit
def session_id(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'produit_encours' in session:
            print(session['produit_encours'],'-------------------------------------gdgsds---------------------')
            return f(*args, **kwargs)
        else:
            return redirect(url_for('produit.produit'))       
    return wrap

#Vérification produit
def ver_session():
    if 'produit_encours' in session:
        return session['produit_encours']
    
    





