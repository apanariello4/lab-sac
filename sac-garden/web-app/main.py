import os
import json
import base64
from datetime import datetime, timedelta

from flask import Flask, render_template, render_template_string, request
from google.cloud import firestore

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/nello/Desktop/credentials.json'

app = Flask(__name__)
db = firestore.Client(project="sac-garden1")


def string_to_timedelta(date):
    if "years" in date or "year" in date:
        years = float(date.split(' ')[0])
        days = years * 365
        delta = timedelta(days=days)
    elif "months" in date or "month" in date:
        months = float(date.split(' ')[0])
        days = months * 30
        delta = timedelta(days=float(days))
    elif "days" in date or "day" in date:
        days = float(date.split(' ')[0])
        delta = timedelta(days=days)
    return delta


def compute_color(date):
    today = datetime.today().date()
    if date < today:
        return "gray"
    elif date - today <= timedelta(days=10):
        return "cyan"
    elif date - today > timedelta(days=10):
        return "blue"


@app.route('/', methods=["GET"])
def index():

    plants_list = []
    growth_list = []
    sprout_list = []
    dates_ref = db.collection('dates').list_documents()
    for date in dates_ref:
        plants_ref = db.collection(f'dates/{date.id}/plants').stream()
        for plant in plants_ref:
            plant_dict = plant.to_dict()

            growth_time = string_to_timedelta(
                plant_dict['plant']['full-growth'])
            sprout_time = string_to_timedelta(
                plant_dict['plant']['sprout-time'])

            plant_date = datetime.strptime(date.id, '%d%m%Y')

            plants_list.append({
                "name": plant_dict['plant']['name'],
                "growth_time": growth_time,
                "sprout_time": sprout_time,
                "plant_date":  plant_date,
                "grow_date": (plant_date + growth_time).date(),
                "sprout_date": (plant_date + sprout_time).date()
            })

    event_list = []
    for plant in plants_list:
        event_list.append({
            "name": plant['name'],
            "event": "growth",
            "date": plant['grow_date'],
            "color": compute_color(plant['grow_date'])
        })
        event_list.append({
            "name": plant['name'],
            "event": "sprout",
            "date": plant['sprout_date'],
            "color": compute_color(plant['sprout_date'])
        })

    event_list = sorted(event_list, key=lambda x: x['date'])
    print(event_list)
    return render_template('index.html', events_list=event_list)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
