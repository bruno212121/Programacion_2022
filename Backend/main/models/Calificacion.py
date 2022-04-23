from .. import db

class Qualification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    poemId = db.Column(db.Integer, db.ForeignKey('poem.id'), nullable=False)
    score = db.Column(db.Integer, primary_key=False)
    comment = db.Column(db.String(100), nullable=False)


    user = db.relationship('User', back_populates="qualification", uselist=False, single_parent=True)
    poem = db.relationship('Poem', back_populates="qualification", uselist=False, single_parent=True)


    def __repr__(self):
        return f'<UserId: {self.userId}, PoemId: {self.poemId}, Score: {self.score}, Comment: {self.comment}>'

    def to_json(self):
        poem = [poem.to_json() for poem in self.poem]
        user = [user.to_json() for user in self.user]
        quali_json = {
            'id': self.id,
            'name': (self.name),
            'password': (self.password),
            'rol': (self.rol),
            'email': (self.email),
            'poem': poem,
            'user': user,
        }
        return quali_json

    def to_json_short(self):
        quali_json = {
            'id': self.id,
            'score': int(self.score),
            'comment': str(self.comment),
            'userId': self.user.to_json(),
            'poemId': self.poem.to_json(),
        }
        return quali_json

    @staticmethod

    def from_json(quali_json):
        id = quali_json.get('id')
        poemId = quali_json.get('poemId')
        score = quali_json.get('score')
        comment = quali_json.get('comment')
        return quali(id=id,
                     poemId=poemId,
                     score=score,
                     comment=comment,
                     )

