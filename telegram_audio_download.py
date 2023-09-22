from requests import get
from json import loads
import os
from pydub import AudioSegment
# import numpy as np
# from tqdm import tqdm

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
    mp3file = get(download_url)

    with open('audio.mp3', 'wb') as f:
        f.write(mp3file.content)
    
    src = "audio.mp3"  # Replace with the path to your audio file
    des = "output.wav"  # Replace with the desired output path and filename

    try:
        sound = AudioSegment.from_mp3(src)
        sound.set_channels(1)  # Convert to mono
        sound = sound.set_frame_rate(16000)  # Set the sampling rate to 16kHz
        sound = sound.set_channels(1)  # Ensure mono channel
        sound.export(des, format="wav")  # Export as WAV file
    except Exception as e:
        print(f"Error converting audio: {e}")


