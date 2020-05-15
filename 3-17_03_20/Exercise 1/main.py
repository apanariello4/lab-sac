from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def helloworld():
    return render_template('greeting.html', recipient='index page')

@app.route('/test/', methods=['GET'])
def helloworld2():
    return render_template('greeting.html', recipient='test page')

@app.errorhandler(404)
def not_found(e): 
    return render_template("404.html") 

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)