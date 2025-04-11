from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, send_file, jsonify, request

from . import agent
from util import mongodb_util

print("*** Init Flask App ***")
app = Flask(__name__, static_url_path='/', static_folder='static')

def helloworld():
    #for every chat agent.act
    chat_ids= mongodb_util.read_chatids()
    for chat_id in chat_ids:
        reactioN =agent.react(chat_id)
        print(reactioN)
        if reactioN:
            mongodb_util.insert_message(chat_id, datetime.now(), False, agents_response)

#scheduler = BackgroundScheduler()
#scheduler.add_job(helloworld, 'interval', minutes=1)
#scheduler.start()

@app.route("/")
def indexPage():
    return send_file("static/index.html")


@app.route('/chats')
def load_chats():
    return jsonify(mongodb_util.read_chatoverview())


@app.route('/chats/<chat_id>')
def get_chat(chat_id):
    return jsonify(mongodb_util.read_chathistory_json(chat_id))


@app.route('/send-msg', methods=['POST'])
def send_message():
    data = request.get_json()
    chat_id = data.get('chat_id')
    msg = data.get('msg')
    print(chat_id, msg)
    mongodb_util.insert_message(chat_id, datetime.now(), True, msg)
    agents_response = agent.react(chat_id)
    if agents_response:
        mongodb_util.insert_message(chat_id, datetime.now(), False, agents_response)
        return jsonify({'response': agents_response})
    return jsonify({'response': 'No Response needed...'})