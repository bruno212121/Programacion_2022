from .. import db

class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, primary_Key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Title: {self.title}, UserId: {self.user_id}, Poem: {self.body}, Date: {self.date}>'

    def to_json(self):
        poem_json = {
            'id': self.id,
            'userId': self.userId,
            'title': self.title,
            'body': self.body,
        }
        return poem_json

    def to_json_short(self):
        poem_json = {
            'id': self.id,
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
        return Poem(id=id,
                     userId=userId,
                     title=title,
                     body=body,
                     )