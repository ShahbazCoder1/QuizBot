import google.generativeai as genai
from tqdm import tqdm
import time
from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

SUBJECT = None
TOPIC = None 
LEVEL = None
STATE = None


TOKEN: Final = '7068344943:AAEIFEtmH0N64n7ombEPfDcMpPCOYwN3WFU'
BOT_USERNAME: Final = '@Quisly_Bot'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'''
      ____          _ 
     / __ \        (_) 
    | |  | | _   _  _  ____ 
    | |  | || | | || ||_  / 
    | |__| || |_| || | / /_ 
     \___\_\ \__,_||_|/____|
     ____          _   
    |  _ \        | |  
    | |_) |  ___  | |_ 
    |  _ <  / _ \ | __|
    | |_) || (_) || |_ 
    |____/  \___/  \__|
    ''' )

    await update.message.reply_text("Enter the subject you wish to take the quiz on: ")
    global STATE
    STATE = "subject"



async def subj(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global SUBJECT
    global STATE
    SUBJECT = update.message.text
    await update.message.reply_text("Enter the topic you wish to take a quiz on: ")
    STATE = "topic"


async def topi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global TOPIC
    global STATE
    TOPIC = update.message.text
    await update.message.reply_text("Enter the level of the quiz [beginner/intermediate/advanced]: ")
    STATE = "level"

async def leve(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global LEVEL
    LEVEL = update.message.text
    await update.message.reply_text("\nGenerating quiz questions, please wait...")

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global STATE
    if STATE == "subject":
        await subj(update, context)
        #STATE = TOPIC
    elif STATE == "topic":
        await topi(update, context)
        #STATE = LEVEL
    elif STATE == "level":
        await leve(update, context)
        STATE = None
    else:
        await update.message.reply_text("Invalid input. Please try again.")



def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))
 
    application.run_polling()

if __name__ == '__main__':
    main()