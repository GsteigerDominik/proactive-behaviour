import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

from src.prototyp7.decision_engine import should_answer
from src.prototyp7.mongodb_adapter import insert_message, read_chathistory
from src.prototyp7.text_engine import generate_response

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.ERROR)
logging.basicConfig(format='%(asctime)s %(message)s')
logging.getLogger(__name__).setLevel(logging.INFO)

load_dotenv()
TELEGRAMM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


async def react(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    logger.info('Contacted by User with Msg '+user_message)
    insert_message(TELEGRAM_CHAT_ID, datetime.now(), True, user_message)

    chat_hist = read_chathistory(TELEGRAM_CHAT_ID)
    should= should_answer(chat_hist)
    logger.info('Decision: '+str(should))
    if should.contact_user:
        response = generate_response(chat_hist)
        insert_message(TELEGRAM_CHAT_ID, datetime.now(), False, response)
        await update.message.reply_text(response)


# save msg
# act accordingly

async def act(application):
    while True:
        await asyncio.sleep(30)
        chat_hist = read_chathistory(TELEGRAM_CHAT_ID)
        should= should_answer(chat_hist)
        logger.info('Should Contact Proactive: '+str(should))
        if should.contact_user:
            response = generate_response(chat_hist)
            insert_message(TELEGRAM_CHAT_ID, datetime.now(), False, response)
            await application.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=response)

    # act accordingly


application = Application.builder().token(TELEGRAMM_TOKEN).build()
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, react))
application.job_queue.run_repeating(lambda ctx: asyncio.create_task(act(application)), interval=30, first=0)

application.run_polling()
