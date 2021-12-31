# Flask
from flask import redirect, url_for, render_template, session, request, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
import os
import secrets

# Earthelp
from earthelp import app, db, bcrypt, mail
from earthelp.data.models.users import Users
from earthelp.data.models.posts import Posts
from earthelp.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                            PostForm, RequestResetForm, ResetPasswordForm)
from earthelp.services.authentication import *


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): #validate --> chequea que los campos fueron llenados correctamente
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(name=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Successful registration",'succces')
        flash(f"{form.username.data.capitalize()} !! Now log in ")
        return redirect(url_for("login"))
    
    return render_template('register.html', form = form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('start'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email= form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            if teacher_test(user) == True:
                return redirect(url_for('teachers'))
            else:
                return redirect(url_for('start'))
        else:
            flash("Incorrect username or password","danger")
    return render_template('login.html', form = form)


@app.route('/teachers', methods=['GET'])
@login_required
def teachers():
    if teacher_test(current_user) == True: 
        students_list()
        return render_template('teachers.html',students=students_list())
    else:
        return redirect(url_for('start'))
    

@app.route('/start', methods=['GET'])
@login_required
def start():
    return render_template('start.html')


@app.route('/readings', methods=['GET'])
@login_required
def readings():
    return render_template('readings.html')


@app.route('/games', methods=['GET', 'POST'])
@login_required
def games():
    return render_template('games.html')


def save_picture(form_picture):
    ''' Funcion para guardar la imagen del usuario '''
    
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) #Ponemos dos variables porque recibe el nombre del archivo y la extension por separado. Como no vamos a usar el nombre solo ponemos un guion bajo
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (120,120)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Updated account')
        return redirect(url_for('user'))
    elif request.method == 'GET':
        form.username.data = current_user.name
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + 
                         current_user.image_file) #Agrega imagen por defecto
    return render_template('user.html', image_file=image_file, form=form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post have been created', 'succces')
        return redirect(url_for('start'))
    
    return render_template('create_post.html', title='New_post', form=form, legend = 'New post')


@app.route('/post/all', methods=['GET', 'POST'])
@login_required
def read_post():
    posts = Posts.query.all()
    return render_template('read_post.html', posts=posts)

                   #Indico con tipado estatico que el post es un entero
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Posts.query.get_or_404(post_id) #Si no encuentra el post, envia un error 404
    return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Posts.query.get_or_404(post_id) #Si no encuentra el post, envia un error 404
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', "success")
        return redirect(url_for('post', post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update post', form=form, legend = 'Update post')    


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id) #Si no encuentra el post, envia un error 404
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', "success")
    return redirect(url_for('start'))


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('start'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('start'))
    user = Users.verify_reset_token(token)
    if user is None:
        flash ('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit(): #validate --> chequea que los campos fueron llenados correctamente
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to login','success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.errorhandler(403)
def not_found(error):
    return render_template("404.html", error=error)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", error=error)


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html", error=error)