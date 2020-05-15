from flask import Flask, render_template
from google.cloud import firestore
from datetime import datetime

app = Flask(__name__)
db = firestore.Client()

@app.route('/', methods=['GET'])
def index():
    ref = db.collection(u'cinema').get()
    bookings = {}
    for r in ref:
        date, time = r.id.split('T')
        if date not in bookings:
            bookings[date] = {}

        bookings[date][time] = len(r.to_dict()['bookedSeats'])
    return render_template('booking_list.html', bookings = bookings)

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    return datetime.strptime(date, '%d%m%Y').strftime("%Y/%m/%d")

if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)
