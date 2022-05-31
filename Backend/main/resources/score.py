from xmlrpc.client import TRANSPORT_ERROR
from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ScoreModel, UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import poeta_required, admin_required_or_poeta_required
from flask_mail import Mail
from main.mail.functions import sendMail

class Score(Resource):
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
    @jwt_required
    def delete(self, id):
        claims = get_jwt()
        user_id = get_jwt_identity()
        score = db.session.query(ScoreModel).get_or_404(id)
        if "rol" in claims:
            if claims['rol'] == "admin" or user_id == score.user_id:
                db.session.delete(score)
                db.session.commit()
                return '', 204
            else:
                return "Only admins and users can delete qualifications"


class Scores(Resource):
    @jwt_required()
    def get(self):
        scores = db.session.query(ScoreModel).all()
        return jsonify([score.to_json_short() for score in scores])


    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        score = ScoreModel.from_json(request.get_json())
        user_score = db.session.query(UserModel).get(user_id)
        claims = get_jwt()
        if "rol" in claims:
            if claims['rol'] == "poeta":
                score.userId = int(user_id)
                db.session.add(score)
                db.session.commit()
                sent = sendMail([score.poem.user], "Has recibido una calificación", 'register', user_score=user_score,
                                user=score.poem.user, poem=score.poem)
                return score.to_json(), 201
            else:
                return "Este usuario no está autorizado para realizar esta acción."
