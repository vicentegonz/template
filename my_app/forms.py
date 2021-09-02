from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from my_app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password =PasswordField('Confirm Password',
                            validators = [DataRequired(), EqualTo('password')])
    register = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    login = SubmitField('Log In')

class OrderForm(FlaskForm):
    producto = StringField('Producto', validators = [DataRequired()])
    cantidad = StringField('Cantidad', validators = [DataRequired()])
    tipo = SelectField("Tipo", choices=["Compra", "Venta"])
    generate = SubmitField("Generar orden")
