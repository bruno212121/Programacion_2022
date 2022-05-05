import statistics
from .. import db


class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', back_populates="poem", uselist=False, single_parent=True)
    qualification = db.relationship('Qualification', back_populates="poem", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Title: {self.title}, UserId: {self.user_id}, Poem: {self.body}, Date: {self.date}>'

    def get_average_qualification(self):
        if len(self.qualification) == 0:
            return 0
        else:
            qualification_list = []
            for qualification in self.qualification:
                qualification_list.append(qualification.qualification)
                return statistics.mean(qualification_list)

    def to_json(self):
        poem_json = {
            'id': self.id,
            'userId': self.userId,
            'title': self.title,
            'body': self.body,
            'date': str(self.date.strftime("%d-%m-%Y")),
            'avg_qualification': self.get_average_qualification(),
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
