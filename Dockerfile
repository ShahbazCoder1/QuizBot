FROM python:3.8
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN pip install python-telegram-bot --upgrade

# Set environment variables
ENV TOKEN
ENV USERNAME
ENV API_KEY
ENV YOUTUBE_API
ENV SEND_EMAIL
ENV PASSWORD
ENV RECEIVER_EMAIL

CMD ["python", "Telegram Bot/quizly_telegram_bot.py"]
