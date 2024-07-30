# Quizly Bot

Quizly Bot is a Telegram bot that allows users to take quizzes on various subjects and topics with adjustable difficulty levels.

![Quizly Banner](https://github.com/ShahbazCoder1/QuizBot/blob/main/Images/Quizly%20Banner.jpg)

## Features

- Multiple subjects to choose from (Mathematics, Physics, Chemistry, Biology, Computer Science, History, Geography, Politics, English, General Knowledge)
- User-defined topics within each subject
- Three difficulty levels: Beginner, Intermediate, and Advanced
- 10-question quizzes generated dynamically using Google's Generative AI
- Score tracking and display
- Feedback submission feature

## Commands

- `/start` - Begin a new quiz
- `/help` - Show available commands
- `/about` - Display information about the bot
- `/stop` - Stop the current quiz
- `/feedback` - Submit feedback about the bot

## Technologies Used

- Python 3
- python-telegram-bot
- Google Generative AI (Gemini 1.5 Flash model)
- smtplib for email notifications

## Setup

1. Clone the repository
2. Install the required dependencies:
`pip install python-telegram-bot google-generativeai`
3. Set up your Telegram Bot Token and Google API Key in the code
4. Run the bot:
`python quizly_telegram_bot.py`

## How It Works

1. The bot presents a list of subjects to choose from
2. Users enter their desired topic within the chosen subject
3. Users select the difficulty level
4. The bot generates a 10-question quiz using Google's Generative AI
5. Questions are presented one at a time as Telegram polls
6. The bot tracks correct and incorrect answers
7. After completing the quiz, users receive their final score

## Feedback

Users can submit feedback using the `/feedback` command. Feedback is sent via email to the developers.

## Developers

- **[Md Shahbaz Hashmi Ansari](https://github.com/ShahbazCoder1)**
- **[Vidhi Agrawal](https://github.com/Vidhi-28)**

## License

This project is open source and available under the [GPL-3.0 License](LICENSE).

## Acknowledgements

- This project uses the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library
- Quiz questions are generated using [Google's Generative AI](https://developers.generativeai.google/)
