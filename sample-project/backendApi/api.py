from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'

# Initialize util

# Utility functions

# Resources Classes


# api.add_resource("", f'{basePath}/')


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)