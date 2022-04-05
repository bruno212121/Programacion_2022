from flask_restful import Resource
from flask import request

POEMAS = {
    1: {'firstname': 'DON QUIJOTE0', 'lastname': 'DE LA MANCHA'},
    2: {'firstname': 'HERCULES', 'lastname': 'GAGO'},
}

class Poem(Resource):
    def get(self,id):
        if int(id) in POEMAS:
            return POEMAS[int(id)]
        return '', 404

    def delete(self,id):
        if int(id) in POEMAS:
            del POEMAS[int(id)]
            return '', 204
        return '', 404

class Poems(Resource):
    def get(self):
        return POEMAS
    def post(self):
        poem = request.get_json()
        id = int(max(POEMAS.keys())) + 1
        POEMAS[id] = poem
        return POEMAS[id], 201