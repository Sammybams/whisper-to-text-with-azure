from dotenv import load_dotenv
from datetime import datetime
from moviepy.editor import *
import os

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk

# Get Configuration Settings
load_dotenv()
cog_key = os.getenv('COG_SERVICE_KEY')
cog_region = os.getenv('COG_SERVICE_REGION')

# Configure speech service
speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)
print('Ready to use speech service in:', speech_config.region)


def main():
    try:

        # Get spoken input
        command = TranscribeCommand()
        if command.lower() == 'what time is it?':
            TellTime()

    except Exception as ex:
        print(ex)

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
    print('Unable to recognize speech.')
    
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    # print('Unable to recognize speech.')

    # Process speech input
    # Process speech input
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print(command)
    else:
        
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)

    # Return the command
    return command


def TellTime():
    now = datetime.now()
    response_text = 'The time is {}:{:02d}'.format(now.hour,now.minute)


    # Configure speech synthesis
    

    # Synthesize spoken output


    # Print the response
    print(response_text)


if __name__ == "__main__":
    main()