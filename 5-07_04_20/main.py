import os
from flask import Flask, request, render_template
from flask_restful import Resource, Api
from requests import get, post
from google.cloud import firestore
from airports import Airports

# Project ID is determined by the GCLOUD_PROJECT environment variable

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = """
            /home/nello/Desktop/lab_sac/4-23_03_20/exercise-2/credentials.json
            """

db = firestore.Client()
app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'

airport_util = Airports()

class AirportNames(Resource):
    def get(self, iataCode):
        if len(iataCode) != 3:
            return None, 400

        airport_ref = db.collection(u'airports').document(iataCode)
        return_val = airport_util.get_airport_by_iata(iataCode, airport_ref)
        print(return_val)

        if return_val is None:
            return None, 400
        else:
            return {'name' : return_val}, 200

    def post(self, iataCode):
        if len(iataCode) != 3:
            return None, 400

        airport_ref = db.collection(u'airports').document(iataCode)
        return_val = airport_util.get_airport_by_iata(iataCode, airport_ref)

        if return_val is not None:
            return None, 201

        airportName = request.get_json()['airportName']

        if len(airportName) > 250:
            return None, 400

        airport = {
            u'iataCode':iataCode,
            u'airportName':airportName
        }
        db.collection(u'airports').document(iataCode).set(airport)
        return None, 200

api.add_resource(AirportNames, f'{basePath}/airportName/<string:iataCode>')

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'GET':
        return render_template('insert.html')
    elif request.method == 'POST':
        iataCode = request.form['iataCode']
        airportName = request.form['airportName']

        r = post(f'http://127.0.0.1:5000{basePath}/airportName/{iataCode}',
                 json={'airportName':airportName})

        if r.status_code != 200:
            return render_template('insert.html', recipient='Invalid or already existing')

        return render_template('insert.html', recipient='Success')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')

    elif request.method == 'POST':

        iataCode = request.form['iataCode']
        r = get(f'http://127.0.0.1:5000{basePath}/airportName/{iataCode}')

        if r.status_code != 200:
            return render_template('search.html', airportName="Invalid or Missing IATA")

        airportName = r.json()['name']

        return render_template('search.html', airportName=airportName)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
