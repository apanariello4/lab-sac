import os

from google.cloud import firestore

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/nello/Desktop/credentials.json'

db = firestore.Client()


class Videogame(object):
    def __init__(self):
        self.title = 'Star Wars Jedi: Fallen Order'
        self.year = 2019
        self.console = 'ps4'
        self.price = 35.00

    def get_game_info(self, user_id, game_id):
        ref = db.document(f'users/{user_id}/games/{game_id}').get()
        if ref.exists:
            return ref.to_dict()
        return None

    def insert_game(self, user_id, game_id, **kwargs) -> bool:
        ref = db.document(f'users/{user_id}/games/{game_id}')
        ref.set({
            'title': kwargs.get('title', self.title),
            'year': kwargs.get('year', self.year),
            'console': kwargs.get('console', self.console),
            'price': kwargs.get('price', self.price)
        })

        return True

    def update_price(self, user_id, game_id, price):
        ref = db.document(f'users/{user_id}/games/{game_id}')
        ref.update({'price': price})
        return True
