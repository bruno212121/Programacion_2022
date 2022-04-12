from flask_restful import Resource
from flask import request
from .. import db
from main.models import PoemaModel


class Poem(Resource):
    def get(self,id):
        poem = db.session.query(PoemaModel).get_or_404(id)
        return poem.to_json()

def delete(self,id):
        poem = db.session.query(PoemaModel).get_or_404(id)
        db.session.delete(poem)
        db.session.commit()
        return '', 204

class Poems(Resource):
    def get(self):
        poems = db.session.query(PoemaModel).all()
        return jsonify([poem.to_json_short() for poem in poems])

    def post(self):
        poem = PoemaModel.from_json(request.get_json())
        db.session.add(poem)
        db.session.commit()
        return poem.to_json(), 201