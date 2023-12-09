import random

import vk_api
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

import telegram

from environs import Env

from LogsHandler import TelegramLogsHandler
from dialogflow_api import detect_intent_texts


def main():
    try:
        env = Env()
        env.read_env()

        vk_token = env('VK_TOKEN')
        tg_token = env('TG_TOKEN')
        admin_chat_id = env('ADMIN_CHAT_ID')
        project_id = env('PROJECT_ID')

        bot = telegram.Bot(token=tg_token)
        bot.logger.addHandler(TelegramLogsHandler(bot, admin_chat_id))
        bot.logger.warning('ВК бот запущен')

        vk_session = vk.VkApi(token=vk_token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                answer, fallback = detect_intent_texts(event.text, project_id)
                if not fallback:
                    vk_api.messages.send(user_id=event.user_id, message=answer, random_id=random.randint(1,1000))
    except Exception as e:
        error_message = f"Бот упал с ошибкой: {str(e)}"
        bot.logger.warning(error_message)


if __name__ == "__main__":
    main()
