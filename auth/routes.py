from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from .forms import LoginForm, RegistrationForm
from models import db, User

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('index')
            flash(f'¡Bienvenido de nuevo, {user.username}!', 'success')
            return redirect(next_page)
        flash('Correo electrónico o contraseña no válidos.', 'danger')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data.lower(),
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
