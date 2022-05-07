from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ScoreModel


class Score(Resource):

    def delete(self, id):
        score = db.session.query(ScoreModel).get_or_404(id)
        db.session.delete(score)
        db.session.commit()
        return '', 204

    def get(self, id):
        score = db.session.query(ScoreModel).get_or_404(id)
        return score.to_json()


class Scores(Resource):

    def get(self):
        scores = db.session.query(ScoreModel).all()
        return jsonify([score.to_json_short() for score in scores])

    def post(self):
        score = ScoreModel.from_json(request.get_json())
        db.session.add(score)
        db.session.commit()
        return score.to_json(), 201
