from flask_restful import Resource
from flask import request


QUALIFICATION = {
    1: {'qualification': 5 },
    2: {'qualification': 7},
    3: {'qualification': 8}
}

class Qualification(Resource):
    def delete(self, id):
        if int(id) in QUALIFICATION:
            del QUALIFICATION[int(id)]
            return '', 204
        return '', 404
    def get(self, id):
        if int(id) in QUALIFICATION:
            return QUALIFICATION[int(id)]
        return '', 404

class Qualifications(Resource):
    def get(self):
        return QUALIFICATION
    def post(self):
        quali = request.get_json()
        id = int(max(QUALIFICATION.keys())) + 1
        QUALIFICATION[(id)] = quali
        return QUALIFICATION[id], 201
