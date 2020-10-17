import os
from datetime import datetime
from uuid import UUID

from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import Schema, ValidationError, fields
import validators
from Levenshtein import distance

from module import Meme

app = Flask(__name__)
api = Api(app)

base_path = "/api/v1"

meme_util = Meme()


def is_valid_uuid(uuid_to_test, version=4):
    uuid_to_test = uuid_to_test.replace('-', '')
    try:
        val = UUID(uuid_to_test, version=version)
    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        return False

    return val.hex == uuid_to_test


def validDate(date):
    try:
        datetime.strptime(date, '%d%m%Y')
        return True
    except ValueError:
        return False


def validate_tags(tags):
    for tag in tags:
        if len(tag) < 3 or len(tag) > 30:
            return False
    return True

def validate_url(url):
        val = validators.url(url)
        if val is not True:
            return False
        return True


class MemeSchema(Schema):
    title = fields.Str(required=True, validate=lambda x: len(x) <= 100)
    link = fields.Str(required=True, validate=lambda x: validate_url(x))
    media = fields.Str(required=True, validate=lambda x: x in [
                       "image", "video"])
    tags = fields.List(fields.Str, required=True, validate=lambda x: len(
        x) >= 2 and validate_tags(x))
    # field = fields.Boolean()


def validate_body(json):
    try:
        body = MemeSchema().load(json)
    except ValidationError as e:
        print(e)
        return None
    return body


class MemeClass(Resource):
    def get(self, meme_id):
        if not is_valid_uuid(meme_id):
            return None, 404

        r = meme_util.get_meme(meme_id)

        if not r:
            return None, 404

        return r, 200

    def post(self, meme_id):
        if not is_valid_uuid(meme_id):
            return None, 400

        if request.is_json:
            json = request.get_json()
        else:
            return None, 400

        body = validate_body(json)

        if body is None:
            return None, 400

        r = meme_util.get_meme(meme_id)

        if r is not None:
            return None, 409

        p = meme_util.insert_meme(meme_id, body)

        if not p:
            return None, 400

        return None, 201


api.add_resource(
    MemeClass, f'{base_path}/meme/<string:meme_id>')


class MemeByTagResource(Resource):
    def get(self, tag):
        if len(tag) < 3 or len(tag) > 30:
            return None, 404

        tag = tag.replace("%20"," ")

        memes_by_tag = meme_util.get_meme_by_tag(tag)

        if not memes_by_tag:
            return None, 404

        memes_and_distance = []

        for meme in memes_by_tag:
            min_distance = 100
            for meme_tag in meme["tags"]:
                leven = distance(tag, meme_tag)
                if leven < min_distance:
                    min_distance = leven

            memes_and_distance.append([meme, min_distance])

        sorted_memes = sorted(memes_and_distance, key=lambda x: x[1])

        return sorted_memes[:5]


api.add_resource(MemeByTagResource, f'{base_path}/list/<string:tag>')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
