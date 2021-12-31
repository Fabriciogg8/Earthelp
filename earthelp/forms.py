from earthelp.data.models.users import Users
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])  
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])  
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])  
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = Users.query.filter_by(name=username.data).first() #name porque viene de la columna de users carpeta models
        if user:
            raise ValidationError('Usuario inválido | Invalid user')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first() 
        if user:
            raise ValidationError('Email inválido | Invalid email')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])  
    remember = BooleanField('Remember me') 
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])  
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.name:
            user = Users.query.filter_by(name=username.data).first() 
            if user:
                raise ValidationError('Usuario inválido | Invalid user')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first() 
            if user:
                raise ValidationError('Email inválido | Invalid email')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first() 
        if user is None:
            raise ValidationError('There is no account with that email. You must register first')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])  
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')