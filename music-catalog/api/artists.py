class Artists(object):
    def __init__(self):
        pass

    def get_artist_name_by_id(self, artist_id, db):
        try:
            return db.collection(u'artists').document(artist_id).get().to_dict().get('name')
        except:
            return None

    def insert_artist(self, artist_id, artist_name, db):
        db.collection(u'artists').document(artist_id).set({u'name': artist_name})


class Discs(object):
    def __init__(self):
        pass

    def get_disc_info_by_id(self, artist_id, disc_id, db):
        try:
            artist_ref = db.collection(u'artists').document(artist_id)
        except:
            return None

        try:
            disc_ref = artist_ref.collection(u'discs').document(disc_id)
        except:
            return None

        info = disc_ref.get().to_dict()

        return info

    def insert_disc(self, artist_id, disc_id, disc_info, db):
        artist_ref = db.collection(u'artists').document(artist_id)

        try:
            discs_ref = artist_ref.collection(u'discs')
        except:
            return None

        discs_ref.document(disc_id).set(disc_info)

        return "Success"


class Genres(object):
    def __init__(self):
        pass

    def get_discs_by_genre(self, genre, db):
        artists_ref = db.collection(u'artists')
        discs_by_genre = []

        for artist in artists_ref.stream():
            genres = artists_ref.document(artist.id).collection(u'discs').where(u'genre', u'==', genre).stream()

            for disc in genres:

                disc = {
                    'name': disc.get('name'),
                    'genre': disc.get('genre'),
                    'year': disc.get('year')
                }

                discs_by_genre.append(disc)

        return discs_by_genre
