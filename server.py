from flask import Flask, request, jsonify
from flask import session as cookies
from flask_mail import Message, Mail
from dotenv import load_dotenv
from os import getenv
from flask_cors import CORS
from datetime import datetime, timedelta
from jwt import encode

from database import *
from functions import *

app = Flask(__name__)
app.secret_key = getenv('secret_key')

mail = Mail()
CORS(app, origins=['*'], supports_credentials=True)



@app.route('/login', methods = ['POST'])
def login():
    print(request.method)
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
        return 'Joaaa'
    
@app.route('/')
def init():
    user1 = Users(
        FullName = 'Jesús Calderón Vargas',
        Direction = 'Calle 9 Carrera 35 #95',
        Email = 'jesusmcalderonv2002@gmail.com',
        Password = passwordHash('hola'),
        Birthdate = datetime.utcnow(),
        Active = True
    )

    session.add(user1)
    session.commit()

    return jsonify(response = 'Usuario cerado de manera exitosa')


@app.route('/verify')
@jwt_required
def verify():
    return 'Hola'

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    mail.init_app(app)
    app.run(debug=True)