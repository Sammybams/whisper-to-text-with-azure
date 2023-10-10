import requests
import os 

BOT_TOKEN= os.getenv('BOT_TOKEN')

webhook_url = 'https://whisper-to-text.azurewebsites.net/'

response = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={webhook_url}')
print(response.json())

response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo')
print(response.json())
