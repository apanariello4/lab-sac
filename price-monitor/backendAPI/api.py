import urllib.parse
from uuid import UUID

from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from price import Monitoring

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'

# Initialize util
monitor_util = Monitoring()

# Utility functions


def is_valid_uuid(uuid_to_test, version=4):
    uuid_to_test = uuid_to_test.replace('-', '')
    try:
        val = UUID(uuid_to_test, version=version)
    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        return False

    return val.hex == uuid_to_test


def decode_url(coded_url):
    return urllib.parse.unquote(coded_url)


def encode_url(decoded_url):
    return urllib.parse.quote(decode_url)


def is_valid_number(string_number):
    try:
        number = int(string_number)
    except:
        return False
    if number < 1 or number > 100:
        return False

    return number
# Resources Classes


class Monitor(Resource):
    def get(self, user, object_uri):
        if not is_valid_uuid(user):
            return None, 400

        object_uri = decode_url(object_uri)

        percentage = monitor_util.get_monitor_percentage(user, object_uri)
        if not percentage:
            return None, 404

        return percentage, 200

    def post(self, user, object_uri):
        if not is_valid_uuid(user):
            return None, 400

        object_uri = decode_url(object_uri)

        if request.is_json:
            body = request.get_json()
        else:
            return None, 400

        if 'percentage' not in body:
            return None, 400

        percentage = body["percentage"]

        if not monitor_util.insert_monitor(user, object_uri, percentage):
            return None, 409

        return None, 201


api.add_resource(
    Monitor, f'{basePath}/monitor/<string:user>/<string:object_uri>')


class Objects(Resource):
    def get(self, object_uri):
        object_uri = decode_url(object_uri)

        if not object_uri:
            return None, 400

        objects = monitor_util.get_objects(object_uri)
        if not objects:
            return None, 404

        return objects, 200


api.add_resource(
    Objects, f'{basePath}/details/<string:object_uri>')


class ListObjects(Resource):
    def get(self, user):
        if not is_valid_uuid(user):
            return None, 400

        objects = monitor_util.get_monitored_objects(user)
        if not objects:
            return None, 400

        return objects, 200


api.add_resource(ListObjects, f'{basePath}/monitor/<string:user>')

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
