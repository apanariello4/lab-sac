import os
import uuid

from flask import Flask, request, render_template
from flask_restful import Resource, Api
from requests import get, post
from google.cloud import firestore

from api.api import Artist, Disc, Genre

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/nello/Desktop/lab_sac/music-catalog/credentials.json'

db = firestore.Client()
app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'
host_path = 'http://127.0.0.1:5000'

api.add_resource(Artist, f'{basePath}/artist/<string:artist_id>')
api.add_resource(Disc, f'{basePath}/disc/<string:artist_id>/<string:disc_id>')
api.add_resource(Genre, f'{basePath}/genre/<string:genre>')


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'GET':
        return render_template('insert.html')
    elif request.method == 'POST':
        artist_id = request.form['artist_id']
        artist_name = request.form['artist_name']
        r = post(f'{host_path}{basePath}/artist/{artist_id}', json={'artist_name': artist_name})

        if r.status_code != 200:
            return render_template('insert.html', recipient='Invalid id')
        
        return render_template('insert.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    elif request.method == 'POST':
        genre = request.form['genre']
        r = get(f'{host_path}{basePath}/genre/{genre}')
        if r.status_code != 200:
            return render_template('search.html', error="Error")
        return render_template('search.html', discs=r.json())


@app.route('/', methods=['GET'])
def index():
    artist_uuid = "b735b474-be1c-4a3c-9316-c39a45192998"
    disc_uuid = uuid.uuid4()
    disc_info = {
        'name': 'Album Name',
        'genre': 'rock',
        'year': 2000
    }
    # r = post(f'http://127.0.0.1:5000{basePath}/disc/{artist_uuid}/{disc_uuid}', json=disc_info)

    artists_ref = db.collection(u'artists').stream()
    artists_id = {}
    for artist in artists_ref:
        discs_ref = db.collection(u'artists').document(artist.id).collection(u'discs').stream()
        discs = {}
        for disc in discs_ref:
            discs[disc.id] = disc.to_dict()
        artist_and_discs = {
            'name': artist.to_dict().get('name'),
            'discs': discs
        }
        artists_id[artist.id] = artist_and_discs

    return render_template('index.html', artists=artists_id)


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
