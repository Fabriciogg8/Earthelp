# Python
import json
import os
import secrets
from datetime import datetime
from PIL import Image

# APP
from earthelp import app, db, bcrypt, mail

# Flask
from flask_mail import Message
from flask import url_for


def teacher_test(user):
    ''' Funcion que comprueba si el usuario es un Teacher '''
    
    with open("/Users/Usuario/Desktop/EARTHELP/app/earthelp/data/teacherEmail", 'r') as f:
        teacher = json.load(f)
    for key, value in teacher.items():
        if user.email in value:
            return True
        else:
            file_path = "/Users/Usuario/Desktop/EARTHELP/app/earthelp/data/studentsEmail"
            with open(file_path, 'r') as f:
                student = json.load(f)
                student.update({
                        user.email:('Email: ' + user.email + ' - User: ' + user.name + ' - Last login: '
                                    + datetime.now().strftime('%d/%m/%Y - %H:%M'))
                        })
            with open(file_path, 'w') as f:
                json.dump(student, f)
            return False

def students_list():
    ''' Funcion que imprime una lista de los estudiantes '''
    file_path = "/Users/Usuario/Desktop/EARTHELP/app/earthelp/data/studentsEmail"
    with open(file_path, 'r') as f:
        student = json.load(f)
        list = []
        for key, value in student.items():
            list.append(value)
    return list
    
    
def save_picture(form_picture):
    ''' Funcion para guardar la imagen del usuario '''
    
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) #Ponemos dos variables porque recibe el nombre del archivo y la extension por separado. Como no vamos a usar el nombre solo ponemos un guion bajo
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, '/app/earthelp/static/profile_pics', picture_fn)
    output_size = (120,120)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    ''' Funcion para solicitar un email para recuperar
        la contrasena'''
        
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
            sender='fgonzalezguasque@gmail.com', 
            recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)} 
    
If you didn't make this request then simply ignore this email
    '''
    mail.send(msg)