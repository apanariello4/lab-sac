from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/', methods=['GET'])
def helloworld():
    d = {}
    for i in range(random.randint(5,10)):
        d[f'key {i}'] = random.randrange(9)
    return render_template('list.html', recipient=d)

@app.errorhandler(404)
def not_found(e): 
    return render_template("404.html") 

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)