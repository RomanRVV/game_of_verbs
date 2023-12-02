import random

import vk_api
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

import uuid
import telegram

from environs import Env
import logging

from tg_bot import MyLogsHandler


def detect_intent_texts(event, vk_api):

    from google.cloud import dialogflow

    project_id = "gameofverbs-406212"

    language_code = "ru"

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, str(uuid.uuid4()))

    text_input = dialogflow.TextInput(text=event.text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if not response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response.query_result.fulfillment_text,
            random_id=random.randint(1,1000)
        )


def main():
    try:
        env = Env()
        env.read_env()

        vk_token = env('vk_token')
        tg_token = env('tg_token')
        admin_chat_id = env("admin_chat_id")

        bot = telegram.Bot(token=tg_token)
        bot.logger.addHandler(MyLogsHandler(bot, admin_chat_id))
        bot.logger.warning('ВК бот запущен')

        vk_session = vk.VkApi(token=vk_token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                detect_intent_texts(event, vk_api)
    except Exception as e:
        error_message = f"Бот упал с ошибкой: {str(e)}"
        bot.logger.warning(error_message)


if __name__ == "__main__":
    main()
