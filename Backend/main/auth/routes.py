from flask import request, jsonify, Blueprint
from .. import db
from main.models import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

#Blueprint para acceder a los métodos de autenticación
auth = Blueprint('auth', __name__, url_prefix='/auth')

#Método de logueo
@auth.route('/login', methods=['POST'])
def login():
    #Busca al profesor en la db por mail
    professor = db.session.query(UserModel).filter(UserModel.email == request.get_json().get("email")).first_or_404()
    #Valida la contraseña
    if user.validate_pass(request.get_json().get("password")):
        #Genera un nuevo token
        #Pasa el objeto professor como identidad
        access_token = create_access_token(identity=user)
        #Devolver valores y token
        data = {
            'id': str(professor.id),
            'email': professor.email,
            'access_token': access_token
        }

        return data, 200
    else:
        return 'Incorrect password', 401
"""
#Método de registro
@auth.route('/register', methods=['POST'])
def register():
    #Obtener professor
    professor = ProfessorModel.from_json(request.get_json())
    #Verificar si el mail ya existe en la db
    exists = db.session.query(ProfessorModel).filter(ProfessorModel.email == professor.email).scalar() is not None
    if exists:
        return 'Duplicated mail', 409
    else:
        try:
            #Agregar professor a DB
            db.session.add(professor)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return str(error), 409
        return professor.to_json() , 201
"""