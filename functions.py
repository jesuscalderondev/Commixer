from werkzeug.security import generate_password_hash, check_password_hash
from flask import session as cookies
from flask import request, jsonify
from functools import wraps
from jwt import ExpiredSignatureError, InvalidTokenError, decode
from os import getenv
from dotenv import load_dotenv


load_dotenv()

def passwordHash(password:str):
    return generate_password_hash(password)

def passwordVerify(passHash:str, passUnHashed):
    return check_password_hash(passHash, passUnHashed)


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization').split(" ")[1]

        if not token:
            return jsonify({'error': 'Falta el token'}), 401

        try:
            payload = decode(token, getenv('secret_key'), algorithms=['HS256'])
        except ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except InvalidTokenError as e:
            print(e)
            return jsonify({'error': 'Token invalido'}), 401

        # Verifica si el usuario está activo (opcional)
        # if payload['active'] is not True:
        #    return jsonify({'error': 'Usuario inactivo'}), 401

        # Si el token es valido, continúa con la función
        return f(*args, **kwargs)

    return decorated