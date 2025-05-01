import os
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
import telegram
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from flask import Flask, send_file, jsonify, request

from app import agent
from app.util import mongodb_util

print("*** Init Flask App ***")
app = Flask(__name__, static_url_path='/', static_folder='static')
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
HEROKU_URL = os.getenv('HEROKU_URL')
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)


def acting():
    chat_ids = mongodb_util.read_chatids()
    for chat_id in chat_ids:
        action = agent.react(chat_id)
        if action:
            mongodb_util.insert_message(chat_id, datetime.now(ZoneInfo("Europe/Zurich")), False, action)


# First Start the scheduler so no multithreading happends then add the job
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(acting, 'interval', minutes=5)


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


@app.route('/bot/{}'.format(TELEGRAM_BOT_TOKEN), methods=['POST'])
async def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    # get the chat_id to be able to respond to the same user
    original_chat_id = update.message.chat.id
    chat_id = 'tg-' + str(update.message.chat.id)
    msg = update.message.text.encode('utf-8').decode()

    mongodb_util.insert_message(chat_id, datetime.now(ZoneInfo("Europe/Zurich")), True, msg)
    agents_response = agent.react(chat_id)
    if agents_response:
        mongodb_util.insert_message(chat_id, datetime.now(ZoneInfo("Europe/Zurich")), False, agents_response)
        await bot.sendMessage(chat_id=original_chat_id, text=agents_response)

    return 'ok'


# Only for setup purposes
@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    response = requests.post(
        f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook',
        data={'url': HEROKU_URL}
    )
    if response.status_code == 200:
        print('Webhook has been set successfully!')
    else:
        print('Failed to set webhook. Please check your API token and URL.')
    return 'ok'
