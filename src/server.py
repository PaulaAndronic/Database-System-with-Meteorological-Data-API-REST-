from flask import Flask, request, flash, json, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy import func
from sqlalchemy.orm import column_property
import os
import sys

user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
database = os.environ["POSTGRES_DB"]
host = os.environ["POSTGRES_HOST"]
port =os.environ["POSTGRES_PORT"]
print(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')
sys.stdout.flush()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JSON_SORT_KEYS'] = False
app.secret_key = 'hi'

db = SQLAlchemy(app)

class Countries(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(100), unique=True, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    def __init__(self, nume, lat, lon):
        self.nume = nume
        self.lat = lat
        self.lon = lon

class Cities(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    idTara = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    numeOras = db.Column(db.String(100), unique=True, nullable=False)
    latOras = db.Column(db.Float, nullable=False)
    lonOras = db.Column(db.Float, nullable=False)

    def __init__(self, idTara, nume, lat, lon):
        self.numeOras = nume
        self.idTara = idTara
        self.latOras = lat
        self.lonOras = lon

class Temperatures(db.Model):
    __tablename__ = 'temperatures'
    id = db.Column(db.Integer, primary_key=True)
    idOras = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    valoare = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    datetime = column_property(func.to_char(timestamp, 'YYYY-MM-DD'))

    def __init__(self, idOras, valoare):
        self.idOras = idOras
        self.valoare = valoare
        self.timestamp = func.now()

@app.route('/api/countries', methods=['GET'])
def get_countries():
    countries = Countries.query.all()
    results = [
        {
            "id": country.id,
            "nume": country.nume,
            "lat": country.lat,
            "lon": country.lon
        } for country in countries]

    return jsonify(results), 200

@app.route("/api/countries", methods=['POST'])
def post_countries():
    global next_id

    params = request.json
    if not params:
        return Response(status=400)

    pnume = params.get('nume')
    if not pnume:
        return Response(status=400)

    plat = params.get('lat')
    if not plat:
        return Response(status=400)

    plon = params.get('lon')
    if not plon:
        return Response(status=400)

    entry = Countries(pnume, plat, plon)
    db.session.add(entry)
    try:
        db.session.commit()
        return jsonify({'id': entry.id}), 201
    except IntegrityError:
        db.session.rollback()
        return Response(status=409)
    


@app.route('/api/countries/<int:id>', methods=['DELETE'])
def delete_country(id):
   
    Countries.query.filter_by(id=id).delete()

    try: 
        db.session.commit()
        return Response(status=200)
    except IntegrityError:
        db.session.rollback()
        return Response(status=404)


@app.route('/api/countries/<int:id>', methods=['PUT'])
def put_countries(id):

    params = request.json
    if not params:
        return Response(status=400)

    pnume = params.get('nume')
    if not pnume:
        return Response(status=400)

    plat = params.get('lat')
    if not plat:
        return Response(status=400)

    plon = params.get('lon')
    if not plon:
        return Response(status=400)

    country = Countries.query.filter_by(id=id).first()

    country.nume = pnume
    country.lat = plat
    country.lon = plon

    db.session.add(country)

    try: 
        db.session.commit()
        return Response(status=200)
    except IntegrityError:
        db.session.rollback()
        return Response(status=409)


@app.route("/api/cities", methods=['POST'])
def post_cities():
    global next_id_city

    params = request.json
    if not params:
        return Response(status=400)

    idT = params.get('idTara')

    pnume = params.get('nume')

    plat = params.get('lat')

    plon = params.get('lon')
    
    entry = Cities(idT, pnume, plat, plon)

    db.session.add(entry)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return Response(status=409)
    
    return jsonify({'id': entry.id}), 201
    
@app.route('/api/cities', methods=['GET'])
def get_cities():
    cities = Cities.query.all()
    results = [
        {
            "id": city.id,
            "idTara": city.idTara,
            "nume": city.numeOras,
            "lat": city.latOras,
            "lon": city.lonOras
        } for city in cities]

    return jsonify(results), 200

@app.route('/api/cities/country/<int:idTara>', methods=['GET'])
def get_cities_by_country(idTara):
    cities = Cities.query.all()
    copy_cities = []
    for city in cities:
        if city.idTara == idTara:
            copy_cities.append(city)

    results = [
        {
            "id": city.id,
            "idTara": city.idTara,
            "nume": city.numeOras,
            "lat": city.latOras,
            "lon": city.lonOras
        } for city in copy_cities]
    
    return jsonify(results), 200

@app.route('/api/cities/<int:id>', methods=['DELETE'])
def delete_cities(id):
   
    Cities.query.filter_by(id=id).delete()

    try: 
        db.session.commit()
        return Response(status=200)
    except IntegrityError:
        db.session.rollback()
        return Response(status=404)


@app.route('/api/cities/<int:id>', methods=['PUT'])
def put_cities(id):

    params = request.json
    if not params:
        return Response(status=400)

    pId = params.get('idTara')
    if not pId:
        return Response(status=400)

    pnume = params.get('nume')
    if not pnume:
        return Response(status=400)

    plat = params.get('lat')
    if not plat:
        return Response(status=400)

    plon = params.get('lon')
    if not plon:
        return Response(status=400)

    city = Cities.query.filter_by(id=id).first()

    city.idTara = pId
    city.nume = pnume
    city.lat = plat
    city.lon = plon

    db.session.add(city)

    try: 
        db.session.commit()
        return Response(status=200)
    except IntegrityError:
        db.session.rollback()
        return Response(status=409)

@app.route('/api/temperatures', methods=['POST'])
def post_temperatures():

    params = request.json
    if not params:
        return Response(status=400)

    idOras = params.get('idOras')
    if not idOras:
        return Response(status=400)

    valoare = params.get('valoare')
    if not valoare:
        return Response(status=400)

    city = Cities.query.filter_by(id=idOras).first()
    
    entry = Temperatures(idOras, valoare)

    if not city:
        return Response(status=404)

    db.session.add(entry)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return Response(status=409)
    except DataError:
        db.session.rollback()
        return Response(status=409)
    return jsonify({'id': entry.id}), 201
    

@app.route('/api/temperatures', methods=['GET'])
def get_temperatures():
    cities = Cities.query.all()
    temperatures = Temperatures.query.all()
    copy_cities = []
    copy_temperatures = []
    lat_URL = request.args.get('lat')
    lon_URL = request.args.get('lon')
    until_URL = request.args.get('until')
    from_URL = request.args.get('from')
    
    for city in cities:
        if lat_URL and not lon_URL:
            if city.latOras == float(lat_URL):
                copy_cities.append(city)
        if lon_URL and not lat_URL:
            if city.lonOras == float(lon_URL):
                copy_cities.append(city)
        if lon_URL and lat_URL:
            if city.latOras == float(lat_URL) and city.lonOras == float(lon_URL):
                copy_cities.append(city)

    for temperature in temperatures:
        for copy_city in copy_cities:
            if temperature.idOras == copy_city.id:
                if not until_URL and not from_URL:
                    copy_temperatures.append(temperature)
                if until_URL and not from_URL:
                    if temperature.datetime <= float(until_URL):
                        copy_temperatures.append(temperature)
                if from_URL and not until_URL:
                    if temperature.datetime >= format(from_URL):
                        copy_temperatures.append(temperature)
                if until_URL and from_URL:
                    if temperature.datetime <= format(until_URL) and temperature.datetime >= format(from_URL):
                        copy_temperatures.append(temperature)

    if not copy_cities:
        for temperature in temperatures:
            if temperature.datetime <= format(until_URL) and not from_URL and until_URL:
                copy_temperatures.append(temperature)
            if temperature.datetime >= format(from_URL) and not until_URL and from_URL:
                copy_temperatures.append(temperature)
            if temperature.datetime <= format(until_URL) and temperature.datetime >= format(from_URL) and until_URL and from_URL:
                copy_temperatures.append(temperature)
            if not until_URL and not from_URL:
                copy_temperatures.append(temperature)    

    results = [
        {
            "id": temperature.id,
            "valoare": temperature.valoare,
            "timestamp": temperature.datetime
        } for temperature in copy_temperatures]

    return jsonify(results), 200


@app.route('/api/temperatures/cities/<int:id>', methods=['GET'])
def get_temperatures_by_city(id):
    cities = Cities.query.all()
    temperatures = Temperatures.query.all()
    copy_temperatures = []
    until_URL = request.args.get('until')
    from_URL = request.args.get('from')

    for temperature in temperatures:
        if temperature.idOras == id:
            if temperature.datetime <= format(until_URL) and not from_URL and until_URL:
                copy_temperatures.append(temperature)
            if temperature.datetime >= format(from_URL) and not until_URL and from_URL:
                copy_temperatures.append(temperature)
            if temperature.datetime <= format(until_URL) and temperature.datetime >= format(from_URL) and until_URL and from_URL:
                copy_temperatures.append(temperature)
            if not until_URL and not from_URL:
                copy_temperatures.append(temperature)

    results = [
        {
            "id": temperature.id,
            "valoare": temperature.valoare,
            "timestamp": temperature.datetime
        } for temperature in copy_temperatures]

    return jsonify(results), 200


@app.route('/api/temperatures/countries/<int:id>', methods=['GET'])
def get_temperatures_by_country(id):
    cities = Cities.query.all()
    temperatures = Temperatures.query.all()
    copy_temperatures = []
    copy_cities = []
    until_URL = request.args.get('until')
    from_URL = request.args.get('from')

    for city in cities:
        if city.idTara == id:
            copy_cities.append(city)

    for temperature in temperatures:
        for city in copy_cities:
            if temperature.idOras == city.id:
                if temperature.datetime <= format(until_URL) and not from_URL and until_URL:
                    copy_temperatures.append(temperature)
                if temperature.datetime >= format(from_URL) and not until_URL and from_URL:
                    copy_temperatures.append(temperature)
                if temperature.datetime <= format(until_URL) and temperature.datetime >= format(from_URL) and until_URL and from_URL:
                    copy_temperatures.append(temperature)
                if not until_URL and not from_URL:
                    copy_temperatures.append(temperature)

    results = [
        {
            "id": temperature.id,
            "valoare": temperature.valoare,
            "timestamp": temperature.datetime
        } for temperature in copy_temperatures]

    return jsonify(results), 200

@app.route('/api/temperatures/<int:id>', methods=['DELETE'])
def delete_temperatures(id):
   
    Temperatures.query.filter_by(id=id).delete()

    try: 
        db.session.commit()
        return Response(status=200)
    except IntegrityError:
        db.session.rollback()
        return Response(status=404)


@app.route('/api/temperatures/<int:id>', methods=['PUT'])
def put_temperatures(id):

    params = request.json
    if not params:
        return Response(status=400)

    pId = params.get('idOras')
    if not pId:
        return Response(status=400)

    pvaloare = params.get('valoare')
    if not pvaloare:
        return Response(status=400)

    temperature = Temperatures.query.filter_by(id=id).first()

    temperature.idOras = pId
    temperature.valoare = pvaloare

    db.session.add(temperature)

    try: 
        db.session.commit()
        return Response(status=200)
    except IntegrityError:
        db.session.rollback()
        return Response(status=409)



if __name__ == '__main__':
    db.create_all()
    app.run("0.0.0.0")
