from werkzeug.security import generate_password_hash, check_password_hash
from flask import session as cookies
from flask import request, jsonify
from functools import wraps
from jwt import ExpiredSignatureError, InvalidTokenError, decode, encode
from datetime import datetime, timedelta
from os import getenv
from dotenv import load_dotenv


load_dotenv()

def passwordHash(password:str):
    return generate_password_hash(password)

def passwordVerify(passHash:str, passUnHashed:str):
    return check_password_hash(passHash, passUnHashed)

def creatreJWT(email):
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(minutes=10)
    }

    return encode(payload, getenv('SECRET_KEY'), algorithm='HS256')

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization').split(" ")[1]

        if not token:
            return jsonify({'error': 'Falta el token'}), 401

        try:
            payload = decode(token, getenv('SECRET_KEY'), algorithms=['HS256'])
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

def requiredSession(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = cookies.get("token")

        if not token:
            return jsonify({'error': 'Falta el token'}), 401

        try:
            payload = decode(token, getenv('SECRET_KEY'), algorithms=['HS256'])
            cookies["token"] = creatreJWT(payload['email'])
            # Verifica si el usuario está activo (opcional)
        except ExpiredSignatureError:
            cookies.pop("token")
            return jsonify({'error': 'Token expirado'}), 401
        except InvalidTokenError as e:
            print(e)
            return jsonify({'error': 'Token invalido'}), 401

        
        

        # Si el token es valido, continúa con la función
        return f(*args, **kwargs)

    return decorated