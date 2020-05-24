import os
import json
import base64

from flask import Flask, render_template, render_template_string, request
from google.cloud import firestore

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/nello/Desktop/credentials.json'

app = Flask(__name__)
db = firestore.Client(project="sac-vg-market3")

# os.environ["PUBSUB_VERIFICATION_TOKEN"]
app.config["PUBSUB_VERIFICATION_TOKEN"] = os.environ["PUBSUB_VERIFICATION_TOKEN"]

MESSAGES = []


@app.route('/pubsub/push', methods=['POST'])
def pubsub():
    print("Received pubsub push")
    if request.args.get('token', '') != app.config["PUBSUB_VERIFICATION_TOKEN"]:
        return 'invalid request', 404

    envelope = json.loads(request.data.decode('utf-8'))
    payload = base64.b64decode(envelope['message']['data'])
    attributes = envelope['message']['attributes']
    game_info = {
        'title': attributes['title'],
        'console': attributes['console'],
        'user_id': attributes['user_id'],
        'game_id': attributes['game_id']
    }
    if game_info not in MESSAGES:
        MESSAGES.append(game_info)

    return 'ok', 200


@app.route('/topics', methods=['GET'])
def topics():
    return render_template('index.html', games_list=MESSAGES)


@app.route('/<string:user_id>/<string:game_id>', methods=["GET"])
def details(user_id, game_id):
    game_info = db.document(f'users/{user_id}/games/{game_id}').get().to_dict()
    return render_template_string("<html><body>{%for k, v in game_info.items()%} {{k}} : {{v}} </br>{% endfor %}</body></html>", game_info=game_info)


@app.route('/', methods=["GET"])
def index():
    games_list = []
    users_ref = db.collection('users').list_documents()
    for user in users_ref:
        games_ref = db.collection(f'users/{user.id}/games').stream()
        for game in games_ref:
            game_info = game.to_dict()
            games_list.append({
                'title': game_info['title'],
                'console': game_info['console'],
                'game_id': game.id,
                'user_id': user.id
            })

    return render_template('index.html', games_list=games_list)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
