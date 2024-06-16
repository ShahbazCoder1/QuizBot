import google.generativeai as genai
from tqdm import tqdm
import time
from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, ContextTypes, MessageHandler, filters

SUBJECT, TOPIC, LEVEL = range(3)


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

    #intructions here:
    await update.message.reply_text("Welcome to Quiz Bot. Get ready to challenge your knowledge with our exciting quiz. Choose the subject, topic and difficulty level according to your convenience and answer the questions that follows.\n")
    await update.message.reply_text("Enter the subject you wish to take the quiz on: ")
    return SUBJECT


async def subj(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['subject'] = update.message.text
    await update.message.reply_text("Enter the topic you wish to take a quiz on: ")
    return TOPIC

async def topi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['topic'] = update.message.text
    await update.message.reply_text("Enter the level of the quiz [beginner/intermediate/advanced]: ")
    return LEVEL

async def leve(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['level'] = update.message.text
    await update.message.reply_text("\nGenerating quiz questions, please wait...")

'''
async def quizRun(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # Program Start here:
    GOOGLE_API_KEY='AIzaSyC_1F8N1oLYOXvv_MJ21Yp0GlRU6ksT2R4'

    genai.configure(api_key=GOOGLE_API_KEY) #apikey configuration

    model = genai.GenerativeModel('gemini-1.5-flash') #model setup
    # User input
    await update.message.reply_text("Enter the subject you wish to take the quiz on: ")
    sub = await update.message.text
    await update.message.reply_text("Enter the topic you wish to take a quiz on: ").upper()
    topic = await update.message.text
    await update.message.reply_text("Enter the level of the quiz [beginner/intermediate/advanced]: ").upper()
    level = await update.message.text
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
'''

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SUBJECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, subj)],
            TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, topi)],
            LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, leve)],

        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()