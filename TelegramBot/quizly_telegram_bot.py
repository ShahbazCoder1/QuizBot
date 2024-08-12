'''
Title: Quizly - Telegram AI Quiz Bot
Code Written by: 𝗠𝗱 𝗦𝗵𝗮𝗵𝗯𝗮𝘇 𝗛𝗮𝘀𝗵𝗺𝗶 𝗔𝗻𝘀𝗮𝗿𝗶, 𝗩𝗶𝗱𝗵𝗶 𝗔𝗴𝗿𝗮𝘄𝗮𝗹
programing languages: Python
Description: This code creates a Telegram bot called Quizly that lets you play quizzes, get help, and even give feedback! 
It's like having a friendly AI quizmaster right in your Telegram chats. We have modified the main.py into a Telegram Bot.
Code Version: V1.0
Copyright ©: Open-source
'''
import google.generativeai as genai
import os
import time
from typing import Final
from telegram import Update, Poll, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, PollHandler, CallbackQueryHandler, filters
from youtube_video_suggestion import get_youtube_video_recommendation
from feedback_email import send_feedback_email
from firestore.user_data import get_user_record, add_user_record, update_user_record, check_user_record
from translate.translations import _, translations
from validation.validate_dict import get_validated_dict, convert_dict, escape_reserved_characters
from validation.validate_input import validate_subject, validate_topic
from flask_web_dev.keep_alive import keep_alive #use this if you want to run it in a web deployment
keep_alive()

TOKEN: Final = os.environ.get('TOKEN')
BOT_USERNAME: Final = os.environ.get('USERNAME')
GOOGLE_API_KEY: Final = os.environ.get('API_KEY')
youtube_api_key: Final = os.environ.get('YOUTUBE_API')
user_record = {}

#console print
print("\033[38;2;255;153;51m  ****             * \n * ** *            \n\033[0m"
  "* *  * *  *** *** *** *****  *** ***   ***\n* *  * *  * * * * * * *_  *  * * * *   * *\n"
  "*  **  *  * *_* * * *  * *_  * *  * *_* * \n\033[32m *   * *  *     * * * *    * * *   *   *  \n"
  "  *** * *  *****  *** ****** ***    * *  \n                                    ***  \033[0m")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update_lang(update,context)
    chat_id = await get_chat_id(update, context)
    await update.message.reply_text(_(chat_id,"Here are the available commands: \n/start - Begin with your quiz \n/help - Show this help message \n/about - See a description of the bot \n/stop- Stop the quiz \n/feedback - Send feedback \n/language - Set the bot's language"))

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update_lang(update,context)
    chat_id = await get_chat_id(update, context)
    keyboard = [
        [InlineKeyboardButton("GitHub", url="https://github.com/ShahbazCoder1/QuizBot ")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(_(chat_id,"📚 You can use this bot to take quizzes on different subjects across various topics. You can also adjust the difficulty level according to your convenience. \n\n🏅 Your score will be displayed after you finish the quiz.\n\nNOTE: This quiz is created with AI, and while we strive for accuracy, there's always a chance for a mistake.\n\n𝗪𝗶𝘁𝗵 ❤️ 𝗽𝗿𝗼𝘂𝗱𝗹𝘆 𝗺𝗮𝗱𝗲 𝗶𝗻 𝗜𝗻𝗱𝗶𝗮 🇮🇳"), reply_markup=reply_markup)

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['STATE'] = "lang"
    chat_id = await get_chat_id(update, context)
    message = context.user_data.get('message')
    keyboard = [
        [InlineKeyboardButton(_(chat_id,"English"), callback_data="en:English"),InlineKeyboardButton(_(chat_id,"Hindi"), callback_data="hi:Hindi")],
        [InlineKeyboardButton(_(chat_id,"Spanish"), callback_data="es:Spanish")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if message is not None:
        await message.edit_text(_(chat_id,"Select the Language for the Bot:"), reply_markup=reply_markup)
        return
    await update_lang(update,context)
    await context.bot.send_message(chat_id=chat_id, text=_(chat_id,"Select the Language for the Bot:"), reply_markup=reply_markup)

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update_lang(update,context)
    chat_id = await get_chat_id(update, context)
    await update.message.reply_text(_(chat_id,"Enter your Feedback message: \n\nIf you don't want to send Feedback, type /cancel"))
    context.user_data['waiting_for_feedback'] = True

async def cancel_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update_lang(update,context)
    chat_id = await get_chat_id(update, context)
    await update.message.reply_text(_(chat_id,"Feedback cancelled."))
    context.user_data['waiting_for_feedback'] = False

async def handle_feedback_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update_lang(update,context)
    chat_id = await get_chat_id(update, context)
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
    await update.message.reply_text(_(chat_id,"Thank you for your feedback!"))
    context.user_data['waiting_for_feedback'] = False
    del data

async def update_lang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = await get_chat_id(update, context)
    user_id = str(chat_id)
    data = get_user_record(user_id)
    context.user_data.update({'Language': data['language'], 'Lcode': data['lang']})
    translations.set_language(chat_id,data['lang'])

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = await get_chat_id(update, context)
    user_data = user_record.get(str(chat_id))
    try:
        poll_id = user_data.get('poll_id')
    except Exception as e:
        await update.message.reply_text(_(chat_id,"No active quiz to stop."))
        return

    if poll_id != -1:
        await loadQuiz(update, context, stop=True, poll_id=poll_id, chat_id=chat_id)
        user_record[str(chat_id)]['poll_id'] = -1
    else:
        await update.message.reply_text(_(chat_id,"No active quiz to stop.") if user_data else _(chat_id,"No active quiz session found."))

async def setup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = await get_chat_id(update, context)
    await context.bot.send_message(chat_id, text=_(chat_id,"The Quizly Quiz adventure begins now!"))
    context.user_data['STATE'] = "get"
    keyboard = [
        [InlineKeyboardButton(_(chat_id,"/Language"), callback_data="Language"), InlineKeyboardButton(_(chat_id,"Continue"), callback_data="Continue")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['message'] = await context.bot.send_message(chat_id=chat_id, text=_(chat_id,"Do you want to Change Quizly defualt language?"), reply_markup=reply_markup)

async def resetAll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global user_record
    context.user_data.update({
        'SUBJECT': None,
        'TOPIC': None,
        'LEVEL': None,
        'STATE': None,
        'firstTime': False,
        'message': None,
        'c_id': await get_chat_id(update, context)
    })
    user_id = str(context.user_data.get('c_id'))
    user_record[user_id] = {
        "cor": 0,
        "icor": 0,
        "poll_id": -1,
        "message": None,
        "topic": None
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await resetAll(update, context)

    chat_id = context.user_data.get('c_id')
    user_id = str(chat_id)
    if not check_user_record(user_id): 
        await setup(update, context)
        return 
    await update_lang(update,context)
    keyboard = [
        [_(chat_id,"Mathematics"), _(chat_id,"Physics")],
        [_(chat_id,"Chemistry"), _(chat_id,"Biology")],
        [_(chat_id,"Computer Science"), _(chat_id,"History")],
        [_(chat_id,"Geography"), _(chat_id,"Politics")],
        [_(chat_id,"English"), _(chat_id,"General Knowledge")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await context.bot.send_message(chat_id=chat_id, text=_(chat_id,"Enter the subject you wish to take the quiz on:"), reply_markup=reply_markup)
    context.user_data['STATE'] = "subject"

async def subj(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    subject = update.message.text
    chat_id = await get_chat_id(update, context)

    if await validate_subject(subject):
        context.user_data['SUBJECT'] = subject
        await update.message.reply_text(_(chat_id, "Enter the topic you wish to take a quiz on:"))
        context.user_data['STATE'] = "topic"
    else:
        await update.message.reply_text(_(chat_id, "Invalid subject. Please enter a valid subject."))

async def topi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    topic = update.message.text
    subject = context.user_data.get('SUBJECT')
    chat_id = await get_chat_id(update, context)

    if await validate_topic(subject, topic):
        context.user_data.update({
            'TOPIC': topic,
            'STATE': "level"
        })
        keyboard = [
            [InlineKeyboardButton(_(chat_id, "Beginner"), callback_data="Beginner")],
            [InlineKeyboardButton(_(chat_id, "Intermediate"), callback_data="Intermediate")],
            [InlineKeyboardButton(_(chat_id, "Advanced"), callback_data="Advanced")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(_(chat_id, "Enter the level of the quiz:"), reply_markup=reply_markup)
    else:
        await update.message.reply_text(_(chat_id, "Invalid topic for {subject}. Please enter a relevant topic.").format(subject=subject))

async def leve(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_data = context.user_data
    SUBJECT, TOPIC, LEVEL, c_id, LANGUAGE = map(user_data.get, ['SUBJECT', 'TOPIC', 'LEVEL', 'c_id', 'Language'])
    message = await context.bot.send_message(chat_id=c_id, text=_(c_id,"Generating quiz questions, please wait..."))

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = f"""Generate a python dictionary with 10 {LEVEL} level questions on {TOPIC} from {SUBJECT}.
    Each question should have four options (A, B, C, D) and an answer key along with the explanation of the correct answer. 
    All the questions, options and explanation should be in {LANGUAGE} language.
    All reserved characters should be with a backslash (\) if they are part of the question, options or explanation text.
    Use this structure:
    {{
        'Q1': {{
            'question': 'Question text',
            'options': {{'A': 'Option A', 'B': 'Option B', 'C': 'Option C', 'D': 'Option D'}},
            'answer': 'Correct letter (A, B, C, or D)'
            'explanation': 'Explanation text'
        }},
        ...
    }}
    Return only the Python dictionary code."""

    response = model.generate_content(prompt)
    response_text = response.text.strip('`python').strip()
    try:
        quiz = convert_dict(response_text)
    except Exception as e:
        quiz = get_validated_dict(response_text) 
    await message.edit_text(_(c_id,"Generating quiz questions, please wait... \n\n𝐍𝐨𝐭𝐞: 𝐓𝐡𝐢𝐬 𝐪𝐮𝐢𝐳 𝐪𝐮𝐞𝐬𝐭𝐢𝐨𝐧𝐬 𝐢𝐬 𝐜𝐫𝐞𝐚𝐭𝐞𝐝 𝐰𝐢𝐭𝐡 𝐀𝐈, 𝐚𝐧𝐝 𝐰𝐡𝐢𝐥𝐞 𝐰𝐞 𝐬𝐭𝐫𝐢𝐯𝐞 𝐟𝐨𝐫 𝐚𝐜𝐜𝐮𝐫𝐚𝐜𝐲, 𝐭𝐡𝐞𝐫𝐞'𝐬 𝐚𝐥𝐰𝐚𝐲𝐬 𝐚 𝐜𝐡𝐚𝐧𝐜𝐞 𝐟𝐨𝐫 𝐚 𝐦𝐢𝐬𝐭𝐚𝐤𝐞."))
    time.sleep(3)
    await message.edit_text(_(c_id,"Let's Begin"))

    # First Question
    value = quiz['Q1']
    question_text = value['question']
    truncated_question = (question_text[:297] + '...') if len(question_text) > 300 else question_text
    options = [opt[:97] + '...' if len(opt) > 100 else opt for opt in value['options'].values()]
    answer_index = ['a', 'b', 'c', 'd'].index(value['answer'].lower())
    explanation_text = value['explanation']
    truncated_explanation = (explanation_text[:197] + '...') if len(explanation_text) > 200 else explanation_text

    message = await context.bot.send_poll(
        chat_id=c_id, 
        question=f"Q1: {truncated_question}", 
        options=options, 
        type=Poll.QUIZ, 
        correct_option_id=answer_index,
        explanation=escape_reserved_characters(truncated_explanation),
        explanation_parse_mode = ParseMode.MARKDOWN_V2

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
        "message": chat_data.get('message_id'),
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
        question_text = value['question']
        truncated_question = (question_text[:297] + '...') if len(question_text) > 300 else question_text
        options = [opt[:97] + '...' if len(opt) > 100 else opt for opt in value['options'].values()]
        answer_index = ['a', 'b', 'c', 'd'].index(value['answer'].lower())
        explanation_text = value['explanation']
        truncated_explanation = (explanation_text[:197] + '...') if len(explanation_text) > 200 else explanation_text

        message = await context.bot.send_poll(
            chat_id=chat_id, 
            question=f"\nQ{question_index}: {truncated_question}", 
            options=options, 
            type=Poll.QUIZ, 
            correct_option_id=answer_index,
            explanation=escape_reserved_characters(truncated_explanation),
            explanation_parse_mode = ParseMode.MARKDOWN_V2
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

        completion_message = _(chat_id,"Congratulations! You have completed the quiz on {topic}\n\n🎯 𝗬𝗼𝘂𝗿 𝘀𝗰𝗼𝗿𝗲:\n\n✅ Correct answers: {cor}\n❌ Incorrect answers: {incor}").format(topic=topic, cor=cor, incor=incor)
        if cor <= 5:
            try:
                videos = get_youtube_video_recommendation(topic, youtube_api_key, max_results=3)
                reply_markup = InlineKeyboardMarkup(videos)
                completion_message += _(chat_id,"\n\nHere are some recommended videos to improve your knowledge on {topic}:").format(topic=topic)
                await context.bot.send_message(chat_id=chat_id, text=completion_message, reply_markup=reply_markup)
            except Exception as e:
                print(f"An error occurred while fetching video recommendations: {e}")
                await context.bot.send_message(chat_id=chat_id, text=completion_message)
        else:
            completion_message += _(chat_id,"\n\nGreat job! Your performance in the quiz on {topic} is outstanding! 🌟").format(topic=topic)
            await context.bot.send_message(chat_id=chat_id, text=completion_message)

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    STATE = context.user_data.get('STATE')
    query = update.callback_query
    await query.answer()

    chat_id = await get_chat_id(update, context)
    user_id = str(chat_id)

    if STATE == "level":
        context.user_data['LEVEL'] = query.data
        await leve(update, context)
        return

    if STATE == "get":
        if query.data == "Language":
            context.user_data['firstTime'] = True
            await set_language(update, context)
        else:
            add_user_record(user_id, "en", "English", update.callback_query.from_user.first_name)
            await update_lang(update, context)
            await context.user_data.get('message').edit_text(_(chat_id, "English is set as your Default Language"))
            await start(update, context)
        return

    if STATE == "lang":
        language_code, language_name = query.data.split(':')
        is_first_time = context.user_data.get('firstTime', False)

        if is_first_time:
            add_user_record(user_id, language_code, language_name, update.callback_query.from_user.first_name)
            translations.set_language(chat_id,language_code)
            await context.user_data.get('message').edit_text(_(chat_id, "{language_name} is set as your default language").format(language_name=language_name))
            await start(update, context)
        else:
            update_user_record(user_id, language_code, language_name)
            translations.set_language(chat_id,language_code)
            await query.message.reply_text(_(chat_id, "{language_name} is set as your default language").format(language_name=language_name))

        await update_lang(update, context)
        return

    await query.message.reply_text(_(user_id, "Invalid input. Please try again."))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = await get_chat_id(update, context)
    STATE = context.user_data.get('STATE')
    if STATE == "subject":
        await subj(update, context)
    elif STATE == "topic":
        await topi(update, context)
    else:
        await update.message.reply_text(_(chat_id,"Please use the provided buttons to interact with the bot."))

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"An error occurred: {context.error}")
    try:
        chat_id = await get_chat_id(update, context)
        await context.bot.send_message(chat_id=chat_id, text=_(chat_id, "An error occurred. Please try again later."))
    except:
        print("Failed to send error message to user.")

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
    application.add_error_handler(error_handler)
    application.run_polling()

if __name__ == '__main__':
    main()