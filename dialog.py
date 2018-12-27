import uuid
import requests
import logging

from settings import Settings


def get_answer(text):
    url = 'https://api.recast.ai/build/v1/dialog'

    data = {
        "message":
            {
                "type": "text",
                "content": text
            },
        "conversation_id": uuid.uuid4().hex,
        "language": "en"
    }

    headers = {
        'Authorization': 'Token ' + Settings.RECAST_AI_TOKEN,
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=data, headers=headers)

    if not response.ok:
        logging.error('Request to RECAST.AU failed with status code: {}. Content: {}'
                      .format(response.status_code, response))
        return None

    response_data = response.json()
    answer = response_data['results']['messages'][0]['content']

    return answer
