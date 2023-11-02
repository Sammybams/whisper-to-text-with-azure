from dotenv import load_dotenv
from datetime import datetime
from moviepy.editor import *
import os
import time
# Import namespaces
import azure.cognitiveservices.speech as speech_sdk

# Get Configuration Settings
load_dotenv()
cog_key = os.getenv('COG_SERVICE_KEY')
cog_region = os.getenv('COG_SERVICE_REGION')

# Configure speech service
speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)
# print('Ready to use speech service in:', speech_config.region)

def TranscribeCommand():
    command = ''
    output_file = "audio.wav"
    audioclip = AudioFileClip("audio.ogg")
    audio_params = {
        "codec": "pcm_s16le",
        "fps": 16000,  # Set the desired sampling rate: 16000 Hz
        # "fps": 8000,  # Alternatively, set the sampling rate to 8000 Hz
        "nchannels": 1,  # Mono audio
        "bitrate": "16k"  # Set the desired bitrate
    }


    audioclip.write_audiofile(output_file, codec=audio_params["codec"],fps=audio_params["fps"],nbytes=2,bitrate=audio_params["bitrate"])
    
    # Configure speech recognition
    audio_config = speech_sdk.AudioConfig(filename="audio.wav")
    # audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    # print('Unable to recognize speech.')
    
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    # print('Unable to recognize speech.')

    # use Start Continuous Recognition to process long audio file
    # speech_recognizer.start_continuous_recognition()
    # print('Unable; to recognize speech.')
    # time.sleep(10)
    # speech_recognizer.stop_continuous_recognition()
    done = False
    def stop_cb(evt: speech_sdk.SpeechRecognitionEventArgs):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        nonlocal done
        done = True

    all_texts = []
    def handle_final_result(evt):
        all_texts.append(evt.result.text)

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognized.connect(handle_final_result)
    # speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    # speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    # speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    # speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    # speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()
    # print(speech_sdk.SessionEventArgs.result.text)
    # </SpeechContinuousRecognitionWithFile>
    
    # print("\n".join(all_texts))
    # Process speech input
    return "\n".join(all_texts)


if __name__ == "__main__":
    main()
