from flask import Flask, request, jsonify
from flask import session as cookies
from dotenv import load_dotenv
from os import getenv, mkdir, path, makedirs
from flask_cors import CORS
from datetime import datetime, timedelta
from jwt import encode
import re
from decimal import Decimal

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
            return jsonify({'error': 'Incorrect credentials'}), 401
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

@app.route('/getProducts')
def obtenerCatalogo():
    products = session.query(Products).filter(Products.Available == True, Products.Display == True).all()

    listProducts = []

    for product in products:
        sources = [source.Url for source in product.Sources]
        measures = []

        for measure in product.Measures:
            measures.append({
                'name' : measure.Name,
                'price' : measure.Price
            })

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
                'measures' : measures,
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
        name = data['name']
        size = data['size']
        weight = data['weight']
        description = data['description']
        stock = data['stock']
        quantity = data['quantity']
        color = data['color']
        measures = data['measures']

        newProduct = Products(name, description, stock, quantity, size, weight, color)
        session.add(newProduct)
        session.commit()

        measuresList = measures.split(", ")
        print(measuresList)

        for measure in measuresList:
            params = measure.split(":")
            try:
                price = params[1]
                price = Decimal(price)
                name = params[0]

                newMeasure = Measure(newProduct.Id, name, price)
                session.add(newMeasure)
            except Exception as e:
                return jsonify(error = f'{e}', register = 'failed')

        
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