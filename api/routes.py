from flask import request
from flask_restful import Api, Resource, fields, marshal_with
from models import db, Juego
from . import api_bp

api = Api(api_bp)

# Estructura de serialización JSON (Capítulo 14 / Flask-RESTful)
juego_fields = {
    'id': fields.Integer,
    'nombre': fields.String,
    'descripcion': fields.String,
    'precio': fields.Float
}

class JuegoListResource(Resource):
    """
    Endpoint para listar todos los videojuegos o crear uno nuevo.
    """
    @marshal_with(juego_fields)
    def get(self):
        """GET /api/juegos - Retorna la lista completa de videojuegos (200 OK)"""
        juegos = Juego.query.all()
        return juegos, 200

    @marshal_with(juego_fields)
    def post(self):
        """POST /api/juegos - Crea un nuevo videojuego recibiendo JSON (201 Created)"""
        data = request.get_json() or {}
        
        # Validación básica de payload
        if 'nombre' not in data or 'precio' not in data:
            return {'error': 'Faltan campos obligatorios (nombre, precio)'}, 400

        nuevo_juego = Juego(
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            precio=float(data['precio'])
        )
        db.session.add(nuevo_juego)
        db.session.commit()
        
        return nuevo_juego, 201


class JuegoResource(Resource):
    """
    Endpoint para consultar, actualizar o eliminar un videojuego por ID.
    """
    @marshal_with(juego_fields)
    def get(self, id):
        """GET /api/juegos/<id> - Obtiene los detalles de un videojuego"""
        juego = Juego.query.get(id)
        if not juego:
            return {'error': 'Juego no encontrado'}, 404
        return juego, 200

    @marshal_with(juego_fields)
    def put(self, id):
        """PUT /api/juegos/<id> - Actualiza un videojuego existente"""
        juego = Juego.query.get(id)
        if not juego:
            return {'error': 'Juego no encontrado'}, 404

        data = request.get_json() or {}
        if 'nombre' in data:
            juego.nombre = data['nombre']
        if 'descripcion' in data:
            juego.descripcion = data['descripcion']
        if 'precio' in data:
            juego.precio = float(data['precio'])

        db.session.commit()
        return juego, 200

    def delete(self, id):
        """DELETE /api/juegos/<id> - Elimina un videojuego (204 No Content)"""
        juego = Juego.query.get(id)
        if not juego:
            return {'error': 'Juego no encontrado'}, 404

        db.session.delete(juego)
        db.session.commit()
        return '', 204


# Registro de Recursos en la API
api.add_resource(JuegoListResource, '/juegos')
api.add_resource(JuegoResource, '/juegos/<int:id>')
