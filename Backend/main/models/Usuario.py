from .. import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    approbation = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(100), nullable=False)
    qualification = db.relationship('Qualification', back_populates="user", cascade="all, delete-orphan")
    poem = db.relationship('Poem', back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Name: {self.name}, Email: {self.email}, Pass: {self.approbation}, Rol: {self.rol}>'

    def to_json(self):
        qualification = [quali.to_json() for quali in self.qualification]
        poem = [poem.to_json() for poem in self.poem]
        user_json = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'approbation': self.approbation,
            'rol': self.rol,
            'qualification': qualification,
            'poem': poem,
        }
        return user_json

    def to_json_short(self):
        user_json = {
            'id': self.id,
            'name': self.name,
        }
        return user_json

    @staticmethod

    def from_json(user_json):
        id = user_json.get('id')
        name = user_json.get('name')
        email = user_json.get('email')
        approbation = user_json.get('approbation')
        rol = user_json.get('rol')
        return User(id=id,
                    name=name,
                    email=email,
                    approbation=approbation,
                    rol=rol,
                    )