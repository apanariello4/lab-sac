import os
from uuid import UUID

from flask import request
from flask_restful import Resource
from google.cloud import firestore


from api.artists import Artists, Discs, Genres

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/nello/Desktop/lab_sac/music-catalog/credentials.json'

db = firestore.Client()

artist_util = Artists()
disc_util = Discs()
genre_util = Genres()
genres = ["rock", "pop", "electronic", "dance"]


def is_valid_uuid(uuid_to_test, version=4):
    uuid_to_test = uuid_to_test.replace('-', '')
    try:
        val = UUID(uuid_to_test, version=version)
    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        return False

    return val.hex == uuid_to_test


class Artist(Resource):
    def get(self, artist_id):
        if is_valid_uuid(artist_id) is False:
            return None, 404

        artist_name = artist_util.get_artist_name_by_id(artist_id, db)

        if artist_name is None:
            return None, 404

        artist_info = {
            'id': artist_id,
            'name': artist_name
        }
        return artist_info, 200

    def post(self, artist_id):
        if is_valid_uuid(artist_id) is False:
            return None, 409

        if artist_util.get_artist_name_by_id(artist_id, db) is not None:
            return None, 409

        artist_name = request.get_json()['artist_name']

        if artist_name is None:
            return None, 409

        artist_util.insert_artist(artist_id, artist_name, db)
        return None, 201


class Disc(Resource):
    def get(self, artist_id, disc_id):
        if is_valid_uuid(artist_id) is False or is_valid_uuid(disc_id) is False:
            return None, 400

        disc_info = disc_util.get_disc_info_by_id(artist_id, disc_id, db)

        if disc_info is None:
            return None, 409

        return disc_info, 200

    def post(self, artist_id, disc_id):
        if is_valid_uuid(artist_id) is False or is_valid_uuid(disc_id) is False:
            return None, 400

        if artist_util.get_artist_name_by_id(artist_id, db) is None:
            return "Artist does not exists", 409

        name = request.get_json()['name']
        year = request.get_json()['year']
        genre = request.get_json()['genre']

        if name is None:
            return None, 400

        if year < 1990 or year > 2020:
            return None, 400

        if genre not in genres:
            return None, 400

        disc_info = {
            "name": name,
            "year": year,
            "genre": genre
        }
        if disc_util.insert_disc(artist_id, disc_id, disc_info, db) is None:
            return "Invalid", 409

        return None, 201


class Genre(Resource):
    def get(self, genre):
        if genre not in genres:
            return "Invalid input.", 400

        return genre_util.get_discs_by_genre(genre, db), 200
