from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import QualificationModel
from sqlalchemy import func

class Qualification(Resource):
    def delete(self, id):
        quali = db.session.query(QualificationModel).get_or_404(id)
        db.session.delete(quali)
        db.session.commit()
        return '', 204

    def get(self, id):
        quali = db.session.query(QualificationModel).get_or_404(id)
        return quali.to_json()


class Qualifications(Resource):
    def get(self):
        quali = db.session.query(QualificationModel).all()
        return jsonify([quali.to_json_short() for quali in quali])

    def post(self):
        quali = PoemModel.from_json(request.get_json())
        db.session.add(quali)
        db.session.commit()
        return poem.to_json(), 201
