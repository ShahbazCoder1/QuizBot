import google.generativeai as genai
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from typing import Final
from telegram import Update, Poll, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, PollHandler, CallbackQueryHandler, filters


TOKEN: Final = '7068344943:AAEIFEtmH0N64n7ombEPfDcMpPCOYwN3WFU'
BOT_USERNAME: Final = '@Quisly_Bot'

print("  ____          _ \n / __ \\        (_)\n| |  | | _   _  _  ____\n| |  | || | | || ||_  /\n| |__| || |_| || | / /_\n \\___\\_\\ \\__,_||_|/____|\n ____          _   \n|  _ \\        | |  \n| |_) |  ___  | |_ \n|  _ <  / _ \\ | __|\n| |_) || (_) || |_ \n|____/  \\___/  \\__|")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Here are the available commands: \n/start - Begin with your quiz \n/help - Show this help message \n/about - See a description of the bot \n/stop- Stop the quiz")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("You can use this bot to take quizzes on different subjects across various topics. You can also adjust the difficulty level according to your convenience. \n\nYour score will be displayed after you finish the quiz. \n\nDEVELOPER INFO: \n-MD SHAHBAZ HASHMI ANSARI (https://github.com/ShahbazCoder1)\n-VIDHI AGARWAL (https://github.com/Vidhi-28) \n\nSource Code at: https://github.com/ShahbazCoder1/QuizBot")

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Enter your Feedback message: ")
    
    # Store the chat_id to use it later
    context.user_data['waiting_for_feedback'] = True
    
async def handle_feedback_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('waiting_for_feedback'):
        from_email = 'quizlyfeedback@gmail.com'
        from_password = 'htlq kwaj wekx pvsl'
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = "shahbazhashmi14a@gmail.com , shahbazhashmiansari@gmail.com"
        msg['Subject'] = "Someone has given a feedback about Quizly Bot"
        body = update.message.text
        # Attach the message body
        msg.attach(MIMEText(body, 'plain'))

        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable security
        server.login(from_email, from_password)

        # Send the email
        server.send_message(msg)
        server.quit()

        await update.message.reply_text("Thank you for your feedback!")
        context.user_data['waiting_for_feedback'] = False
    else:
        await handle_message(update, context)

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question_index = context.user_data.get('question_index')
    c_id = context.user_data.get('c_id')
    question_index=len(quiz)+1
    await loadQuiz(c_id,update, context)

async def resetAll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['SUBJECT'] = None
    context.user_data['TOPIC'] = None 
    context.user_data['LEVEL'] = None
    context.user_data['STATE'] = None
    context.user_data['c_id'] = await get_chat_id(update, context)
    context.user_data['quiz'] = None
    context.user_data['question_index'] = 0
    context.user_data['cor'] = 0
    context.user_data['incor'] = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await resetAll(update, context)
    await update.message.reply_text("Get ready for Quizly Quiz!")
    keyboard = [
        ["Mathematics", "Physics"],
        ["Chemistry", "Biology"],
        ["Computer Science", "History"],
        ["Geography", "Politics"],
        ["English", "General Knowledge"]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await update.message.reply_text("Enter the subject you wish to take the quiz on: ", reply_markup=reply_markup)
    context.user_data['STATE'] = "subject"

async def subj(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['SUBJECT'] = update.message.text
    await update.message.reply_text("Enter the topic you wish to take a quiz on: ")
    context.user_data['STATE'] = "topic"

async def topi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['TOPIC'] = update.message.text
    keyboard = [
        [InlineKeyboardButton("Beginner", callback_data="Beginner")],
        [InlineKeyboardButton("Intermediate", callback_data="Intermediate")],
        [InlineKeyboardButton("Advanced", callback_data="Advanced")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Enter the level of the quiz: ", reply_markup=reply_markup)
    context.user_data['STATE'] = "level"

async def leve(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    SUBJECT = context.user_data.get('SUBJECT')
    TOPIC = context.user_data.get('TOPIC')
    LEVEL = context.user_data.get('LEVEL')
    c_id = context.user_data.get('c_id')
    message = await context.bot.send_message(chat_id=c_id, text="Generating quiz questions, please wait...")
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
    context.user_data['quiz'] = eval(response.text.replace("```","").replace("python","").replace(f"{TOPIC.lower()}_questions = ",''))
    await message.edit_text("Let's Begin")
    await loadQuiz(c_id,update, context)

#obtain chat id 
async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = -1
    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]
    return chat_id

async def poll_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Check if context.user_data exists
    if context.user_data is None:
        print("Warning: context.user_data is None")
        return  # Exit the function if there's no user data

    c_id = context.user_data.get('c_id')
    
    # If c_id is not found in user_data, try to get it from the update
    if c_id is None:
        c_id = await get_chat_id(update, context)
        if c_id == -1:
            print("Error: Unable to determine chat_id")
            return 
            
    correct_answer = update.poll.correct_option_id
    option_1_text = update.poll.options[correct_answer].text
    answers = update.poll.options
    await ansCheck(answers,option_1_text, context)
    ret = ""
    for answer in answers:
        if answer.voter_count ==1:
            ret = answer.text
            break
    if option_1_text == ret:
        context.user_data['cor'] += 1 
        print("correct")
    else:
        context.user_data['incor'] += 1 
        print("incorrect")
    await loadQuiz(c_id,update, context)

async def loadQuiz(c_id, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    quiz = context.user_data.get('quiz') 
    cor = context.user_data.get('cor')
    incor = context.user_data.get('incor')
    question_index = context.user_data.get('question_index')
    question_index += 1
    if question_index <= len(quiz):
        question_key = f"Q{question_index}"
        value = quiz[question_key]
        options = value['options']
        opt = list(options.values())
        ans = ['a', 'b', 'c', 'd']
        answer_index = ans.index(value['answer'].lower())
        message = await context.bot.send_poll(chat_id=c_id, question=f"\n{question_index}: {value['question']}",options=opt, type=Poll.QUIZ, correct_option_id=answer_index)
    else:
        await context.bot.send_message(chat_id=c_id, text=f"Quiz Completed.\nNumber of correct answers: {cor} \nNumber of incorrect answers:{incor}")
        await resetAll(update, context)

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    STATE = context.user_data.get('STATE')
    query = update.callback_query
    await query.answer()
    if STATE == "level":
        context.user_data['LEVEL'] = query.data
        await leve(update, context)
    else:
        await query.message.reply_text("Invalid input. Please try again.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    STATE = context.user_data.get('STATE')
    if STATE == "subject":
        await subj(update, context)
    elif STATE == "topic":
        await topi(update, context)
    else:
        await update.message.reply_text("Please use the provided buttons to interact with the bot.")

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("feedback", feedback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_feedback_message))
    application.add_handler(CallbackQueryHandler(handle_input))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(PollHandler(poll_handler))
    application.run_polling()

if __name__ == '__main__':
    main()