import os

from flask import Flask, render_template_string
from google.cloud import pubsub_v1, firestore
import random
from requests import get, post

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/nello/Desktop/lab_sac/credentials.json'
PROJECT_ID = 'sac-pubsub1'

pub = pubsub_v1.PublisherClient()
topic = f'projects/{PROJECT_ID}/topics/visits'
api_visits_trigger = "https://us-central1-sac-pubsub1.cloudfunctions.net/api_visits"

base_template = '<html><body><h1>{{ page }} Page</h1></body></html>'
visits_template = '<html><body><h1>{% for visit, value in visits.items() %}{{ visit }} - {{ value["counter"] }} <br>{% endfor %}</h1></body></html>'
error_template = '<html><body>Error</body></html>'


app = Flask(__name__)
db = firestore.Client()


@app.errorhandler(404)
def page_not_found(e):
    pub.publish(topic, b'Visited page 404', page='404')
    return render_template_string(base_template, page='404'), 404


@app.route('/')
def index():
    # pub.publish(topic, b'Visited page index', page='index')
    r = post(api_visits_trigger, json={
        "page": "index",
        "visits": random.randint(1, 100)
    })

    return render_template_string(base_template, page='index')


@app.route('/login')
def login():
    pub.publish(topic, b'Visited page login', page='login')
    return render_template_string(base_template, page='login')


@app.route('/logout')
def logout():
    pub.publish(topic, b'Visited page logout', page='logout')
    return render_template_string(base_template, page='logout')


@app.route('/visits')
def visits():
    r = get(api_visits_trigger)
    visits = r.json()
    if not visits:
        return render_template_string(error_template)
    return render_template_string(visits_template, visits=visits)


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
