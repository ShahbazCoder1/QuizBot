import google.generativeai as genai
import ast
import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Final
from telegram import Update, Poll, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, PollHandler, CallbackQueryHandler, filters
from  youtube_video_suggestion import get_youtube_video_recommendation


TOKEN: Final = os.getenv('token')
BOT_USERNAME: Final = os.getenv('username')
GOOGLE_API_KEY=os.getenv('api_key')
youtube_api_key = os.getenv('youtube_api')

print("  ____          _ \n / __ \\        (_)\n| |  | | _   _  _  ____\n| |  | || | | || ||_  /\n| |__| || |_| || | / /_\n \\___\\_\\ \\__,_||_|/____|\n ____          _   \n|  _ \\        | |  \n| |_) |  ___  | |_ \n|  _ <  / _ \\ | __|\n| |_) || (_) || |_ \n|____/  \\___/  \\__|")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Here are the available commands: \n/start - Begin with your quiz \n/help - Show this help message \n/about - See a description of the bot \n/stop- Stop the quiz")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("GitHub", url="https://github.com/ShahbazCoder1/QuizBot ")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📚 You can use this bot to take quizzes on different subjects across various topics. You can also adjust the difficulty level according to your convenience. \n\n🏅 Your score will be displayed after you finish the quiz.\n\n𝗪𝗶𝘁𝗵 ❤️ 𝗽𝗿𝗼𝘂𝗱𝗹𝘆 𝗺𝗮𝗱𝗲 𝗶𝗻 𝗜𝗻𝗱𝗶𝗮 🇮🇳", reply_markup=reply_markup)

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Coming Soon!")

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Enter your Feedback message: \n\nIf you don't want to send Feedback, type /cancel")
    context.user_data['waiting_for_feedback'] = True

async def cancel_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Feedback canceled.")
    context.user_data['waiting_for_feedback'] = False

async def handle_feedback_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('waiting_for_feedback'):
        chat = update.message.chat
        user = update.message.from_user
        date = update.message.date
        name = chat.first_name
        chat_id = chat.id
        chat_type = chat.type
        message_date = date.strftime("%Y-%m-%d %H:%M:%S")
        timezone = date.tzinfo
        is_bot = user.is_bot

        from_email = os.getenv('send_email')
        from_password = os.getenv('password')
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = os.getenv('receiver_email')
        msg['Subject'] = "Someone has given a feedback about Quizly Bot"
        body = f"""
        <html>
        <body>
            <p>Hi There,</p>
            <p>Quizly has a new feedback:</p>
            <blockquote>{update.message.text}</blockquote>
            <p><strong>Sender Details:</strong></p>
            <ul>
                <li><strong>Name:</strong> {name}</li>
                <li><strong>User ID:</strong> {chat_id}</li>
                <li><strong>Chat Type:</strong> {chat_type}</li>
                <li><strong>Date & Time Zone:</strong> {message_date} ({timezone})</li>
                <li><strong>Is Bot:</strong> {is_bot}</li>
            </ul>
        </body>
        </html>
        """
        # Attach the message body
        msg.attach(MIMEText(body, 'html'))
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
    chat_id = await get_chat_id(update, context)
    for poll_id, data in context.bot_data.items():
        #print(poll_id, '\n\n',data)
        if data.get('chat_id') == chat_id:
            await loadQuiz(update, context, stop=True, poll_id=poll_id)
            break
    else:
        await update.message.reply_text("No active quiz to stop.")

async def resetAll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['SUBJECT'] = None
    context.user_data['TOPIC'] = None 
    context.user_data['LEVEL'] = None
    context.user_data['STATE'] = None
    context.user_data['c_id'] = await get_chat_id(update, context)

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
    
    genai.configure(api_key=GOOGLE_API_KEY) #apikey configuration
    model = genai.GenerativeModel('gemini-1.5-flash') #model setup
    response = model.generate_content(f"""Generate a python dictionary which contains 10 {LEVEL} level questions on {TOPIC} from {SUBJECT} along with four options as possible answers for each question. Show the four options along with alphabets assigned to them serially.

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
    response_text = response.text.replace("```", "").replace("python", "").replace(f"{TOPIC.lower()}_questions = ", "")
    quiz = ast.literal_eval(response_text)
    await message.edit_text("Let's Begin")
    #First Question
    question_key = f"Q{1}"
    value = quiz[question_key]
    options = value['options']
    opt = list(options.values())
    ans = ['a', 'b', 'c', 'd']
    answer_index = ans.index(value['answer'].lower())
    message = await context.bot.send_poll(chat_id=c_id, question=f"Q{1}: {value['question']}",options=opt, type=Poll.QUIZ, correct_option_id=answer_index)
    payload = {
    message.poll.id: {
        "chat_id": c_id, 
        "message_id": message.message_id, 
        "message": message, 
        "cor_count": 0, 
        "incor_count": 0,
        "quiz": quiz,
        "question_index": 1,
        "topic": TOPIC
      }
    }
    context.bot_data.update(payload)

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
    poll_id = update.poll.id
    chat_data = context.bot_data.get(poll_id)
    chat_id = chat_data.get('chat_id')
    correct_answer = update.poll.correct_option_id
    option_1_text = update.poll.options[correct_answer].text
    answers = update.poll.options
    ret = ""
    for answer in answers:
        if answer.voter_count == 1:
            ret = answer.text
            break

    if option_1_text == ret:
        chat_data['cor_count'] = chat_data.get('cor_count') + 1
        #print('\n\n',chat_data.get('cor_count'))
    else:
        chat_data['incor_count'] = chat_data.get('incor_count') + 1
        #print('\n\n' , chat_data.get('incor_count'))
    await loadQuiz(update, context,poll_id=poll_id)

async def loadQuiz(update: Update, context: ContextTypes.DEFAULT_TYPE, stop = False, poll_id = None) -> None:
    #print('\n\npoll is ',poll_id)
    chat_data = context.bot_data.get(poll_id)
    #print(chat_data)
    chat_id = chat_data.get('chat_id')
    quiz = chat_data.get('quiz') 
    TOPIC = chat_data.get('topic')
    cor = chat_data.get('cor_count')
    incor = chat_data.get('incor_count')
    print(f"\n\ncorrect {cor} \n\nIncorrect {incor}")
    question_index = chat_data.get('question_index') + 1
    chat_data['question_index'] = question_index

    if stop: question_index = len(quiz)+1

    if question_index <= len(quiz):
        #if stop: break
        question_key = f"Q{question_index}"
        value = quiz[question_key]
        options = value['options']
        opt = list(options.values())
        ans = ['a', 'b', 'c', 'd']
        answer_index = ans.index(value['answer'].lower())
        message = await context.bot.send_poll(chat_id=chat_id, question=f"\nQ{question_index}: {value['question']}",options=opt, type=Poll.QUIZ, correct_option_id=answer_index)
        payload = {
        message.poll.id: {
            "chat_id": chat_id, 
            "message_id": message.message_id, 
            "message": message, 
            "cor_count": cor, 
            "incor_count": incor,
            "quiz": quiz,
            "question_index": question_index,
            "topic": TOPIC
        }
        }
        context.bot_data.update(payload)
    else:
        if cor <= 5:
            videos =None
            while videos is None:
                try:
                    videos = get_youtube_video_recommendation(TOPIC, youtube_api_key, max_results=3)
                except Exception as e:
                    print(f"An error occurred: {e}")
                finally:
                    reply_markup = InlineKeyboardMarkup(videos)
                    await context.bot.send_message(chat_id=chat_id, text=f"Quiz Completed.\nNumber of correct answers: {cor} \nNumber of incorrect answers:{incor} \n\nHere are some recommended videos to improve your knowledge on {TOPIC}:", reply_markup=reply_markup)
        else:
            await context.bot.send_message(chat_id=chat_id, text=f"Quiz Completed.\nNumber of correct answers: {cor} \nNumber of incorrect answers:{incor}")

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
    application.add_handler(CommandHandler("cancel", cancel_feedback))
    application.add_handler(CommandHandler("language", set_language))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_feedback_message))
    application.add_handler(CallbackQueryHandler(handle_input))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(PollHandler(poll_handler))
    application.run_polling()

if __name__ == '__main__':
    main()