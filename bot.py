#import the necessary packages
from telegram import Update, Bot
from telegram.ext import  filters, CommandHandler, MessageHandler, ContextTypes, Application
import os
from dotenv import load_dotenv

# import script to download audio file
from telegram_audio_download import download_file

# import Transcription command from speech script
from speech import TranscribeCommand

BOT_TOKEN= os.getenv('BOT_TOKEN')
WEB_SERVER = os.getenv('WEB_SERVER')

PORT = int(os.environ.get('PORT', '8080'))
print(f"PORT {PORT}")
bot = Bot(token=BOT_TOKEN)
# bot.setWebhook(f'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEB_SERVER}')


#logging
import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

load_dotenv()



#start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Give a simple explanation of what the bot does"""
    text = "Whisper to Text bot helps you transcribe voice notes and audio within your chats to text. "
    text += "I can also help with transalation and summarization.\n\n"
    text += "To use me, simply reply to an audio or voice note with the following commands:\n"
    text += "- /transcribe - Transcribe audio or voice note to text\n"
    text += "- /translate - Translate text from audio or voice note to another language\n"
    text += "- /summarize - Summarize text from audio or voice note\n"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    

async def transcribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Transcribe voice note or audio to text"""
    # Get audio file to which transcribe command is replied to
    if update.message.reply_to_message is None:
        # No audio or voice note found
        await update.message.reply_text("Please reply to an audio or voice note to transcribe")
        return
    
    # Get audio file id
    if update.message.reply_to_message.voice:
        # Get voice note file id
        audio_id = update.message.reply_to_message.voice.file_id

        try:
            download_file(BOT_TOKEN, audio_id)
            await update.message.reply_text(TranscribeCommand())

        except:
            await update.message.reply_text("Cannot transcribe file because the size is more than 20MB")

    elif update.message.reply_to_message.audio:
        # Get audio file id
        audio_id = update.message.reply_to_message.audio.file_id

        try:
            download_file(BOT_TOKEN, audio_id)
            await update.message.reply_text(TranscribeCommand())

        except:
            await update.message.reply_text("Cannot transcribe file because the size is more than 20MB")

    else:
        # No audio or voice note found
        await update.message.reply_text("Please reply to an audio or voice note to transcribe")
        return
    
        
if __name__ == "__main__":
    application = Application.builder().token(BOT_TOKEN).build()
    start_handler = CommandHandler("start", start)
    transcribe_handler = CommandHandler("transcribe", transcribe)
    application.add_handler(start_handler)
    application.add_handler(transcribe_handler)
    # application.run_polling()
    application.run_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=BOT_TOKEN,webhook_url=WEB_SERVER+BOT_TOKEN)