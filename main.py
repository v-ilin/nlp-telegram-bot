import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler

TOKEN = ''
BASE_URL = ''

updater = Updater(TOKEN, BASE_URL)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)

updater.start_polling()
