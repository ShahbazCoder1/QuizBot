import google.generativeai as genai
from tqdm import tqdm
import time
from typing import Final
from telegram import Update,Poll
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
    global STATE
    LEVEL = update.message.text
    await update.message.reply_text("\nGenerating quiz questions, please wait...")
    #await quizRun(update, context)


async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global STATE
    if STATE == "subject":
        await subj(update, context)
    elif STATE == "topic":
        await topi(update, context)
    elif STATE == "level":
        await leve(update, context)
    else:
        await update.message.reply_text("Invalid input. Please try again.")


'''async def quizRun(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # Program Start here:
    global LEVEL
    global TOPIC
    global SUBJECT
    GOOGLE_API_KEY='AIzaSyC_1F8N1oLYOXvv_MJ21Yp0GlRU6ksT2R4'

    genai.configure(api_key=GOOGLE_API_KEY) #apikey configuration

    model = genai.GenerativeModel('gemini-1.5-flash') #model setup
    
    response = model.generate_content(f"Generate a python dictionary which contains 10 {LEVEL} level questions on {TOPIC} from {SUBJECT} along with four options as possible answers for each question. Show the four options along with alphabets assigned to them serially. Return only the dictonary code part.")

    incor = 0
    cor = 0

    quiz = eval(response.text.replace("```","").replace("python","").replace(f"{TOPIC.lower()}_questions=",""))

    await update.message.reply_text(quiz)


    for key, value in quiz.items():
        #await update.message.reply_text(f"\nQ: {value['question']}")
        options = value['options']
        #for opt_key, opt_value in options.items():
            #await update.message.reply_text(f"{opt_key}: {opt_value}")
        message=await update.effective_message.reply_poll(value['question'],options,type=Poll.QUIZ,correct_option_id=options.index
        (value['options']))'''
       

    

    
async def send_quiz_polls(update, context):
    # Program Start here:
    global LEVEL
    global TOPIC
    global SUBJECT
    GOOGLE_API_KEY='AIzaSyC_1F8N1oLYOXvv_MJ21Yp0GlRU6ksT2R4'

    genai.configure(api_key=GOOGLE_API_KEY) #apikey configuration

    model = genai.GenerativeModel('gemini-1.5-flash') #model setup
    
    response = model.generate_content(f"Generate a python dictionary which contains 10 {LEVEL} level questions on {TOPIC} from {SUBJECT} along with four options as possible answers for each question. Show the four options along with alphabets assigned to them serially. Return only the dictonary code part.")

    incor = 0
    cor = 0

    quiz = eval(response.text.replace("```","").replace("python","").replace(f"{TOPIC.lower()}_questions=",""))
    for key, value in quiz.items():
        question = value['Question']
        options = list(value['Options'].values())
        
        # Determine the correct option ID based on the correct answer key
        correct_answer_key = value['Correct_Answer']
        correct_option_id = list(value['Options'].keys()).index(correct_answer_key)
        
        # Send the quiz poll
        await update.effective_message.reply_poll(
            question=question,
            options=options,
            type=Poll.QUIZ,
            correct_option_id=correct_option_id
        )

# Example usage in a handler function:
# async def quiz_command(update: Update, context: CallbackContext):
#     await send_quiz_polls(update, context)



        '''
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
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))
    application.add_handler(CommandHandler("quiz", send_quiz_polls))
    application.run_polling()

if __name__ == '__main__':
    main()