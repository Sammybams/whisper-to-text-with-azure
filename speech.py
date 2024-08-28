import os
import requests
from dotenv import load_dotenv
load_dotenv()

def TranscribeCommand():
    
    # Define the endpoint and subscription key
    url = f"https://eastus.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2024-05-15-preview"
    subscription_key = os.getenv('SUBSCRIPTION_KEY')
    
    # Set up headers with your subscription key
    # subscription_key = 'YourSubscriptionKey'
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Accept': 'application/json'
    }
    
    # Define the files and data for the request
    files = {
        'audio': open('audio.ogg', 'rb')  # Replace with your audio file path
    }
    data = {
        'definition': '''
        {
            "locales": ["en-US"],
            "profanityFilterMode": "Masked"
        }
        '''
    }
    # "channels": [0, 1]
    
    response = requests.post(url, headers=headers, files=files, data=data)

    # Check the response
    if response.status_code == 200:
        print('Success!')
        # print(response.json())
        # print(response.json()['combinedPhrases'][0]['text'])
        return response.json()['combinedPhrases'][0]['text']
        
    else:
        error_message = ""
        # print('Error:', response.status_code)
        # print(response.text)
        error_message += f'Error: {response.status_code}\n{response.text}'
        return error_message
