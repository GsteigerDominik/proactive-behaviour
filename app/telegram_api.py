from datetime import datetime
from zoneinfo import ZoneInfo

import flask
import requests
import telegram
from flask import request, Blueprint
from telegram.request import HTTPXRequest

from app import env, agent
from app.util import mongodb_util

telegram_blueprint = Blueprint('telegram_blueprint', __name__, )


# Just set a longer timeout (no pool config possible in older versions)
request = HTTPXRequest(read_timeout=10.0, connect_timeout=10.0)
bot = telegram.Bot(token=env.TELEGRAM_BOT_TOKEN, request=request)


@telegram_blueprint.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    response = requests.post(
        f'https://api.telegram.org/bot{env.TELEGRAM_BOT_TOKEN}/setWebhook',
        data={'url': env.HEROKU_URL}
    )
    if response.status_code == 200:
        print('Webhook has been set successfully!')
    else:
        print('Failed to set webhook. Please check your API token and URL.')
    return 'ok'


@telegram_blueprint.route('/bot/{}'.format(env.TELEGRAM_BOT_TOKEN), methods=['POST'])
async def respond():
    update = telegram.Update.de_json(flask.request.get_json(force=True), bot)
    original_chat_id = update.message.chat.id
    chat_id = 'tg-' + str(update.message.chat.id)
    msg = update.message.text.encode('utf-8').decode()

    mongodb_util.insert_message(chat_id, datetime.now(ZoneInfo("Europe/Zurich")), True, msg)
    agents_response = agent.act(chat_id)
    if agents_response:
        await send_telegram_msg(original_chat_id, agents_response)
        mongodb_util.insert_message(chat_id, datetime.now(ZoneInfo("Europe/Zurich")), False, agents_response)
    return 'ok'


async def send_telegram_msg(chat_id, text):
    await bot.sendMessage(chat_id=chat_id, text=text)
