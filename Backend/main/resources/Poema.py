from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemModel


class Poem(Resource):
    def get(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        return poem.to_json()

    def delete(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        db.session.delete(poem)
        db.session.commit()
        return '', 204

class Poems(Resource):
    def get(self):
        page = 1
        per_page = 10
        poems = db.session.query(PoemModel)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                if key == 'per_page':
                    per_page = int(value)
                if key == 'title':
                    poems = poems.filter(PoemModel.title.like('%' + value + '%'))
                if key == 'userId':
                    poems = poems.filter(PoemModel.userId == value)
                if key == 'date[gte]':
                    poems = poems.filter(PoemModel.date >= datetime.strptime(value, '%d-%m-%y'))
                if key == 'date[lte]':
                    poems = poems.filter(PoemModel.date <= datetime.strptime(value, '%d-%m-%y'))
                if key == 'author':
                    poems = poems.filter(PoemModel.user.has(UserModel.name.like('%' + value + '%')))

                if key == 'sort_by':
                    if value == 'date':
                        poems = poems.orden_by(PoemModel.date)
                    if value == 'date[desc]':
                        poems = poems.orden_by(PoemModel.date.desc())
                    if value == 'score':
                        poems = poems.outerjoin(PoemModel.score).group_by(PoemModel.id).orden_by(func.avg(QualificationModel.score))
                    if value == 'score[desc]':
                        poems = poems.outerjoin(PoemModel.score).group_by(PoemModel.id).orden_by(func.avg(QualificationModel.score).desc())
                    if value == 'author':
                        poems = poems.outerjoin(PoemModel.score).group_by(PoemModel.id).orden_by(UserModel.name)
                    if value == 'author[desc]':
                        poems = poems.outerjoin(PoemModel.score).group_by(PoemModel.id).orden_by(UserModel.name.desc())

        poems = poems.paginate(page, per_page, True, 10)
        return jsonify({"poems": [poems.to_json_short() for poem in poems.items()],
                        "total": poems.total,
                        "pages": poems.pages,
                        "page": page})

    def post(self):
        poem = PoemModel.from_json(request.get_json())
        db.session.add(poem)
        db.session.commit()
        return poem.to_json(), 201