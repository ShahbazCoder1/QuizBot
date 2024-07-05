import google.generativeai as genai
from tqdm import tqdm
import time
from typing import Final
from telegram import Update, Poll
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, PollHandler, filters

SUBJECT = None
TOPIC = None 
LEVEL = None
STATE = None
c_id = None


TOKEN: Final = '7068344943:AAEIFEtmH0N64n7ombEPfDcMpPCOYwN3WFU'
BOT_USERNAME: Final = '@Quisly_Bot'

print("  ____          _ \n / __ \\        (_)\n| |  | | _   _  _  ____\n| |  | || | | || ||_  /\n| |__| || |_| || | / /_\n \\___\\_\\ \\__,_||_|/____|\n ____          _   \n|  _ \\        | |  \n| |_) |  ___  | |_ \n|  _ <  / _ \\ | __|\n| |_) || (_) || |_ \n|____/  \\___/  \\__|")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Get ready for Quizly Quiz!")

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
    global SUBJECT, TOPIC, LEVEL, STATE, c_id
    LEVEL = update.message.text
    await update.message.reply_text("\nGenerating quiz questions, please wait...")
    #await quizRun(update, context)

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
    C = 0
    c_id = await get_chat_id(update, context)
    q = 'What is the capital of Italy?'
    answers = ['Rome', 'London', 'Amsterdam']
    #send poll
    message = await context.bot.send_poll(chat_id=c_id, question=q,options=answers, type=Poll.QUIZ, correct_option_id=0)


#obtain chat id 
async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = -1
    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]
    return chat_id

async def poll_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  
    global c_id
    cor = 0
    incor = 0
    correct_answer = update.poll.correct_option_id
    option_1_text = update.poll.options[correct_answer].text
    answers = update.poll.options
    ret = ""
    for answer in answers:
        if answer.voter_count ==1:
            ret = answer.text
            break
    if option_1_text == ret:
        cor +=1
        await context.bot.send_message(chat_id=c_id, text="Excellent performance🥳!")
        print("correct")
    else:
        incor +=1
        await context.bot.send_message(chat_id=c_id, text="Incorrect")
        print("incorrect")


    '''for key, value in quiz.items():
        options = value['options']
        opt = list(options.values())
        ans = ['a', 'b', 'c', 'd']
        answer_index = ans.index(value['answer'].lower())
        C +=1 
        message = await update.effective_message.reply_poll(f"\nQ{C}: {value['question']}", opt, type=Poll.QUIZ, correct_option_id= answer_index)

'''
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
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))
    application.add_handler(PollHandler(poll_handler))
    application.run_polling()

if __name__ == '__main__':
    main()
