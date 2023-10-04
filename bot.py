#import the necessary packages
from telegram import Update, File
from telegram.ext import  filters, CommandHandler, MessageHandler, ContextTypes, Application, CallbackContext
import os
from dotenv import load_dotenv
import telegram
import requests


# import script to download audio file
from telegram_audio_download import download_file
from speech import TranscribeCommand

#logging
import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

load_dotenv()

BOT_TOKEN= os.getenv('BOT_TOKEN')

# bot = telegram.Bot(BOT_TOKEN)

# def download_file(URL):
# 	response = requests.get(URL)
# 	with open('voice.ogx', 'wb') as f:
# 		f.write(response.content)

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
        await context.bot.send_message(chat_id=update.effective_chat.id,
            text=f"Please reply to an audio or voice note to transcribe")
        return
    
    # Get audio file id
    if update.message.reply_to_message.voice:
        # Get voice note file id
        audio_id = update.message.reply_to_message.voice.file_id
        # print(audio_id)
        # audio_file = CallbackContext.bot.get_file(audio_id)
        # audio_file.download(f"{audio_id}.ogg")

        # file = await bot.get_file(audio_id)
        # # file.download_to_memory()
        # download_file('https://api.telegram.org/file/bot{0}/{1}'.format(BOT_TOKEN, file.file_path))
        try:
            download_file(BOT_TOKEN, audio_id)
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                text=TranscribeCommand())
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                text=f"Cannot transcribe file because the size is more than 20MB")
        # downloaded_file = bot.download_file(file.file_path)
        # with open('new_file.ogg', 'wb') as new_file:
        #     new_file.write(downloaded_file)

    elif update.message.reply_to_message.audio:
        # Get audio file id
        audio_id = update.message.reply_to_message.audio.file_id
        # print(audio_id)
        # audio_file = CallbackContext.bot.get_file(audio_id)
        # audio_file.download(f"{audio_id}.ogg")

        # file = await bot.get_file(audio_id)
        # file.download_to_memory()
        try:
            download_file(BOT_TOKEN, audio_id)
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                text=TranscribeCommand())
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                text=f"Cannot transcribe file because the size is more than 20MB")
        # downloaded_file = bot.download_file(file.file_path)
        # with open('new_file.ogg', 'wb') as new_file:
        #     new_file.write(downloaded_file)

    else:
        # No audio or voice note found
        await context.bot.send_message(chat_id=update.effective_chat.id,
            text=f"Please reply to an audio or voice note to transcribe")
        return
    
    # Get audio file object
    # File(audio_id, audio_unique_id).download()
    # audio_file = await context.bot.get_file(audio_id)
    # Download audio file
    # audio_file.download('audio.ogg')

    # audio = update.message.reply_to_message.voice.file_id
    print("Hello")
    
        
if __name__ == "__main__":
    application = Application.builder().token(BOT_TOKEN).build()
    # start_handler = CommandHandler("start", start, filters.ChatType.GROUPS)
    start_handler = CommandHandler("start", start)
    # transcribe_handler = CommandHandler("transcribe", transcribe, filters.ChatType.GROUPS)
    transcribe_handler = CommandHandler("transcribe", transcribe)
    application.add_handler(start_handler)
    application.add_handler(transcribe_handler)
    application.run_polling()

