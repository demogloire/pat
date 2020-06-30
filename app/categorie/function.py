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

def avatar(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/image', picture_fn)
    output_sz = (370,350)
    i= Image.open(form_picture)
    i.thumbnail(output_sz)
    i.save(picture_path)
    return picture_fn


#Autorisation admin
def autorisation_super_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.type_user =='Super admin':
            return f(*args, **kwargs)
        else:
            return redirect(url_for('main.main'))       
    return wrap
