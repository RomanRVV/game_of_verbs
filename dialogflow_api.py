import os

import uuid
from google.cloud import dialogflow


def detect_intent_texts(text, project_id):

    language_code = "ru"

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, str(uuid.uuid4()))

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    answer = response.query_result.fulfillment_text
    fallback = response.query_result.intent.is_fallback

    return answer, fallback
