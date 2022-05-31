from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel
from datetime import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required, admin_required_or_poeta_required

class User(Resource):

    @jwt_required()
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json()

    @admin_required_or_poeta_required
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(user, key, value)
            db.session.add(user)
            db.session.commit()
        return user.to_json(), 201

    @admin_required_or_poeta_required
    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


class Users(Resource):

    @admin_required
    def get(self):
        page = 1
        per_page = 10
        users = db.session.query(UserModel)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == "page":
                    page = int(value)
                if key == "per_page":
                    per_page = value
                if key == "name":
                    users = users.filter(UserModel.name.like("%"+value+"%"))

                if key == 'sort_by':
                    if value == 'name':
                        users = users.orden_by(UserModel.name)
                    if value == 'name[desc]':
                        users = users.orden_by(UserModel.name.desc())

        users = users.paginate(page, per_page, True, 30)
        return jsonify({'users': [user.to_json() for user in users.items],
                        'total': users.total,
                        'pages': users.pages,
                        'page': page})

    @admin_required
    def post(self):
        users = UserModel.from_json(request.get_json())
        db.session.add(users)
        db.session.commit()
        return users.to_json(), 201
