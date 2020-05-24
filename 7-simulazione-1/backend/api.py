from uuid import UUID

from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import Schema, ValidationError, fields

from videogame import Videogame

app = Flask(__name__)
api = Api(app)

base_path = "/api/v1"

vg = Videogame()


def is_valid_uuid(uuid_to_test, version=4):
    uuid_to_test = uuid_to_test.replace('-', '')
    try:
        val = UUID(uuid_to_test, version=version)
    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        return False

    return val.hex == uuid_to_test


class ItemSchema(Schema):
    title = fields.Str(required=True, validate=lambda x: len(x) <= 100)
    year = fields.Int(required=True, validate=lambda x: 2010 <= x <= 2020)
    console = fields.Str(required=True, validate=lambda x: x in [
                         'ps4', 'xbox1', 'switch'])
    price = fields.Float(required=True, validate=lambda x: x >= 0.01)


def validate_body(json):
    try:
        body = ItemSchema().load(json)
    except ValidationError:
        return None

    return body


class Marketplace(Resource):
    def get(self, user_id, game_id):
        if not is_valid_uuid(user_id) or not is_valid_uuid(game_id):
            return None, 404

        game_info = vg.get_game_info(user_id, game_id)

        if game_info is None:
            return None, 404

        return game_info, 200

    def post(self, user_id, game_id):
        if not is_valid_uuid(user_id) or not is_valid_uuid(game_id):
            return None, 400

        if request.is_json:
            json = request.get_json()
        else:
            return None, 400

        body = validate_body(json)

        if body is None:
            return None, 400

        game_info = vg.get_game_info(user_id, game_id)
        if game_info is not None:
            return None, 409

        insertion = vg.insert_game(user_id, game_id, **body)
        if not insertion:
            return None, 400
        return None, 201


api.add_resource(
    Marketplace, f'{base_path}/game/<string:user_id>/<string:game_id>')


class Update(Resource):
    def post(self, user_id, game_id):
        if not is_valid_uuid(user_id) or not is_valid_uuid(game_id):
            return None, 404

        if request.is_json:
            json = request.get_json()
        else:
            return None, 404

        if 'price' not in json:
            return None, 404

        price = json['price']
        old_price = vg.get_game_info(user_id, game_id)['price']

        if old_price is None:
            return None, 404

        if old_price < price:
            return None, 409

        updated = vg.update_price(user_id, game_id, price)

        if not updated:
            return None, 404
        return None, 200


api.add_resource(
    Update, f'{base_path}/update/<string:user_id>/<string:game_id>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
