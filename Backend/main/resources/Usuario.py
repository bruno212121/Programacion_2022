from flask_restful import Resource
from flask import request

USUARIOS = {
    1 : {'firstname' : 'Sacha', 'lastname' : 'Fenske'},
    2 : {'firstname' : 'Santiago', 'lastname' : 'Moyano'},
    3 : {'firstname' : 'Lucas', 'lastname' : 'Galdame'},
    4 : {'firstname' : 'Bruno', 'lastname' : 'Rosales'},
    5 : {'firstname' : 'Douglas', 'lastname' : 'Arenas'}
}

class User(Resource):
    def get(self,id):
        if int(id) in USUARIOS:
            return USUARIOS[int(id)]
        return '', 404
    def delete(self, id):
        if int(id) in USUARIOS:
            del USUARIOS[int(id)]
            return '', 204
        return '', 404

class Users(Resource):
    def get(self):
        return USUARIOS
    def post(self):
        user = request.get_json()
        id = int(max(USUARIOS.keys())) + 1
        USUARIOS[(id)] = user
        return USUARIOS[id], 201

