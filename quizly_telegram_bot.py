import google.generativeai as genai
from tqdm import tqdm
import time
from typing import Final
from telegram import Update, Poll
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, PollAnswerHandler,PollHandler, filters

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
    global SUBJECT
    global TOPIC
    global LEVEL
    global STATE
    LEVEL = update.message.text
    await update.message.reply_text("\nGenerating quiz questions, please wait...")

    # Program Start here:
    GOOGLE_API_KEY='AIzaSyC_1F8N1oLYOXvv_MJ21Yp0GlRU6ksT2R4'
    genai.configure(api_key=GOOGLE_API_KEY) #apikey configuration
    model = genai.GenerativeModel('gemini-1.5-flash') #model setup
    response = model.generate_content(f"""Generate a python dictionary which contains 10 {LEVEL} level questions on {TOPIC} from {SUBJECT} along with four options as possible answers for each question. Show the four options along with alphabets assigned to them serially. Return only the dictionary code part.

    The dictionary should have the following structure:

    The main dictionary contains 10 key-value pairs, with keys 'Q1' through 'Q10'.
    Each question is represented by a nested dictionary containing three key-value pairs:
    1. 'question': A string containing the question text.
    2. 'options': A nested dictionary with keys 'A', 'B', 'C', and 'D', each corresponding to a possible answer.
    3. 'answer': A string containing the letter of the correct answer ('A', 'B', 'C', or 'D').

    Example structure for one question:

    {{
        'Q1': {{
            'question': 'What is the question text?',
            'options': {{
                'A': 'First option',
                'B': 'Second option',
                'C': 'Third option',
                'D': 'Fourth option'
            }},
            'answer': 'C'
        }}
    }}

    Ensure that all questions are related to the specified topic and subject, and match the specified difficulty level. Return only the Python dictionary code, without any additional text or explanations.""")
    
    quiz = eval(response.text.replace("```","").replace("python","").replace(f"{TOPIC.lower()}_questions = ",''))

    #print(quiz)

    for key, value in quiz.items():
        options = value['options']
        opt = list(options.values())
        ans = ['a', 'b', 'c', 'd']
        answer_index = ans.index(value['answer'].lower())
        message = await update.effective_message.reply_poll(f"\nQ: {value['question']}", opt, type=Poll.QUIZ, correct_option_id= answer_index)


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

def main():
    global STATE
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))
    application.run_polling()

if __name__ == '__main__':
    main()





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