import os
import telegram
from environs import Env

import logging
import uuid

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from google.cloud import dialogflow


class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = bot

    def emit(self, record):
        log_message = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_message)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")


def detect_intent_texts(update: Update, context: CallbackContext):

    project_id = os.environ.get('PROJECT_ID')

    language_code = "ru"

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, str(uuid.uuid4()))

    text_input = dialogflow.TextInput(text=update.message.text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    context.bot.send_message(chat_id=update.effective_chat.id, text=response.query_result.fulfillment_text)


def main():
    try:
        env = Env()
        env.read_env()
        tg_token = env('TG_TOKEN')
        admin_chat_id = env('ADMIN_CHAT_ID')
        bot = telegram.Bot(token=tg_token)
        bot.logger.addHandler(TelegramLogsHandler(bot, admin_chat_id))
        bot.logger.warning('ТГ бот запущен')

        updater = Updater(token=tg_token)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, detect_intent_texts))

        updater.start_polling()
        updater.idle()
    except Exception as e:
        error_message = f"Бот упал с ошибкой: {str(e)}"
        bot.logger.warning(error_message)


if __name__ == '__main__':
    main()
