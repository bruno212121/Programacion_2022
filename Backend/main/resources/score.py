from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ScoreModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import poeta_required, admin_required_or_poeta_required

class Score(Resource):
    @jwt_required()
    def delete(self, id):
        score = db.session.query(ScoreModel).get_or_404(id)
        db.session.delete(score)
        db.session.commit()
        return '', 204
    @jwt_required()
    def get(self, id):
        score = db.session.query(ScoreModel).get_or_404(id)
        return score.to_json_short()
    @jwt_required()
    def put(self, id):
        score = db.session.query(ScoreModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(score, key, value)

class Scores(Resource):
    @jwt_required()
    def get(self):
        scores = db.session.query(ScoreModel).all()
        return jsonify([score.to_json_short() for score in scores])
    @poeta_required
    def post(self):
        score = ScoreModel.from_json(request.get_json())
        db.session.add(score)
        db.session.commit()
        return score.to_json_short(), 201
