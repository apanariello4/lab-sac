import os

from google.cloud import firestore

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/nello/Desktop/lab_sac/credentials.json'

db = firestore.Client()


class Monitoring(object):
    def __init__(self):
        pass

    def get_monitor_percentage(self, user, object_uri):
        ref = db.collection(u'users').document(user).get()
        # ref = ref.collection(u'objects').document(object_uri).get()
        if ref.exists:
            objects = ref.to_dict()
            if object_uri in objects:
                return objects[object_uri][0]
        else:
            return False

    def insert_monitor(self, user, object_uri, percentage):
        ref = db.collection(u'users').document(user)

        if ref.get().exists:
            ref.update({object_uri: firestore.ArrayUnion([percentage])})
        else:
            ref.set({object_uri: firestore.ArrayUnion([percentage])})

        return True

    def get_objects(self, object_uri):
        # .where(u'object_uri',u'==',object_uri).stream()
        ref = db.collection(u'users').stream()
        objects = []
        for user in ref:
            if object_uri in user.to_dict():
                objects.append({
                    "user_uuid": user.id,
                    "percentage": user.get(object_uri)[0]
                })
        return(objects)

    def get_monitored_objects(self, user):
        ref = db.collection(u'users').document(user).get()
        if ref.exists:
            objects = []
            for ob in ref.to_dict():
                objects.append({
                    "object_uri": ob,
                    "percentage": ref.get(ob)[0]
                })
            return objects
        return False
