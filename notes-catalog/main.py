import os
import uuid

from flask import Flask, request, render_template
from flask_restful import Resource, Api
from requests import get, post
from google.cloud import firestore

from api.api import *

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/nello/Desktop/lab_sac/music-catalog/credentials.json'

db = firestore.Client()
app = Flask(__name__)
api = Api(app)

base_path = '/api/v1'
host_path = 'http://127.0.0.1:5000'

api.add_resource(Note, f'{base_path}/notes/<string:owner_id>/<string:note_id>')


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'GET':
        return render_template('insert.html')
    elif request.method == 'POST':
        return render_template('insert.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    elif request.method == 'POST':
        genre = request.form['genre']
        r = get(f'{host_path}{base_path}/genre/{genre}')
        if r.status_code != 200:
            return render_template('search.html', error="Error")
        return render_template('search.html', discs=r.json())


@app.route('/', methods=['GET'])
def index():
    owner_id = "bba78818-12a0-4b3e-98f3-f6c980e6ee90"
    # r = get(f"{host_path}{base_path}/notes/{owner_id}/note1")
    r = post(f"{host_path}{base_path}/notes/{owner_id}/note2", json={'note': 'la mia nota'})
    # print(r.json())
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
