from google.cloud import firestore

db = firestore.Client()

class Cinema(object):
    def __init__(self):
        pass

    def post_book_cinema(self, date, time, seat):
        ref = db.collection(u'cinema').document(f'{date}T{time}')
        if ref.get().exists:
            ref.update({
                        "bookedSeats": firestore.ArrayUnion([seat])
            })
        else:
            ref.set({
                        "bookedSeats": firestore.ArrayUnion([seat])
            })

    def get_book_cinema(self, date, time):
        ref = db.collection(u'cinema').document(f'{date}T{time}').get()
        if ref.exists:
            r = ref.to_dict()
            return r['bookedSeats']
        return []
    
    def get_book_date(self, date):
        retVal = []
        for time in ["19:30", "21:00", "22:30"]:
            ref = db.collection(u'cinema').document(f'{date}T{time}').get()
            if ref.exists:
                r = ref.to_dict()
                r['time'] = time
                retVal.append(r)       
        return retVal

