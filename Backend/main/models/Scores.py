from .. import db


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    poemId = db.Column(db.Integer, db.ForeignKey('poem.id'), nullable=False)
    score = db.Column(db.Integer, primary_key=False)
    comment = db.Column(db.String(100), nullable=False)

    user = db.relationship('User', back_populates="scores", uselist=False, single_parent=True)
    poem = db.relationship('Poem', back_populates="scores", uselist=False, single_parent=True)

    def __repr__(self):
        score_json = {
            'id': self.id,
            'score': self.score,
            'comment': self.comment,
            'user': [user.to_json_short() for user in self.user],
            'poem': [poem.to_json_short() for poem in self.poem]
        }
        return score_json

    def to_json(self):
        score_json = {
            'id': self.id,
            'score': self.score,
            'comment': self.comment,
            'user': self.user.to_json_short(),
            'poem': self.poem.to_json_short()
        }
        return score_json

    def to_json_short(self):
        score_json = {
            'id': self.id,
            'userId': self.userId,
            'poemId': self.poemId,
            'score': int(self.score),
            'comment': str(self.comment),
        }
        return score_json

    @staticmethod
    def from_json(score_json):
        id = score_json.get('id')
        userId = score_json.get('userId')
        poemId = score_json.get('poemId')
        score = score_json.get('score')
        comment = score_json.get('comment')
        return Score(id=id,
                     userId=userId,
                     poemId=poemId,
                     score=score,
                     comment=comment,
                     )
