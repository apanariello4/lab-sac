from datetime import datetime
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from cinema import Cinema
from urllib.parse import quote

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'

cinema = Cinema()

def validDate(date):
    try:
        datetime.strptime(date, '%d%m%Y')
        return True
    except ValueError:
        return False

def validTime(time):
    if time in ["19:30", "21:00", "22:30"]:
        return True
    return False

def SeatToInt(seat):
    return (ord(str.upper(seat['row'])) - ord('A')) * 10 + seat['seat']

def IntToSeat(val):
    return {'row': chr(ord('A') + int(val)//10), 'seat': int(val) % 10}
        

class BookSeat(Resource):
    def get(self, date, time):

        if not validDate(date) or not validTime(time):
            return None, 404
        
        ret = cinema.get_book_cinema(date, time) 
        if not ret:
            return None, 404
        else:
            return {'items': [IntToSeat(x) for x in ret]}

    def post(self, date, time):
        if not validDate(date):
            return None, 400
        
        if not validTime(time):
            return None, 404
        
        if request.is_json:
            body = request.get_json()
        else:
            return None, 400

        if 'items' not in body:
            return None, 400

        for seat in body['items']:
            if not ('A' <= str.upper(seat['row']) <= 'L'):
                return None, 400
            if seat['seat'] < 1 or seat['seat'] > 11:
                return None, 400

        requested_seats = [SeatToInt(x) for x in body['items']]

        if not requested_seats:
            return None, 400

        booked_seats = cinema.get_book_cinema(date, time)
        
        if (set(requested_seats) & set(booked_seats)):
            return None, 409
        
        for rs in requested_seats:
            cinema.post_book_cinema(date, time, rs)

        return None, 201      
        
class BookDate(Resource):
    def get(self, date):
        if not validDate(date):
            return None, 400
        
        ref = cinema.get_book_date(date)
        ret = []
        for obj in ref:
            r = {}
            r['time'] = obj['time']
            r['booked_seats'] = {}
            r['booked_seats']['items'] = [IntToSeat(x) for x in obj['bookedSeats']]
            ret.append(r)
        return ret

class AutoBook(Resource):
    def post(self, date, time):
        if not validDate(date):
            return None, 404
        
        if not validTime(time):
            return None, 404
        
        if request.is_json:
            body = request.get_json()
        else:
            return None, 400

        if 'num' not in body:
            return None, 400
             
        occ = cinema.get_book_cinema(date, time)
        num = body['num']

        if len(occ) + num > 100:
            return None, 409
        
        mid = 5
        while mid < 100:
            ref = set(list(range(mid - num // 2, mid + num // 2)))
            if ref - set(occ) == ref:
                for x in ref:
                    cinema.post_book_cinema(date, time, x)
                return None, 201
            else:
                mid += 10
        return None, 403


api.add_resource(BookSeat, f'{basePath}/book/<string:date>/<string:time>')
api.add_resource(BookDate, f'{basePath}/book/<string:date>')
api.add_resource(AutoBook, f'{basePath}/auto/<string:date>/<string:time>')

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)