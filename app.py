from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required
from config import Config
from models import db, User
from auth import auth as auth_blueprint
from api import api_bp  # <-- 1. Importar el blueprint de la API
import controllers

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar BD
db.init_app(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Inicia sesión para acceder a GameVault.'
login_manager.login_message_category = 'warning'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registrar Blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(api_bp, url_prefix='/api')  # <-- 2. Registrar el blueprint de la API con prefijo /api

# -------------------------------------------------------------
# Rutas Protegidas del CRUD
# -------------------------------------------------------------

@app.route('/')
@app.route('/juegos')
@login_required
def index():
    juegos = controllers.obtener_juegos()
    return render_template('index.html', juegos=juegos)

@app.route('/juegos/agregar', methods=['GET', 'POST'])
@login_required
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        controllers.insertar_juego(nombre, descripcion, precio)
        return redirect(url_for('index'))
    return render_template('agregar.html')

@app.route('/juegos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    juego = controllers.obtener_juego_por_id(id)
    if not juego:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        controllers.actualizar_juego(id, nombre, descripcion, precio)
        return redirect(url_for('index'))

    return render_template('editar.html', juego=juego)

@app.route('/juegos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    controllers.eliminar_juego(id)
    return redirect(url_for('index'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=8000)
