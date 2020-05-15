from flask import Flask, render_template, request
from google.cloud import firestore
import time

# Project ID is determined by the GCLOUD_PROJECT environment variable
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="4-23_03_20/exercise-2/credentials.json"

db = firestore.Client()
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

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        users_ref = db.collection(u'users')
        users = users_ref.stream()

        username = request.form['username']
        password = request.form['password']

        for doc in users:
            if doc.get("username") == username and doc.get("password") == password:
                last_access = doc.get("last_access")
                
                users_ref.document(doc.id).update({u'last_access':firestore.SERVER_TIMESTAMP})

                return render_template('greeting_link.html', recipient=username, last_access=last_access)
        
        return render_template('login.html', recipient='Invalid username or password')

@app.route('/chat/<room>', methods=['GET','POST'])
def chat(room):
    
    room_ref = db.collection(u'rooms').document(room)
    msgs_ref = room_ref.collection(u'messages')
    
    if request.method == 'GET':
        
        msg_query = msgs_ref.order_by(u'timestamp',direction=firestore.Query.DESCENDING).limit(30).stream()
        
        msgs = ''
        for msg in msg_query:
            msgs += (f'{msg.id}: \n from: {msg.get("from")} \n {msg.get("msg")}\n\n')
        
        chat_name = room_ref.get().to_dict().get('name')
        if chat_name is None:
            chat_name = 'Anonymous Chat'

        return render_template('chat.html', msgs=msgs.replace("\n", "<br />"), chat_name=chat_name)
    elif request.method == 'POST':

        username = request.form['username']
        if username == '':
            username = "Anonymous"
        message = request.form['msg']

        msg_db = {
            u'from':username,
            u'msg':message,
            u'timestamp':firestore.SERVER_TIMESTAMP
        }
        n_messages = room_ref.get().to_dict().get('n_messages') #number of messages in db
        messageN = "message" + str(n_messages+1) #compute the name of the next message
        msgs_ref.document(messageN).set(msg_db) #add the item in the db
        room_ref.update({u'n_messages':int(n_messages)+1}) #update the counter

        msg_query = msgs_ref.order_by(u'timestamp',direction=firestore.Query.DESCENDING).limit(30).stream()
        #get the last 30 messages sent
        msgs = ''
        for msg in msg_query:
            msgs += (f'{msg.id}: \n from: {msg.get("from")} \n {msg.get("msg")}\n\n')
        
        chat_name = room_ref.get().to_dict().get('name')
        if chat_name == '':
            chat_name = 'Anonymous'

        return render_template('chat.html', msgs=msgs.replace("\n", "<br />"), chat_name=chat_name)

@app.route('/', methods=['GET'])
def helloworld():
    return render_template('index.html')
    #return current_app.send_static_file('index.html) #for static html in static folder

@app.route('/chat_list', methods=['GET'])
def chat_list():
    return render_template('chat_list.html')

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html") 

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)