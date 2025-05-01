import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, send_file, jsonify, request

from app import agent
from app.telegram_api import send_telegram_msg, telegram_blueprint
from app.util import mongodb_util

print("*** Init Flask App ***")
app = Flask(__name__, static_url_path='/', static_folder='static')
app.register_blueprint(telegram_blueprint)


async def acting():
    chat_ids = mongodb_util.read_chatids()
    for chat_id in chat_ids:
        action = agent.react(chat_id)
        if action:
            mongodb_util.insert_message(chat_id, datetime.now(ZoneInfo("Europe/Zurich")), False, action)
            if chat_id.startswith('tg-'):
                await send_telegram_msg(chat_id.removeprefix('tg-'), text=action)


# First Start the scheduler so no multithreading happends then add the job
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(lambda: asyncio.run(acting()), 'interval', minutes=5)


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
    mongodb_util.insert_message(chat_id, datetime.now(ZoneInfo("Europe/Zurich")), True, msg)
    agents_response = agent.react(chat_id)
    if agents_response:
        mongodb_util.insert_message(chat_id, datetime.now(ZoneInfo("Europe/Zurich")), False, agents_response)
        return jsonify({'response': agents_response})
    return jsonify({'response': 'no response reload to delete me'})
