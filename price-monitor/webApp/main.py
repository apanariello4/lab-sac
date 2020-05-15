import os
from uuid import UUID

from flask import Flask, render_template, request
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client()

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/nello/Desktop/lab_sac/credentials.json'


def is_valid_uuid(uuid_to_test, version=4):
    uuid_to_test = uuid_to_test.replace('-', '')
    try:
        val = UUID(uuid_to_test, version=version)
    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        return False

    return val.hex == uuid_to_test


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        user_uuid = request.form['user_uuid']
        if not is_valid_uuid(user_uuid):
            return render_template('index.html')

        ref = db.collection(u'users').document(user_uuid).get()
        if ref.exists:
            objects = []
            for ob in ref.to_dict():
                objects.append({
                    "object_uri": ob,
                    "percentage": ref.get(ob)[0]
                })
            return render_template('index.html', objects=objects)
        return render_template('index.html')


# Numero di utenti   -  Numero medio di oggetti monitorati(per utente)  -  Scontistica media richiesta
@app.route('/stats', methods=['GET'])
def stats():
    ref = db.collection(u'users')
    users_number = 0
    objects = 0
    percentages = 0
    for user in ref.stream():
        users_number += 1
        for ob in user.to_dict():
            objects += 1
            percentages += user.get(ob)[0]

    mean_objects = objects / users_number
    mean_percentage = percentages / objects

    recipient = {
        'users_number': users_number,
        'mean_objects': mean_objects,
        'mean_percentage': mean_percentage
    }

    return render_template('stats.html', recipient=recipient)


if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)
