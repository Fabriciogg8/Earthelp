from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os


app = Flask(__name__)
app.secret_key = "super_secret_key"
app.permanent_session_lifetime = timedelta(minutes = 30) # duración de la session despues de cerrar el navegador

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///earthelp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
bcrypt = Bcrypt(app) #para guardar el password de forma segura
login_manager = LoginManager(app) #inicialización de flask_login
login_manager.login_view = 'login'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)


from earthelp import routes
from earthelp.services.authentication import *

app.jinja_env.globals.update(teacher_test=teacher_test, students_list=students_list)