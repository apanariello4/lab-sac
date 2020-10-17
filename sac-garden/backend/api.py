from datetime import datetime
from uuid import UUID

from flask import Flask, request
from flask_restful import Api, Resource
from garden import Garden
from marshmallow import Schema, ValidationError, fields

app = Flask(__name__)
api = Api(app)

base_path = "/api/v1"

garden = Garden()


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


def valid_plant(plant):
    if 3 <= len(plant) <= 20:
        return True
    return False


class PlantDetailsSchema(Schema):
    name = fields.Str(required=True, validate=lambda x: len(x) >= 3)
    # sprout - time = fields.Str(required=True, validate=lambda x: len(x) >= 5)
    # full - growth = fields.Str(required=True, validate=lambda x: len(x) >= 5)
    edible = fields.Boolean()


class PlantInfoSchema(Schema):
    plant = fields.Nested(Schema.from_dict({
        "name": fields.Str(required=True, validate=lambda x: len(x) >= 3),
        "sprout-time": fields.Str(required=True, validate=lambda x: len(x) >= 5),
        "full-growth": fields.Str(required=True, validate=lambda x: len(x) >= 5),
        "edible": fields.Boolean()
    }))
    num = fields.Int(required=True, validate=lambda x: x >= 1)


def validate_body(json):
    try:
        body = PlantInfoSchema().load(json)
    except ValidationError as e:
        print(e)
        return None

    return body


class SmartGarden(Resource):
    def get(self, date, plant):
        if not validDate(date) or not valid_plant(plant):
            return None, 404

        info = garden.get_plant(date, plant)

        if info is None:
            return None, 404

        return info, 200

    def post(self, date, plant):
        if not validDate(date) or not valid_plant(plant):
            return None, 400

        if request.is_json:
            json = request.get_json()
        else:
            return None, 400

        body = validate_body(json)

        if garden.get_plant(date, plant) is not None:
            return None, 409

        r = garden.insert_plant(date, plant, body)

        if not r:
            return None, 400

        return None, 201


api.add_resource(
    SmartGarden, f'{base_path}/garden/plant/<string:date>/<string:plant>')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
