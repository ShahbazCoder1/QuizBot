import google.generativeai as genai
from tqdm import tqdm
import time
from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN: Final = '7068344943:AAEIFEtmH0N64n7ombEPfDcMpPCOYwN3WFU'
BOT_USERNAME: Final = '@Quisly_Bot'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #await update.message.reply_text('Hello! Use /poll to create a poll.')


    await update.message.reply_text( '''
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

    #intructions here:
    await update.message.reply_text("Welcome to Quiz Bot. Get ready to challenge your knowledge with our exciting quiz. Choose the subject, topic and difficulty level according to your convenience and answer the questions that follows.\n")


    # Program Start here:
    GOOGLE_API_KEY='API_KEY'

    genai.configure(api_key=GOOGLE_API_KEY) #apikey configuration

    model = genai.GenerativeModel('gemini-1.5-flash') #model setup
    # User input
    sub=input("Enter the subject you wish to take the quiz on: ").upper()
    topic = input("Enter the topic you wish to take a quiz on: ").upper()
    level= input("Enter the level of the quiz [beginner/intermediate/advanced]: ").upper()
    # Start the progress bar
    await update.message.reply_text("\nGenerating quiz questions, please wait...")
    with tqdm(total=100, desc="Generating", ncols=100) as pbar:
        response = None
        while response is None:
            pbar.update(20) #progress bar update by 20/100
            try:
             # Response here
                response = model.generate_content(f"Generate a python dictionary which contains 10 {level} level questions on {topic} from {sub} along with four options as possible answers for each question. Show the four options along with alphabets assigned to them serially. Return only the dictonary code part.")
                pbar.update(50) #progress bar update by 50/100
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                pbar.update(100)
                time.sleep(0.5) 

    incor = 0
    cor = 0

    quiz = eval(response.text.replace("```","").replace("python",""))

    await update.message.reply_text(quiz)


    for key, value in quiz.items():
        await update.message.reply_text(f"\nQ: {value['question']}")
        options = value['options']
        for opt_key, opt_value in options.items():
            await update.message.reply_text(f"{opt_key}: {opt_value}")

        x = input("Enter your answer (a-d): ").strip().lower()

        if x == value['answer']:
            cor += 1
            await update.message.reply_text("Correct")
        else:
            incor += 1
            await update.message.reply_text("Incorrect")


    await update.message.reply_text(f"\nNumber of correct answers: {cor}")
    await update.message.reply_text(f"Number of incorrect answers: {incor} \n")  
    if cor==10:
        await update.message.reply_text("Excellent performance🥳!")
    elif cor>7:
        await update.message.reply_text("Great performance😃!")
    elif cor>5:
        await update.message.reply_text("Good job! Just a little more push🥰")
    else:
        await update.message.reply_text("Keep working. Better luck next time :)")

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    application.run_polling()

if __name__ == '__main__':
    main()
'''

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello')


app = ApplicationBuilder().token("7068344943:AAEIFEtmH0N64n7ombEPfDcMpPCOYwN3WFU").build()

app.add_handler(CommandHandler("hello", hello))

app.run_polling() '''