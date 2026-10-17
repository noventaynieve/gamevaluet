from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User

class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir.')])
    submit = SubmitField('Registrarse')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('El correo electrónico ya está registrado.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('El nombre de usuario ya está ocupado.')
