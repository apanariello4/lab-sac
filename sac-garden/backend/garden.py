import os

from google.cloud import firestore

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/nello/Desktop/credentials.json'

db = firestore.Client()


class Garden(object):
    def __init__(self):
        pass

    def insert_plant(self, date, plant, body):
        ref = db.document(f'dates/{date}/plants/{plant}')
        ref.set({
            "plant": {
                "name": body["plant"]["name"],
                "sprout-time": body["plant"]["sprout-time"],
                "full-growth": body["plant"]["full-growth"],
                "edible": body["plant"]["edible"]
            },
            "num": body["num"]
        })

        return True

    def get_plant(self, date, plant):
        ref = db.document(f'dates/{date}/plants/{plant}').get()
        if ref.exists:
            return ref.to_dict()
        return None
