import requests
import os 

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN= os.getenv('BOT_TOKEN')

webhook_url = 'https://whisper-to-text.azurewebsites.net/' + BOT_TOKEN

response = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={webhook_url}')

if response.status_code == 200:
    print('Webhook URL successfully set.')
else:
    print(f'Failed to set the webhook URL. Status code: {response.status_code}')
