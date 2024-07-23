FROM python:3.11.8

WORKDIR /app

COPY . .

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
