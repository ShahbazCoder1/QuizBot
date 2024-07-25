from flask import Flask
from TelegramBot.quizly_telegram_bot import main


app = Flask(__name__)

@app.route('/')
def run_code():
    result = main()
    return result

if __name__ == '__main__':
    app.run()