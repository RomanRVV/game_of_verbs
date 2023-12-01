import vk_api
import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
import uuid


def echo(event, vk_api):

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

    vk_api.messages.send(
        user_id=event.user_id,
        message=response.query_result.fulfillment_text,
        random_id=random.randint(1,1000)
    )


def main():
    env = Env()
    env.read_env()

    vk_token = env('vk_token')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)


if __name__ == "__main__":
    main()
    