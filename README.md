# Quizly - Telegram AI Quiz Bot 🤖📚

![GitHub](https://img.shields.io/github/license/ShahbazCoder1/QuizBot)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)
[![Live](https://img.shields.io/badge/Live-Quizly%20Bot-brightgreen?style=flat&logo=telegram)](https://bot-d5sa.onrender.com)

Quizly is an intelligent Telegram bot that offers engaging quizzes on various subjects with adjustable difficulty levels. Powered by Google's Generative AI, it provides a dynamic learning experience for users.

[![Chat with Quizly](https://img.shields.io/badge/Chat%20with-Quizly-blue?style=for-the-badge&logo=telegram)](https://t.me/@Quisly_Bot)

![Quizly Banner](https://github.com/ShahbazCoder1/QuizBot/blob/main/Images/Quizly%20Banner.jpg)

## Features

- 📚 Multiple subjects: Mathematics, Physics, Chemistry, Biology, Computer Science, History, Geography, Politics, English, General Knowledge
- 🎯 User-defined topics within each subject
- 🔢 Three difficulty levels: Beginner, Intermediate, and Advanced
- 🧠 10-question quizzes generated dynamically using Google's Generative AI
- 📊 Score tracking and display
- 🌐 Multi-language support
- 📝 Feedback submission feature
- 🎥 YouTube video recommendations for improvement

## Commands

- `/start` - Begin a new quiz
- `/help` - Show available commands
- `/about` - Display information about the bot
- `/stop` - Stop the current quiz
- `/feedback` - Submit feedback about the bot
- `/language` - Set the bot's language

## Technologies Used

- Python 3.7+
- python-telegram-bot
- Google Generative AI (Gemini 1.5 Flash model)
- YouTube Data API
- Firebase Firestore
- smtplib for email notifications

## Setup

1. Clone the repository:
   
   ```Bash
   git clone https://github.com/ShahbazCoder1/QuizBot.git
   cd QuizBot
2. Install the required dependencies:

   ```Bash
   pip install -r requirements.txt
3. Install gettext for translations:
- On Ubuntu/Debian:
  ```
  sudo apt-get install gettext
  ```
- On macOS (using Homebrew):
  ```
  brew install gettext
  ```
- On Windows:
  Download and install gettext from the [GNU gettext website](https://www.gnu.org/software/gettext/)

4. Set up environment variables:
- `TOKEN`: Your Telegram Bot Token
- `USERNAME`: Your Telegram Bot Username
- `API_KEY`: Your Google Generative AI API Key
- `YOUTUBE_API`: Your YouTube Data API Key

5. Set up Firebase:
- Create a Firebase project and download the service account key JSON file
- Replace the `service_account.json` with the path of your service account key JSON file in `TelegramBot/firestore/user_data.py:14`
  
6. Prepare translations:
- Compile .po files to .mo files:
   ```Bash
   msgfmt -o locale/<lang>/LC_MESSAGES/messages.mo locale/<lang>/LC_MESSAGES/messages.po
- NOTE: replace `<lang>` with language code, e.g., 'es' for Spanish

7. Run the bot:
   ```Bash
   python quizly_telegram_bot.py
  - For Production mode:
    ```Bash
    gunicorn app:app & python TelegramBot/quizly_telegram_bot.py
Note: Make sure to update your translations and recompile .mo files whenever you add or modify translatable strings in your code.

## Project IDX Setup

For users working with [Google Project IDX](https://idx.google.com/), we provide a `Project-IDX_nix_setup.txt` file in the repository. This file contains the `.idx/dev.nix` configuration used in this project. To set up your Project IDX workspace:

1. Create a `.idx` directory in your Project IDX workspace if it doesn't already exist.
2. Create a `dev.nix` file inside the `.idx` directory.
3. **Copy the contents of `Project-IDX_nix_setup.txt` and paste them into your `dev.nix` file.**

This configuration sets up the necessary environment for running the Quizly bot in Project IDX, including Python and required dependencies. After setting up, you can proceed with the bot configuration and execution as described in the Setup section.

**NOTE: Remember to first clone the code from this repository to Project IDX.**

## First-Time Setup

When a user starts the bot for the first time:

1. The bot will greet the user and offer language selection
2. User selects their preferred language
3. The bot saves the user's language preference
4. User is presented with the subject selection menu to start their first quiz

## How It Works

1. The bot presents a list of subjects to choose from
2. Users enter their desired topic within the chosen subject
3. Users select the difficulty level
4. The bot generates a 10-question quiz using Google's Generative AI
5. Questions are presented one at a time as Telegram polls
6. The bot tracks correct and incorrect answers
7. After completing the quiz, users receive their final score
8. For scores of 5 or less, the bot suggests relevant YouTube videos for improvement

## Feedback

Users can submit feedback using the `/feedback` command. Feedback is sent via email to the developers.

## Developer

- **[Md Shahbaz Hashmi Ansari](https://github.com/ShahbazCoder1)**

### Former Contributor

- **[Vidhi Agrawal](https://github.com/Vidhi-28)** (Initial development phase)

This project was initially developed collaboratively, with Vidhi Agrawal contributing during the early stages. Since then, Md Shahbaz Hashmi Ansari has continued solo development and maintenance of the project.

## License

This project is open source and available under the [GPL-3.0 License](LICENSE).

## Acknowledgements

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library
- [Google's Generative AI](https://developers.generativeai.google/)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [Firebase Firestore](https://firebase.google.com/docs/firestore)

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.
