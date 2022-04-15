from .. import db

class Qualification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    poemId = db.Column(db.Integer)
    score = db.Column(db.Integer, primary_key=False)
    comment = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<UserId: {self.userId}, PoemId: {self.poemId}, Score: {self.score}, Comment: {self.comment}>'

    def to_json(self):
        quali_json = {
            'userId': self.userId,
            'poemId': self.poemId,
            'score': self.score,
            'comment': self.comment,
        }
        return quali_json

    def to_json_short(self):
        quali_json = {
            'score': self.score,
            'poemId': self.poemId,
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

