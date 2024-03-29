from flask import Flask, request, jsonify
from flask import session as cookies
from dotenv import load_dotenv
from os import mkdir, path, makedirs
from flask_cors import CORS
from datetime import datetime, timedelta
from jwt import encode
import re
import os

from database import *
from functions import *

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

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
            return jsonify({'error': 'Incorrect credentials'}), 401
    except Exception as e:
        print(e)
        return jsonify({'error': f'{e}', 'data' : data})
    
@app.route('/')
def init():
    print(os.environ['FULLNAME_TEST'], os.environ['DIRECTION_TEST'], os.environ['EMAIL_TEST'])
    try:
        user1 = Users(
            FullName = os.environ['FULLNAME_TEST'],
            Direction = os.environ['DIRECTION_TEST'],
            Email = os.environ['EMAIL_TEST'],
            Password = passwordHash(os.environ['PASS_TEST']),
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

@app.route('/getProducts')
def obtenerCatalogo():
    products = session.query(Products).filter(Products.Available == True, Products.Display == True).all()

    listProducts = []

    for product in products:
        sources = [source.Url for source in product.Sources]


        listProducts.append(
            {
                'name' : product.Name,
                'id' : product.Description,
                'stock' : product.Stock,
                'quantity' : product.Quantity,
                'size' : product.Size,
                'weight' : product.Weight,
                'color' : product.Color,
                'cover' : product.Cover,
                'price' : product.Price,
                'id' : product.Id,
                'source' : sources
            }
        )

    if len(products) > 0:
        response = jsonify(products = listProducts, productsReturn = 'ready')
    else:
        response = jsonify(productsReturn = 'empty')

    return response, 200

@app.route('/createProduct', methods = ['POST'])
def createProduct():
    if request.method != 'POST':
        return jsonify(access = 'denied')
    try:
        data = request.json()
    except:
        try:
            data = request.form
        except:
            return jsonify(process = 'Error: no se han enviado datos en el formulario')
        
    
    try:
        price = data['price']
        name = data['name']
        size = data['size']
        weight = data['weight']
        description = data['description']
        stock = data['stock']
        quantity = data['quantity']
        color = data['color']
        cover = data['cover']

        newProduct = Products(name, description, stock, quantity, size, weight, color, cover, price)

        session.add(newProduct)
        session.commit()

        nameFolder = name.replace(' ', '')

        nameFolder = re.sub(r'[^\w\s]','', name).lower()

        folder = f'media/products/{nameFolder}'

        if path.exists('/media/products'):
            makedirs(folder)
        else:
            makedirs('media')
            makedirs('media/products')
            makedirs(folder)
        
        
        details = []

        if 'profile' in request.files:

            files = request.files
            keys = files.keys()

            for key in keys:
                archive = files[key]
                if archive.content_type in ['image/png', 'image/jpg', 'image/jpeg', 'image/webp']:
                    archiveName = archive.filename.lower().replace(' ', '')
                    url = f'{folder}/{archiveName}'
                    archive.save(url)
                    newSource = ProductMedia(newProduct.Id, url, archive.content_type)
                    
                    try:
                        session.add(newSource)
                        session.commit()
                    except Exception as e:
                        session.rollback()
                        details.append(f'{e}')
                
        return jsonify(register = 'success', details = details), 200
    except Exception as e:
        session.rollback()
        return jsonify(error = f'{e}', register = 'failed')


Base.metadata.create_all(engine)


if __name__ == '__main__':
    app.run(debug=True)