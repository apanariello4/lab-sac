from flask import Flask, render_template, request

app = Flask(__name__)

ERROR = "String too short or too long"

@app.route('/greeting', methods=['GET','POST'])
def greeting():
    if request.method == 'GET':
        return render_template('greeting_form.html', recipient='')
    elif request.method == 'POST':
        recipient = request.form['greeting_name']
        if len(recipient)>3 and len(recipient)<20:
            return render_template('greeting_link.html', recipient=recipient)
        else:
            return render_template('greeting_form.html', recipient=ERROR)

@app.route('/', methods=['GET'])
def helloworld():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html") 

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)