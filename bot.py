#import the necessary packages
from telegram import Update
from telegram.ext import  filters, CommandHandler, MessageHandler, ContextTypes, Application
import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN= os.getenv('BOT_TOKEN')
print(BOT_TOKEN)