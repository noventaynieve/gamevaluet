import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_required
from werkzeug.exceptions import HTTPException
from config import Config
from models import db, User
from auth import auth as auth_blueprint
from api import api_bp  # Blueprint de la API
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
app.register_blueprint(api_bp, url_prefix='/api')

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

# -------------------------------------------------------------
# Manejadores de Errores Personalizados y JSON para API
# -------------------------------------------------------------

@app.errorhandler(400)
def bad_request_error(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Bad Request', 'message': str(error)}), 400
    return render_template('400.html'), 400

@app.errorhandler(404)
def not_found_error(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not Found', 'message': 'Recurso no encontrado'}), 404
    return render_template('404.html'), 404

@app.errorhandler(405)
def method_not_allowed_error(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Method Not Allowed', 'message': 'Método HTTP no permitido'}), 405
    return render_template('405.html'), 405

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal Server Error', 'message': 'Error interno del servidor'}), 500
    return render_template('500.html'), 500

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    if request.path.startswith('/api/'):
        return jsonify({'error': e.name, 'description': e.description}), e.code
    return e

# -------------------------------------------------------------
# Configuración del Sistema de Registro (Logs en errors.log)
# -------------------------------------------------------------
if not app.debug:
    file_handler = RotatingFileHandler('errors.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('GameVault startup')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=8000)
