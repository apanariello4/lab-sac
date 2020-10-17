import os

from google.cloud import firestore

# try:
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/nello/Desktop/credentials.json'
# except:
#     pass


db = firestore.Client()


class Meme(object):
    def __init__(self):
        pass

    def insert_meme(self, meme_id, body):
        ref = db.document(f'memes/{meme_id}')
        ref.set(body)
        return True

    def get_meme(self, meme_id):
        ref = db.document(f'memes/{meme_id}').get()
        if ref.exists:
            return ref.to_dict()
        return None

    def get_meme_by_tag(self, tag):
        ref = db.collection(u'memes').stream()
        meme_by_tag = []
        for meme in ref:
            if tag in meme.to_dict().get("tags"):
                meme_by_tag.append(meme.to_dict())
        return meme_by_tag
