FROM python:3.8
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN pip install python-telegram-bot --upgrade

CMD ["python", "Telegram Bot/quizly_telegram_bot.py"]
