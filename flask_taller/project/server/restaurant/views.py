# project/server/restaurant/views.py

from flask import request, make_response, jsonify
from flask.views import MethodView

from project.server import db, api, app
from project.server.models import Restaurante, User, BlacklistToken
from flask_restful import Resource
import jwt
from flask_marshmallow import Marshmallow
from sqlalchemy import desc


ma = Marshmallow(app)

class Restaurante_Schema(ma.Schema):
    class Meta:
        fields = ("id","nombre","lugar","categoria","direccion","telefono","logo_rest","menu","domicilio","user_id")

post_schema = Restaurante_Schema() #Un solo restaurante
posts_schema = Restaurante_Schema(many = True) # varios restaurantes

def get_token(auth_header):
    # get auth token
    ans = False
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            ans = True
    return ans


class RecursoListarRestaurantes(Resource):
    
    def get(self):
        auth_header = request.headers.get('Authorization')
        auth_token = get_token(auth_header)
        if auth_token:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, app.config.get('SECRET_KEY'))
            restaurantes = Restaurante.query.filter_by(user_id=payload['sub']).order_by(desc(Restaurante.id))
            return posts_schema.dump(restaurantes)
        else:
            responseObject = {
                'status': 'Error',
                'message': 'acceso denegado!, inicia sesion para adquirir permisos'
            }
            return make_response(jsonify(responseObject))

    def post(self):
        auth_header = request.headers.get('Authorization')
        auth_token = get_token(auth_header)
        if auth_token:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, app.config.get('SECRET_KEY'))
            nuevo_restaurante = Restaurante(
                nombre = request.json['nombre'],
                lugar = request.json['lugar'],
                categoria = request.json['categoria'],
                direccion = request.json['direccion'],
                telefono = request.json['telefono'],
                logo_rest = request.json['logo_rest'],
                menu = request.json['menu'],
                domicilio = request.json['domicilio'],
                user_id = payload['sub']
            )
            db.session.add(nuevo_restaurante)
            db.session.commit()
            return post_schema.dump(nuevo_restaurante)
        else:
            responseObject = {
                'status': 'Error',
                'message': 'acceso denegado!, inicia sesion para adquirir permisos'
            }
            return make_response(jsonify(responseObject))

class RecursoUnRestaurante(Resource):
    
    def get(self, id_restaurante):
        auth_header = request.headers.get('Authorization')
        auth_token = get_token(auth_header)
        if auth_token:
            restaurante = Restaurante.query.get_or_404(id_restaurante)
            return post_schema.dump(restaurante)
        else:
            responseObject = {
                'status': 'Error',
                'message': 'acceso denegado!, inicia sesion para adquirir permisos'
            }
            return make_response(jsonify(responseObject))

    def put(self, id_restaurante):
        auth_header = request.headers.get('Authorization')
        auth_token = get_token(auth_header)
        if auth_token:

            restaurante = Restaurante.query.get_or_404(id_restaurante)
            if 'nombre' in request.json:
                restaurante.nombre = request.json['nombre']
            if 'lugar' in request.json:
                restaurante.lugar = request.json['lugar']
            if 'categoria' in request.json:
                restaurante.categoria = request.json['categoria']
            if 'direccion' in request.json:
                restaurante.direccion = request.json['direccion']
            if 'telefono' in request.json:
                restaurante.telefono = request.json['telefono']
            if 'logo_rest' in request.json:
                restaurante.logo_rest = request.json['logo_rest']
            if 'menu' in request.json:
                restaurante.menu = request.json['menu']
            if 'domicilio' in request.json:
                restaurante.domicilio = request.json['domicilio']
            
            db.session.commit()
            return post_schema.dump(restaurante)
        else:
            responseObject = {
                'status': 'Error',
                'message': 'acceso denegado!, inicia sesion para adquirir permisos'
            }
            return make_response(jsonify(responseObject))

    def delete(self, id_restaurante):
        auth_header = request.headers.get('Authorization')
        auth_token = get_token(auth_header)
        if auth_token:

            restaurante = Restaurante.query.get_or_404(id_restaurante)
            db.session.delete(restaurante)
            db.session.commit()
            return 'Eliminacion Exitosa'
        else:
            responseObject = {
                'status': 'Error',
                'message': 'acceso denegado!, inicia sesion para adquirir permisos'
            }
            return make_response(jsonify(responseObject))
        



