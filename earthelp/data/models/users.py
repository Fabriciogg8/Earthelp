from earthelp import db, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
from earthelp.data.models.posts import *
from flask_login import UserMixin

@login_manager.user_loader  #funcion para autentificar el usuario al iniciar sesión
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique= True, nullable= False)
    email = db.Column(db.String(100), unique= True, nullable= False)
    image_file = db.Column(db.String(20), nullable= False, default='default.png')
    password = db.Column(db.String(100), nullable= False)
    posts = db.relationship('Posts', backref='author', lazy=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('UTF-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Users.query.get(user_id)


