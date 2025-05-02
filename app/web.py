from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Blueprint, send_file, jsonify, request

from app import agent
from app.util import mongodb_util

web_blueprint = Blueprint('web_blueprint', __name__, )


@web_blueprint.route("/")
def indexPage():
    return send_file("static/index.html")


@web_blueprint.route('/chats')
def load_chats():
    return jsonify(mongodb_util.read_chatoverview())


@web_blueprint.route('/chats/<chat_id>')
def get_chat(chat_id):
    return jsonify(mongodb_util.read_chathistory_json(chat_id))


@web_blueprint.route('/send-msg', methods=['POST'])
def send_message():
    data = request.get_json()
    chat_id = data.get('chat_id')
    msg = data.get('msg')
    mongodb_util.insert_message(chat_id, datetime.now(ZoneInfo("Europe/Zurich")), True, msg)
    agents_response = agent.act(chat_id)
    if agents_response:
        mongodb_util.insert_message(chat_id, datetime.now(ZoneInfo("Europe/Zurich")), False, agents_response)
        return jsonify({'response': agents_response})
    return jsonify({'response': 'no response reload to delete me'})
