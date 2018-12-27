import os
import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext.dispatcher import run_async

from settings import Settings
from audio import audio2text
from dialog import get_answer

updater = Updater(Settings.TELEGRAM_BOT_TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def handle_start_command(bot, update):
    response = 'Start command'
    bot.send_message(chat_id=update.message.chat_id, text=response)


def handle_text_message(bot, update):
    message = update.message.text
    response = 'Received: {}'.format(message)
    bot.send_message(chat_id=update.message.chat_id, text=response)


@run_async
def handle_voice_message(bot, update):
    voice_file_id = update.message.voice.file_id
    voice_file = bot.get_file(voice_file_id)

    if not os.path.exists(Settings.VOICE_UPLOAD_DIR):
        os.makedirs(Settings.VOICE_UPLOAD_DIR)
    file_path = os.path.join(Settings.VOICE_UPLOAD_DIR, voice_file_id + '.ogg')

    voice_file.download(file_path)

    # text = audio2text(file_path)
    text = 'how are you?'

    answer = get_answer(text)
    bot.send_message(chat_id=update.message.chat_id, text=answer)


start_command_handler = CommandHandler('start', handle_start_command)
text_messages_handler = MessageHandler(Filters.text, handle_text_message)
voice_messages_handler = MessageHandler(Filters.voice, handle_voice_message)

dispatcher.add_handler(text_messages_handler)
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(voice_messages_handler)

updater.start_polling()
