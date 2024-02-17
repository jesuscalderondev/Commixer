from flask import Flask, request, jsonify
from flask import session as cookies
from dotenv import load_dotenv
from os import getenv
from flask_cors import CORS
from datetime import datetime, timedelta
from jwt import encode

from database import *
from functions import *

load_dotenv()

app = Flask(__name__)
app.secret_key = getenv('secret_key')

CORS(app, origins=['*'], supports_credentials=True)


@app.route('/login', methods = ['POST'])
def login():
    try:
        try:
            data = request.get_json()
        except:
            data = request.form

        email = data['email']
        password = data['password']

        user = session.query(Users).filter(Users.Email == email).first()
        if passwordVerify(user.Password, password):
            payload = {
                'username': user.Email,
                'exp': datetime.utcnow() + timedelta(minutes=60)
            }
            token = encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'token': token})
        else:
            return jsonify({'error': 'Credenciales incorrectas'}), 401
    except Exception as e:
        print(e)
        return jsonify({'error': f'{e}', 'data' : data})
    
@app.route('/')
def init():
    print(getenv('FULLNAME_TEST'), getenv('DIRECTION_TEST'), getenv('EMAIL_TEST'))
    try:
        user1 = Users(
            FullName = getenv('FULLNAME_TEST'),
            Direction = getenv('DIRECTION_TEST'),
            Email = getenv('EMAIL_TEST'),
            Password = passwordHash(getenv('PASS_TEST')),
            Birthdate = datetime.utcnow(),
            Active = True
        )

        session.add(user1)
        session.commit()

        return jsonify(response = 'Usuario cerado de manera exitosa')
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify(response = 'El usuario ya está disponible', error = f'{e}')


@app.route('/verify')
@jwt_required
def verify():
    return jsonify({
        'reponse' : 'Acceso concedido'
    })

Base.metadata.create_all(engine)


if __name__ == '__main__':
    app.run(debug=True)