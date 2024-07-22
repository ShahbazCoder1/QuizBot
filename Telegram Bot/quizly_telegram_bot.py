'''
Title: Quizly - Telegram AI Quiz Bot
Code Written by: 𝗠𝗱 𝗦𝗵𝗮𝗵𝗯𝗮𝘇 𝗛𝗮𝘀𝗵𝗺𝗶 𝗔𝗻𝘀𝗮𝗿𝗶, 𝗩𝗶𝗱𝗵𝗶 𝗔𝗴𝗿𝗮𝘄𝗮𝗹
programing languages: Python
Description: This code creates a Telegram bot called Quizly that lets you play quizzes, get help, and even give feedback! 
It's like having a friendly quizmaster right in your Telegram chats. We have modified the main.py into a Telegram Bot.
Code Version: V1.0
Copyright ©: Open-source
'''

import google.generativeai as genai
import ast
import os
import time
from typing import Final
from telegram import Update, Poll, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, PollHandler, CallbackQueryHandler, filters
from youtube_video_suggestion import get_youtube_video_recommendation
from feedback_email import send_feedback_email


TOKEN: Final = os.getenv('token')
BOT_USERNAME: Final = os.getenv('username')
GOOGLE_API_KEY: Final = os.getenv('api_key')
youtube_api_key: Final = os.getenv('youtube_api')
user_record = {}

print("  ____          _ \n / __ \\        (_)\n| |  | | _   _  _  ____\n| |  | || | | || ||_  /\n| |__| || |_| || | / /_\n \\___\\_\\ \\__,_||_|/____|\n ____          _   \n|  _ \\        | |  \n| |_) |  ___  | |_ \n|  _ <  / _ \\ | __|\n| |_) || (_) || |_ \n|____/  \\___/  \\__|")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Here are the available commands: \n/start - Begin with your quiz \n/help - Show this help message \n/about - See a description of the bot \n/stop- Stop the quiz \n/feedback - Send feedback \n/language - Set the bot's language (Coming Soon!)")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("GitHub", url="https://github.com/ShahbazCoder1/QuizBot ")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📚 You can use this bot to take quizzes on different subjects across various topics. You can also adjust the difficulty level according to your convenience. \n\n🏅 Your score will be displayed after you finish the quiz.\n\nNOTE: This quiz is created with AI, and while we strive for accuracy, there's always a chance for a mistake.\n\n𝗪𝗶𝘁𝗵 ❤️ 𝗽𝗿𝗼𝘂𝗱𝗹𝘆 𝗺𝗮𝗱𝗲 𝗶𝗻 𝗜𝗻𝗱𝗶𝗮 🇮🇳", reply_markup=reply_markup)

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Coming Soon!")

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Enter your Feedback message: \n\nIf you don't want to send Feedback, type /cancel")
    context.user_data['waiting_for_feedback'] = True

async def cancel_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Feedback canceled.")
    context.user_data['waiting_for_feedback'] = False

async def handle_feedback_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.user_data.get('waiting_for_feedback'):
        await handle_message(update, context)
        return
  
    data = {
            "chat": update.message.chat,
            "user": update.message.from_user,
            "date": update.message.date,
            "name": update.message.chat.first_name,
            "chat_id": update.message.chat.id,
            "chat_type": update.message.chat.type,
            "is_bot": update.message.from_user.is_bot,
            "feedback_text": update.message.text
    }
    send_feedback_email(data)
    await update.message.reply_text("Thank you for your feedback!")
    context.user_data['waiting_for_feedback'] = False
    del data
        
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = await get_chat_id(update, context)
    user_data = user_record.get(str(chat_id))
    try:
        poll_id = user_data.get('poll_id')
    except Exception as e:
        await update.message.reply_text("No active quiz to stop.")
        return

    if poll_id != -1:
        await loadQuiz(update, context, stop=True, poll_id=poll_id, chat_id=chat_id)
        user_record[str(chat_id)]['poll_id'] = -1
    else:
        await update.message.reply_text("No active quiz to stop." if user_data else "No active quiz session found.")


async def resetAll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global user_record
    context.user_data.update({
        'SUBJECT': None,
        'TOPIC': None,
        'LEVEL': None,
        'STATE': None,
        'c_id': await get_chat_id(update, context)
    })
    user_id = str(context.user_data.get('c_id'))
    user_record[user_id] = {
        "cor": 0,
        "icor": 0,
        "poll_id": -1,
        "topic": None
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await resetAll(update, context)
    
    keyboard = [
        ["Mathematics", "Physics"],
        ["Chemistry", "Biology"],
        ["Computer Science", "History"],
        ["Geography", "Politics"],
        ["English", "General Knowledge"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text("Get ready for Quizly Quiz!")
    await update.message.reply_text("Enter the subject you wish to take the quiz on: ", reply_markup=reply_markup)
    
    context.user_data['STATE'] = "subject"

async def subj(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['SUBJECT'] = update.message.text
    await update.message.reply_text("Enter the topic you wish to take a quiz on: ")
    context.user_data['STATE'] = "topic"

async def topi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.update({
        'TOPIC': update.message.text,
        'STATE': "level"
    })
    
    keyboard = [
        [InlineKeyboardButton("Beginner", callback_data="Beginner")],
        [InlineKeyboardButton("Intermediate", callback_data="Intermediate")],
        [InlineKeyboardButton("Advanced", callback_data="Advanced")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Enter the level of the quiz: ", reply_markup=reply_markup)

async def leve(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_data = context.user_data
    SUBJECT, TOPIC, LEVEL, c_id = map(user_data.get, ['SUBJECT', 'TOPIC', 'LEVEL', 'c_id'])

    message = await context.bot.send_message(chat_id=c_id, text="Generating quiz questions, please wait...")
    # Program Start here:
    
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""Generate a python dictionary with 10 {LEVEL} level questions on {TOPIC} from {SUBJECT}.
    Each question should have four options (A, B, C, D) and an answer key.
    Use this structure:
    {{
        'Q1': {{
            'question': 'Question text',
            'options': {{'A': 'Option A', 'B': 'Option B', 'C': 'Option C', 'D': 'Option D'}},
            'answer': 'Correct letter (A, B, C, or D)'
        }},
        ...
    }}
    Return only the Python dictionary code."""

    response = model.generate_content(prompt)
    response_text = response.text.strip('`python').strip()
    quiz = ast.literal_eval(response_text)
    await message.edit_text("Generating quiz questions, please wait... \n\n𝐍𝐨𝐭𝐞: 𝐓𝐡𝐢𝐬 𝐪𝐮𝐢𝐳 𝐪𝐮𝐞𝐬𝐭𝐢𝐨𝐧𝐬 𝐢𝐬 𝐜𝐫𝐞𝐚𝐭𝐞𝐝 𝐰𝐢𝐭𝐡 𝐀𝐈, 𝐚𝐧𝐝 𝐰𝐡𝐢𝐥𝐞 𝐰𝐞 𝐬𝐭𝐫𝐢𝐯𝐞 𝐟𝐨𝐫 𝐚𝐜𝐜𝐮𝐫𝐚𝐜𝐲, 𝐭𝐡𝐞𝐫𝐞'𝐬 𝐚𝐥𝐰𝐚𝐲𝐬 𝐚 𝐜𝐡𝐚𝐧𝐜𝐞 𝐟𝐨𝐫 𝐚 𝐦𝐢𝐬𝐭𝐚𝐤𝐞.")
    time.sleep(3)
    await message.edit_text("Let's Begin")

    # First Question
    value = quiz['Q1']
    options = list(value['options'].values())
    answer_index = ['a', 'b', 'c', 'd'].index(value['answer'].lower())

    message = await context.bot.send_poll(
        chat_id=c_id, 
        question=f"Q1: {value['question']}", 
        options=options, 
        type=Poll.QUIZ, 
        correct_option_id=answer_index
    )

    context.bot_data[message.poll.id] = {
        "chat_id": c_id,
        "message_id": message.message_id,
        "message": message,
        "cor_count": 0,
        "incor_count": 0,
        "quiz": quiz,
        "question_index": 1,
        "topic": TOPIC
    }

#obtain chat id 
async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        return update.message.chat.id
    if update.callback_query:
        return update.callback_query.message.chat.id
    if update.poll:
        return context.bot_data[update.poll.id]['chat_id']
    return -1

async def poll_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global user_record
    poll_id = update.poll.id
    chat_data = context.bot_data.get(poll_id)
    chat_id = chat_data.get('chat_id')
    user_id = str(chat_id)

    correct_answer = update.poll.correct_option_id
    correct_option_text = update.poll.options[correct_answer].text

    # Find the selected answer efficiently
    selected_option = next((answer for answer in update.poll.options if answer.voter_count == 1))

    is_correct = selected_option and selected_option.text == correct_option_text

    # Update counts
    count_key = 'cor_count' if is_correct else 'incor_count'
    chat_data[count_key] = chat_data.get(count_key) + 1

    # Update user_record efficiently
    user_record.setdefault(user_id, {}).update({
        "cor": chat_data.get('cor_count'),
        "icor": chat_data.get('incor_count'),
        "poll_id": poll_id,
        "topic": chat_data.get('topic')
    })

    await loadQuiz(update, context, poll_id=poll_id, chat_id=chat_id)

async def loadQuiz(update: Update, context: ContextTypes.DEFAULT_TYPE, stop=False, poll_id=None, chat_id=None) -> None:
    global user_record
    
    chat_data = context.bot_data.get(poll_id)
    user_id = str(chat_id)
    user_data = user_record.get(user_id)
    
    question_index = chat_data.get('question_index') + 1
    quiz = chat_data.get('quiz')
    
    if stop:
        question_index = len(quiz) + 1

    if question_index <= len(quiz):
        value = quiz[f"Q{question_index}"]
        options = list(value['options'].values())
        answer_index = ['a', 'b', 'c', 'd'].index(value['answer'].lower())
        
        message = await context.bot.send_poll(
            chat_id=chat_id, 
            question=f"\nQ{question_index}: {value['question']}", 
            options=options, 
            type=Poll.QUIZ, 
            correct_option_id=answer_index
        )
        
        context.bot_data[message.poll.id] = {
            "chat_id": chat_id,
            "message_id": message.message_id,
            "message": message,
            "cor_count": user_data.get('cor'),
            "incor_count": user_data.get('icor'),
            "quiz": quiz,
            "question_index": question_index,
            "topic": chat_data.get('topic')
        }
    else:
        cor = user_data.get('cor')
        incor = user_data.get('icor')
        topic = user_data.get('topic')
        
        completion_message = f"Congratulations! You have completed the quiz on {topic}\n\n🎯 𝗬𝗼𝘂𝗿 𝘀𝗰𝗼𝗿𝗲:\n\n✅ Correct answers: {cor}\n❌ Incorrect answers: {incor}"
        
        if cor <= 5:
            try:
                videos = get_youtube_video_recommendation(topic, youtube_api_key, max_results=3)
                reply_markup = InlineKeyboardMarkup(videos)
                completion_message += f"\n\nHere are some recommended videos to improve your knowledge on {topic}:"
                await context.bot.send_message(chat_id=chat_id, text=completion_message, reply_markup=reply_markup)
            except Exception as e:
                print(f"An error occurred while fetching video recommendations: {e}")
                await context.bot.send_message(chat_id=chat_id, text=completion_message)
        else:
            completion_message += f"\n\nGreat job! Your performance in the quiz on {topic} is outstanding! 🌟"
            await context.bot.send_message(chat_id=chat_id, text=completion_message)

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