import telegram
from environs import Env

import logging
import uuid

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")


def detect_intent_texts(update: Update, context: CallbackContext):

    from google.cloud import dialogflow

    project_id = "gameofverbs-406212"

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
    env = Env()
    env.read_env()

    tg_token = env('tg_bot_key')

    updater = Updater(token=tg_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, detect_intent_texts))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
