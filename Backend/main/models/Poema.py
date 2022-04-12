from .. import db

class Poema(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, primary_Key=True)
    title = db.Column(db.String(100), nullable=False )
    body = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        poem_json = {
            'id': self.id,
            'userId': self.userId,
            'title': self.title,
            'body': self.body,
        }
        return poem_json
    @staticmethod

    def from_json(poem_json):
        id = poem_json.get('id')
        userId = poem_json.get('userId')
        title = poem_json.get('title')
        body = poem_json.get('body')
        return Poema(id=id,
                     userId=userId,
                     title=title,
                     body=body,
                     )