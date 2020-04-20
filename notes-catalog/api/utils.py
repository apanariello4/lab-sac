class Notes(object):
    def __init__(self):
        pass

    def get_note_by_id(self, owner_id, note_id, db):
        try:
            owner_ref = db.collection(u'owners').document(owner_id)
            note_ref = owner_ref.collection(u'notes').document(note_id)
            note = note_ref.get().to_dict().get('note')
        except:
            return False

        return note

    def insert_note(self, owner_id, note_id, note, db):
        try:
            owner_ref = db.collection(u'owners').document(owner_id)
            notes_ref = owner_ref.collection(u'notes')
        except:
            return False

        notes_ref.document(note_id).set({u'note': note})
        return True


class NoteShare(object):
    def __init__(self):
        pass

    def check_first_note(owner_id, db):
        try:
            owner_ref = db.collection(u'owners').document(owner_id)
        except:
            return False

        return True

    def share_note(recipient_id, shared_note_id, note, db):
        owner_ref = db.collection(u'owners').document(recipient_id)
        owner_ref.collection(u'notes').document(shared_note_id).set({u'note': note})
