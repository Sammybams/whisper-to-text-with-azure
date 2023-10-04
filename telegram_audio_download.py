from requests import get
from json import loads
import os


def get_file_path(token, file_id):
    get_path = get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(token, file_id))
    json_doc = loads(get_path.text)
    try:
        file_path = json_doc['result']['file_path']
    except Exception as e:  # Happens when the file size is bigger than the API condition
        # print('Cannot download a file because the size is more than 20MB')
        return 'Cannot download a file because the size is more than 20MB'

    return 'https://api.telegram.org/file/bot{}/{}'.format(token, file_path)


def download_file(bot_token, audio_id):
    download_url = get_file_path(bot_token, audio_id)
    oggfile = get(download_url)

    with open('audio.ogg', 'wb') as f:
        f.write(oggfile.content)