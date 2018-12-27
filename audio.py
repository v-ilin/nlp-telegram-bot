import uuid
import requests
import logging

from settings import Settings

CHUNK_SIZE = 64 * 1024


def read_file_by_chunks(file_path):
    with open(file_path, 'rb') as f:
        chunk = f.read(CHUNK_SIZE)
        while chunk:
            yield chunk
            chunk = f.read(CHUNK_SIZE)


def audio2text(file_path):
    url = 'http://asr.yandex.net/asr_xml?uuid={}&key={}&topic={}&lang={}' \
        .format(uuid.uuid4().hex, Settings.YANDEX_SPEECHKIT_KEY, 'notes', 'ru-RU')
    response = requests.post(url, data=read_file_by_chunks(file_path),
                             headers={'Content-Type': 'audio/ogg;codecs=opus'})

    if not response.ok:
        logging.error('Request to Yandex Speech Kit failed with status code: {}'
                      .format(response.status_code))
        return 'Error! Failed to recognize speech!'

    # response = response.json()
    return response.text
