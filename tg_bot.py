import telegram
from environs import Env

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from LogsHandler import TelegramLogsHandler
from dialogflow_api import detect_intent_texts


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")


def send_answer(update: Update, context: CallbackContext, project_id):
    text = update.message.text
    answer, fallback = detect_intent_texts(text, project_id)

    update.message.reply_text(answer)


def main():
    try:
        env = Env()
        env.read_env()
        tg_token = env('TG_TOKEN')
        admin_chat_id = env('ADMIN_CHAT_ID')
        project_id = env('PROJECT_ID')
        bot = telegram.Bot(token=tg_token)
        bot.logger.addHandler(TelegramLogsHandler(bot, admin_chat_id))
        bot.logger.warning('ТГ бот запущен')

        updater = Updater(token=tg_token)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,
                                              lambda update, context: send_answer(update, context, project_id)))

        updater.start_polling()
        updater.idle()
    except Exception as e:
        error_message = f"Бот упал с ошибкой: {str(e)}"
        bot.logger.warning(error_message)


if __name__ == '__main__':
    main()
