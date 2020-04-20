import os
from uuid import UUID

from flask import request
from flask_restful import Resource
from google.cloud import firestore


from api.utils import *

credential_path = '/home/nello/Desktop/lab_sac/music-catalog/credentials.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

db = firestore.Client()

note_util = Notes()
share_note_util = NoteShare()


def is_valid_uuid(uuid_to_test, version=4):
    uuid_to_test = uuid_to_test.replace('-', '')
    try:
        val = UUID(uuid_to_test, version=version)
    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        return False

    return val.hex == uuid_to_test


def checkLength(id):
    if len(id) > 16 or len(id) < 5:
        return False
    return True


class Note(Resource):
    def get(self, owner_id, note_id):
        if is_valid_uuid(owner_id) is False or checkLength(note_id) is False:
            return "Invalid input data", 409

        note = note_util.get_note_by_id(owner_id, note_id, db)
        if note is False:
            return "Invalid or missing NoteID", 400

        return_note = {
            'id': note_id,
            'note': note
        }

        return return_note, 200

    def post(self, owner_id, note_id):
        if is_valid_uuid(owner_id) is False or checkLength(note_id) is False:
            return "Invalid input data", 409

        note = note_util.get_note_by_id(owner_id, note_id, db)
        if note is not False:
            return "NoteID already present", 400

        note = request.get_json()['note']
        if len(note) > 250:
            return "Invalind input data", 409

        r = note_util.insert_note(owner_id, note_id, note, db)
        if r is False:
            return "Error", 409

        return "Succes", 200


class Share(Resource):
    def post(self, owner_id, recipient_id):
        if is_valid_uuid(owner_id) is False or is_valid_uuid(recipient_id) is False:
            return "Invalid input data", 400
        
        if owner_id == recipient_id:
            return "Invalid path", 404

        shared_note_id = request.get_json()['id']
        if checkLength(shared_note_id) is False:
            return "Invalid input data", 400
        
        note = note_util.get_note_by_id(owner_id, shared_note_id, db)
        if note is False:
            return "Invalid path", 404
        
        if share_note_util.check_first_note(recipient_id, db) is False:
            return "Invalid path", 404
        
        share_note_util.share_note(recipient_id, shared_note_id, note, db)
        return "Succes", 200

