from .. import jwt
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        #Verificar que el JWT es correcto
        verify_jwt_in_request()
        #Obtener claims de adentro del JWT
        claims = get_jwt()
        #Verificar que el rol sea admin
        if claims['rol'] == "admin":
            #Ejecutar función
            return fn(*args, **kwargs)
        else:
            return 'Only admins can access', 403
    return wrapper


def admin_required_or_poeta_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Verificar que el JWT es correcto
        userId = verify_jwt_in_request()
        # Obtener claims de adentro del JWT
        claims = get_jwt()
        # Verificar que el rol sea admin o poeta
        if claims['rol'] == "admin" or userId == id:
            # Ejecutar función
            return fn(*args, **kwargs)
        else:
            return 'Only admins or poets can access', 403
    return wrapper


def poeta_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['rol'] == "poeta":
            return fn(*args, **kwargs)
        else:
            return 'Only admins can access', 403
    return wrapper


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.additional_claims_loader
def add_claims_to_access_token(user):
    claims = {
        'rol': user.rol,
        'id': user.id,
        'email': user.email
    }
    return claims