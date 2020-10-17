import os
import json
import base64
from datetime import datetime, timedelta

from flask import Flask, render_template, render_template_string, request
from google.cloud import firestore

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/nello/Desktop/credentials.json'

app = Flask(__name__)
db = firestore.Client(project="sac-esame15")


@app.route('/info/<string:meme_id>', methods=["GET"])
def info():
    # GET info from db
    return render_template()



@app.route('/', methods=["GET"])
def index():
    ref = db.collection(u'memes').stream()
    memes_by_tag = []
    for meme in ref:
        for tag in meme.to_dict().get("tags"):
            memes_by_tag.append([tag, meme.to_dict(), meme.id])

    print(memes_by_tag)
    unique_tags = []
    for meme in memes_by_tag:
        if meme[0] not in unique_tags:
            unique_tags.append(meme[0])

    for tag in unique_tags:
        for meme in memes_by_tag:
            if tag == memes_by_tag[0]:
                print(meme)


    return render_template('index.html', unique_tags=unique_tags, memes=memes_by_tag)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
