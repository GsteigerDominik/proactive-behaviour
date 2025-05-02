import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, send_file, jsonify, request

from app import agent
from app.telegram_api import send_telegram_msg, telegram_blueprint
from app.util import mongodb_util
from app.web import web_blueprint

print("*** Init Flask App ***")
app = Flask(__name__, static_url_path='/', static_folder='static')
app.register_blueprint(web_blueprint)
app.register_blueprint(telegram_blueprint)


async def primitive_tact():
    print('Takt gestartet')
    chat_ids = mongodb_util.read_chatids()
    for chat_id in chat_ids:
        action = agent.act(chat_id)
        if action:
            if chat_id.startswith('tg-'):
                await send_telegram_msg(chat_id.removeprefix('tg-'), text=action)
            mongodb_util.insert_message(chat_id, datetime.now(ZoneInfo("Europe/Zurich")), False, action)

# First Start the scheduler so no multithreading happends then add the job
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(lambda: asyncio.run(primitive_tact()), 'interval', minutes=5,max_instances=1)
